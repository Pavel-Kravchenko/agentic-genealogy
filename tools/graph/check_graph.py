#!/usr/bin/env python3
"""Structural and chronological checks of a family graph (persons file + links file).

    python3 check_graph.py --persons persons.json --links links.json

Three categories are counted separately because they are fixed differently:

  ERROR    the graph is broken as a structure (dangling ids, unknown link type, ancestor cycle,
           unreadable date, missing required field). Only errors give exit code 1.
  FINDING  the graph is intact but the data contradict each other (a child older than its mother,
           a child born long after the mother died). Do not "fix" findings by adjusting the data:
           list them, check the documents, keep the dispute visible.
  STATE    a field holds a legitimate but unfinished value: the event is absent (`null`) or its
           confidence is "disputed". Not a defect, no effect on the exit code.

The JSON schema is in SCHEMA.md. Python 3.9+, standard library only.
"""
import argparse
import json
import re
import sys
from collections import defaultdict, namedtuple

LINK_TYPES = {"PARENT", "SPOUSE", "HALF_SIBLING", "GODPARENT",
              "GUARANTOR", "ADOPTIVE_PARENT", "POSSIBLE_KIN"}
CONFIDENCE = {"high", "medium", "low"}
SEX = {"m", "f"}
PARENT_TYPES = {"PARENT", "ADOPTIVE_PARENT"}
REQUIRED_PERSON_FIELDS = ("id", "name", "variants", "sex", "family", "birth", "death", "disputes")
DISPUTED = "disputed"

# Defaults of the chronology checks (all overridable on the command line)
MIN_MOTHER_AGE = 14
MAX_MOTHER_AGE = 50
MAX_MONTHS_AFTER_PARENT_DEATH = 9
MIN_YEAR, MAX_YEAR = 1500, 2100

EXACT = ""
APPROX, BEFORE, AFTER, BETWEEN, DOUBLE_YEAR = "approx", "before", "after", "between", "double year"

Date = namedtuple("Date", "year month day qualifier end_year")

# Canonical qualifiers are English; GEDCOM abbreviations and the Russian qualifiers that old
# graphs and imported files carry are read as aliases.
QUALIFIERS = {
    "~": APPROX, "abt": APPROX, "cal": APPROX, "est": APPROX, "ca": APPROX, "circa": APPROX,
    "около": APPROX, "ок": APPROX,
    "before": BEFORE, "bef": BEFORE, "до": BEFORE,
    "after": AFTER, "aft": AFTER, "после": AFTER,
}
QUALIFIER_RE = re.compile(
    r"^(~|circa|abt|cal|est|ca|около|ок|before|bef|до|after|aft|после)\.?\s*(.*)$", re.I)
BETWEEN_RE = re.compile(r"^(?:between|bet|from|между)\s+(.+?)\s+(?:and|to|и)\s+(.+)$", re.I)
DOUBLE_YEAR_RE = re.compile(r"^(\d{4})/(\d{2}|\d{4})$")


def parse_date(text, min_year=MIN_YEAR, max_year=MAX_YEAR):
    """Parse a graph date together with its qualifier.

    '1861-03-09'          -> Date(1861, 3, 9, EXACT, None)
    '1938-07'             -> Date(1938, 7, None, EXACT, None)
    '~1800'               -> Date(1800, None, None, APPROX, None)
    'before 1800'         -> Date(1800, None, None, BEFORE, None)   (also 'BEF 1800', 'до 1800')
    'between 1759 and 1762' -> Date(1759, None, None, BETWEEN, 1762)
    '1760/61'             -> Date(1760, None, None, DOUBLE_YEAR, 1761)

    Returns None for an empty date. Raises ValueError on anything else that is not a date.
    """
    if text is None or text == "":
        return None
    t = text.strip()

    m = DOUBLE_YEAR_RE.match(t)
    if m:
        year = int(m.group(1))
        tail = m.group(2)
        end = int(tail) if len(tail) == 4 else year - year % 100 + int(tail)
        _check_year(year, text, min_year, max_year)
        _check_year(end, text, min_year, max_year)
        if end <= year:
            raise ValueError("double year runs backwards: %r" % text)
        return Date(year, None, None, DOUBLE_YEAR, end)

    m = BETWEEN_RE.match(t)
    if m:
        start = _parse_core(m.group(1), text, min_year, max_year)
        end = _parse_core(m.group(2), text, min_year, max_year)
        if end.year < start.year:
            raise ValueError("range runs backwards: %r" % text)
        return Date(start.year, start.month, start.day, BETWEEN, end.year)

    qualifier = EXACT
    m = QUALIFIER_RE.match(t)
    if m:
        qualifier = QUALIFIERS[m.group(1).lower()]
        t = m.group(2)
    return _parse_core(t, text, min_year, max_year)._replace(qualifier=qualifier)


def _parse_core(text, original, min_year, max_year):
    """ISO part without qualifier: YYYY, YYYY-MM or YYYY-MM-DD."""
    parts = text.strip().split("-")
    if len(parts) > 3:
        raise ValueError("not a date: %r" % original)
    numbers = [int(p) for p in parts]          # ValueError on garbage, on purpose
    year = numbers[0]
    month = numbers[1] if len(numbers) > 1 else None
    day = numbers[2] if len(numbers) > 2 else None
    _check_year(year, original, min_year, max_year)
    if month is not None and not (1 <= month <= 12):
        raise ValueError("month out of range: %r" % original)
    if day is not None and not (1 <= day <= 31):
        raise ValueError("day out of range: %r" % original)
    return Date(year, month, day, EXACT, None)


def _check_year(year, original, min_year, max_year):
    if not (min_year <= year <= max_year):
        raise ValueError("year out of range: %r" % original)


def earliest_month(d):
    """Earliest point of an inexact date, in months. 'before YYYY' has no lower bound."""
    if d.qualifier == BEFORE:
        return float("-inf")
    return d.year * 12 + (d.month or 1) - 1


def latest_month(d):
    """Latest point of an inexact date, in months. 'after YYYY' has no upper bound."""
    if d.qualifier == AFTER:
        return float("inf")
    if d.end_year is not None:
        return d.end_year * 12 + 11
    return d.year * 12 + (d.month or 12) - 1


def age_at(born, child_born):
    """Age in whole years at the child's birth, at the precision available."""
    years = child_born.year - born.year
    if born.month and child_born.month and child_born.month < born.month:
        years -= 1
    return years


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check(persons, links, min_mother_age=MIN_MOTHER_AGE, max_mother_age=MAX_MOTHER_AGE,
          max_months_after_death=MAX_MONTHS_AFTER_PARENT_DEATH):
    """Run all checks. Returns (errors, findings, states) where states is {kind: [line]}."""
    errors, findings, states = [], [], defaultdict(list)

    # ---------- 1. schema and unique ids ----------
    nodes = {}
    for p in persons:
        pid = p.get("id")
        if not pid:
            errors.append("node without id: %r" % p)
            continue
        if pid in nodes:
            errors.append("duplicate id: %s" % pid)
        nodes[pid] = p
        for field in REQUIRED_PERSON_FIELDS:
            if field not in p:
                errors.append("%s: missing required field '%s'" % (pid, field))
        if p.get("sex") not in SEX:
            errors.append("%s: sex '%s' - only m/f allowed" % (pid, p.get("sex")))
        for event in ("birth", "death"):
            e = p.get(event)
            if e is None:
                states["event absent from graph"].append("%s/%s" % (pid, event))
                continue
            if e.get("confidence") == DISPUTED:
                reason = "; ".join(p.get("disputes") or []) or "field 'disputes' is empty"
                if len(reason) > 120:
                    reason = reason[:120] + "..."
                states["confidence 'disputed'"].append("%s/%s: %s" % (pid, event, reason))
            elif e.get("confidence") not in CONFIDENCE:
                errors.append("%s/%s: confidence '%s' is not one of %s"
                              % (pid, event, e.get("confidence"), "/".join(sorted(CONFIDENCE | {DISPUTED}))))
            if e.get("confidence") == "high" and not e.get("source"):
                errors.append("%s/%s: confidence 'high' without a source" % (pid, event))
            try:
                parse_date(e.get("date"))
            except ValueError as ex:
                errors.append("%s/%s: %s" % (pid, event, ex))

    # ---------- 1a. a node's own chronology ----------
    for pid, p in nodes.items():
        try:
            b = parse_date((p.get("birth") or {}).get("date"))
            d = parse_date((p.get("death") or {}).get("date"))
        except ValueError:
            continue                      # already reported above
        if b and d and latest_month(d) < earliest_month(b):
            findings.append("%s: death (%s) before birth (%s)"
                            % (pid, p["death"]["date"], p["birth"]["date"]))

    # ---------- 2. links: types, references, sources ----------
    parents = defaultdict(list)           # child -> [parent] (PARENT only)
    parental = defaultdict(list)          # child -> [parent] (incl. adoptive, for the cycle check)
    spouses = set()
    for l in links:
        frm, ltype, to = l.get("from"), l.get("type"), l.get("to")
        if ltype not in LINK_TYPES:
            errors.append("unknown link type '%s': %s -> %s" % (ltype, frm, to))
            continue
        if frm not in nodes:
            errors.append("link %s: 'from' = %s - no such node" % (ltype, frm))
            continue
        if to not in nodes:
            errors.append("link %s: 'to' = %s - no such node" % (ltype, to))
            continue
        if frm == to:
            errors.append("link %s points at itself: %s" % (ltype, frm))
            continue
        if l.get("confidence") not in CONFIDENCE:
            errors.append("link %s %s->%s: confidence '%s'" % (ltype, frm, to, l.get("confidence")))
        if l.get("confidence") == "high" and not l.get("source"):
            errors.append("link %s %s->%s: confidence 'high' without a source" % (ltype, frm, to))
        if ltype == "PARENT":
            parents[to].append(frm)
        if ltype in PARENT_TYPES:
            parental[to].append(frm)
        if ltype == "SPOUSE":
            if (to, frm) in spouses or (frm, to) in spouses:
                errors.append("link SPOUSE %s--%s written twice (it is symmetric, write it once)" % (frm, to))
            spouses.add((frm, to))

    # ---------- 3. at most two parents ----------
    for child, plist in parents.items():
        if len(set(plist)) > 2:
            findings.append("%s has more than two parents: %s" % (child, ", ".join(sorted(set(plist)))))

    # ---------- 4. cycles: an ancestor who is their own descendant ----------
    WHITE, GREY, BLACK = 0, 1, 2
    colour = defaultdict(int)
    path = []

    def visit(node):
        colour[node] = GREY
        path.append(node)
        for parent in parental.get(node, []):
            if colour[parent] == GREY:
                ring = path[path.index(parent):] + [parent]
                errors.append("ancestor cycle: " + " -> ".join(ring))
            elif colour[parent] == WHITE:
                visit(parent)
        path.pop()
        colour[node] = BLACK

    sys.setrecursionlimit(10000)
    for pid in nodes:
        if colour[pid] == WHITE:
            visit(pid)

    # ---------- 5. parent/child chronology ----------
    for child, plist in parents.items():
        try:
            cb = parse_date((nodes[child].get("birth") or {}).get("date"))
        except ValueError:
            continue
        if cb is None:
            continue
        for parent in set(plist):
            pnode = nodes[parent]
            try:
                pb = parse_date((pnode.get("birth") or {}).get("date"))
                pd = parse_date((pnode.get("death") or {}).get("date"))
            except ValueError:
                continue
            if pb is not None:
                if latest_month(cb) < earliest_month(pb):
                    findings.append("%s (%s) was born before their parent %s (%s)"
                                    % (child, nodes[child]["birth"]["date"], parent, pnode["birth"]["date"]))
                elif pnode.get("sex") == "f":
                    years = age_at(pb, cb)
                    if years < min_mother_age or years > max_mother_age:
                        findings.append("mother %s (%s) would have been %d at the birth of %s (%s)"
                                        % (parent, pnode["birth"]["date"], years,
                                           child, nodes[child]["birth"]["date"]))
            if pd is not None:
                gap = earliest_month(cb) - latest_month(pd)
                if gap > max_months_after_death:
                    who = "mother" if pnode.get("sex") == "f" else "father"
                    findings.append("%s (%s) was born more than %d months after the death of the %s %s (%s)"
                                    % (child, nodes[child]["birth"]["date"], max_months_after_death,
                                       who, parent, pnode["death"]["date"]))
    return errors, findings, states


def main(argv=None):
    ap = argparse.ArgumentParser(description="Structural and chronological checks of a family graph.")
    ap.add_argument("--persons", required=True, help="persons JSON file")
    ap.add_argument("--links", required=True, help="links JSON file")
    ap.add_argument("--min-mother-age", type=int, default=MIN_MOTHER_AGE)
    ap.add_argument("--max-mother-age", type=int, default=MAX_MOTHER_AGE)
    ap.add_argument("--max-months-after-death", type=int, default=MAX_MONTHS_AFTER_PARENT_DEATH,
                    help="a child born later than this after a parent's death is a finding")
    args = ap.parse_args(argv)

    persons, links = load_json(args.persons), load_json(args.links)
    print("Checking: %s + %s" % (args.persons, args.links))
    errors, findings, states = check(persons, links, args.min_mother_age, args.max_mother_age,
                                     args.max_months_after_death)

    print("Nodes: %d   links: %d" % (len(persons), len(links)))
    by_type = defaultdict(int)
    for l in links:
        by_type[l.get("type")] += 1
    print("Links by type: " + ", ".join("%s %d" % (t, by_type[t]) for t in sorted(by_type, key=str)))
    by_conf = defaultdict(int)
    for p in persons:
        by_conf[(p.get("birth") or {}).get("confidence")] += 1
    print("Birth-date confidence: " + ", ".join("%s %d" % (c, by_conf[c]) for c in sorted(by_conf, key=str)))

    print("\nERRORS (structure broken, must be fixed): %d" % len(errors))
    for t in errors:
        print("  ! " + t)
    print("\nFINDINGS (data contradict each other, do not fix by adjusting data): %d" % len(findings))
    for t in findings:
        print("  ~ " + t)
    total = sum(len(v) for v in states.values())
    print("\nFIELD STATES (legitimate values, not defects): %d" % total)
    for kind in sorted(states):
        print("  . %s: %d" % (kind, len(states[kind])))
    for kind in sorted(states):
        if kind == "event absent from graph":
            continue                       # listing every empty event is noise
        for t in states[kind]:
            print("    . %s - %s" % (kind, t))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
