#!/usr/bin/env python3
"""Find and merge duplicates in the graph: one person recorded twice - in Cyrillic and in Latin
script ('Примеров Иван' / 'Primerow Ivan'), or under a maiden and a married surname.

    python3 merge_duplicates.py --persons persons.json --links links.json           # show only
    python3 merge_duplicates.py --persons persons.json --links links.json --apply   # merge
    python3 merge_duplicates.py --persons persons.json --links links.json --invariants   # graph invariants
    python3 merge_duplicates.py --self-test                                         # regression on synthetic data

Dry run is the default. --apply copies both graph files to the snapshot directory first, then merges
and writes the files and a markdown report of the merges.

Each event (birth, death) of the imported copy is merged into ours field by field (dates compared after
strip(), places without regard to case and blanks):
  - Our event is entirely empty (no date, no place, no source, no note): the imported event is taken as a
    whole (date, place, style, source and its confidence, or `low` when it has none). Nothing of ours is
    mixed in. An event of ours that holds only a source or a note is left as it is; theirs is listed.
  - Our event holds a value: no field of ours is changed, no empty field of ours is filled and `style` is
    never copied. Where both copies hold a value and they agree, the other copy's source is added to our
    source (once), but only when no field of that event differs. A bare year against a fuller date of the
    same year and qualifier is no disagreement: when theirs is the less precise it counts as agreement,
    when theirs is the fuller it is listed as "more precise value in the other copy, not written" and its
    source is not added. Where the values really differ, ours stays and one sentence with both values,
    both calendar styles (for a date) and both sources is added to the person's `disputes`; the event's
    `confidence` is NOT changed. A value of the other copy for a field we lack is not written: it is
    listed as "decide by hand".
The dry run prints, and the report written by --apply contains, three separate lists: disagreements
(written into `disputes`), more precise values not written, and values for fields we lack not written.
A pair skipped because one of its nodes was already merged in the same run is printed too.

A candidate pair has the same sex and either (a) the same FULL birth or death date and compatible names
(one recognisable in the other after transliteration) or a shared spouse or child, or (b) the same full
set of at least two name tokens, compatible names, and a shared relative or the same birth date. Twins are not
glued together because their names differ. Only an imported node (id prefix `ext-`) is merged INTO
one of ours.

Three refusals; none is bypassed silently, each is said aloud and the pair is not merged:
  1. both nodes were created by an importer: only imported into ours, otherwise a duplicate in the
     source is passed off as our person;
  2. the nodes carry different `external_ids` from one source: the source itself says they are two people;
  3. the merge would make a parent not older than the child: generation arithmetic outranks a name
     and date match.
Python 3.9+, standard library only. Schema: SCHEMA.md.
"""
import argparse
import collections
import copy
import os
import re
import sys
import time

import gedcom_import as gi

IMPORTED_PREFIXES = ("ext-",)     # id prefixes of nodes created by an importer
MIN_GAP = 12                      # years between a parent's birth and a child's birth
MAX_SPREAD = 20                   # a larger spread of birth years means different people


class Graph:
    def __init__(self, persons, links, imported_prefixes=IMPORTED_PREFIXES, min_gap=MIN_GAP,
                 max_spread=MAX_SPREAD):
        self.persons, self.links = persons, links
        self.P = {p["id"]: p for p in persons}
        self.prefixes, self.min_gap, self.max_spread = tuple(imported_prefixes), min_gap, max_spread

    def imported(self, pid):
        return pid.startswith(self.prefixes)


def tokens(name):
    """Name tokens transliterated to Latin, so that 'Примеров' and 'Primerow' meet."""
    t = []
    for w in gi.key_tokens(name) + gi.key_tokens(re.sub(r"[^A-Za-z ]", " ", name)):
        w = gi.translit(w).lower()
        w = re.sub(r"[^a-z]", "", w)
        if len(w) > 2 and w not in t:
            t.append(w)
    return t


def compatible(a, b):
    """At least one name is recognised in full in the other (with a typo of one or two letters)."""
    ta = tokens(a["name"] + " " + " ".join(a.get("variants") or []))
    tb = tokens(b["name"] + " " + " ".join(b.get("variants") or []))
    if not ta or not tb:
        return False
    hit = sum(1 for x in ta if any(gi.lev(x, y) <= 2 for y in tb))
    return hit >= min(len(ta), len(tb)) and hit >= 1


def date_of(p, k):
    return (p.get(k) or {}).get("date") or ""


def year_of(p, k):
    d = date_of(p, k)[:4]
    return int(d) if d.isdigit() else None


def neighbours(links):
    """Spouses and children - but NOT parents: twins share parents, while a shared husband or a
    shared child belongs to one and the same person."""
    n = collections.defaultdict(set)
    for l in links:
        if l["type"] == "SPOUSE":
            n[l["from"]].add(("s", l["to"]))
            n[l["to"]].add(("s", l["from"]))
        elif l["type"] in ("PARENT", "ADOPTIVE_PARENT"):
            n[l["from"]].add(("c", l["to"]))
    return n


def kinship(links, birth_only=False):
    """-> (children[parent], parents[child]). `birth_only` drops ADOPTIVE_PARENT: a correctly recorded
    stepmother is a second 'mother' of the child and must not be reported as corruption."""
    types = ("PARENT",) if birth_only else ("PARENT", "ADOPTIVE_PARENT")
    children, parents = collections.defaultdict(set), collections.defaultdict(set)
    for l in links:
        if l["type"] in types:
            children[l["from"]].add(l["to"])
            parents[l["to"]].add(l["from"])
    return children, parents


def refusal(g, own, other, children, parents):
    """-> reason why the merge is forbidden, or None."""
    a, b = g.P[own], g.P[other]
    if g.imported(own) and g.imported(other):
        return "both nodes were created by an importer (%s and %s) - an imported node may only be merged into ours" % (own, other)
    ea, eb = a.get("external_ids") or {}, b.get("external_ids") or {}
    for source in set(ea) & set(eb):
        if ea[source] and eb[source] and ea[source] != eb[source]:
            return "different external_ids from source '%s' (%s != %s) - the source holds them to be different people" % (
                source, ea[source], eb[source])
    ya, yb = year_of(a, "birth"), year_of(b, "birth")
    if ya and yb and abs(ya - yb) > g.max_spread:
        return "birth years differ by %d years (%d and %d) - not one person" % (abs(ya - yb), ya, yb)
    # generation arithmetic on the merged set of links: the merged node keeps our date, the links of both
    result = ya or yb
    if result:
        for child in children[own] | children[other]:
            yc = year_of(g.P[child], "birth") if child in g.P else None
            if yc is not None and yc - result < g.min_gap:
                return "after the merge the parent (b. %d) would not be older than the child '%s' (b. %d)" % (
                    result, g.P[child]["name"], yc)
        for parent in parents[own] | parents[other]:
            yp = year_of(g.P[parent], "birth") if parent in g.P else None
            if yp is not None and result - yp < g.min_gap:
                return "after the merge the parent '%s' (b. %d) would not be older than the person (b. %d)" % (
                    g.P[parent]["name"], yp, result)
    return None


def candidates(g):
    """-> (pairs to merge, refused pairs with reason)."""
    near = neighbours(g.links)
    children, parents = kinship(g.links)
    groups = collections.defaultdict(list)
    for p in g.persons:
        for k in ("birth", "death"):
            if len(date_of(p, k)) == 10:
                groups[(k, date_of(p, k))].append(p["id"])
        groups[("name", tuple(sorted(set(gi.key_tokens(p["name"])))))].append(p["id"])
    pairs, refused = set(), {}
    for key, ids in groups.items():
        if len(ids) < 2 or (key[0] == "name" and not key[1]):
            continue
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                own, other = (a, b) if not g.imported(a) else (b, a)
                if not g.imported(other):
                    continue          # only imported nodes are merged into ours
                if g.P[own]["sex"] != g.P[other]["sex"]:
                    continue
                shared = near[own] & near[other]
                names_agree = compatible(g.P[own], g.P[other])
                if key[0] == "name":
                    # a namesake by one word is no argument; a shared relative or the same birth date is
                    if len(key[1]) < 2 or not (shared or date_of(g.P[own], "birth") == date_of(g.P[other], "birth") != ""):
                        continue
                    if not names_agree:
                        continue
                elif not (names_agree or shared):
                    continue          # the date matched, but neither name nor relatives do
                reason = refusal(g, own, other, children, parents)
                if reason:
                    refused[(own, other)] = reason
                else:
                    pairs.add((own, other))
    return sorted(pairs), refused


def _style(ev):
    return ev.get("style") or "not stated"


def _place_key(v):
    return " ".join(v.casefold().split())


def _compare_field(field, ov, tv):
    """-> 'agree', 'precise' (theirs is the fuller date of the same year), 'differ'. Both values are
    non-empty. Dates are compared after strip(); places without regard to case and blanks."""
    if field == "date":
        if ov == tv:
            return "agree"
        (oq, ob), (tq, tb) = gi.split_qual(ov), gi.split_qual(tv)
        if oq == tq and gi.year(ob) == gi.year(tb) and (len(ob) == 4 or len(tb) == 4):
            return "precise" if len(tb) > len(ob) else "agree"
        return "differ"
    return "agree" if _place_key(ov) == _place_key(tv) else "differ"


def event_changes(ea, eb):
    """Compare one event of ours with the same event of the other copy; both hold a value.
    -> (agree, differ, precise, lacking): lists of fields (differ: (field, ours, theirs))."""
    agree, differ, precise, lacking = [], [], [], []
    for field in ("date", "place"):
        ov, tv = (ea.get(field) or "").strip(), (eb.get(field) or "").strip()
        if not tv:
            continue
        if not ov:
            lacking.append((field, tv))
            continue
        how = _compare_field(field, ov, tv)
        if field == "date" and ov == tv:        # same date string: the calendar still has to match
            os_, ts = (ea.get("style") or "").strip(), (eb.get("style") or "").strip()
            if os_ and ts and os_ != ts:
                how = "differ"
            elif ts and not os_:
                how = "precise"
        if how == "agree":
            agree.append(field)
        elif how == "precise":
            precise.append((field, ov, tv))
        else:
            differ.append((field, ov, tv))
    return agree, differ, precise, lacking


def _holds_value(ev):
    return bool((ev or {}).get("date") or (ev or {}).get("place"))


def _add_source(ev, source):
    """Append a source to an event's source list (segments joined by '; '), once."""
    have = [s.strip() for s in (ev.get("source") or "").split(";") if s.strip()]
    s = (source or "").strip()
    if s and s not in have:
        ev["source"] = "; ".join(have + [s])


def dispute_sentence(g, own, other, k, field, ours, theirs):
    a, b = g.P[own], g.P[other]
    if field == "date":
        ours = "%s (calendar: %s)" % (ours, _style(a[k]))
        theirs = "%s (calendar: %s)" % (theirs, _style(b[k]))
    return "%s %s: %s in our record (source: %s), %s in the imported record `%s` (source: %s); ours kept." % (
        k, field, ours, (a[k].get("source") or "none"), theirs, other, (b[k].get("source") or "none"))


Merge = collections.namedtuple("Merge", "disputes precise lacking")


def merge_into(g, own, other):
    """Merge `other` into `own`, event by event (birth, death), field by field.
    Our event entirely empty (no date, no place, no source, no note): the other copy's event is taken as
    a whole, with its confidence or `low`. An event of ours that holds only a source or a note is left as
    it is and the other copy's event is listed. Otherwise no field of ours is changed or filled in and
    `style` is never copied:
    values that agree add the other copy's source (only when no field of the event differs); a bare year
    against a fuller date of the same year is a refinement (agreement when theirs is the less precise,
    listed in `precise` when theirs is the fuller); a real difference is written into our `disputes`
    (both values, both calendar styles, both sources) and the confidence stays; a field we lack is listed
    in `lacking`. -> Merge(disputes, precise, lacking): lists of sentences."""
    a, b = g.P[own], g.P[other]
    res = Merge([], [], [])
    for k in ("birth", "death"):
        eb = b.get(k) or {}
        if not _holds_value(eb):
            continue
        if gi.event_untouched(a.get(k)):
            a[k] = dict(eb, date=eb.get("date"), style=eb.get("style") or "", place=eb.get("place") or "",
                        confidence=eb.get("confidence") or "low", source=eb.get("source") or "")
            continue
        if not _holds_value(a.get(k)):
            res.lacking.append("%s: %s %s in the imported record `%s` (source: %s); our event holds a source "
                               "or a note and no value, not written: decide by hand"
                               % (k, eb.get("date") or "", eb.get("place") or "", other, eb.get("source") or "none"))
            continue
        ea = a[k]
        agree, differ, precise, lacking = event_changes(ea, eb)
        for field, ov, tv in differ:
            res.disputes.append(dispute_sentence(g, own, other, k, field, ov, tv))
        for field, ov, tv in precise:
            if field == "date":
                ov, tv = "%s (calendar: %s)" % (ov, _style(ea)), "%s (calendar: %s)" % (tv, _style(eb))
            res.precise.append("%s %s: %s in our record, %s in the imported record `%s` (source: %s); "
                               "more precise value in the other copy, not written"
                               % (k, field, ov, tv, other, eb.get("source") or "none"))
        for field, tv in lacking:
            res.lacking.append("%s %s: %s in the imported record `%s` (source: %s); value in the other copy "
                               "for a field we lack, not written: decide by hand"
                               % (k, field, tv, other, eb.get("source") or "none"))
        if agree and not differ:
            _add_source(ea, eb.get("source"))
    sentences = res.disputes
    disputes = a.setdefault("disputes", [])
    disputes.extend(x for x in sentences if x not in disputes)
    variants = a.setdefault("variants", [])
    for v in [b["name"]] + (b.get("variants") or []):
        if v and v != a["name"] and v not in variants:
            variants.append(v)
    if b.get("notes") and b["notes"] not in (a.get("notes") or ""):
        a["notes"] = ((a.get("notes") or "") + " " if a.get("notes") else "") + \
            "From the imported record `%s`: %s" % (other, b["notes"])
    for s in b.get("sources") or []:
        a.setdefault("sources", [])
        if s not in a["sources"]:
            a["sources"].append(s)
    for src, uid in (b.get("external_ids") or {}).items():      # an id of ours is never replaced
        if uid and not (a.get("external_ids") or {}).get(src):
            if not a.get("external_ids"):
                a["external_ids"] = {}
            a["external_ids"][src] = uid
    disputes.extend(x for x in (b.get("disputes") or []) if x not in disputes)
    return res


# ---------- graph invariants ----------
def violations(persons, links, min_gap=MIN_GAP):
    """Cheap arithmetic invariants. They catch the gluing of two different people at once."""
    by = {p["id"]: p for p in persons}
    children, parents = kinship(links, birth_only=True)
    bad = []
    for child, kin in parents.items():
        yc = year_of(by[child], "birth") if child in by else None
        for p in kin:
            yp = year_of(by[p], "birth") if p in by else None
            if yc is not None and yp is not None and yc - yp < min_gap:
                bad.append(("parent not older than child", child, by[child]["name"], yc, p, by[p]["name"], yp))
        sexes = collections.Counter((by[p]["sex"] or "?") for p in kin if p in by)
        for sex, n in sexes.items():
            if sex in ("m", "f") and n > 1:
                bad.append(("more than one birth parent of one sex", child, by[child]["name"],
                            yc, "|".join(sorted(kin)), "%s x%d" % (sex, n), None))
    return bad


def print_invariants(persons, links, min_gap):
    bad = violations(persons, links, min_gap)
    age = [x for x in bad if x[0].startswith("parent not older")]
    sexes = [x for x in bad if x[0].startswith("more than one")]
    print("persons %d, links %d" % (len(persons), len(links)))
    print("\nparent not older than child: %d" % len(age))
    for _, c, cn, cy, p, pn, py in age:
        print("  %-36s b.%s  <- %-34s b.%s  (%s)" % (cn[:36], cy, pn[:34], py, p))
    print("\nmore than one birth parent of one sex: %d" % len(sexes))
    for _, c, cn, cy, ids, sex, _x in sexes:
        print("  %-36s %s  %s" % (cn[:36], sex, ids))
    return bad


def apply_merge(g, pairs, refused, persons_path, links_path, snapshot_dir, report_path):
    if not pairs:
        print("nothing to merge: no snapshot taken, no file rewritten")
        if refused:         # refusals still reach the report
            lines = ["# Merged duplicates, run of %s" % time.strftime("%Y-%m-%d %H:%M"), "",
                     "Nothing was merged.", "", "## Merge refused", ""]
            lines += ["- **%s** <- `%s`: %s" % (g.P[own]["name"], other, why)
                      for (own, other), why in sorted(refused.items())]
            with open(report_path, "a", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n\n")
            print("report:", report_path)
        return
    snaps = gi.snapshot(persons_path, links_path, snapshot_dir)
    print("snapshot:", ", ".join(snaps))
    remove, skipped = {}, []
    clashes, precise, lacking = [], [], []
    for own, other in pairs:
        if other in remove or own in remove:
            skipped.append((own, other))
            print("skipped: %s <- %s (one of the two nodes was already merged in this run)" % (own, other))
            continue
        res = merge_into(g, own, other)
        for sentence in res.disputes:
            clashes.append((own, other, sentence))
            print("disagreement kept as a dispute of %s: %s" % (own, sentence))
        for sentence in res.precise:
            precise.append((own, other, sentence))
            print("more precise value in the other copy, not written (%s): %s" % (own, sentence))
        for sentence in res.lacking:
            lacking.append((own, other, sentence))
            print("value for a field we lack, not written (%s): %s" % (own, sentence))
        remove[other] = own
    before = len(g.links)
    new_links, seen = [], set()
    for l in g.links:
        l = dict(l)
        l["from"], l["to"] = remove.get(l["from"], l["from"]), remove.get(l["to"], l["to"])
        if l["from"] == l["to"]:
            continue
        key = (l["from"], l["type"], l["to"])
        if key in seen:
            continue
        seen.add(key)
        new_links.append(l)
    kept = [p for p in g.persons if p["id"] not in remove]
    new_violations = len(violations(kept, new_links, g.min_gap)) - len(violations(g.persons, g.links, g.min_gap))
    if new_violations > 0:
        raise SystemExit("the merge would create %d new invariant violations - graph not written; "
                         "run --invariants" % new_violations)
    gi.write_graph(kept, new_links, persons_path, links_path)
    print("merged: %d; persons left %d; links %d (were %d)" % (len(remove), len(kept), len(new_links), before))
    lines = ["# Merged duplicates, run of %s" % time.strftime("%Y-%m-%d %H:%M"), "",
             "One person recorded twice, by us and in an imported tree. The imported record was merged "
             "into ours and its name kept among the variants.", ""]
    lines += ["- **%s** <- `%s` (%s)" % (g.P[own]["name"], other, g.P[other]["name"]) for other, own in remove.items()]
    if clashes:
        lines += ["", "## Disagreements between the copies (ours kept, written into `disputes`)", ""]
        lines += ["- **%s** <- `%s`: %s" % (g.P[own]["name"], other, sentence) for own, other, sentence in clashes]
    for title, rows in (("More precise values in the other copy - NOT WRITTEN, decide by hand", precise),
                        ("Values for a field we lack, or for an event of ours that holds only a source or a note - NOT WRITTEN, "
                         "decide by hand", lacking)):
        if rows:
            lines += ["", "## " + title, ""]
            lines += ["- **%s** <- `%s`: %s" % (g.P[own]["name"], other, sentence) for own, other, sentence in rows]
    if skipped:
        lines += ["", "## Pairs skipped (one node was already merged in this run; run again)", ""]
        lines += ["- **%s** <- `%s`" % (g.P[own]["name"], other) for own, other in skipped]
    if refused:
        lines += ["", "## Merge refused", ""]
        lines += ["- **%s** <- `%s`: %s" % (g.P[own]["name"], other, why)
                  for (own, other), why in sorted(refused.items())]
    with open(report_path, "a", encoding="utf-8") as f:     # append: an earlier run's log is never overwritten
        f.write("\n".join(lines) + "\n\n")
    print("report:", report_path)


# ---------- self-test ----------
def _p(pid, name, sex="m", born=None, uid=None):
    p = {"id": pid, "name": name, "sex": sex, "variants": [], "family": "",
         "birth": {"date": born, "style": "", "place": "", "confidence": "", "source": ""},
         "death": {"date": None, "style": "", "place": "", "confidence": "", "source": ""},
         "disputes": []}
    if uid:
        p["external_ids"] = {"external": uid}
    return p


def _parent(a, b):
    return {"from": a, "type": "PARENT", "to": b, "confidence": "medium", "source": "", "note": ""}


def self_test():
    """Regression: two different people under one name must not collapse into one."""
    # 1. A real duplicate: ours and an imported node, the same person - must merge.
    g = Graph([_p("primerov-ivan", "Примеров Иван", born="1887-03-04"),
               _p("ext-primerow-ivan", "Primerow Ivan", born="1887-03-04", uid="u-1"),
               _p("primerov-son", "Примеров Пётр", born="1917-06-08")],
              [_parent("primerov-ivan", "primerov-son")])
    pairs, refused = candidates(g)
    assert pairs == [("primerov-ivan", "ext-primerow-ivan")], "real duplicate not merged: %s" % (pairs,)
    assert not refused, "real duplicate refused: %s" % refused

    # 2. Different external_id from one source: the source holds them to be different people.
    g = Graph([_p("primerov-ivan", "Примеров Иван", born="1887-03-04", uid="u-1"),
               _p("ext-primerow-ivan", "Primerow Ivan", born="1887-03-04", uid="u-2")], [])
    pairs, refused = candidates(g)
    assert not pairs, "merged two people of the source: %s" % (pairs,)
    assert refused and "external_ids" in list(refused.values())[0], "stayed silent: %s" % refused

    # 3. Both nodes imported: an imported node is only merged into ours.
    g = Graph([_p("ext-obraztsov-pyotr", "Obraztsov Pyotr", born="1827-06-21", uid="u-1"),
               _p("ext-obraztsov-pyotr-2", "Obraztsov Pyotr", born="1827-06-21", uid="u-2")], [])
    pairs, refused = candidates(g)
    assert not pairs, "merged two imported nodes: %s" % (pairs,)

    # 4. Generation arithmetic: the merge would make a father younger than his daughter - refuse.
    g = Graph([_p("obraztsov-pyotr", "Obraztsov Pyotr", born="1788"),
               _p("ext-obraztsov-pyotr", "Obraztsov Pyotr", born="1827-06-21", uid="u-9"),
               _p("obraztsova-anna", "Obraztsova Anna", sex="f", born="1820-03-05")],
              [_parent("obraztsov-pyotr", "obraztsova-anna"), _parent("ext-obraztsov-pyotr", "obraztsova-anna")])
    pairs, refused = candidates(g)
    assert not pairs, "merged people born in 1788 and 1827: %s" % (pairs,)
    assert refused, "stayed silent instead of refusing"
    why = list(refused.values())[0]
    assert "differ" in why or "older" in why, "unclear reason: %s" % why

    # 4b. The date exists only on the imported node: the arithmetic must use it.
    g = Graph([_p("obraztsov-pyotr", "Obraztsov Pyotr"),
               _p("ext-obraztsov-pyotr", "Obraztsov Pyotr", born="1827-06-21", uid="u-9"),
               _p("obraztsova-anna", "Obraztsova Anna", sex="f", born="1820-03-05")],
              [_parent("obraztsov-pyotr", "obraztsova-anna"), _parent("ext-obraztsov-pyotr", "obraztsova-anna")])
    pairs, refused = candidates(g)
    assert not pairs, "merged, making a father b. 1827 the father of a daughter b. 1820: %s" % (pairs,)
    assert "older" in list(refused.values())[0], "unclear reason: %s" % refused

    # 5. The invariant catches an already corrupted graph.
    bad = violations(g.persons, g.links)
    assert any(x[0].startswith("parent not older") for x in bad), "invariant is blind: %s" % bad
    # 6. A stepmother is not corruption: an adoptive parent is not a second parent of the same sex.
    ps = [_p("father", "Father", born="1867-02-03"), _p("mother", "Mother", sex="f", born="1872-02-03"),
          _p("stepmother", "Stepmother", sex="f", born="1882-02-03"), _p("son", "Son", born="1897-02-03")]
    ls = [_parent("father", "son"), _parent("mother", "son"),
          dict(_parent("stepmother", "son"), type="ADOPTIVE_PARENT")]
    assert not violations(ps, ls), "stepmother taken for corruption: %s" % violations(ps, ls)
    ls[2] = _parent("stepmother", "son")          # the same link as a birth parent: must surface
    assert any(x[0].startswith("more than one") for x in violations(ps, ls)), \
        "invariant does not see two birth mothers"

    # 7. Both copies hold a value and the values differ: ours stays, the disagreement goes into
    #    `disputes` with both values and both sources, and their source is NOT added to our value.
    ours = _p("primerov-ivan", "Примеров Иван", born="1887-03-04")
    ours["birth"].update(place="Place A", source="baptism entry A")
    ours["death"].update(date="1950-01-02", source="burial entry A")
    theirs = _p("ext-primerow-ivan", "Primerow Ivan", born="1887-03-04", uid="u-1")
    theirs["birth"].update(place="Place B", source="tree B")
    theirs["death"].update(date="1950-01-02", source="tree B")
    g = Graph([ours, theirs], [])
    assert candidates(g)[0] == [("primerov-ivan", "ext-primerow-ivan")], "test 7 pair is not a candidate"
    found = merge_into(g, "primerov-ivan", "ext-primerow-ivan")
    assert ours["birth"]["place"] == "Place A", "our place was changed: %s" % ours["birth"]
    assert ours["birth"]["source"] == "baptism entry A", "their source was added to a value it contradicts: %s" % ours["birth"]
    assert len(ours["disputes"]) == 1, "dispute entry missing or doubled: %s" % ours["disputes"]
    d = ours["disputes"][0]
    assert all(x in d for x in ("Place A", "Place B", "baptism entry A", "tree B")), "dispute lacks values or sources: %s" % d
    assert found.disputes == ours["disputes"], "merge_into does not report the disagreement: %s" % (found,)
    assert ours["death"]["source"] == "burial entry A; tree B", "source not added where values agree: %s" % ours["death"]
    # 8. Field by field. `_merge_one` merges one event of an imported copy into ours.
    def _merge_one(ours_ev, theirs_ev, k="birth"):
        o = _p("obraztsov-ferapont", "Образцов Ферапонт")
        t = _p("ext-obraztsov-ferapont", "Obraztsov Ferapont", uid="u-5")
        o[k].update(ours_ev)
        t[k].update(theirs_ev)
        g = Graph([o, t], [])
        return o, merge_into(g, o["id"], t["id"])
    # Place disagrees, our date empty, theirs has a date in Old Style: nothing of theirs is filled in.
    o, m = _merge_one(dict(place="Place A", source="register A", confidence="high"),
                      dict(date="1880-01-01", style="OS", place="Place B", source="tree B", confidence="low"))
    b = o["birth"]
    assert not b["date"] and b["style"] == "" and b["source"] == "register A" and b["confidence"] == "high", \
        "a value of the other copy was mixed into ours: %s" % b
    assert len(o["disputes"]) == 1 and "Place B" in o["disputes"][0], "one place dispute expected: %s" % o["disputes"]
    assert len(m.lacking) == 1 and "1880-01-01" in m.lacking[0] and "not written" in m.lacking[0], \
        "the date is not listed as not written: %s" % (m.lacking,)
    # Dates disagree, ours without a style, theirs Old Style: our date and style stay, both styles named.
    o, m = _merge_one(dict(date="1880-01-13", source="register A", confidence="high"),
                      dict(date="1880-01-01", style="OS", source="tree B"))
    b = o["birth"]
    assert b["date"] == "1880-01-13" and b["style"] == "" and b["source"] == "register A" and b["confidence"] == "high", \
        "our date, style, source or confidence changed: %s" % b
    assert len(o["disputes"]) == 1 and "OS" in o["disputes"][0] and "not stated" in o["disputes"][0] \
        and "1880-01-13" in o["disputes"][0] and "1880-01-01" in o["disputes"][0], \
        "dispute lacks a date or a style: %s" % o["disputes"]
    # A bare year against the full date of the same year is a refinement, not a disagreement.
    o, m = _merge_one(dict(date="1943-07-14", source="memory"), dict(date="1943", source="tree B"), "death")
    d = o["death"]
    assert not o["disputes"] and not m.disputes and d["date"] == "1943-07-14" and d["source"] == "memory; tree B", \
        "less precise copy not counted as agreement: %s %s" % (d, o["disputes"])
    o, m = _merge_one(dict(date="1943", source="memory"), dict(date="1943-07-14", source="tree B"), "death")
    d = o["death"]
    assert not o["disputes"] and d["date"] == "1943" and d["source"] == "memory", \
        "more precise copy changed ours or was disputed: %s %s" % (d, o["disputes"])
    assert len(m.precise) == 1 and "1943-07-14" in m.precise[0], "not listed as more precise: %s" % (m.precise,)
    # Places that differ only by blanks or case agree.
    o, m = _merge_one(dict(place="Obraztsovo", source="register A"), dict(place="  obraztsovo ", source="tree B"))
    assert not o["disputes"] and o["birth"]["source"] == "register A; tree B", \
        "blanks or case made a dispute: %s %s" % (o["birth"], o["disputes"])
    # Our event entirely empty: theirs is taken as a whole, confidence theirs or low.
    o, m = _merge_one({}, dict(date="1880-01-01", style="OS", place="Place B", source="tree B", confidence="medium"))
    assert o["birth"] == {"date": "1880-01-01", "style": "OS", "place": "Place B", "source": "tree B",
                          "confidence": "medium"}, "event not taken as a whole: %s" % o["birth"]
    o, m = _merge_one({}, dict(date="1880-01-01", place="Place B", source="tree B"))
    assert o["birth"]["confidence"] == "low", "default confidence is not low: %s" % o["birth"]
    assert not o["disputes"], "dispute written for an empty event"
    # An event of ours without date and place but with our own source and note is not replaced.
    kept = dict(date=None, style="", place="", confidence="low", source="family memory", note="register searched")
    o, m = _merge_one(dict(kept), dict(date="1915", place="Place B", source="tree B"))
    assert o["birth"] == kept, "our sourced event was replaced: %s" % o["birth"]
    assert len(m.lacking) == 1 and "not written" in m.lacking[0], "their event is not listed: %s" % (m,)
    # The same date under two stated calendars is a dispute; a calendar stated only in theirs is listed.
    o, m = _merge_one(dict(date="1880-01-13", style="NS", source="doc A"), dict(date="1880-01-13", style="OS", source="tree B"))
    assert len(m.disputes) == 1 and o["birth"]["source"] == "doc A", "two calendars passed as agreement: %s" % (m,)
    o, m = _merge_one(dict(date="1880-01-13", source="doc A"), dict(date="1880-01-13", style="OS", source="tree B"))
    assert len(m.precise) == 1 and not m.disputes and o["birth"].get("style", "") == "" and o["birth"]["source"] == "doc A", \
        "a calendar stated only in theirs was not listed: %s %s" % (m, o["birth"])
    # Places that differ inside brackets or by a number disagree; a source is added by whole entry.
    o, m = _merge_one(dict(place="Place A (N uezd)", source="doc A"), dict(place="Place A (M uezd)", source="tree B"))
    assert len(m.disputes) == 1, "different bracket text passed as agreement: %s" % (m,)
    o, m = _merge_one(dict(date="1880", source="tree B2"), dict(date="1880", source="tree B"))
    assert o["birth"]["source"] == "tree B2; tree B", "source lost to a substring match: %s" % o["birth"]
    # An external id of ours is never replaced; their notes are labelled.
    ours = _p("primerov-ivan", "Примеров Иван", born="1887-03-04", uid="I17")
    theirs = _p("ext-primerow-ivan", "Primerow Ivan", born="1887-03-04")
    theirs["external_ids"], theirs["notes"] = {"external": ""}, "their remark"
    g = Graph([ours, theirs], [])
    merge_into(g, "primerov-ivan", "ext-primerow-ivan")
    assert ours["external_ids"] == {"external": "I17"}, "our external id was replaced: %s" % ours["external_ids"]
    assert "imported record" in ours["notes"] and "their remark" in ours["notes"], "notes not labelled: %s" % ours.get("notes")
    # 7b. A pair skipped because one of its nodes was merged earlier in the run is said aloud.
    import contextlib, io, tempfile
    with tempfile.TemporaryDirectory() as tmp:
        pp, lp = os.path.join(tmp, "persons.json"), os.path.join(tmp, "links.json")
        ps = [_p("primerov-ivan", "Примеров Иван", born="1887-03-04"),
              _p("primerov-ivan-2", "Примеров Иван", born="1887-03-04"),
              _p("ext-primerow-ivan", "Primerow Ivan", born="1887-03-04", uid="u-1")]
        gi.write_graph(ps, [], pp, lp)
        g = Graph(ps, [])
        pairs, refused = candidates(g)
        assert len(pairs) == 2, "test 7b needs two pairs sharing one imported node: %s" % (pairs,)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            apply_merge(g, pairs, refused, pp, lp, os.path.join(tmp, "snap"), os.path.join(tmp, "report.md"))
        assert "skipped" in buf.getvalue(), "skipped pair not printed: %s" % buf.getvalue()
        with open(os.path.join(tmp, "report.md"), encoding="utf-8") as f:
            assert "skipped" in f.read(), "skipped pair not in the report"
    print("merge_duplicates self-test passed: real duplicate found, refusals fired, "
          "invariant sees corruption and does not treat a stepmother as corruption, "
          "a differing value becomes a dispute and keeps ours, nothing of theirs is mixed into an event "
          "that holds a value, a skipped pair is reported")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Find and merge duplicates in the graph; dry run by default. An imported event is taken "
                    "whole only into an entirely empty event of ours; otherwise no field of ours is changed or "
                    "filled in: agreeing values add the other copy's source, a real difference is written "
                    "into `disputes` (the event's confidence is not changed), more precise values and values "
                    "for fields we lack are listed and not written.")
    ap.add_argument("--persons", help="persons JSON file")
    ap.add_argument("--links", help="links JSON file")
    ap.add_argument("--apply", action="store_true", help="merge (after a snapshot), write the graph files and a report with the "
                    "disagreements, the more precise values and the values for fields we lack")
    ap.add_argument("--invariants", action="store_true", help="check graph invariants, change nothing")
    ap.add_argument("--self-test", action="store_true", help="regression test on synthetic data")
    ap.add_argument("--snapshot-dir", help="default: 'snapshots' next to the persons file")
    ap.add_argument("--report", help="merge report written by --apply (default: merged_duplicates.md next to the persons file)")
    ap.add_argument("--imported-prefix", action="append", default=None,
                    help="id prefix of nodes created by an importer; repeatable (default: %s)" % ",".join(IMPORTED_PREFIXES))
    ap.add_argument("--min-gap", type=int, default=MIN_GAP, help="minimum years between parent and child (default: %(default)s)")
    ap.add_argument("--max-spread", type=int, default=MAX_SPREAD,
                    help="larger spread of birth years means different people (default: %(default)s)")
    args = ap.parse_args(argv)

    if args.self_test:
        self_test()
        return 0
    if not (args.persons and args.links):
        ap.error("--persons and --links are required")
    persons, links = gi.load_graph(args.persons, args.links)
    if args.invariants:
        print_invariants(persons, links, args.min_gap)
        return 0
    g = Graph(persons, links, args.imported_prefix or IMPORTED_PREFIXES, args.min_gap, args.max_spread)
    pairs, refused = candidates(g)
    print("duplicates found: %d" % len(pairs))
    for own, other in pairs:
        print("  %-46s <- %-42s" % (g.P[own]["name"][:46], g.P[other]["name"][:42]))
    for own, other in pairs:
        # preview on copies: the dry run changes nothing
        pg = Graph([copy.deepcopy(g.P[own]), copy.deepcopy(g.P[other])], [], g.prefixes, g.min_gap, g.max_spread)
        res = merge_into(pg, own, other)
        for sentence in res.disputes:
            print("    disagreement, ours kept, would be written into `disputes`: %s" % sentence)
        for sentence in res.precise:
            print("    more precise value in the other copy, not written: %s" % sentence)
        for sentence in res.lacking:
            print("    value for a field we lack, not written: %s" % sentence)
    if refused:
        print("\n!!! MERGE REFUSED: %d pairs - matched, but must not be merged." % len(refused), file=sys.stderr)
        for (own, other), why in sorted(refused.items()):
            print("  . %s (`%s`) <- %s (`%s`)" % (g.P[own]["name"], own, g.P[other]["name"], other), file=sys.stderr)
            print("    %s" % why, file=sys.stderr)
    if not args.apply:
        print("dry run: nothing written (use --apply)")
        return 0
    base = os.path.dirname(os.path.abspath(args.persons))
    apply_merge(g, pairs, refused, args.persons, args.links,
                args.snapshot_dir or os.path.join(base, "snapshots"),
                args.report or os.path.join(base, "merged_duplicates.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
