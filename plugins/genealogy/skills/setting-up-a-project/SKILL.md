---
name: setting-up-a-project
description: Use when starting a new family-history research project with Claude, when an existing pile of scans, notes and tree exports has no structure, or when a project has no entry file, no dead-ends ledger or no rule for what git tracks
---

# Setting up a family-history project

## Core principle

The project must be readable by a session that knows nothing: one entry file, a small set of ledgers with
fixed roles, one structured source of truth for people, and everything else either generated or archived.

## Layout

Create this tree (names can be in the family's language; roles must not change). Starter files are in
`templates/` in this skill's directory: copy them, then fill the angle brackets.

```
<project>/
  CLAUDE.md             standing rules for every session (from templates/CLAUDE.md)
  START_HERE.md         entry file: state, what waits for whom, do-not list, reading order
  JOURNAL.md            dated log of sessions: history, not instructions
  FACTS.md              what a document proves, with shelf marks; weak evidence in its own section
  DEAD_ENDS.md          what was searched and not found; read before any search
  OPEN_QUESTIONS.md     unresolved leads, each with what would answer it and who can
  SOURCES.md            every database and archive: what it holds, how to reach it, traps, what is dead
  KNOW_HOW.md           techniques that cost time to find
  CATALOG.md            what lies where and what is edited by hand
  Graph/                persons and links (JSON), snapshots/      edited by script only
  Tree/                 generated: viewer, GEDCOM, printable sheets    never edited
  Sources/              scans, archive copies, photos, audio, transcriptions, INVENTORY.md
  Reports/              what each search session or agent wave produced: a record, not edited
  For-the-family/       documents written for relatives in plain language
  Tools/                scripts with self-checks
  Work/                 temporary; may be cleaned
```

One-line rule for the catalogue: only the graph (by script), the transcriptions, the family documents and
the ledgers are edited. Everything else is generated, an archive, or raw material.

## Steps

1. Create the tree and copy the templates. Put an empty `.gitkeep` into each folder that has no file
   yet, or a fresh clone will lack it.
2. `git init`. Use the allow-list ignore file from the templates (it is stored as `gitignore`; rename it
   to `.gitignore`): git tracks text (markdown, scripts, JSON, GEDCOM, CSV); scans, audio, archives and
   office builds are not tracked, because they do not change by editing and weigh gigabytes. Back the
   media up separately; originals are irreplaceable.
3. Fill `CLAUDE.md` with the family's own rules. Ask the people who own the family story, do not assume:
   - how living people appear (a workable default: year of birth only, children by given name only);
   - whose voice any book or memoir is in, and that it changes only on that person's word;
   - what is printed when a document and a gravestone or a memory disagree (both);
   - who decides kinship where documents are silent (the living relative who states it, not a calculation);
   - which language the project works in.
   A rule the family has not yet decided is written as `PROVISIONAL (asked <date>)` with the default in
   use, and the question goes into `START_HERE.md` under "Waits for the family". Until the rule on living
   people is confirmed, treat everyone who may be alive (born less than about 100 years ago, no death
   recorded) as living, and keep them out of anything shared.
4. Put existing material under `Sources/` without renaming the originals. Compute checksums; duplicates
   under different names are common. Normalise names to Unicode NFC whenever a script compares them.
5. Import an existing tree (GEDCOM) into the graph, keeping each record's `_UID` and marking every
   imported person with the import as its source and a low confidence until a document confirms it.
   Online trees hold living people with full dates: apply the living-people rule on import.
6. Write the first `START_HERE.md` (what the project is, what exists, what is known to be weak, the
   queue) and the first dated entry of `JOURNAL.md`.
7. First commit, with the files named explicitly. Pushing anywhere is the researcher's decision.

## Access set-up to decide on day one

| Need | Arrangement |
|---|---|
| `own browser`: sites that need a login or a subscription, or that do not serve automated requests | The researcher uses them personally, in their own browser; agents never get a logged-in browser |
| `human only`: captchas, payments, reading-room orders, visits, letters to private people | A human queue in `START_HERE.md` ("Waits for the researcher") |
| `open page`: a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser` | Where the terms allow it: one site per agent, one request at a time, slowly, stop at the first refusal |
| Network location | Some national sites do not answer from every network; record per site what was observed, with month and year, and the official alternative (written request, visit) |

## Common mistakes

- Starting to search before the dead-ends ledger exists: the first week's zeros are never recorded and are
  repeated in the third.
- Tracking scans in git, or tracking nothing.
- Editing the generated tree instead of the graph.
- One file that is at once state, history and instructions. Keep the entry file short and the journal long.
