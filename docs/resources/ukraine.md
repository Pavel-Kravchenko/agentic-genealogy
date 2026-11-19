# Ukraine: archives, inventories and memorial databases

Resources for ancestors from the former Kiev, Poltava, Chernigov and neighbouring provinces in today's Ukraine.
Statements about site behaviour are observations with their month. The examples are composed illustrations; the
patterns come from real work, the particulars do not. Reach classes: **open page** (a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser`), **own browser** (used by the researcher personally in a browser:
login, subscription, or no automated requests served, for example a browser check), **human only** (payment,
letter, visit), **dead**; see [README.md](README.md).

## Overview

| site | what it holds | reach | notes |
|---|---|---|---|
| Ukrainian Wikisource, namespace `Архів:` (`uk.wikisource.org`) | full inventories of TsDIAK (fond 127 in full, fond 990), oblast archives (Cherkasy, Kiev and others), with page-level contents and links to FamilySearch films | open page (documented MediaWiki API) | the best entry point for Ukrainian archives |
| Wikimedia Commons | PDF scans of some archive files (revision lists, plans, volost board files) | open page (documented API) | |
| TsDIAK `cdiak.archives.gov.ua` | Central State Historical Archive in Kyiv: consistory records (fond 127), consolidated catalogue of church registers | own browser | did not answer from the project's network (September 2026; a 403 naming a geographic block); a written request to the archive, or a person in the country who uses the archive's services under its rules |
| TsDIAK image viewer | images | own browser | |
| "Качиний Інспектор" `inspector.duckarchive.com` | cross-archive catalogue search; shows where images are online | open page | |
| Oblast archives (e.g. Cherkasy, `ck.archives.gov.ua`) | church fonds, volost boards, civil registry books | own browser (browser check, September 2026) | inventories on Wikisource |
| Holodomor museum `holodomormuseum.org.ua` | PDF volumes of the National Book of Memory of Holodomor victims | open page (PDF) | no online search |
| `ridni.org` | surname distribution map from state data 2011-2013 | open page | |
| `reabit.org.ua/nbr/` | "Реабілітовані історією" (Rehabilitated by History) | open page | |
| MyHeritage | Kyiv consistory duplicates, indexed | own browser (subscription) | one surname appeared in several forms (September 2026) |
| FamilySearch | filmed church registers of TsDIAK and oblast archives | own browser (free login) | |

## Ukrainian Wikisource: inventories and film links

- Namespace `Архів:` holds the full inventories of TsDIAK fond 127 (Kiev Spiritual Consistory), fond 990, and of
  oblast archives, split into pre- and post-revolution fonds. Many entries give sheet-level contents and the
  FamilySearch film for the file.
- The wiki text of a page is available with `?action=raw`, and the MediaWiki search API searches the source text.
- Some oblast archive fonds are only partly copied there (single files, not whole fonds).

## TsDIAK (Kyiv)

- The site did not answer from the project's network (403, geographic block, September 2026). The consolidated
  catalogue of church registers is behind that block. Official routes: a written request to the archive, or a
  person in the country who uses the archive's services under its rules.
- Fond 127, consolidated yearly volumes: the consistory bound the registers of a whole uezd for one year into one
  or a few volumes. There may be no file named after your village: look inside the uezd volume for the year. A
  uezd's run in a given inventory can stop in a certain year; look for the later years in other inventories.
- The image viewer is a JavaScript application: a human in a browser.

## "Качиний Інспектор" (duckarchive)

- Its search works by place name and accepts **Cyrillic only**: Latin letters break the search.
- A catalogue entry shows where the images are: a FamilySearch film, the TsDIAK viewer, or other online copies.
- The domain `inspector.duckarchives.gov.ua` does not exist.

## Oblast archives

- An oblast archive site showed a browser check in September 2026; it is read by a person in a browser. The
  Wikisource copies of the inventories are the open finding aid.
- Church fonds of rural parishes can sit in a section of the site that is easy to miss; browse the whole site
  before concluding there are none. Many of the images are on FamilySearch.
- Volost board files of some archives are on Wikimedia Commons as PDFs.

## Holodomor memorial books

- `holodomormuseum.org.ua` offers PDF volumes of the National Book of Memory of Holodomor victims by oblast and
  district. No online search: download the PDF and read it with `pdftotext -layout`.
- **The book's font drops the letters "к" and "у"** in the text layer: a surname containing к or у appears with a
  gap in their place. Search by fragments without those letters.
- Older Holodomor sites: `memorialholodomor.org.ua` showed a hosting placeholder; `map.memorialholodomor.org.ua`
  is alive but maps mass graves without names; `zernapravdy.org.ua` gives HTTP 530; `memorialpolehlym.mva.gov.ua`
  does not answer (observed 2026).
- The national "Народна книга пам'яті" (People's Book of Memory) of 2024 holds 4,180 names; a district may be
  represented by only a few villages.
- Older regional volumes (e.g. Kyiv oblast, 2008) list victims village by village with the names of informants.

## Other Ukrainian resources

- **ridni.org**: surname distribution from state data of 2011-2013 (not self-reported profiles): number of bearers,
  top settlement, rank of the surname.
- **ua.openlist.wiki** (the Ukrainian section of Открытый список): it prints «Знайдено N», not «Найдено N». A check
  that waits for the Russian word treats a valid result as a block; check both. `uk.openlist.wiki` does not exist.
- **Archive of the Security Service (ГДА СБУ)**: written request only. The archive of the Ministry of Internal
  Affairs of Ukraine (ГДА МВС) holds sentences passed in the Ukrainian SSR; not checked.
- Checked in 2026: `uk.rodovid.org` did not answer (HTTP 503, 2026); `genealogy.com.ua` did
  not answer (2026); `genealogia.com.ua` alive but with general text only.

## MyHeritage: Kyiv consistory duplicates

- Needs a subscription; the researcher uses it in their own browser.
- **The transcription gave one surname in several forms**, including one with `?` in place of a letter, and a
  person could be found only by given name (September 2026). Search a branch by **given name or patronymic plus
  the place** of the event. Parents in a record are searchable as persons.
- A place condition also catches villages of the same name in another uezd; filter by the church named in the
  record.
- Take the source reference (volume, page, entry, film, image) from the record card, not from the results list.

## FamilySearch (own login)

FamilySearch holds films of TsDIAK and oblast archive church registers (searchable by place under "Images"); see
`genealogy-services.md`. Traps seen on Ukrainian films (September and November 2026):

- Labels by place can follow the table of contents of a film, not its content: a confession book labelled with a
  village held only town churches.
- The order of frames on a film need not match the sum of the group sizes listed for it; check the header of the
  frame you land on.
- The FamilySearch full-text search did not cover these registers.

## Reading lessons

- **Two villages of the same name in one uezd** are distinguished only by volost, and the volost name is spelled
  inconsistently in records. Collect the variants before filtering.
- A scribe can write "2" with a loop that looks like "9": an age misread this way creates a person who did not
  exist. Compare doubtful digits with other digits in the same entry.
