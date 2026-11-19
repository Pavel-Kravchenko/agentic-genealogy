# Graph tools

Four command-line tools for a family graph kept as two JSON files (`persons.json`, `links.json`).
The schema is in [SCHEMA.md](SCHEMA.md); a fictional graph to try them on is in
[../../examples/sample-family/](../../examples/sample-family/README.md).

Requirements: Python 3.9 or later, standard library only. No network access. Run the commands from this
folder (`gedcom_export.py` and `merge_duplicates.py` import their neighbours by file name). All paths are arguments.

| tool | what it does | writes the graph? |
|---|---|---|
| `check_graph.py` | Structural errors, date contradictions and field states | no |
| `merge_duplicates.py` | Finds one person recorded twice and merges the imported copy into ours | only with `--apply` |
| `gedcom_export.py` | Graph to GEDCOM 5.5.1 | no |
| `gedcom_import.py` | GEDCOM from another tree: comparison report, optionally merge into the graph | only with `--apply` |

Tools that change the graph run as a dry run by default. With `--apply` they first copy both graph files
to a snapshot folder (default `snapshots/` next to `persons.json`) under a date-time stamp and refuse to
overwrite an existing snapshot. Order of work: check, snapshot (automatic), import or merge, check again.

## check_graph.py

```
python3 check_graph.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json
```

Three counts, kept apart because they are fixed differently: ERRORS (broken structure: dangling ids,
unknown type, ancestor cycle, unreadable date, missing field; exit code 1), FINDINGS (the data
contradict each other: a mother under 14 or over 50 at a birth, a child born more than nine months after a
parent's death, a child older than a parent; not fixed by adjusting data) and FIELD STATES (event absent,
confidence `disputed`; not defects). Thresholds: `--min-mother-age`, `--max-mother-age`,
`--max-months-after-death`.

Expected output on the sample: 0 errors, 2 findings, 8 field states.

## merge_duplicates.py

```
python3 merge_duplicates.py --persons P --links L                # list candidate pairs
python3 merge_duplicates.py --persons P --links L --apply        # snapshot, merge, write, report
python3 merge_duplicates.py --persons P --links L --invariants   # parent older than child, one birth parent per sex
python3 merge_duplicates.py --self-test
```

A pair is a candidate when sex agrees and either (a) the full birth or death date agrees and the names are
compatible after transliteration (`Примеров` and `Primerow`) or the two share a spouse or child, or (b) the full
set of name tokens (at least two) agrees, the names are compatible, and they share a relative or the birth date. Only a node
with an importer prefix (`--imported-prefix`, default `ext-`) is merged into one of ours. Three refusals,
each printed to stderr: both nodes imported, different `external_ids` from one source, or generation
arithmetic (the merged parent would not be at least `--min-gap` years, default 12, older than the child;
birth years more than `--max-spread`, default 20, apart). `--apply` also writes `merged_duplicates.md`
(`--report` to move it) and stops without writing if the merge would create a new invariant violation.

Each event (birth, death) of the imported copy is merged into ours field by field. Dates are compared after
trimming blanks, places without regard to case and blanks. The same date under two different stated calendars is a
disagreement; a calendar stated only in the other copy is listed as a more precise value.
- If our event is entirely empty (no date, no place, no source, no note), the imported event is taken as a whole:
  date, place, style, source and its confidence, or `low` when it has none. Nothing of ours is mixed in. An event
  of ours that holds only a source or a note is left as it is, and the imported event is listed.
- If our event holds a value, no field of ours is changed, no empty field of ours is filled and `style` is never
  copied. Where both copies hold a value and they agree, the other copy's source is added to ours (once), but
  only when no field of that event differs. A bare year against a fuller date of the same year and qualifier is
  not a disagreement: when the other copy is the less precise it counts as agreement; when it is the fuller it is
  listed as "more precise value in the other copy, not written" and its source is not added. Where the values
  differ, ours stays and one sentence with both values, both calendar styles (for a date) and both sources is
  added to the person's `disputes`. A value of the other copy for a field we lack is not written: it is listed
  as "decide by hand".

A dispute written by the merge is recorded in `disputes` and in the merge report. It does not change the
event's confidence: an imported tree does not demote a documented value. The dry run prints, and the report
contains, three separate lists: disagreements (written into `disputes`), more precise values not written, and
values for fields we lack not written. A pair skipped because one of its nodes was already merged in the same
run is printed as well.

Expected output on the sample: `duplicates found: 1` and the pair `Примеров Пётр Иванович <- Primerow Pyotr Ivanovich`. The imported copy gives only the year of the death (`1943` against our `1943-07-14`); that is agreement at lower precision, so no disagreement is printed, no dispute is written, and the imported source is added by `--apply` to our death source and to our birth source (the birth place and date agree).

## gedcom_export.py

```
python3 gedcom_export.py --persons P --links L --out tree.ged
python3 gedcom_export.py --persons P --links L --out tree-latin.ged --latin --submitter "Your Name"
python3 gedcom_export.py --persons P --links L --out tree.ged --force      # replace the file of an earlier run
```

Writes persons (names, sex, birth and death with place, notes, disputes, sources), families (from `PARENT`
and `SPOUSE` links; `ADOPTIVE_PARENT` as a family with `PEDI adopted`), associations (`GODPARENT`,
`GUARANTOR`, `POSSIBLE_KIN`, `HALF_SIBLING` as `ASSO`) and the graph id as `REFN`. The bracketed maiden name
becomes a second name with `TYPE maiden`. Before the file is written, the text is checked (dangling pointers, line and
date syntax, one INDI per person); a failed check stops with an error, nothing is written and the exit code is not 0.
An existing `--out` file is not overwritten unless `--force` is given (error and exit code 1 otherwise).

## gedcom_import.py

```
python3 gedcom_import.py tree.ged --persons P --links L                       # report on screen
python3 gedcom_import.py tree.ged --persons P --links L --report merge.md     # report to a file (--force: replace an existing one)
python3 gedcom_import.py tree.ged --persons P --links L --apply               # snapshot, then write
python3 gedcom_import.py --self-test                                          # namesake and no-overwrite regression tests
```

Matching, in order: the same `REFN` as one of our ids, or the same `_UID` as one of our `external_ids`; then
name similarity with a birth and death year check and a bonus for relatives who match by name. Two
namesakes that cannot be told apart are listed under "Ambiguous namesakes" (also on stderr) and neither
merged nor created as new persons. `--apply` never overwrites or removes anything already in the graph. It adds new persons
(id `ext-<name>`), new facts in events that are entirely empty in ours (no date, no place, no source, no note), new
`PARENT` and `SPOUSE` links, and, on persons it matched, labelled notes and sources from the other tree and an
`external_ids` entry where ours has none. A fact enters at confidence `low` (or `medium` with `--confidence medium`), with the import stamp as `source` and, for a Julian date, style
`OS`. Everything else goes to the report and is not written: disagreements under "Clashes"; a more precise value
of the other tree for a field that already holds a value (a full date against our bare year of the same year, a
longer place name, a calendar stated only in their date) under "More precise dates" and "Place refinements"; and a value for an empty field of an event
that already holds another value (for example a birth date when we have only the place) under "Facts for an empty
field of an event we already document". A person decides each of them. With nothing to write, `--apply` takes no
snapshot, rewrites no file and prints that nothing changed. The graph files keep their file mode, and a symlinked
graph file stays a link. `--report` refuses to overwrite an existing file unless `--force` is
given. Options:
`--source-name` (default `external`; key in `external_ids` and prefix of notes), `--source-pattern`
(regular expression; note lines that match, default `https?://`, are stored as sources).

What does not come back: associations (`ASSO`) and the adoptive flag (`PEDI`) are not read; an adoptive
parent returns as `PARENT`. A Julian date (`@#DJULIAN@`) sets `style` `OS` only on a fact added into an
entirely empty event. Russian month abbreviations (ЯНВ ... ДЕК) are read.

Round trip on the sample (graph -> GEDCOM -> empty graph): 19 persons in, 19 out; 23 `PARENT` and 5 `SPOUSE`
links in, 23 and 5 out; the one `GODPARENT` and one `POSSIBLE_KIN` link are not read back.

```
python3 gedcom_export.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json --out /tmp/sample.ged --force
echo '[]' > /tmp/p.json; echo '[]' > /tmp/l.json
python3 gedcom_import.py /tmp/sample.ged --persons /tmp/p.json --links /tmp/l.json --apply
```

## Living people

`gedcom_export.py` exports every person in the graph. It does not filter the living. Before a file leaves
the private project, remove living people from a copy of the graph, or reduce them to what the family has
agreed (see the `checking-privacy-before-sharing` skill), and export from that copy.

## Confidence of imported data

`gedcom_import.py --apply` enters everything it takes from another tree at confidence `low`
(`--confidence medium` raises it), and only into events that are entirely empty in ours, so the confidence of
an event we document is never touched. `merge_duplicates.py` takes an imported event whole only into an
entirely empty event, at the confidence the imported copy carries or `low`. Neither tool replaces an id of ours
in `external_ids`: the importer lists a different id under "Clashes". Notes taken from the imported copy are
labelled: by the merger with the imported record's id, by the importer with the tree name. With nothing to merge or to write, neither tool takes a snapshot or rewrites a file. Another person's tree is working notes, not a document.
