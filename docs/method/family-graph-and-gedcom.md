# The family graph and GEDCOM

The project keeps every person and every relationship in one machine-readable graph, and builds everything
else from it: books, reference lists, ancestor and descendant sheets, GEDCOM files for genealogy sites. This
page describes the concepts and the traps. Exact field names and the JSON layout are in
[`tools/graph/SCHEMA.md`](../../tools/graph/SCHEMA.md). The examples are composed illustrations; the patterns
come from real work, the particulars do not.

## The graph is the single source of truth

Nothing about a person is edited in a book, a sheet or a GEDCOM file directly. Those are outputs and are
regenerated. A reference list in a book that is generated from the graph is never corrected by hand.

What a person carries:

- an identifier, a name as written in the best source, and **name variants** (spelling and transliteration
  variants such as Примеров, Примеровъ, Primerow, Przymierow; a maiden and a married surname);
- sex, family line, birth and death (date with qualifier, place);
- a **dispute** field: where two sources disagree (a document and a gravestone, a document and a relative's
  memory), both values are kept and the disagreement is written out. A disputed date is never smoothed into one
  value without a new document;
- **sources per fact**, each with its shelf mark and leaf or frame (`fond <F>, opis <O>, delo <D>, leaf N`);
- a free note, and an external identifier when the person was imported from another tree.

What a relationship carries: from, to, type, **confidence**, source and note. Types used in practice: parent,
spouse, presumed kinship, godparent, guarantor (a witness at a marriage), half-sibling, adoptive parent. A
relationship that is not proven is entered as presumed kinship with its argument, not as parent.

Principles that shaped the graph:

- The document is primary. A living relative's word decides kinship where documents are silent; a date
  calculation does not override it.
- An identity that is not proven stays as **two separate nodes**, each with its own sources.
- Nothing is invented. Where there is no source, the node says so.
- Notes are joined with `; `, never with a full stop or a tab. The reference-list parser ends a field at a
  semicolon, while a full stop inside an abbreviation does not stop it. A tab is worse: the parser does not see
  it at all, and a "cause of death" field swallowed the place of burial and an address.

## Snapshots before every edit, and what a rollback silently undoes

Every script that writes to the graph first copies the current graph files into a snapshots folder with a
timestamp. Snapshots are never deleted.

**A rollback to a snapshot silently undoes everything done after it.** A batch of restored place values was lost
this way, and only a full audit noticed. After a rollback, replay every step made after the snapshot, from the
journal, not from memory.

The same holds for the book: take the copy **before the first edit**, not after the last one. Once edits have
gone into a book file without a fresh copy, no byte-for-byte rollback is left. The first command of any
session that will edit a book is the copy.

## Apply-scripts: dry run first, refuse to run twice

Every change to the graph is a small script, one per batch of new material, kept with the batch:

1. Without a flag it is a **dry run**: it prints what it would add, change or remove, and writes nothing.
2. With `--apply` it takes the snapshot, then writes.
3. Run a second time, it **refuses** ("node already exists"). A script that can be run twice will one day be
   run twice.
4. After it, the machine checks below must give the same findings as before the edit, no new ones.

Check not only what an agent entered, but also what it said should be removed and did not remove. In one wave
an agent wrote "the schema does not allow editing a link" and left in the graph links it had itself
disproved. A proposal format for removing links existed and
a neighbouring agent was using it. A finding that is not carried out is worse than one not made: it looks
closed.

## Duplicates: search the whole graph, not a prefix

Adding a couple of dozen nodes of one family, an agent searched for existing nodes by the identifier prefix it
expected (`primerov-`). It did not see that an import from another site held the same family under
importer-made identifiers (`imp-primerov-*`, `imp-naidis-*`, even `imp-ivan-ivan` with no surname). Result:
**most of the new nodes were duplicates after `--apply`**.

Rules:

- Before adding a node, search **by name tokens and surname across the whole graph**, and **by full date**. Not
  by identifier prefix, not by the full name string.
- Importers build identifiers their own way. One importer built them from the given name plus an Estonian
  patronymic, which gave nodes with no surname; others had no patronymic. A married woman may sit under her
  husband's surname.
- Run the duplicate finder **before** entering, with the new nodes in a temporary copy, or immediately after
  and merge. A finder run without flags should only show pairs and touch nothing.
- Pairs without a full date, or with a married surname, are not seen by an automatic finder. Merge them by hand
  with the same function the finder uses.

## Merging rules

- Merge the imported node into your own node, never the reverse. The external identifier moves to the kept
  node.
- Re-point every link of the removed node to the kept one, then run the invariant checks in the same step. If a
  child now has two mothers, remove the wrong link in the same step, or the invariant check refuses.
- The merge log is a file of its own. One merge tool **overwrote** its log on `--apply`: copy the log first and
  append.
- Two persons of the same name are told apart by household, parish and religion, not by age (see
  `transcription.md#two-traps-in-reading-the-content`).

## Machine checks, and which were dropped as noisy

Two check scripts run after every edit (the structure check is `tools/graph/check_graph.py`; the anomaly
script is the project's own):

| check | what it finds |
|---|---|
| structure | broken identifiers, unknown link type, a cycle of ancestors, unreadable values; mother's age at a child's birth |
| anomalies | chronology (father's age, death before birth, siblings too close from one mother, spouses' age gap, dates in the future); spouses or parent pairs recorded with the same sex (in historical records almost always an entry error), related spouses, nodes without links, duplicate external ids, duplicate candidates by name; sex against patronymic; broken characters and notes joined by tab or newline; media links to missing persons or files; persons in the GEDCOM export against nodes in the graph |

The structure check sorts its output into three classes, counted separately because they are fixed differently:
**errors** (the graph is broken as a structure; only these give exit code 1), **findings** (the graph is whole,
but the data contradict each other, such as a child older than its mother; these are written out and left, not
"fitted"), and **state** (a legitimate but unfinished value: an event not known, or a confidence lowered to
"disputed"). When the state lines were counted as structure errors they made up nearly all of the output, so the
error count meant nothing and the check complained about a deliberate decision to keep a disputed
birth year. Another lesson from the same script: its default input had been hard-coded to an old, small
snapshot, so the working graph had never been checked. Point a check's default at the live data.

Both scripts use one date parser. Do not write a second copy of the parser in a new check: two parsers drift
apart. The anomaly script reports suspicions for a human to look at and never fails the run.

Dropped because they were noisy:

- "rare spelling next to a frequent one": nearly all hits were false. The project keeps church and civil forms
  of a given name (pairs of the Мария / Марья type) on purpose.
- digits in a name.
- "living persons without patronymic and dates": impossible without the family's own list of who is living.

A node without links, or a "missing parent" in the dispute field, sometimes names the parent outright. Mark such
hits; do not discard them.

Expect new findings whenever the scope of a check grows. When a few hundred new people entered the reference
list, the check found several defects at once that had been invisible only because nobody had looked at
those people. This is the first honest look, not a breakage.

## GEDCOM export and import traps

**Date qualifiers.** The graph stores qualifiers in the working language; GEDCOM accepts only its own keywords.
The exporter translates:

| in the graph (meaning) | in GEDCOM |
|---|---|
| about 1840 | `ABT 1840` |
| before 1815 | `BEF 1815` |
| after 1925 | `AFT 1925` |
| between 1781 and 1784 | `BET 1781 AND 1784` |
| 1760/61 | `1760/61` (dual year, valid GEDCOM) |

The lesson bought on the way: a handover said "first teach the exporter the reverse
translation, then enter the qualifiers". The condition was checked by running the export, it passed, and the
qualifiers were entered. The run had passed only because the forms "before" and "after" did not yet exist in
the graph. The exporter knew "about" and "between" but not these two, and the next export failed on
`2 DATE 15 MAY after 1925`. **Check a tool's readiness by reading its code against every form you are about to
enter, not by a green run on data where those forms are still absent.** After the fix every qualified date
was valid, with an assertion per form in a self-test.

A side trap of the same exporter: it ran its self-test on import, and the self-test wrote the `.ged` file. The
module could not be checked without overwriting the export. Keep self-tests behind an explicit flag.

**Calendar escapes.** One site's GEDCOM writes the calendar escape **after the qualifier**, not before the
date:

```
2 DATE ABT @#DJULIAN@ 1840
```

The project's importer removed the escape only at the start of the value, so on such lines the qualifier was
silently lost: a share of the qualified dates fell into "unparsed" on the first comparison. When reading somebody
else's GEDCOM, do not assume an optional element stands where your own exporter puts it.

And the reverse direction: the project's exporter did **not write `@#DJULIAN@` at all** (one `grep '@#D'` on the
output gives zero). The calendar went to the target site as a human-readable note "date in Old Style", which
that site cannot read by machine. Each service reads its own
dialect; check what a round trip through it keeps.

**Identifiers.** Keep the external identifier of every imported person (sites write their own `_UID` and
record links) on the node, so that a later import of the same tree can be matched and not duplicated.

**A slash in a person's name.** GEDCOM uses slashes to mark the surname (`1 NAME Ivan /Primerov/`), so a slash
anywhere else in a name field is read as a surname delimiter. The same character broke the file system: a script
that made one folder per person named it "Name (years)", and two persons with a disputed birth year got
`Primerov Pyotr Ivanovich (1850/1853-1910)`. The `/` became a directory separator, a nested folder
`1853-1910)` appeared, and the outer name was cut at `(1850`. Nothing failed: both folders existed, the counts
matched, some files simply sat one level too deep, and the cut name looked like a typo. It was found only when
paths on disk were compared with the inventory table. Sanitise any name built from data before creating a file
or folder: replace `/` (and on macOS `:`), and write disputed years as `(1850 or 1853 - 1910)`.

## File names on macOS (NFD)

macOS stores and returns file names in decomposed Unicode (NFD): `й` is `и` plus a combining breve, `ё` is
`е` plus a diaeresis. String literals in scripts are almost always NFC. So

```python
"анкета Примеровой.docx".startswith("анкета")       # True in a console
re.search(r"анкета примеровой", name_from_disk)      # None
```

and nothing fails, there are just zero matches. While sorting one received archive, dozens of person sheets
and hundreds of files were missed this way; the rules were written correctly and looked as if they worked.

The fix is one line at the start of any name normalisation, applied to **both the file name and the path** (a
second script failed after the first was fixed, because it compared an unnormalised path):

```python
import unicodedata
def n(s): return unicodedata.normalize("NFC", s).lower().replace("ё", "е")
```

`unicodedata.is_normalized("NFC", name)` returning `False` tells you in a second that a name is NFD. The same
applies to `grep` over file lists and to comparing names on disk with names in a Markdown inventory.

## Small script traps

- In zsh, `for args in "--ancestors <id>"; do cmd $args; done` passes the string as one word. Write `${=args}`.
  Many sheets "failed" on a first run because of this.
- A place-name normaliser driven by regular expressions over-matches: a pattern for a city also matched the
  adjective form of its oblast and a village whose name began with the same word. After each new place rule,
  run a summary that must come out zero (for example "events after 1917 still printed with a pre-1917 uezd").
- A printed card may silently drop a note in brackets after a name when the line does not fit its width. Keep
  such notes short.
