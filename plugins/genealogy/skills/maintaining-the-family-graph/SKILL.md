---
name: maintaining-the-family-graph
description: Use when adding, changing, merging or removing persons and links in a family-history data file, importing or exporting GEDCOM, rolling back to a snapshot, hunting duplicates, or when a script over names or file names returns zero matches for something that is plainly there
---

# Maintaining the family graph

## Core principle

One structured file of persons and links is the source of truth; trees, charts, GEDCOM files and
reference lists are generated from it and never edited. Every change to it is scripted, snapshotted and
checked, because the errors that matter here are silent.

## What a person record must be able to hold

- a primary name and a list of name variants, each variant with the document it comes from;
- birth and death as objects: date, calendar style, place **as written in the document**, confidence, source;
- a dispute list: competing values and unresolved contradictions, kept, never smoothed;
- sources per fact, and external ids from imports;
- for links: type, confidence, source, and room for "possibly the same person / possibly related".

Display conventions (unified place names, modern jurisdictions) live in a separate mapping used at print
time. The graph keeps the place as the document gives it.

The repository's `tools/graph/SCHEMA.md` describes one working layout.

## Changing the graph

1. **Search before adding.** Look for the person by given name and surname across the whole file, then by
   full date. Do not search by id prefix: imported persons sit under the importer's prefix, sometimes
   without a surname or without a patronymic, and a prefix search never sees them.
2. **Run the duplicate finder before and after.**
3. **Change by script**: dry run by default, `--apply` writes a dated snapshot first, a second run refuses.
   The repository has tools for merging and for GEDCOM import; for any other edit (a new person, a new
   source, a dispute) write a short script for that one change with the same three properties, and keep
   it with the material it enters. When a new document names parents, compare them with the parents
   already linked.
4. **Merge imported records into your documented ones**, not the reverse. Read the dry-run list first:
   `merge_duplicates.py --apply` merges every listed pair at once. After a merge check for impossible
   structures (two mothers, three parents). Where a new document agrees on one field and disagrees on
   another (same date, another place), keep the existing value, add the document as a source, and write
   the disagreement into the dispute list; do not pick.
5. **Run the structural checks**: same findings as before, apart from what the change explains.
6. **Commit the snapshot, then the change**, with explicit paths.

## Rolling back

A rollback to a snapshot silently undoes everything done after it. Replay every later step from the
journal, not from memory.

## Silent failures to guard against

| Trap | Symptom | Guard |
|---|---|---|
| macOS returns file names in Unicode NFD | A name with й or ё is never found; a regex over names gives an honest-looking zero | `unicodedata.normalize("NFC", name)` on every name before comparing |
| A slash in a person's name | The per-person folder is silently created somewhere else | Reject or replace path separators when building paths from names |
| Date qualifiers in the graph's language ("about", "before", "after") | GEDCOM consumers reject or drop the date | Map qualifiers to `ABT` / `BEF` / `AFT` / `BET..AND` on export; keep the original text in a note |
| Calendar escape not at the start of a date line in an imported file | Julian dates read as Gregorian or dropped | Parse the escape wherever it stands |
| Notes joined with a full stop or a tab | A downstream parser swallows the next field | Join with "; " |
| A regex in the display mapping that matches too much | A province name is printed as a village | After each new mapping entry, run a count that must be zero |
| A person with no links, or a parent mentioned only in the dispute field | Looks like noise | Flag it; it sometimes names the missing parent outright |

## GEDCOM

- Match records between trees by `_UID` (or the service's stable id), never by name.
- Each service has a dialect. Export one file per target service, and test the import on a small file
  before uploading the whole tree.
- After an export and re-import the counts of persons and links must match; run the round trip as a test.
- Living people: export without them, or with year only, according to the family's rule
  (see `checking-privacy-before-sharing`). The repository's `gedcom_export.py` does not filter them:
  remove them from a copy of the graph before exporting.

## Machine checks worth having, and not

Worth having: structure (dangling links, more than two parents), mother's age at birth, death before
birth, children born after a parent's death, duplicate candidates.

Usually noisy: "rare spelling next to a frequent one" (historical spelling pairs are kept on purpose),
digits in a name, and "living person without dates" (undecidable without a list from the family).

Keep one date parser and import it everywhere; a second copy drifts.
