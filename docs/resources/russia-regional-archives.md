# Archives of Russia: federal and regional

What the state archives of the Russian Federation put online, how far a visitor, a browser session or only a
human in the reading room can get, and how each site looks when it refuses rather than when it has nothing.
Everything below was observed in 2026; each behaviour carries the month it was seen. Sites and opening
hours change: treat every line as an observation, not a guarantee, and check the archive's site. The examples
are composed illustrations; the patterns come from real work, the particulars do not.

Reach classes (see `README.md`): **open page**, **own browser**, **human only**, **dead**. Sites of ministries
and military archives are described only by what a visitor sees and the official route.

## How Russian archives publish finding aids and scans

### Portal types

Russian archives use four kinds of online finding aid. The kind decides what a "no result" means.

| portal type | what it holds | typical reach | what a zero means |
|---|---|---|---|
| Regional "AIS" catalogues on the КАИСА (KAISA) platform, e.g. `archpskov.kaisa.ru`, `kaisa.tambovarchiv.ru`, `ulian.kaisa.ru` | fonds, inventories (описи), file cards with sheet counts and dates; sometimes an e-reading room with scans (электронный читальный зал, ЭЧЗ) | open page for the catalogue; scans usually behind a subscription | only that no *described* file matches |
| Oblast-wide portals of the scholarly reference apparatus (научно-справочный аппарат, НСА), e.g. `af.yar-archives.ru` | catalogues of every archive of the oblast in one search, filter "digitised only" | own browser (observed Sep 2026) | only that no card title matches your exact spelling |
| Archive websites with downloadable inventories, e.g. `ogugauo.ru` (Ulyanovsk) | inventories as PDF (often with a `.doc` beside it) | open page | after a full read of the inventory: "not in this fond" |
| Aggregators: Яндекс.Архив (Yandex Archive, `yandex.ru/archive`), `epoisk.ru` | Yandex Archive: full text of recognised scans and inventories for about 29 participating archives; `epoisk.ru`: search over the scanned inventories of ЦГАМ | Yandex Archive: own browser (needs a login since October 2026); `epoisk.ru`: open page | nothing, if the archive is not a participant |

Yandex Archive covers Moscow and several provinces in full text, and only the participating archives
(August-September 2026): for any other archive a zero there says nothing. Its catalogue traps are in `full-text-archives.md`.

Published archive guides (путеводители) of Russian archives are collected at `guides.rusarchives.ru`. Its
full-text search joins words with OR, ignores quotes and does not rank, so a two-word query returns tens of
thousands of hits (observed Aug-Sep 2026). Walk the list of guides and their subject trees instead.

### What "digitised" means

- **"Inventory digitised" is not "file digitised".** Many catalogue entries offer only a scan of the inventory
  page, not of the file. Check that page images open before you plan around a file.
- **"Digitised" can still mean closed.** On the Yaroslavl portal and the Ulyanovsk e-reading room the images
  exist but sit behind a login and a subscription.
- **Some digitised files never reach the public portal.** They can be shown only on the reading-room
  computers, under working shelf marks that may not match the published catalogue. Only the archive can say how
  the two relate.
- **Full text is partial.** For Moscow, recognised text covered roughly three quarters of the parish registers,
  and nothing before the 1870s; revision lists (ревизские сказки) were not recognised and must be read page by
  page (observed Aug 2026).
- **OCR of tables can scramble row order.** In tabular revision lists the recognised text comes out in the wrong
  row order, so a list read top to bottom gives plausible nonsense: other people's ages on other people's
  names. Rebuild the table from the positions of the text blocks (columns first, then rows), and check every
  contested value on the full-size image (observed Sep 2026).
- **Printed headers can give the wrong year.** In a volume of parish registers of the war years the printed
  page headers still carried a pre-war year. Date the page by the dean's certification signature at the end of
  each month, and by the change of the estate title "крестьянинъ" (peasant) to "Гражданинъ" (citizen) after
  February 1917 (observed Sep 2026).
- **Catalogue titles can be wrong.** In one fond a file titled "no sheet in inventory" with dates that did not match its content was a
  parish register of a different village and decade; another title misspelled the village; and a yearly run
  jumped by about twenty file numbers. Identify files by the archive's own index, not by the title (observed
  Sep 2026).
- **Inventory date ranges can mislead.** The preamble of one inventory of early Soviet civil registration
  books warns that they are "decayed, bound in disorder". On the Pskov catalogue take dates from
  «Хронологические рамки» (chronological frame), not «Крайние даты» (outer dates); on the Tambov catalogue do
  not rely on the end dates on the *fond* card (observed Sep 2026).

### Civil registration books

**Civil registration books reach the state archive only after 100 years** (Federal Law 143-FZ, art. 77, as
read in 2026; our reading, not legal advice), not 75 as often repeated. A book of 1950 is still with the registry office. For a given book,
ask the registry office or the archive. On the Soviet adult death record forms seen, there was **no field for the
parents**, so a death record will not answer a parentage question.

## Federal archives

| archive | what it holds / what is online | reach | block signature / trap | notes |
|---|---|---|---|---|
| **РГИА** (Russian State Historical Archive, St Petersburg), catalogue `fgurgia.ru` | catalogue of fonds, inventories, files; name and geographic indexes | own browser (observed Aug-Sep 2026) | - | slow: answers can take 10-20 s |
| **ЦГИА СПб** (Central State Historical Archive of St Petersburg), `spbarchives.ru` | catalogue | own browser | - | did not answer from the project's network (2026); a written request, or, where the site is available to you, your own browser under its terms |
| **ГА РФ** (State Archive of the Russian Federation), inventories at `opisi.garf.su` | inventory tree | own browser | no search form, only the tree (Sep 2026) | access rules for personal data and the request form: on the archive's own site; by those rules (our reading, not legal advice) files older than 75 years are open and later ones need proof of kinship: ask the archive |
| **РГАДА** (Russian State Archive of Ancient Acts, Moscow) | records older than 1740, e.g. census books and lists of the 17th and early 18th centuries | human only | - | reading room in Moscow; order ahead (contact details: see the archive's own site); one separate order per fond (observed 2026) |
| **ЦАМО** (Central Archive of the Ministry of Defence, Podolsk) | WWII service and loss records | human only for the archive itself; its data reach the public through ОБД «Мемориал», «Подвиг народа» and «Память народа» | - | written request (contact details: see the archive's own site). See `war-and-losses.md` for the online entries |
| **РГВИА** (Russian State Military History Archive) | WWI and earlier army records | human only (written request); its online entry `gwar.mil.ru` is own browser | - | regimental papers cannot be searched without the regiment's name; a recruit's service record (формулярный список) gives the regiment |
| **РГВА** (Russian State Military Archive) | Red Army records, including the Winter War | human only | - | request form needs call-up office and unit number |

Fond-level facts at ГА РФ that save a wrong request (observed Aug-Sep 2026):

- Ф. Р-9526 (Directorate for Repatriation) holds the repatriation lists that ОБД «Мемориал» uses.
- Ф. Р-9414 (GULAG) holds orders, reports and statistics only; there are no prisoners' personal files.
- No central name index of First World War refugees was found in the federal guides (observed 2026); look
  regionally, and read the fond-level description before writing a request.
- Fond 10035 (NKVD investigation files for Moscow and Moscow oblast) is in practice listed by name in the
  «Открытый список» (Open List) database, 77,353 cards, and in «Бессмертный барак».

**Lutheran registers of Pskov province are not in Pskov.** First copies 1833-1885 and 1899-1909 are in РГИА
(the consistory fond); registers 1892-1917 are in ЦГИА СПб. The parish lists of members (книги прихожан) had no
second copy, so a lost first copy cannot be replaced (observed Aug 2026).

РГИА search behaviour (observed Aug-Sep 2026):

- Search is **by substring**: a short surname also matches every longer name that contains it (a query for
  "Пример" returns Примеров and also any Апримеров), so filter the results.
- Pre-reform spellings (with ъ, і, ѣ) are not found at all; search in modern spelling.

**Справочно-информационный центр федеральных государственных архивов** (the reference centre of the federal
archives under Rosarchiv) answers questions about federal archives only. Its "no information" covers none of
the regional archives, the departmental archives (FSB, MVD) or the civil registry offices.

## Regional archives

### Moscow city (ЦГА Москвы, ЦГАМ) and Moscow oblast (ЦГАМО)

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `cgamos.ru` (portal of the Moscow city archive) | fonds catalogue, scans with subscription | own browser (Sep 2026) | a 403 page with an almost empty body | scans behind a subscription |
| Yandex Archive | Moscow consistory copies of parish registers and confession lists, parish copies, revision lists, catalogue of 10,409 ЦГАМ fonds | own browser (needs a login since October 2026) | see `full-text-archives.md` | both archives are participants |
| `epoisk.ru` | search over the scanned inventories of ЦГАМ, and a table of 173 fonds marked for parish registers, confession lists and revision lists | open page, no login (Aug 2026) | three outcomes (hits, zero, error) are clearly distinct | |
| ЦГАМ and ЦГАМО reading rooms | originals and server copies | human only | - | order forms mark a file as "Сервер" (digitised, read on screen) or issue the original; if an order stays "with the staff" for long, ask the reading room |

Traps:

- Revision lists in the Moscow treasury chamber fond are not recognised by full text; browse them page by page.
- A year that a secondary table lists as a gap in a confession-list series can exist and be readable; check
  the inventory itself before declaring a year missing.
- Headers of parish-register volumes can give the wrong year (see "What digitised means").

### Yaroslavl oblast

The former Yaroslavl state archive (ГАЯО) is now ГБУ ЯО «РЦОМиАД»; its party-archive section is ЦДНИ,
its personnel-records section ЦДЛС, and it has branch archives in several towns of the oblast.

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `af.yar-archives.ru` | finding aids of **all 26 archives of the oblast**: fonds, inventories, file cards, one search across all, filter for digitised files; the regional archive alone has 2,060 fonds | own browser (Sep 2026) | a refusal page instead of the catalogue | remote images: behind a subscription of the archive, after an ЕСИА login (Gosuslugi, the state services account) |
| Yandex Archive | - | - | - | **no Yaroslavl fonds at all** |
| Forum ЯрИРО, `forum.yar-genealogy.ru` | researchers' extracts from the regional archive's files, with sheet and scan numbers | own browser; guest search is switched off | - | browse through the "navigator" topics for surnames and for places |

Traps on the portal (observed Sep 2026):

- With morphology switched on, several words are joined with AND: a record type plus a place name can give
  zero while the record type alone gives hundreds. Search one word at a time.
- Village names in the catalogue are not normalised: two spellings of one hamlet gave two different result
  sets. Search every spelling, and search by the root of a volost name, because the files and the committee
  name spell it differently.
- A zero for a surname in every spelling across all archives of the portal is a statement about card titles,
  not about people.
- A lock icon «Просмотр образа ограничен» ("image viewing restricted") can stand next to some files and not
  others, with no open page explaining it. Ask the archive what it means.
- The portal shows whether a file is digitised. Check that the files you need are digitised before planning
  around them.
- The archive's own contact page is in windows-1251, and a page-to-text tool returned a wrong street name from
  it. Read the page itself and decode cp1251 explicitly.

### Pskov oblast (ГАПО)

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `archpskov.kaisa.ru` (AIS of the Pskov oblast archives) | ГАПО and four more archives: fonds, inventories, files with sheet counts and dates | open page (Aug-Sep 2026) | sometimes down for hours | the file level is reached by walking the tree of fonds and inventories, not by search |

Traps:

- Take dates from «Хронологические рамки», not «Крайние даты».
- A reply letter can give narrower dates than the files hold; check the inventory.

Contact details: see the archive's own site.

### Ryazan oblast (ГАРО)

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `garo62.ru` | contacts | open page | - | contact details: see the archive's own site |
| ЕГИС «АНРО», `anro.ryazan.gov.ru` (e-reading room) | inventories only | own browser | a 403 page naming a geographic restriction | did not answer from the project's network (September 2026); the site said it was under reinstallation, with full launch announced for Q4 2026; written request to the archive |
| `62info.ru` | a local researcher's survey of the archive's parish registers, by parish and year, with file numbers | open page | the normal page shows only the first third; the print version shows the whole text | the survey is split into parts; a letter missing from one part may be in another |
| Forum ВГД, a topic on the archive's confession lists | volunteer index of villages | open page, encoding cp1251 | some pages are shown only to registered users | volunteers there take requests to look up villages |
| `nashipredki.com` | inventories of Ryazan confession lists | open page | - | a catalogue compiled from FamilySearch data; on the fonds we checked (Sep 2026) it listed fewer films than FamilySearch |

The archive can suspend genealogical requests for a period, and it answers postal requests on parish registers only for
a range of years; other years need the reading room, in person or by a representative (observed Sep 2026;
check the archive's site).

### Tambov oblast (ГАТО, Tambov)

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `kaisa.tambovarchiv.ru` | catalogue of fonds, inventories and files | open page (Sep 2026) | - | the church-book database on the same site is a separate part (next row) |
| church-book database on `kaisa.tambovarchiv.ru` | parish register database | own browser | - | - |
| `tambovarchiv.ru` file pages | archive guide (путеводитель, PDF with text layer); a geographic index of the revision-list fond (PDF: villages to file numbers) | open page | - | run `pdftotext -layout` on the index, or columns mix and villages get other villages' file numbers |

The guide traces where parish registers went after the revolution, which tells you which fond to ask for.

Contact details: see the archive's own site. The archive confirms a written
request with a registration notice that gives an incoming number and the department that will answer
(observed Sep 2026).

### Ulyanovsk oblast (ГАУО) and Simbirsk province

In September 2026 the Yandex Archive part for Simbirsk province was open without a login; it needs one since
October 2026.

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| `ogugauo.ru` | all inventories as PDF, no login | open page | - | a `.doc` with a text layer often sits next to the PDF: search it instead of running OCR |
| Yandex Archive | parish registers of the province, 1850s-1914 | own browser (needs a login since October 2026) | see `full-text-archives.md` | |
| `ulian.kaisa.ru` (e-reading room) | registers 1913-1919 scanned, not in Yandex | own browser, subscription | - | - |

Reading an inventory through to the end changes what you can say: "this fond has no such list" instead of "not
found in the digitised part". That difference is the reason to read the whole inventory.

Neighbouring Samara: a consistory fond covers the parishes of its own province as it then was, not of today's
oblast (see "Writing to a Russian archive" below). The Samara
archive's AIS requires an ЕСИА login (Sep 2026).

### Tula oblast (ГАТО, Tula)

| source | what it holds | reach | notes |
|---|---|---|---|
| `svrt.ru/lib/mater_po_gen.pdf`: Зайцев, «Материалы для генеалогических исследований в фондах ГАТО (Тула)», 2017 | fonds of parish registers, townspeople (мещане) and the Tula gunsmiths | open page (PDF) | - |
| `nashipredki.com` | catalogue of Tula parish registers by parish | open page | - |
| `archive.org`, collection of Tula province memorial books (памятные книжки) and address calendars | with OCR | open page | - |

### Tver oblast (ГАТО, Tver)

| source | what it holds | reach | notes |
|---|---|---|---|
| `archives.tverreg.ru` (the Tver state archive) | parish registers (behind a subscription), civil registration fond | own browser | did not answer from the project's network (September 2026); a written request, or, where the site is available to you, your own browser under its terms |
| `tverarchive.ru` | - | dead | no longer the institution's site (observed September 2026); do not open and do not cite |
| `archive.org`, Tver province memorial books | with OCR | open page | - |
| `visz.nlr.ru`, Book of Memory of victims of repression (Leningrad and Kalinin oblasts) | search by name | open page | - |

### Other regional sources

- Regional MVD information centres (ИЦ УМВД) often take requests only through the web form on the regional
  ministry site. A negative reply may give no article, term or dates and covers
  only that centre's holdings.
- A municipal archive of a district town may hold only a few modern administrative files on a village. Read a
  municipal archive's catalogue on the oblast portal before you write to it.

## Writing to a Russian archive

What a request must contain:

1. The person: surname in every spelling you know (Примеров, Примеровъ, Прымеров), given name, patronymic if
   known, and the approximate years.
2. The **place as named in the year of the event**: province (губерния), uezd, volost, parish and village.
   Russian borders moved in 1918-1929: uezds were transferred between provinces or abolished, and records
   stayed with the archive of the old unit. Ask the archive that holds the old unit, and name the old unit.
3. The genre of record and the years: parish registers, confession lists, revision lists, household lists,
   civil registration books, refugee questionnaires. If you know the fond and inventory from the catalogue, give
   them; the archive will not look for them on your behalf.
4. The scope you want read: "the whole file", "every village of Obraztsovskaya volost", "all three spellings".
   Without it the reply may cover only the name as written.
5. Which archive holds what: check the catalogue first. A reply from the wrong archive costs months.

Practical points (observed 2026; check the archive's site):

- Many archives take requests only on their own form or by post, and some answer postal requests only for a
  range of years.
- РГАДА wants one order per fond, sent ahead.
- Confirm the archive's postal address against its own website; two different street names circulated for
  one archive.

### What a negative reply covers, and what it does not

An archive answers the question it read and reads the volume it judged sufficient. Before you write "not in
the archive", read the reply for these limits:

| the reply says | what it actually closes | what stays open |
|---|---|---|
| "no record" for one district office, searched from a given year to today | that district office, those years | earlier years, neighbouring districts and the regional registry archive |
| "no record", searched one spelling | that spelling, that parish, those years | every other spelling: re-request with the variants |
| "no record", searched by name | the name as written | the same person under another household (a servant, a lodger): re-request a full read by village |
| "not in the catalogue" | the *described* holdings | undescribed or misfiled material |
| "the file was checked" | the part of the file matching your wording | the rest of the file (a file can cover a whole province while only one uezd was read) |
| "these documents are not held" (не сохранились, на хранении нет) | final for that archive and those years | other genres, other archives |
| "the federal archives hold nothing" | federal archives under Rosarchiv | regional, departmental (FSB, MVD) and civil registry archives |
| an answer that covers an extra item and is silent on your main question | only the extra item | the main question: ask again |
| "no such village in the reference book" | the reference book's list of places | settler colonies, which were often listed as estates, not villages |

A reply that refuses because records are missing for a given span is final for that span. A reply can cover
only the few years of a series that survive; do not read the first surviving year as the year of the record.

Keep every reply with its outgoing number, date, what was asked and what was read, so nobody orders the same
search twice.
