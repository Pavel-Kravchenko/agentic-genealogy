#!/usr/bin/env python3
"""Export the family graph (persons.json + links.json) to GEDCOM 5.5.1.

    python3 gedcom_export.py --persons persons.json --links links.json --out tree.ged
    python3 gedcom_export.py --persons persons.json --links links.json --out tree-latin.ged --latin

With --latin the main name and the places are transliterated from Cyrillic (BGN/PCGN without
diacritics) for services that match only Latin script; the Cyrillic original is written as a second
name (TYPE aka). Notes are not touched.

The graph is only read, never changed, so there is no snapshot. Before the file is written, the text is
checked (dangling pointers, line syntax, date syntax, person count); a failed check stops with an error.
An existing --out file is not overwritten unless --force is given.
Python 3.9+, standard library only. Schema: SCHEMA.md.
"""
import argparse
import collections
import datetime
import os
import re
import sys

import check_graph
from check_graph import APPROX, BEFORE, AFTER, BETWEEN, DOUBLE_YEAR, parse_date

MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
RANK = {"high": 3, "medium": 2, "low": 1, "": 0, None: 0}
MAX_LINE = 200                      # GEDCOM lines are cut with CONC at this length (limit is 255)

_TR = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z",
       "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
       "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
       "щ": "shch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
       "і": "i", "ї": "yi", "є": "ye", "ґ": "g", "ѣ": "e"}

# Endings that mark a Russian surname when the person has no `family` match in the name.
SURNAME_SUFFIXES = ("ов", "ова", "ев", "ева", "ёв", "ёва", "ин", "ина", "ын", "ына", "ский", "ская",
                    "цкий", "цкая", "ко", "ук", "юк", "чук", "як", "ян", "их", "ых", "ой", "ей")
PATRONYMIC_ENDINGS = ("ович", "евич", "овна", "евна", "ична", "инична")
# Bracket remarks that mean 'maiden name': Russian and English spellings are read as input.
MAIDEN_RE = re.compile(r"^(?:дев|урожд|née|nee|born)\.?\s*(\S+)", re.I)

ROLE = {"GODPARENT": "godparent", "GUARANTOR": "guarantor",
        "POSSIBLE_KIN": "possible relative", "HALF_SIBLING": "half-sibling"}


def translit(s, latin):
    """Cyrillic -> Latin (BGN/PCGN without diacritics) when `latin`; Latin and punctuation unchanged."""
    if not latin or not s:
        return s
    out = []
    for ch in s:
        lo = ch.lower()
        if lo in _TR:
            r = _TR[lo]
            out.append(r.capitalize() if ch != lo and r else r)
        else:
            out.append(ch)
    return "".join(out)


def _fmt(year, month, day):
    if day:
        return "%d %s %d" % (day, MONTHS[month - 1], year)
    if month:
        return "%s %d" % (MONTHS[month - 1], year)
    return str(year)


def gedcom_date(text):
    """Graph date -> GEDCOM date: '1903-02-14' -> '14 FEB 1903', '~1840' -> 'ABT 1840',
    'before 1815' -> 'BEF 1815', 'after 1925' -> 'AFT 1925', 'between 1781 and 1784' ->
    'BET 1781 AND 1784', '1760/61' -> '1760/61'. Raises ValueError on a date the graph cannot parse."""
    d = parse_date(text)
    if d is None:
        return ""
    base = _fmt(d.year, d.month, d.day)
    if d.qualifier == APPROX:
        return "ABT " + base
    if d.qualifier == BEFORE:
        return "BEF " + base
    if d.qualifier == AFTER:
        return "AFT " + base
    if d.qualifier == BETWEEN:
        return "BET %s AND %d" % (base, d.end_year)
    if d.qualifier == DOUBLE_YEAR:
        return "%d/%02d" % (d.year, d.end_year % 100)
    return base


def split_name(p):
    """-> (given names + patronymic, surname, [bracket remarks]). The surname is the token that matches
    `family`; failing that, the first token with a surname ending. If none is found the whole string
    is the given name. Bracket remarks ('(née X)', '(b. 1900)') are taken out of the main name:
    left in, they would break the GEDCOM line in two."""
    extras = re.findall(r"\(([^)]*)\)", p["name"])
    clean = re.sub(r"\s*\([^)]*\)", "", p["name"]).strip()
    toks = clean.split()
    family = (p.get("family") or "").strip()
    if family and len(toks) > 1:
        stem = re.sub(r"(ы|и)$", "", family)
        for i, t in enumerate(toks):
            if t.startswith(stem):
                return " ".join(toks[:i] + toks[i + 1:]), t, extras
    if len(toks) > 1 and toks[0].endswith(SURNAME_SUFFIXES) and not toks[0].endswith(PATRONYMIC_ENDINGS):
        return " ".join(toks[1:]), toks[0], extras
    return clean, "", extras


class Writer:
    def __init__(self):
        self.lines = []

    def emit(self, level, tag, text=""):
        """One GEDCOM line; line breaks become CONT, long pieces CONC."""
        text = (text or "").replace("\r", "")
        if not text:
            self.lines.append("%d %s" % (level, tag))
            return
        first = True
        for part in text.split("\n"):
            chunks = [part[i:i + MAX_LINE] for i in range(0, len(part), MAX_LINE)] or [""]
            for j, ch in enumerate(chunks):
                t = tag if first else ("CONT" if j == 0 else "CONC")
                lvl = level if first else level + (0 if tag in ("CONT", "CONC") else 1)
                self.lines.append("%d %s %s" % (lvl, t, ch))
                first = False

    def note(self, level, text):
        if text:
            self.emit(level, "NOTE", text)


def pick(links_, sex, P):
    """Of several candidate parents of one sex take the most confident; the rest go to ASSO."""
    cands = [s for s in links_ if P[s["from"]]["sex"] == sex]
    cands.sort(key=lambda s: -RANK.get(s["confidence"], 0))
    return (cands[0] if cands else None), cands[1:]


def build(persons, links, latin=False, submitter="family graph export"):
    """-> list of GEDCOM lines."""
    P = {p["id"]: p for p in persons}
    IND = {pid: "@I%d@" % (i + 1) for i, pid in enumerate(P)}
    tr = lambda s: translit(s, latin)
    w = Writer()

    parents = collections.defaultdict(list)      # child -> [link]
    adoptive = collections.defaultdict(list)
    spouses = []
    assoc = collections.defaultdict(list)        # person -> (who, role, link)
    for s in links:
        t = s["type"]
        for end in (s["from"], s["to"]):
            if end not in P:
                raise ValueError("link %s %s -> %s points at an unknown person %r; run check_graph.py first"
                                 % (t, s["from"], s["to"], end))
        if t == "PARENT":
            parents[s["to"]].append(s)
        elif t == "ADOPTIVE_PARENT":
            adoptive[s["to"]].append(s)
        elif t == "SPOUSE":
            spouses.append(s)
        elif t in ROLE:
            assoc[s["to"]].append((s["from"], ROLE[t], s))
        else:
            raise ValueError("unknown link type %r: %s -> %s" % (t, s["from"], s["to"]))

    families = {}                                # (husband, wife, pedigree) -> dict
    child_famc = collections.defaultdict(list)   # child -> [(family key, pedigree)]

    def family(key):
        return families.setdefault(key, {"chil": [], "notes": []})

    for child, plinks, pedi in ([(c, l, "") for c, l in parents.items()] +
                                [(c, l, "adopted") for c, l in adoptive.items()]):
        f, extra_f = pick(plinks, "m", P)
        m, extra_m = pick(plinks, "f", P)
        for s in extra_f + extra_m:
            assoc[child].append((s["from"], "other version of the parent", s))
        if not f and not m:
            continue
        key = (f["from"] if f else None, m["from"] if m else None, pedi)
        fam = family(key)
        fam["chil"].append(child)
        child_famc[child].append((key, pedi))
        for s in (f, m):
            if s:
                fam["notes"].append("Child %s <- %s: confidence %s. %s%s" % (
                    P[child]["name"], P[s["from"]]["name"], s["confidence"],
                    (s["note"] + " " if s.get("note") else ""), s.get("source", "")))

    for s in spouses:
        a, b = s["from"], s["to"]
        h, wf = (a, b) if P[a]["sex"] == "m" else (b, a)
        family((h, wf, ""))["marr"] = s

    FID = {k: "@F%d@" % (i + 1) for i, k in enumerate(families)}
    spouse_fams = collections.defaultdict(list)
    for k in families:
        for pid in (k[0], k[1]):
            if pid:
                spouse_fams[pid].append(k)

    # ---------- header ----------
    today = datetime.date.today()
    w.emit(0, "HEAD")
    w.emit(1, "SOUR", "agentic-genealogy")
    w.emit(2, "NAME", "family graph export")
    w.emit(1, "DATE", "%d %s %d" % (today.day, MONTHS[today.month - 1], today.year))
    w.emit(1, "SUBM", "@SUB1@")
    w.emit(1, "GEDC")
    w.emit(2, "VERS", "5.5.1")
    w.emit(2, "FORM", "LINEAGE-LINKED")
    w.emit(1, "CHAR", "UTF-8")
    w.emit(0, "@SUB1@ SUBM")
    w.emit(1, "NAME", tr(submitter))

    # ---------- persons ----------
    for pid, p in P.items():
        w.emit(0, "%s INDI" % IND[pid])
        given, surn, extras = split_name(p)
        given_l, surn_l = tr(given), tr(surn)
        w.emit(1, "NAME", "%s /%s/" % (given_l, surn_l) if surn_l else given_l)
        if given_l:
            w.emit(2, "GIVN", given_l)
        if surn_l:
            w.emit(2, "SURN", surn_l)
        if latin and (given_l, surn_l) != (given, surn):   # the Cyrillic original as a second name
            w.emit(1, "NAME", "%s /%s/" % (given, surn) if surn else given)
            w.emit(2, "TYPE", "aka")
        for extra in extras:
            m = MAIDEN_RE.match(extra)
            if m:                   # maiden name as a separate name, as GEDCOM expects
                w.emit(1, "NAME", "%s /%s/" % (given_l, tr(m.group(1))))
                w.emit(2, "TYPE", "maiden")
            else:
                w.emit(1, "NICK", tr(extra))
        for v in p.get("variants", []):
            w.emit(1, "NAME", tr(v))
            w.emit(2, "TYPE", "aka")
        w.emit(1, "SEX", {"m": "M", "f": "F"}.get(p["sex"], "U"))
        for key, tag in (("birth", "BIRT"), ("death", "DEAT")):
            e = p.get(key) or {}
            if not (e.get("date") or e.get("place")):
                continue
            w.emit(1, tag)
            if e.get("date"):
                w.emit(2, "DATE", gedcom_date(e["date"]))
            if e.get("place"):
                w.emit(2, "PLAC", tr(e["place"]))
            n = []
            if e.get("style") == "OS":
                n.append("Date in Old Style.")
            if e.get("confidence"):
                n.append("Confidence: %s." % e["confidence"])
            if e.get("source"):
                n.append("Source: %s" % e["source"])
            w.note(2, " ".join(n))
        body = []
        if p.get("notes"):
            body.append(p["notes"])
        for d in p.get("disputes", []):
            body.append("Disputed: " + d)
        for s in p.get("sources") or []:
            body.append("Source: " + s)
        w.note(1, "\n".join(body))
        for other, role, s in assoc.get(pid, []):
            w.emit(1, "ASSO", IND[other])
            w.emit(2, "RELA", role)
            w.note(2, " ".join(x for x in [s.get("note"), s.get("source")] if x))
        for key, pedi in child_famc.get(pid, []):
            w.emit(1, "FAMC", FID[key])
            if pedi:
                w.emit(2, "PEDI", pedi)
        for key in spouse_fams.get(pid, []):
            w.emit(1, "FAMS", FID[key])
        w.emit(1, "REFN", pid)

    # ---------- families ----------
    for key, fam in families.items():
        w.emit(0, "%s FAM" % FID[key])
        if key[0]:
            w.emit(1, "HUSB", IND[key[0]])
        if key[1]:
            w.emit(1, "WIFE", IND[key[1]])
        for c in fam["chil"]:
            w.emit(1, "CHIL", IND[c])
        notes = list(fam["notes"])
        s = fam.get("marr")
        if s:
            w.emit(1, "MARR")
            w.note(2, "Confidence: %s. %s%s" % (s["confidence"], (s["note"] + " " if s.get("note") else ""),
                                                s.get("source", "")))
        if key[2] == "adopted":
            notes.insert(0, "Adoptive family.")
        w.note(1, "\n".join(notes))

    w.emit(0, "TRLR")
    return w.lines, len(P), len(families)


def validate(text, n_persons):
    """GEDCOM must have no dangling pointers, well-formed lines and dates, and one record per person."""
    ptrs = set(re.findall(r"@[IF]\d+@", text))
    defined = set(re.findall(r"^0 (@[IF]\d+@)", text, re.M))
    if not ptrs <= defined:
        raise SystemExit("export check failed: dangling pointers %s" % sorted(ptrs - defined))
    for ln in text.split("\r\n"):
        if not ln:
            continue
        if not re.match(r"^\d+ (@[^@]+@ )?[A-Z_]+", ln):
            raise SystemExit("export check failed: malformed line %r" % ln)
        if len(ln) >= 255:
            raise SystemExit("export check failed: line longer than 255: %r" % ln[:80])
    if text.count("\r\n0 @I") != n_persons:
        raise SystemExit("export check failed: %d INDI records for %d persons"
                         % (text.count("\r\n0 @I"), n_persons))
    if not text.rstrip().endswith("0 TRLR"):
        raise SystemExit("export check failed: no TRLR record at the end")
    bad = [ln for ln in text.split("\r\n") if ln.startswith("2 DATE ")
           and not re.match(r"^2 DATE (ABT |EST |CAL |BEF |AFT |BET .+ AND )?"
                            r"(\d{1,2} )?([A-Z]{3} )?\d{3,4}(/\d{2})?$", ln)]
    if bad:
        raise SystemExit("export check failed: dates not in GEDCOM syntax: %s" % bad[:5])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Export the family graph to GEDCOM 5.5.1.")
    ap.add_argument("--persons", required=True, help="persons JSON file")
    ap.add_argument("--links", required=True, help="links JSON file")
    ap.add_argument("--out", required=True, help="GEDCOM file to write; refuses to overwrite an existing file")
    ap.add_argument("--force", action="store_true", help="let --out overwrite an existing file")
    ap.add_argument("--latin", action="store_true",
                    help="transliterate names and places to Latin; Cyrillic original as a second name")
    ap.add_argument("--submitter", default="family graph export",
                    help="name written into the SUBM record (default: %(default)s)")
    args = ap.parse_args(argv)

    if os.path.exists(args.out) and not args.force:
        raise SystemExit("output file exists, not overwriting: %s (use --force)" % args.out)
    persons = check_graph.load_json(args.persons)
    links = check_graph.load_json(args.links)
    lines, n_persons, n_fams = build(persons, links, args.latin, args.submitter)
    text = "\r\n".join(lines) + "\r\n"
    validate(text, n_persons)
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("persons %d, families %d -> %s" % (n_persons, n_fams, args.out))
    print("export check passed: pointers intact, line and date syntax in order")
    return 0


if __name__ == "__main__":
    sys.exit(main())
