#!/usr/bin/env python3
"""Read a GEDCOM file (from another tree, or one made by gedcom_export.py), compare it with the
graph and report what would be merged. Dry run by default.

    python3 gedcom_import.py FILE.ged --persons persons.json --links links.json
    python3 gedcom_import.py FILE.ged --persons persons.json --links links.json --report merge.md
    python3 gedcom_import.py FILE.ged --persons persons.json --links links.json --apply
    python3 gedcom_import.py --self-test          # regression tests (namesakes, no overwrite, empty events, nothing to write, writer)

--apply never overwrites or removes anything already in the graph. It adds new persons, new facts in events
that are entirely empty in ours (no date, no place, no source, no note), new links, and, on persons it
matched, labelled notes and sources from the other tree and an external id where ours has none. A fact enters
at confidence `low` (or `medium` with --confidence medium) with the import stamp as source. Everything
else goes to the report and a person decides: disagreements ("Clashes"); more precise values of the
other tree for a field that already holds a value (a full date against our bare year of the same year,
a longer place name, a calendar stated only in their date); and values for an
empty field of an event that already holds another value ("Facts for an empty field of an event we
already document"). None of these is written. Before any write the two graph files are copied to the
snapshot directory with a date-time stamp; with nothing to write, no snapshot is taken, no file is
rewritten and the tool says so. The graph files keep their file mode and a symlinked file stays a
link. --report refuses to overwrite an existing file unless --force is given.

Dates: GEDCOM qualifiers become graph qualifiers (ABT -> ~, BEF -> before, AFT -> after,
BET..AND -> between X and Y); a Julian calendar escape (@#DJULIAN@) becomes style "OS" on the event.
Russian month abbreviations (ЯНВ ФЕВ МАР АПР МАЯ ИЮН ИЮЛ АВГ СЕН ОКТ НОЯ ДЕК) are read as input.
Python 3.9+, standard library only. Schema: SCHEMA.md.
"""
import argparse
import collections
import copy
import datetime
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import unicodedata

MONTHS = {m: i + 1 for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split())}
MONTHS_RU = {m: i + 1 for i, m in enumerate("ЯНВ ФЕВ МАР АПР МАЯ ИЮН ИЮЛ АВГ СЕН ОКТ НОЯ ДЕК".split())}

DEFAULT_SOURCE_NAME = "external"
IMPORT_CONFIDENCE = "low"      # set by --confidence; another tree is not a document
DEFAULT_SOURCE_PATTERN = r"https?://"     # note lines matching this go to `sources`, the rest to `notes`
IMPORTED_PREFIX = "ext-"                  # id prefix of persons created by this importer
MATCH_THRESHOLD = 0.75                    # minimum score of an accepted pair
GAP = 0.05    # two candidates whose scores differ by less than this cannot be told apart: a choice
              # between them would be decided by sort order, that is, at random


# ---------- graph files: load, snapshot, write (shared with merge_duplicates.py) ----------
def load_graph(persons_path, links_path):
    for path in (persons_path, links_path):
        if not os.path.isfile(path):
            raise SystemExit("graph file not found: %s" % path)
    with open(persons_path, encoding="utf-8") as f:
        persons = json.load(f)
    with open(links_path, encoding="utf-8") as f:
        links = json.load(f)
    return persons, links


def snapshot(persons_path, links_path, snapshot_dir):
    """Copy both graph files to snapshot_dir with a date-time stamp. Returns the two new paths."""
    os.makedirs(snapshot_dir, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out = []
    for path in (persons_path, links_path):
        base, ext = os.path.splitext(os.path.basename(path))
        dst = os.path.join(snapshot_dir, "%s_%s%s" % (base, stamp, ext))
        if os.path.exists(dst):
            raise SystemExit("snapshot already exists, not overwriting: %s" % dst)
        shutil.copy2(path, dst)
        out.append(dst)
    return out


def _write_json_atomic(data, path):
    """Write to a temporary file in the same directory, then os.replace(): no truncated file on interruption."""
    path = os.path.realpath(path)          # write through a symlink: the link stays a link
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        if os.path.exists(path):
            os.chmod(tmp, stat.S_IMODE(os.stat(path).st_mode))      # keep the mode of the target
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def write_graph(persons, links, persons_path, links_path):
    _write_json_atomic(persons, persons_path)
    _write_json_atomic(links, links_path)


# ---------- GEDCOM parsing ----------
def parse(path):
    """-> tree of records {xref, tag, value, sub:[...]}."""
    root, stack = [], []
    with open(path, encoding="utf-8-sig") as f:        # malformed UTF-8 raises, on purpose
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            m = re.match(r"^(\d+)\s+(@[^@]+@)?\s*(\w+)\s?(.*)$", line)
            if not m:
                raise ValueError("%s line %d is not GEDCOM: %r" % (path, lineno, line[:80]))
            lvl, xref, tag, value = int(m.group(1)), m.group(2), m.group(3), m.group(4)
            if tag in ("CONC", "CONT") and stack:
                node = stack[-1][1]
                node["value"] += ("\n" if tag == "CONT" else "") + value
                continue
            node = {"xref": xref, "tag": tag, "value": value, "sub": []}
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            (stack[-1][1]["sub"] if stack else root).append(node)
            stack.append((lvl, node))
    return root


def sub(node, tag):
    return next((s for s in node["sub"] if s["tag"] == tag), None)


def subs(node, tag):
    return [s for s in node["sub"] if s["tag"] == tag]


def val(node, *path):
    cur = node
    for t in path:
        cur = sub(cur, t)
        if cur is None:
            return ""
    return cur["value"].strip()


def _iso(raw):
    """'14 FEB 1903' -> 1903-02-14; a dual year '1884/85' is kept as written."""
    m = re.match(r"^(?:(\d{1,2})\s+)?(?:([A-ZА-Я]{3})\s+)?(\d{3,4})(/\d{2})?$", raw.strip().upper())
    if not m:
        return ""
    d, mo, y, dual = m.groups()
    month = MONTHS.get(mo) or MONTHS_RU.get(mo)
    iso = y.zfill(4) + (dual or "")
    if month:
        iso += "-%02d" % month
        if d:
            iso += "-%02d" % int(d)
    return iso


QUAL_GRAPH = {"ABT": "~", "CAL": "~", "EST": "~", "BEF": "before ", "AFT": "after "}


def gdate(s):
    """GEDCOM date -> (graph date, qualifier string). 'ABT 1850' -> '~1850', 'BEF 1815' -> 'before 1815',
    'BET 1781 AND 1784' -> 'between 1781 and 1784'. The qualifier string carries the raw GEDCOM
    qualifier and the word JULIAN when the date is in the Julian calendar."""
    if not s:
        return "", ""
    raw = s.strip()
    qual = ""
    cal = re.match(r"^@#D([A-Z]+)@\s*(.*)$", raw)
    if cal:
        raw = cal.group(2)
        if cal.group(1) == "JULIAN":
            qual = "JULIAN"
    q = ""
    m = re.match(r"^(ABT|CAL|EST|BEF|AFT|FROM|BET)\b\s*(.*)$", raw, re.I)
    if m:
        q, raw = m.group(1).upper(), m.group(2)
        qual = (qual + " " + q).strip()
    # some exporters write the calendar after the qualifier: 'ABT @#DJULIAN@ 1840'
    cal = re.match(r"^@#D([A-Z]+)@\s*(.*)$", raw)
    if cal:
        raw = cal.group(2)
        if cal.group(1) == "JULIAN":
            qual = ("JULIAN " + qual).strip()
    ends = re.split(r"\b(?:AND|TO)\b", raw, flags=re.I)
    iso = _iso(ends[0])
    if not iso:
        return "", qual
    if q == "BET" and len(ends) > 1 and _iso(ends[1]):
        return "between %s and %s" % (iso, _iso(ends[1])), qual
    return QUAL_GRAPH.get(q, "") + iso, qual


def event(indi, tag):
    e = sub(indi, tag)
    if not e:
        return {}
    iso, qual = gdate(val(e, "DATE"))
    plac = sub(e, "PLAC")
    place = plac["value"].strip() if plac else ""
    src = [x["value"].strip() for x in subs(e, "SOUR") if x["value"].strip()]
    return {"date": iso, "qualifier": qual, "place": place,
            "cause": val(e, "CAUS"), "source": "; ".join(src)}


def read_gedcom(path):
    """-> (persons, families) in the graph's terms, keyed by GEDCOM xref."""
    root = parse(path)
    persons, families = {}, {}
    for node in root:
        if node["tag"] == "INDI":
            names = [n["value"] for n in subs(node, "NAME")]
            given = surn = ""
            if names:
                first = names[0]
                mm = re.match(r"^(.*?)/([^/]*)/(.*)$", first)
                if mm:
                    given, surn = (mm.group(1) + " " + mm.group(3)).strip(), mm.group(2).strip()
                else:
                    given = first.strip()
            given = (val(node, "NAME", "GIVN") or given).strip()
            surn = val(node, "NAME", "SURN") or surn
            if not surn or surn.lower() in given.lower():
                full = given
            else:
                full = (surn + " " + given).strip()
            notes = [n["value"].strip() for n in subs(node, "NOTE") if n["value"].strip()]
            persons[node["xref"]] = {
                "xref": node["xref"], "name": re.sub(r"\s+", " ", full),
                "surname": surn, "given": given,
                "variants": [re.sub(r"/", "", n).strip() for n in names[1:]],
                "sex": {"M": "m", "F": "f"}.get(val(node, "SEX"), ""),
                "birth": event(node, "BIRT"), "death": event(node, "DEAT"),
                "burial": event(node, "BURI"),
                "residence": [{"place": val(r, "PLAC"), "date": gdate(val(r, "DATE"))[0]}
                              for r in subs(node, "RESI")],
                "events": [{"type": val(ev, "TYPE"), "date": gdate(val(ev, "DATE"))[0],
                            "place": val(ev, "PLAC"), "note": val(ev, "NOTE")}
                           for ev in subs(node, "EVEN")],
                "notes": "\n".join(notes),
                "uid": val(node, "_UID"), "refn": val(node, "REFN"),
            }
        elif node["tag"] == "FAM":
            families[node["xref"]] = {
                "husband": val(node, "HUSB"), "wife": val(node, "WIFE"),
                "children": [c["value"] for c in subs(node, "CHIL")],
                "marriage": event(node, "MARR"),
            }
    # spread families into person relations
    for fam in families.values():
        for c in fam["children"]:
            if c in persons:
                persons[c].setdefault("parents", []).extend(
                    [x for x in (fam["husband"], fam["wife"]) if x])
        explicit = bool(fam["marriage"])
        for a, b in ((fam["husband"], fam["wife"]), (fam["wife"], fam["husband"])):
            if a in persons and b:
                persons[a].setdefault("spouses", []).append((b, explicit))
        for p in (fam["husband"], fam["wife"]):
            if p in persons:
                persons[p].setdefault("children", []).extend(fam["children"])
    return persons, families


# ---------- matching ----------
def is_blank(name):
    """A placeholder name such as '?' is not a person."""
    return not re.sub(r"[?\-\s.]+", "", name or "")


def fold_latin(s):
    """Drop diacritics from Latin letters (ä -> a, ū -> u) and keep Cyrillic letters intact (й stays й)."""
    out = []
    for ch in unicodedata.normalize("NFKD", s):
        if unicodedata.combining(ch) and out and ord(out[-1]) < 0x250:
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


def norm(s):
    """Name tokens. A maiden name in brackets is kept: it is often the shared key between two records
    ('Smith Anna (née Jones)' versus 'Jones Anna'); other brackets (comments, years) are dropped."""
    s = fold_latin(unicodedata.normalize("NFKC", s or "").lower().replace("ё", "е"))
    keep = " ".join(re.findall(r"\((?:дев|урожд|née|nee|born)\.?\s*([^)]*)\)", s))
    s = re.sub(r"\(.*?\)", " ", s) + " " + keep
    s = re.sub(r"\b(?:дев|урожд|née|nee)\b\.?", " ", s)
    return "".join(c if c.isalpha() or c == " " else " " for c in s).split()


STOP_WORDS = {"жена", "муж", "дочь", "сын", "первый", "вторая", "первая", "второй", "и",
              "wife", "husband", "daughter", "son", "and"}


def key_tokens(name):
    """Name tokens without service words, sorted: comparison in any word order."""
    return sorted(t for t in norm(name) if t not in STOP_WORDS and len(t) > 1)


def year(date):
    m = re.search(r"\d{3,4}", date or "")
    return m.group(0) if m else ""


def split_qual(d):
    """'~1850' -> ('~', '1850'); 'between 1781 and 1784' -> ('between', '1781 and 1784')."""
    m = re.match(r"^(~|before\s|after\s|between\s)\s*(.*)$", d)
    return (m.group(1).strip(), m.group(2)) if m else ("", d)


def lev(a, b):
    """Levenshtein distance, capped at 3."""
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def similar(ta, tb):
    """Share of the tokens of one name that found a close twin in the other."""
    if not ta or not tb:
        return 0.0
    hit = sum(1 for x in ta if any(lev(x, y) <= 1 for y in tb))
    return hit / max(len(ta), len(tb))


def neighbours_ours(ours, links):
    """id -> names of relatives (parents, children, spouses) from the links, for telling namesakes apart."""
    by = {p["id"]: p for p in ours}
    out = collections.defaultdict(list)
    for l in links:
        if l["type"] not in ("PARENT", "ADOPTIVE_PARENT", "SPOUSE"):
            continue
        a, b = l["from"], l["to"]
        if a in by and b in by:
            out[a].append(tuple(key_tokens(by[b]["name"])))
            out[b].append(tuple(key_tokens(by[a]["name"])))
    return out


def neighbours_theirs(theirs):
    out = {}
    for x, t in theirs.items():
        names = []
        for r in t.get("parents", []) + t.get("children", []):
            if r in theirs:
                names.append(tuple(key_tokens(theirs[r]["name"])))
        for r in t.get("spouses", []):
            if r[0] in theirs:
                names.append(tuple(key_tokens(theirs[r[0]]["name"])))
        out[x] = names
    return out


def kin_bonus(a, b):
    """How many relatives match by name - the deciding argument for namesakes."""
    if not a or not b:
        return 0.0, 0
    hits = 0
    free = list(b)
    for n in a:
        for i, m in enumerate(free):
            if similar(list(n), list(m)) >= 0.7:
                hits += 1
                free.pop(i)
                break
    return min(0.6, 0.3 * hits), hits


def match(ours, theirs, links=(), threshold=MATCH_THRESHOLD, gap=GAP):
    """-> ([(our id, their xref, score, why)], [ambiguous]) - greedy matching of the best pairs.

    Ambiguous are namesakes that cannot be told apart: the best candidate has a rival with
    practically the same score. Such pairs are NOT merged and NOT created as new persons; they go
    to the report and a person decides. Silently choosing one of two namesakes would swap their data.
    """
    nb_o, nb_t = neighbours_ours(ours, links), neighbours_theirs(theirs)
    by_id = {p["id"]: p for p in ours}
    uid_map = {uid: p["id"] for p in ours for uid in (p.get("external_ids") or {}).values() if uid}
    exact, used_o, used_t = [], set(), set()
    for x, t in theirs.items():
        oid = t.get("refn") if t.get("refn") in by_id else uid_map.get(t.get("uid"))
        if oid and oid not in used_o:
            exact.append((oid, x, 2.0, "same identifier"))
            used_o.add(oid)
            used_t.add(x)
    ours_tok = {p["id"]: key_tokens(p["name"]) + [t for v in p.get("variants", []) for t in key_tokens(v)]
                for p in ours}
    ours_name = {p["id"]: key_tokens(p["name"]) for p in ours}
    # index by the first two letters of each token: without it the comparison is quadratic
    idx = collections.defaultdict(set)
    for oid, toks in ours_tok.items():
        for tok in toks:
            idx[tok[:2]].add(oid)
    pairs = []
    for x, t in theirs.items():
        if x in used_t or is_blank(t["name"]):
            continue
        tt = key_tokens(t["name"])
        if not tt:
            continue
        cands = set()
        for tok in tt:
            cands |= idx.get(tok[:2], set())
        by_t = year(t["birth"].get("date", ""))
        dy = year(t["death"].get("date", ""))
        for oid in cands:
            if oid in used_o:
                continue
            s = max(similar(tt, ours_name[oid]), similar(tt, ours_tok[oid]) * 0.98)
            if s < 0.5:
                continue
            o = by_id[oid]
            oby = year((o.get("birth") or {}).get("date"))
            ody = year((o.get("death") or {}).get("date"))
            why = ["name %.0f%%" % (s * 100)]
            score = s
            if by_t and oby:
                d = abs(int(by_t) - int(oby))
                score += 0.45 if d == 0 else 0.2 if d <= 2 else -0.6
                why.append("birth year %s/%s" % (by_t, oby))
            if dy and ody:
                d = abs(int(dy) - int(ody))
                score += 0.25 if d == 0 else -0.35
                why.append("death year %s/%s" % (dy, ody))
            if t["sex"] and o["sex"] and t["sex"] != o["sex"]:
                score -= 0.8
                why.append("sex differs")
            bonus, hits = kin_bonus(nb_t.get(x, []), nb_o.get(oid, []))
            if hits:
                score += bonus
                why.append("matching relatives: %d" % hits)
            pairs.append((score, oid, x, ", ".join(why)))
    pairs.sort(reverse=True)
    rivals_t, rivals_o = collections.defaultdict(list), collections.defaultdict(list)
    for score, oid, x, why in pairs:
        rivals_t[x].append((score, oid))
        rivals_o[oid].append((score, x))
    out, ambiguous = list(exact), []
    for score, oid, x, why in pairs:
        if oid in used_o or x in used_t or score < threshold:
            continue
        our_rivals = [o for s, o in rivals_t[x] if o != oid and o not in used_o and score - s < gap]
        their_rivals = [y for s, y in rivals_o[oid] if y != x and y not in used_t and score - s < gap]
        if our_rivals or their_rivals:
            ambiguous.append({"ours": [oid] + our_rivals, "theirs": [x] + their_rivals,
                              "score": round(score, 2), "why": why})
            # block the whole cluster: otherwise a rival is picked the same way, at random
            used_o.update([oid] + our_rivals)
            used_t.update([x] + their_rivals)
            continue
        used_o.add(oid)
        used_t.add(x)
        out.append((oid, x, round(score, 2), why))
    return out, ambiguous


# ---------- comparing facts ----------
def contains(a, b):
    """A short place name recognised inside a long one is a refinement, not a disagreement."""
    ta, tb = key_tokens(a), key_tokens(b)
    if not ta or not tb or len(ta) > len(tb):
        return False
    hits = sum(1 for x in ta if any(lev(x, y) <= 2 for y in tb))
    return hits / len(ta) >= 0.6


def event_untouched(ev):
    """True when an event of ours holds nothing of its own: no date, no place, no source and no further
    key with a value (`style` and `confidence` alone do not count). Only such an event may be filled from
    another tree; anything else is ours and is listed, not written."""
    ev = ev or {}
    return not any(v.strip() if isinstance(v, str) else v
                   for k, v in ev.items() if k not in ("style", "confidence"))


def compare(o, t):
    """-> (new facts, clashes, refinements, facts for a documented event). A new fact is a value of the
    other tree for an event that is entirely empty in ours (no date, no place, no source, no note). A
    value for an empty field of an event that already holds anything of ours is returned apart (`lacks`):
    it is reported, never written. A calendar stated only in the other tree is reported as a refinement.
    A refinement is a more precise value of the other tree (a full date against our bare year, a longer
    place name) for a field that is not empty in ours: it is reported, never written."""
    add, clash, refine, lacks = {}, [], [], []
    for key in ("birth", "death"):
        oe, te = (o.get(key) or {}), t.get(key, {})
        event_empty = event_untouched(oe)
        for field in ("date", "place"):
            ov, tv = (oe.get(field) or "").strip(), (te.get(field) or "").strip()
            if not tv:
                continue
            if not ov:
                if event_empty:
                    add.setdefault(key, {})[field] = tv
                else:
                    lacks.append(("%s: %s" % (key, field), tv))
            elif field == "date" and ov != tv:
                (oq, ob), (tq, tb) = split_qual(ov), split_qual(tv)
                if oq == tq and year(ob) == year(tb) and (len(ob) == 4 or len(tb) == 4):
                    if len(tb) > len(ob):               # same year, theirs is more precise: listed, never written
                        refine.append(("%s: %s" % (key, field), ov, tv))
                else:
                    clash.append(("%s: %s" % (key, field), ov, tv))
            elif field == "date" and "JULIAN" in (te.get("qualifier") or "") and not (oe.get("style") or "").strip():
                refine.append(("%s: date" % key, "%s (calendar not stated)" % ov, "%s (Julian calendar)" % tv))
            elif field == "place" and norm(ov) != norm(tv):
                if contains(ov, tv) or contains(tv, ov):
                    refine.append(("%s: %s" % (key, field), ov, tv))
                elif similar(key_tokens(ov), key_tokens(tv)) < 0.6:
                    clash.append(("%s: %s" % (key, field), ov, tv))
    if t["sex"] and o["sex"] and t["sex"] != o["sex"]:
        clash.append(("sex", o["sex"], t["sex"]))
    return add, clash, refine, lacks


def extras_of(o, t, source_pattern=DEFAULT_SOURCE_PATTERN):
    """-> (lines for notes, lines for sources): everything that has no field of its own."""
    out, src = [], []
    if t["death"].get("cause"):
        out.append("cause of death: %s" % t["death"]["cause"])
    if t.get("burial", {}).get("place"):
        out.append("burial: %s" % t["burial"]["place"])
    for r in t.get("residence", []):
        if r["place"]:
            out.append("residence%s: %s" % (" " + r["date"] if r["date"] else "", r["place"]))
    for ev in t.get("events", []):
        label = " ".join(x for x in (ev["type"], ev["date"], ev["place"]) if x)
        if label or ev["note"]:
            out.append("; ".join(x for x in (label, ev["note"]) if x))
    for line in (t.get("notes") or "").split("\n"):
        line = re.sub(r"^(Disputed|Source):\s*", "", line.strip())
        if not line:
            continue
        (src if re.search(source_pattern, line) else out).append(line)
    # compare with everything already recorded about this person, not only the notes
    have = re.sub(r"\s+", " ", " ".join(
        [o.get("notes") or ""] + (o.get("disputes") or []) + (o.get("sources") or []) +
        [(o.get(k) or {}).get("source", "") for k in ("birth", "death")]).lower())
    norm_line = lambda x: re.sub(r"\s+", " ", x.strip().lower())
    out = [x for x in out if norm_line(x)[:40] not in have]
    src = [x for x in src if norm_line(x)[:40] not in have]
    return out, src


# ---------- the run ----------
def label(t):
    years = ("%s-%s" % (year(t["birth"].get("date", "")), year(t["death"].get("date", "")))).strip("-")
    return "%s%s" % (t["name"] or "(no name)", " (%s)" % years if years else "")


def run(ged_path, persons, links, source_name=DEFAULT_SOURCE_NAME, source_pattern=DEFAULT_SOURCE_PATTERN):
    """Compare without writing. Returns a dict with everything the report and the write-back need."""
    theirs, fams = read_gedcom(ged_path)
    pairs, ambiguous = match(persons, theirs, links)
    ambiguous_theirs = {x for s in ambiguous for x in s["theirs"]}
    ours_by = {p["id"]: p for p in persons}
    m_ours = {oid: x for oid, x, _, _ in pairs}
    m_theirs = {x: oid for oid, x, _, _ in pairs}

    facts, clashes, refines, extras, lacks = [], [], [], [], []
    for oid, x, score, why in pairs:
        add, clash, refine, lack = compare(ours_by[oid], theirs[x])
        our_uid = (ours_by[oid].get("external_ids") or {}).get(source_name)
        if our_uid and theirs[x].get("uid") and our_uid != theirs[x]["uid"]:
            clash.append(("external id (%s)" % source_name, our_uid, theirs[x]["uid"]))
        if lack:
            lacks.append((oid, x, lack))
        if add:
            facts.append((oid, x, add))
        if clash:
            clashes.append((oid, x, clash))
        if refine:
            refines.append((oid, x, refine))
        ex, sr = extras_of(ours_by[oid], theirs[x], source_pattern)
        if ex or sr:
            extras.append((oid, x, ex, sr))

    # Ambiguous namesakes are not created as new persons either: creating them would double a person
    # we failed to recognise. A human decides, not the sort order.
    new_people = [x for x in theirs if x not in m_theirs and x not in ambiguous_theirs
                  and not is_blank(theirs[x]["name"])]
    ours_only = [p["id"] for p in persons if p["id"] not in m_ours]

    # new links; an adoptive parent looks like an ordinary parent in GEDCOM, so compare as PARENT
    have = {(l["from"], l["to"], "PARENT" if l["type"] == "ADOPTIVE_PARENT" else l["type"]) for l in links}
    new_links, inferred_pairs = [], []
    for x, t in theirs.items():
        if x not in m_theirs:
            continue
        for par in set(t.get("parents", [])):
            if par in m_theirs:
                pair = (m_theirs[par], m_theirs[x], "PARENT")
                if pair not in have:
                    new_links.append(pair)
        for sp, explicit in set(t.get("spouses", [])):
            if sp not in m_theirs:
                continue
            a, b = m_theirs[sp], m_theirs[x]
            if (a, b, "SPOUSE") in have or (b, a, "SPOUSE") in have:
                continue
            target = new_links if explicit else inferred_pairs
            if (b, a, "SPOUSE") in {(q[1], q[0], q[2]) for q in target}:
                continue
            target.append((a, b, "SPOUSE"))
    return {"path": ged_path, "theirs": theirs, "fams": fams, "pairs": pairs, "ambiguous": ambiguous,
            "facts": facts, "clashes": clashes, "refines": refines, "lacks": lacks, "extras": extras,
            "new_people": new_people, "ours_only": ours_only, "new_links": new_links,
            "inferred_pairs": inferred_pairs, "ours_by": ours_by, "m_theirs": m_theirs,
            "source_name": source_name}


def stats(r):
    return {"their persons": len(r["theirs"]), "matched": len(r["pairs"]),
            "new persons": len(r["new_people"]), "new facts": len(r["facts"]),
            "clashes": len(r["clashes"]), "facts for a documented event, not written": len(r["lacks"]),
            "new links": len(r["new_links"]),
            "pairs inferred from shared children": len(r["inferred_pairs"]),
            "more precise dates": sum(1 for _, _, rf in r["refines"] if any(f.endswith(": date") for f, _, _ in rf)),
            "place refinements": sum(1 for _, _, rf in r["refines"] if any(f.endswith(": place") for f, _, _ in rf)),
            "extra notes": len(r["extras"]),
            "ambiguous": len(r["ambiguous"])}


def warn_ambiguous(ambiguous, theirs, ours_by):
    """Loud, on stderr: what was refused and why."""
    print("\n!!! AMBIGUOUS MATCHES: %d - NOTHING MERGED FOR THEM." % len(ambiguous), file=sys.stderr)
    print("    Two namesakes cannot be told apart (candidate scores differ by less than %.2f)." % GAP,
          file=sys.stderr)
    for s in ambiguous:
        print("  . ours:   %s" % "; ".join("%s '%s'" % (o, ours_by[o]["name"]) for o in s["ours"]
                                           if o in ours_by), file=sys.stderr)
        print("    theirs: %s" % "; ".join("%s '%s'" % (x, label(theirs[x])) for x in s["theirs"]
                                           if x in theirs), file=sys.stderr)
        print("    score %.2f (%s) - a person must decide" % (s["score"], s["why"]), file=sys.stderr)
    print("", file=sys.stderr)


def report_text(r):
    theirs, ours_by = r["theirs"], r["ours_by"]
    L, A = [], None
    A = L.append
    A("# Merge report: %s\n" % os.path.basename(r["path"]))
    A("Parsed %d persons and %d families. Matched with the graph: **%d**. New persons: **%d**. "
      "New facts: **%d**. Clashes: **%d**. New links: **%d**. Ambiguous namesakes (not merged): **%d**.\n"
      % (len(theirs), len(r["fams"]), len(r["pairs"]), len(r["new_people"]), len(r["facts"]),
         len(r["clashes"]), len(r["new_links"]), len(r["ambiguous"])))

    A("\n## Ambiguous namesakes - NOT MERGED, decide by hand\n")
    if not r["ambiguous"]:
        A("None.\n")
    for s in r["ambiguous"]:
        A("\n- ours: %s" % "; ".join("**%s** (`%s`)" % (ours_by[o]["name"], o) for o in s["ours"] if o in ours_by))
        A("  theirs: %s" % "; ".join("%s (`%s`)" % (label(theirs[x]), x) for x in s["theirs"] if x in theirs))
        A("  score %.2f (%s) - nothing tells them apart, so they were neither merged nor created as new persons"
          % (s["score"], s["why"]))

    A("\n## Clashes - decide by hand\n")
    if not r["clashes"]:
        A("None.\n")
    for oid, x, cl in r["clashes"]:
        A("\n**%s** <-> %s (`%s`)\n" % (ours_by[oid]["name"], theirs[x]["name"], oid))
        for field, ov, tv in cl:
            A("- %s: ours '%s', theirs '%s'" % (field, ov, tv))

    for title, suffix in (("More precise dates in the other tree (same year, fuller date, or a calendar stated only there) - NOT WRITTEN, "
                           "decide by hand", ": date"),
                          ("Place refinements (same place, more detail) - NOT WRITTEN, transfer if wanted",
                           ": place")):
        A("\n## %s\n" % title)
        rows = [(oid, [x for x in rf if x[0].endswith(suffix)]) for oid, _, rf in r["refines"]]
        rows = [(oid, rf) for oid, rf in rows if rf]
        if not rows:
            A("None.\n")
        for oid, rf in rows:
            A("- **%s** (`%s`): %s" % (ours_by[oid]["name"], oid,
                                       "; ".join("%s ours '%s', theirs '%s'" % (f, ov, tv) for f, ov, tv in rf)))

    A("\n## Cause of death, burial, residence, events, notes (%d)\n" % len(r["extras"]))
    for oid, x, ex, sr in r["extras"]:
        A("- **%s**: %s%s" % (ours_by[oid]["name"], "; ".join(ex), (" - sources: " + " | ".join(sr)) if sr else ""))

    A("\n## New facts for our empty events\n")
    if not r["facts"]:
        A("None.\n")
    for oid, x, add in r["facts"]:
        A("- **%s** (`%s`): %s" % (ours_by[oid]["name"], oid,
                                   "; ".join("%s %s = %s" % (k, f, v) for k, d in add.items() for f, v in d.items())))

    A("\n## Facts for an empty field of an event we already document - NOT WRITTEN, decide by hand\n")
    if not r["lacks"]:
        A("None.\n")
    for oid, x, lack in r["lacks"]:
        A("- **%s** (`%s`): %s" % (ours_by[oid]["name"], oid, "; ".join("%s = %s" % (f, v) for f, v in lack)))

    A("\n## Persons we do not have (%d)\n" % len(r["new_people"]))
    for x in r["new_people"]:
        t = theirs[x]
        years = ("(%s-%s)" % (year(t["birth"].get("date", "")), year(t["death"].get("date", "")))).replace("(-)", "")
        A("- %s %s%s" % (t["name"] or "(no name)", years,
                         " - " + t["notes"].split("\n")[0][:120] if t["notes"] else ""))

    A("\n## New links (%d)\n" % len(r["new_links"]))
    for a, b, k in r["new_links"]:
        A("- %s: %s -> %s" % (k.lower(), ours_by[a]["name"] if a in ours_by else a,
                              ours_by[b]["name"] if b in ours_by else b))

    if r["inferred_pairs"]:
        A("\n## Pairs inferred from shared children (%d) - the file has no marriage record\n"
          % len(r["inferred_pairs"]))
        for a, b, k in r["inferred_pairs"]:
            A("- %s ~ %s" % (ours_by[a]["name"] if a in ours_by else a, ours_by[b]["name"] if b in ours_by else b))

    A("\n## In our graph, not in theirs (%d) - what could be sent back\n" % len(r["ours_only"]))
    for oid in r["ours_only"]:
        p = ours_by[oid]
        years = ("(%s-%s)" % (year((p.get("birth") or {}).get("date")), year((p.get("death") or {}).get("date")))
                 ).replace("(-)", "")
        A("- %s %s" % (p["name"], years))
    return "\n".join(L) + "\n"


def make_id(name, used):
    """ext-<transliterated name>, made unique with a numeric suffix."""
    base = IMPORTED_PREFIX + re.sub(r"[^a-z0-9]+", "-", translit(name).lower()).strip("-")
    pid, n = base, 2
    while pid in used:
        pid, n = "%s-%d" % (base, n), n + 1
    return pid


def apply_changes(r, persons, links):
    """Add new persons, new facts in entirely empty events and new links to the in-memory graph."""
    theirs, m_theirs = r["theirs"], r["m_theirs"]
    stamp = "%s, import %s (%s)" % (r["source_name"], datetime.date.today().isoformat(),
                                    os.path.basename(r["path"]))
    by_id = {p["id"]: p for p in persons}
    for oid, x, add in r["facts"]:
        p = by_id[oid]
        for ev, fields in add.items():
            if not event_untouched(p.get(ev)):       # compare() lists such facts; nothing of ours is written over
                continue
            julian = "date" in fields and "JULIAN" in (theirs.get(x, {}).get(ev, {}).get("qualifier") or "")
            p[ev] = {"date": None, "style": "OS" if julian else "", "place": "",
                     "confidence": IMPORT_CONFIDENCE, "source": stamp}
            p[ev].update(fields)

    for oid, x, ex, sr in r["extras"]:
        p = by_id[oid]
        if ex:
            p["notes"] = ((p.get("notes") or "") + " " if p.get("notes") else "") + \
                "From the %s tree: %s." % (r["source_name"], "; ".join(ex))
        if sr:
            p.setdefault("sources", []).extend("%s: %s" % (r["source_name"], s) for s in sr)

    for x, oid in m_theirs.items():
        if oid in by_id and theirs[x].get("uid"):
            if not by_id[oid].get("external_ids"):      # may be an explicit null
                by_id[oid]["external_ids"] = {}
            if not by_id[oid]["external_ids"].get(r["source_name"]):     # an id of ours is never replaced
                by_id[oid]["external_ids"][r["source_name"]] = theirs[x]["uid"]

    used = {p["id"] for p in persons}
    for x in r["new_people"]:
        t = theirs[x]
        pid = make_id(t["name"], used)
        used.add(pid)
        m_theirs[x] = pid
        ev_notes = ["; ".join(q for q in (e["type"], e["date"], e["place"], e["note"]) if q)
                    for e in t.get("events", [])]
        persons.append({
            "id": pid, "name": t["name"], "variants": t["variants"], "sex": t["sex"], "family": t["surname"],
            "birth": {"date": t["birth"].get("date") or None, "style": "",
                      "place": t["birth"].get("place", ""), "confidence": IMPORT_CONFIDENCE, "source": stamp},
            "death": {"date": t["death"].get("date") or None, "style": "",
                      "place": t["death"].get("place", ""), "confidence": IMPORT_CONFIDENCE, "source": stamp},
            "external_ids": {r["source_name"]: t.get("uid", "")},
            "disputes": [],
            "notes": "; ".join([t["notes"]] * bool(t["notes"].strip()) + [e for e in ev_notes if e]),
            "sources": [stamp],
        })

    # links of the new persons are carried over too
    have = {(l["from"], l["to"], "PARENT" if l["type"] == "ADOPTIVE_PARENT" else l["type"]) for l in links}
    extra = list(r["new_links"])
    for x, t in theirs.items():
        if x not in m_theirs:
            continue
        for par in set(t.get("parents", [])):
            if par in m_theirs:
                extra.append((m_theirs[par], m_theirs[x], "PARENT"))
        for sp, explicit in set(t.get("spouses", [])):
            if sp in m_theirs and explicit:
                extra.append((m_theirs[sp], m_theirs[x], "SPOUSE"))
    added = 0
    for a, b, k in extra:
        if (a, b, k) in have or (k == "SPOUSE" and (b, a, k) in have):
            continue
        have.add((a, b, k))
        links.append({"from": a, "type": k, "to": b, "confidence": IMPORT_CONFIDENCE, "source": stamp,
                      "note": "carried over from the external tree"})
        added += 1
    return added


# ---------- Cyrillic transliteration for ids (BGN/PCGN without diacritics) ----------
TRANS = dict(zip("абвгдежзийклмнопрстуфхцчшщыэюяъь",
                 ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s",
                  "t", "u", "f", "kh", "ts", "ch", "sh", "shch", "y", "e", "yu", "ya", "", ""]))
TRANS["ё"] = "e"


def translit(s):
    """Cyrillic -> Latin, lower case; Latin diacritics are folded; other characters stay."""
    s = fold_latin(s.lower())
    return "".join(TRANS.get(c, c) for c in s)


# ---------- regression: two namesakes in one file ----------
# A round trip through our own export cannot catch this class of bug: the export writes REFN to every
# person and matching goes down the 'same identifier' branch without comparing names. So the
# namesakes are tested separately, on synthetic data.
NAMESAKES_GED = """0 HEAD
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Jaan /Näidis/
1 SEX M
1 BIRT
2 DATE 17 SEP 1864
2 PLAC parish X
0 @I2@ INDI
1 NAME Jaan /Näidis/
1 SEX M
1 BIRT
2 DATE ABT 1797
2 PLAC parish Y
1 DEAT
2 DATE ABT FEB 1840
0 TRLR
"""


def _person(pid, born=None, died=None):
    blank = lambda d: {"date": d, "style": "", "place": "", "confidence": "", "source": ""}
    return {"id": pid, "name": "Näidis Jaan", "sex": "m", "variants": [], "family": "Näidis",
            "birth": blank(born), "death": blank(died), "disputes": []}


def test_namesakes():
    """Two different people with one name must not swap fields: when nothing tells them apart the
    matcher must refuse, and when the dates do tell them apart it must pair them correctly."""
    with tempfile.TemporaryDirectory() as tmp:
        ged = os.path.join(tmp, "namesakes.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(NAMESAKES_GED)
        theirs, _ = read_gedcom(ged)
    births = {x: t["birth"]["date"] for x, t in theirs.items()}
    assert sorted(births.values()) == ["1864-09-17", "~1797"], "synthetic file parsed wrongly: %s" % births

    # 1. Nothing tells them apart: must refuse, not choose at random.
    ours = [_person("naidis-a"), _person("naidis-b")]
    pairs, ambiguous = match(ours, theirs, [])
    assert not pairs, "merged namesakes blindly: %s" % (pairs,)
    assert ambiguous, "stayed silent: the ambiguity was not announced"
    assert {x for s in ambiguous for x in s["theirs"]} == set(theirs), \
        "not all of the ambiguity announced: %s" % (ambiguous,)
    # Same input with renamed ids: the refusal must be the same.
    pairs2, ambiguous2 = match([_person("naidis-z"), _person("naidis-b")], theirs, [])
    assert not pairs2 and ambiguous2, "outcome depends on our ids - that is the bug"

    # 2. Dates tell them apart: must pair correctly, not refuse everything.
    ours = [_person("naidis-1864", born="1864-09-17"), _person("naidis-1797", born="1797", died="1840-02")]
    pairs, ambiguous = match(ours, theirs, [])
    assert not ambiguous, "refused where the dates distinguish: %s" % (ambiguous,)
    assigned = {oid: births[x] for oid, x, _, _ in pairs}
    assert assigned == {"naidis-1864": "1864-09-17", "naidis-1797": "~1797"}, \
        "fields swapped between namesakes: %s" % assigned

    # 3. Ambiguous ones must not leak in as new persons either.
    ours = [_person("naidis-a"), _person("naidis-b")]
    pairs, ambiguous = match(ours, theirs, [])
    amb = {x for s in ambiguous for x in s["theirs"]}
    new = [x for x in theirs if x not in {q[1] for q in pairs} and x not in amb]
    assert not new, "ambiguous namesake created as a new person: %s" % new
    print("namesake test passed: ambiguous pairs refused, distinguishable ones paired correctly")


REFINE_GED = """0 HEAD
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Jaan /Näidis/
1 SEX M
1 BIRT
2 DATE 17 SEP 1864
2 PLAC parish X, Estonia
1 DEAT
2 DATE 3 MAR 1901
"""


def test_refinement_not_written():
    """--apply never changes a non-empty field: a full date of the same year against our bare year
    is listed in the report for a person to decide, and our value, confidence and style stay."""
    ours = _person("naidis-jaan", born="1864", died=None)
    ours["birth"].update(place="parish X", confidence="high", source="baptism entry", style="OS")
    persons, links = [ours], []
    with tempfile.TemporaryDirectory() as tmp:
        ged = os.path.join(tmp, "refine.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(REFINE_GED + "0 TRLR\n")
        r = run(ged, persons, links)
    assert r["pairs"], "test pair was not matched: %s" % (r["pairs"],)
    apply_changes(r, persons, links)
    b = persons[0]["birth"]
    assert b["date"] == "1864", "our bare year was overwritten by --apply: %s" % b
    assert b["confidence"] == "high" and b["style"] == "OS" and b["place"] == "parish X", \
        "a non-empty field of ours was changed: %s" % b
    assert b["source"] == "baptism entry", "source of a refused value was added: %s" % b
    assert persons[0]["death"]["date"] == "1901-03-03", "a fact for an EMPTY field was not added"
    text = report_text(r)
    assert "1864-09-17" in text and "More precise dates" in text, "refinement not listed in the report"
    assert "parish X, Estonia" in text, "place refinement not listed"
    assert "birth date = 1864-09-17" not in text, "refinement listed as a new fact for an empty field"
    print("refinement test passed: a non-empty field is never changed, the more precise value is listed")


APPLY_GED = """0 HEAD
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Jaan /Näidis/
1 SEX M
1 BIRT
2 DATE 17 SEP 1864
0 TRLR
"""


def _graph_files(tmp, persons, links):
    pp, lp = os.path.join(tmp, "persons.json"), os.path.join(tmp, "links.json")
    write_graph(persons, links, pp, lp)
    return pp, lp


def _main_quiet(argv):
    import contextlib
    import io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        main(argv)
    return buf.getvalue()


def test_apply_empty_events_only():
    """a fact enters only an event that is entirely empty. Our birth holds a place, confidence high
    and a source but no date: the date of the other tree is not written, it is listed in its own section."""
    ours = _person("naidis-jaan")
    ours["birth"].update(place="parish X", confidence="high", source="baptism entry")
    with tempfile.TemporaryDirectory() as tmp:
        pp, lp = _graph_files(tmp, [ours], [])
        ged = os.path.join(tmp, "t.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(APPLY_GED)
        before = open(pp, "rb").read()
        report = os.path.join(tmp, "report.md")
        _main_quiet([ged, "--persons", pp, "--links", lp, "--apply", "--report", report])
        after = open(pp, "rb").read()
        text = open(report, encoding="utf-8").read()
    assert after == before, "a graph with a documented event was rewritten: %s" % after.decode("utf-8")[:300]
    assert "NOT WRITTEN" in text and "event we already document" in text and "1864-09-17" in text.split(
        "event we already document")[1], "the date is not listed in the new section"
    # and an entirely empty event still takes the fact, at low confidence, with the import stamp
    ours = _person("naidis-jaan")
    persons = [ours]
    with tempfile.TemporaryDirectory() as tmp:
        ged = os.path.join(tmp, "t.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(APPLY_GED)
        r = run(ged, persons, [])
        apply_changes(r, persons, [])
    b = persons[0]["birth"]
    assert b["date"] == "1864-09-17" and b["confidence"] == "low" and "import" in b["source"], \
        "an empty event did not take the fact at low confidence: %s" % b
    # an event of ours without date and place but with our own source, and an external id of ours, stay
    ours = _person("naidis-jaan")
    ours["birth"].update(style="OS", confidence="medium", source="family memory")
    ours["external_ids"] = {DEFAULT_SOURCE_NAME: "I17"}
    kept = copy.deepcopy(ours)
    with tempfile.TemporaryDirectory() as tmp:
        ged = os.path.join(tmp, "t.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(APPLY_GED.replace("0 TRLR", "1 _UID U99\n0 TRLR") if "_UID" not in APPLY_GED else APPLY_GED)
        persons = [ours]
        r = run(ged, persons, [])
        apply_changes(r, persons, [])
        text = report_text(r)
    assert persons[0]["birth"] == kept["birth"], "our sourced event was written over: %s" % persons[0]["birth"]
    assert persons[0]["external_ids"] == kept["external_ids"], "our external id was replaced: %s" % persons[0]["external_ids"]
    assert "1864-09-17" in text.split("event we already document")[1].split("\n## ")[0], "the fact is not listed"
    assert "I17" in text and "U99" in text, "the differing external id is not listed under Clashes"
    print("apply test passed: only an entirely empty event takes a fact; a documented one is listed")


def test_apply_nothing_to_write():
    """--apply with nothing to write takes no snapshot and rewrites no file."""
    ours = _person("naidis-jaan", born="1864-09-17")
    with tempfile.TemporaryDirectory() as tmp:
        pp, lp = _graph_files(tmp, [ours], [])
        ged = os.path.join(tmp, "t.ged")
        with open(ged, "w", encoding="utf-8") as f:
            f.write(APPLY_GED)
        stamps = [os.stat(x).st_mtime_ns for x in (pp, lp)]
        out = _main_quiet([ged, "--persons", pp, "--links", lp, "--apply"])
        assert not os.path.exists(os.path.join(tmp, "snapshots")), "a snapshot folder was created for nothing"
        assert stamps == [os.stat(x).st_mtime_ns for x in (pp, lp)], "a graph file was rewritten for nothing"
        assert "nothing changed" in out, "no message that nothing changed: %s" % out[-200:]
    print("nothing-to-write test passed: no snapshot, no rewrite")


def test_atomic_writer_keeps_mode_and_link():
    """the atomic writer keeps the mode of an existing file and writes through a symlink."""
    with tempfile.TemporaryDirectory() as tmp:
        real = os.path.join(tmp, "real.json")
        with open(real, "w") as f:
            f.write("[]")
        os.chmod(real, 0o644)
        link = os.path.join(tmp, "link.json")
        os.symlink(real, link)
        _write_json_atomic([{"a": 1}], link)
        assert os.path.islink(link), "the symlink was replaced by a regular file"
        mode = os.stat(real).st_mode & 0o777
        assert mode == 0o644, "mode changed to %o" % mode
        assert json.load(open(real)) == [{"a": 1}], "the real file was not written"
        plain = os.path.join(tmp, "plain.json")
        with open(plain, "w") as f:
            f.write("[]")
        os.chmod(plain, 0o644)
        _write_json_atomic([1], plain)
        assert os.stat(plain).st_mode & 0o777 == 0o644, "mode of a plain file changed"
        leftovers = [x for x in os.listdir(tmp) if x.startswith(".tmp_")]
        assert not leftovers, "temporary files left: %s" % leftovers
    print("writer test passed: mode kept, symlink kept")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare a GEDCOM file with the graph; dry run by default.")
    ap.add_argument("ged", nargs="?", help="GEDCOM file to read")
    ap.add_argument("--persons", help="persons JSON file")
    ap.add_argument("--links", help="links JSON file")
    ap.add_argument("--apply", action="store_true",
                    help="write new persons, facts for entirely empty events (at confidence low) and new links "
                         "into the graph (after a snapshot); never overwrites or removes anything already in the graph "
                         "(labelled notes and sources from the other tree are appended to matched persons); clashes, more "
                         "precise values and values for an empty field of a documented event go to the "
                         "report only; with nothing to write, no snapshot and no rewrite")
    ap.add_argument("--report", help="write the markdown report to this file (default: print it); "
                                     "refuses to overwrite an existing file unless --force is given")
    ap.add_argument("--force", action="store_true", help="let --report overwrite an existing file")
    ap.add_argument("--snapshot-dir", help="where --apply copies the graph first "
                                           "(default: 'snapshots' next to the persons file)")
    ap.add_argument("--source-name", default=DEFAULT_SOURCE_NAME,
                    help="name of the source tree; key in external_ids and prefix of notes (default: %(default)s)")
    ap.add_argument("--source-pattern", default=DEFAULT_SOURCE_PATTERN,
                    help="regular expression: note lines that match are stored as sources (default: %(default)s)")
    ap.add_argument("--confidence", default="low", choices=["low", "medium"],
                    help="confidence given to everything --apply adds from the other tree (default low: "
                         "someone else's tree is not a document; medium only for a tree you know was "
                         "built from documents)")
    ap.add_argument("--self-test", action="store_true", help="run the regression tests (namesakes, no overwrite, empty events only, nothing to "
                                                              "write, atomic writer) and exit")
    args = ap.parse_args(argv)
    global IMPORT_CONFIDENCE
    IMPORT_CONFIDENCE = args.confidence

    if args.self_test:
        test_namesakes()
        test_refinement_not_written()
        test_apply_empty_events_only()
        test_apply_nothing_to_write()
        test_atomic_writer_keeps_mode_and_link()
        return 0
    if not (args.ged and args.persons and args.links):
        ap.error("FILE.ged, --persons and --links are required")
    if not os.path.isfile(args.ged):
        raise SystemExit("GEDCOM file not found: %s" % args.ged)

    if args.report and os.path.exists(args.report) and not args.force:
        raise SystemExit("report file exists, not overwriting: %s (use --force)" % args.report)
    persons, links = load_graph(args.persons, args.links)
    r = run(args.ged, persons, links, args.source_name, args.source_pattern)
    if r["ambiguous"]:
        warn_ambiguous(r["ambiguous"], r["theirs"], r["ours_by"])
    text = report_text(r)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(text)
        print("report:", args.report)
    else:
        print(text)
    print(stats(r))
    if args.apply:
        before = copy.deepcopy((persons, links))
        added = apply_changes(r, persons, links)          # in memory only; the files are written below
        if (persons, links) == before:
            print("nothing changed: nothing to write, no snapshot taken, no file rewritten")
            return 0
        snaps = snapshot(args.persons, args.links, args.snapshot_dir or
                         os.path.join(os.path.dirname(os.path.abspath(args.persons)), "snapshots"))
        print("snapshot:", ", ".join(snaps))
        write_graph(persons, links, args.persons, args.links)
        print("graph updated: persons %d, links %d (+%d)" % (len(persons), len(links), added))
    else:
        print("dry run: nothing written (use --apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
