---
name: checking-privacy-before-sharing
description: Use when anything from a family-history project is about to leave the private project - publishing a repository, notes, a tree, a GEDCOM file, a book, a web page, a forum post, a message to a stranger, or a query sent to an online service - and when writing public documentation or examples derived from real family research
---

# Checking privacy before sharing

## Core principle

Family research is a file on real people, many of them alive, and on third parties who never agreed to be
in it: correspondents, tree owners, archive staff, neighbours in the same register. Nothing leaves the
private project until a check that was seen to fail on a planted name has passed on the real content.

## What identifies a person

Not only the name. Any of these, alone or combined:

- surnames, including those used as search examples and spelling-variant examples;
- small places: village, farm, parish, volost, and the uezd or district of the family;
- shelf marks of specific files, numbers of archive replies, record ids, tree ids, URLs with ids;
- exact dates of family events, military units, employers, addresses;
- names and handles of correspondents, researchers, tree owners;
- photographs, and file names that carry names.

Province-level geography and names of archives and sites are not identifying. Counts from your own
searches (hits for a surname, cards for a volost, sheets in a file) can be: round them or drop them.

## Living people

Decide the rule with the family and write it into the project's instruction file. A workable default:
living people appear with the year of birth only, children with the given name only, no patronymics or
dates unless the person supplied them. This is a family rule, not a legal test; whether publishing data about
living people is lawful depends on the country, so ask a lawyer when in doubt. A tree or file for the public excludes the living entirely.
The dead are not automatically free either: repression files, illegitimacy, illness and wartime records
concern living descendants. Ask the family before publishing them.

## Procedure before anything is published

1. **Write with an invented cast from the start.** Choose fictional surnames and places for examples
   and use them everywhere. Replacing real names afterwards always misses some.
2. **Build a deny-list from your own data**: every surname and name variant, every small place, the
   tokens from your notes on informants and correspondents; with transliterations (several schemes: the
   same surname is spelt differently in English, German and Polish sources) and with stems, so that
   inflected forms are caught. Keep the deny-list outside what is published.
3. **Scan every file** for deny-list hits and for anything shaped like a shelf mark or a record id.
   The repository's `tools/privacy/pii_scan.py` builds the deny-list from a graph in the sample layout
   and scans any text files. A search-and-replace of the surname is not this check: it misses the
   spelling variants, the transliterations, the small places and every other person in the notes.
4. **See the check fail.** Plant a real surname in a copy and confirm the scanner reports it. A check
   that has never gone red is not a check.
5. **Read the inventory of proper nouns.** List every capitalised or non-Latin token that is not a
   dictionary word and read the list yourself. The deny-list knows only people in the graph; it does not
   know the researcher you wrote to last month.
6. **Scan before the first commit**, not after. Git history is published with the repository; a name
   removed in a later commit is still there. If something slipped in, tell the researcher; rewriting the
   history or starting the repository again is their decision.
7. **Check file names, image metadata (EXIF location and device), document properties (author field),
   and tracked changes** in office files.
8. **Publishing is a human decision.** Prepare; do not push, post or send without an explicit yes.

## Queries to outside services

A search is also a disclosure. Do not send a living person's full name and birth date to a service that
does not need it, do not paste family documents into public tools, and do not put contact details into
automated requests.

## Red flags

- "I replaced the names by hand, it is clean"
- "It is only an example, the surname is common anyway"
- "The commit history is fine, I deleted the file in the last commit"
- "The village is tiny, nobody will connect it" (a small place plus a year is often one family)
- Publishing a screenshot of a tree, a register page or a chat
