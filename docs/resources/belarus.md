# Belarus: archives, catalogues and printed sources

Resources for ancestors from the former Grodno, Minsk, Vitebsk, Mogilev and Vilna provinces that lie in today's
Belarus. Statements about site behaviour are observations with their month. The examples are composed
illustrations; the patterns come from real work, the particulars do not. Reach classes: **open page** (a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser`), **own browser** (used by the researcher personally in
a browser: login, subscription, or no automated requests served), **human only** (payment, signature, reading
room), **dead**; see [README.md](README.md).

## Overview

| site | what it holds | reach | notes |
|---|---|---|---|
| NIAB Grodno `niab-grodno.by` | National Historical Archive of Belarus in Grodno: Grodno province records, church registers, recruitment, volost boards | inventories: open page; copies and certificates: human only (written request) | inventories published in full |
| Fond catalogue `fk.archives.gov.by` | fond-level catalogue of all Belarusian archives | open page | no search form; nothing below fond level |
| `hryc.by` | fond lists of many archives; metasearch over inventories | fond lists: open page; search: own browser (subscription) | |
| `radzima.net` | per-village message boards of researchers | open page for reading; registration to post | village names repeat |
| "Памяць" district volumes | district memorial books with village-by-village name lists | human only (printed volumes, through a library) | |
| FamilySearch | "Belarus, Grodno, Church Books, 1649-1915" and filmed catalogues | own browser (free login) | |
| `memory.mil.by`, `partizany.by`, `memory.grsu.by` | war dead and burials; partisans; a small university database | own browser (November 2026) | `memory.mil.by` is a site of the Belarusian Ministry of Defence; see `war-and-losses.md` |

## NIAB Grodno

### Requests

- Contact details: see the archive's own site.
- Since 1 February 2025 the archive accepts biographical requests from private persons (confirmation of a fact
  about a named person, with the shelf mark), not genealogical research requests (as published by the archive, 2026). Ask for what
  you need in those terms. The application form is a `.docx` on the archive's site ("Заявление биогр. запросов").

### Reading a reply

- A name search covers the spellings you give: list them all. Ask for a slice by village as well as by name if
  you want one. A reply may cover the main question and not the secondary points; ask those separately. Record
  which years the archive says it does not hold.
- A name search that finds siblings shows that the surname is readable in those books, which makes a "not found"
  for the target person more credible.

### Published inventories

- The inventories (opisi) are online in full, linked from the archive's "science" section by fond range. Take each file name from the folder page; the
  capitalisation varies.
- The archive publishes close to two thousand inventory files (spreadsheets and PDFs); open the ones for your
  fonds. Some listed inventories are missing online.
- **The PDFs are scans without a text layer** (`pdftotext` returns nothing). They need OCR, e.g.
  `tesseract -l rus+pol`.
- Read `.xls` tables with a spreadsheet library (`xlrd`), not as raw bytes: raw byte search gives false misses.
- The published fond list lets you check whether a fond you expect (e.g. a particular volost board) exists at all
  before writing to ask for it.

### Cross-fond index of church registers

- The archive publishes spreadsheets of church registers by confession (`Cerkvi.xlsx` for Orthodox, and companions
  for Catholic, Jewish, Muslim, Old Believer and Lutheran records): one row per church, with years held
  **separately for births, marriages and deaths**, and the shelf marks.
- It is the archive's own document. Use it to check any claim of a gap (a missing year) before spending a request.
  Prefer it to summary pages on portals, which can be incomplete.
- NIAB in Minsk does not hold Grodno province records. Requests about Grodno province go to Grodno.

## Fond catalogue of Belarusian archives (`fk.archives.gov.by`)

- No search form: browse the pages by archive or use an external search engine. It does not go below fond level.
- Find a fond through the catalogue pages, not by guessing addresses.

## Other Belarusian resources

- **hryc.by**: fond lists of many archives are open; the metasearch over inventories needs a subscription.
- **radzima.net**: village-council pages merge researchers' messages about all their villages. Village names
  repeat across districts: the page you land on can be a namesake in another district. Check the district on the
  page. Researchers who work with a parish's books can be found and contacted through the site.
- **"Памяць" district memorial books** (printed volumes, through a library). A district volume has a section
  per village: a ready village-by-village list of names, also useful to decode numeric village codes in other
  databases.
- **"Указатель населённым местностям Гродненской губернии"** (gazetteer of Grodno province, 1905) on archive.org:
  the `_djvu.txt` is unusable (columns mixed); use `_djvu.xml` with word coordinates. OCR drops the first letter of
  the left column on left-hand pages.
- **Słownik geograficzny Królestwa Polskiego** covers Grodno province villages and volosts in full text; see
  [poland-lithuania-czechia.md](poland-lithuania-czechia.md).
- **Before 1900** the Orthodox parishes of Grodno province belonged to the Lithuanian consistory in Vilna; see the
  LVIA section in [poland-lithuania-czechia.md](poland-lithuania-czechia.md).

## FamilySearch (own login)

- The collection "Belarus, Grodno, Church Books, 1649-1915" had about 1.48 million records, 4.06 million persons
  and 441,000 images (August 2026). Not every fond of NIAB Grodno is in it; check the fond of your parish.
- `nashipredki.com` is a catalogue of East European archive films, compiled from FamilySearch data; on the fonds
  we checked (2026) it listed fewer films than FamilySearch, and it has no pages per film number.
- FamilySearch itself is described in `genealogy-services.md`; it needs the researcher's own login.

## Traps

- **Namesake volosts and villages.** The same volost name exists in other uezds and even other provinces, and a
  namesake can be larger than yours, with many more records in a database. The only reliable separator is the
  uezd written in the record ("<N> уезда"). Filter by uezd, never by volost name alone.
- Browse an archive's whole website before concluding that a fond is missing; part of a site can be easy to miss.
