# Libraries, gazetteers and printed reference works

Digital libraries, gazetteers, address books and printed indexes for the former Russian Empire and its western
borderlands, and how to use them to establish what a place was called and where it belonged in a given year.
Every statement about a site is an observation with its month, not a guarantee. The examples are composed
illustrations; the patterns come from real work, the particulars do not.

## First establish the place, then search

A request to an archive, or a search in a catalogue, uses the name and jurisdiction of the place in the year of the
event: uezd and volost before the Soviet reforms, district and village council after. Without them the answer is an
honest zero. A church register is always older than any questionnaire: find the parish of the village for that year
before writing anywhere.

Procedure:

1. **Read the place in the oldest document you have**, letter by letter, and note every spelling. Volost names are
   written inconsistently, often in several spellings across documents.
2. **Find every place of that name in the province.** Namesakes are common: one uezd can hold two villages of the
   same name, distinguished only by volost. A gazetteer of the right year gives the volost and the distance to the
   uezd town. A place gazetteer is the judge of a place name.
3. **Pin the year.** Use the gazetteer edition closest to the event. Administrative units were abolished and merged:
   when N uezd was abolished in the reforms of the 1920s and its volosts were merged into neighbours, the
   civil registers of the following years are filed under the successor's executive committee, not under the old
   volost.
4. **Pin the church jurisdiction separately.** Dioceses changed too: the Orthodox diocese of Grodno was created
   only in 1900; before that the consistory copies of its parishes were kept by the Lithuanian consistory in Vilna,
   so they are in the Lithuanian State Historical Archive, not in Grodno.
5. **Check which unit an archive's reply covers.** A negative reply about a neighbouring uezd does not cover the
   question asked and closes nothing.
6. **Absence from a gazetteer means little for settler colonies.** Settler colonies were often not listed in
   «Списки населённых мест»: the settlers bought a manor and split it into farms, and the gazetteer knew the place
   as an estate. Monographs on the settlers fill the gap (for Estonian colonies, Nigol 1918; see
   [estonia-latvia.md](estonia-latvia.md)).

## Gazetteers and place lists

| work | what it gives | where | notes |
|---|---|---|---|
| «Списки населённых мест Российской империи» ("Lists of inhabited places") by province | every settlement with uezd, stan or volost, households, population, distance | НЭБ (`rusneb.ru`), Президентская библиотека (`prlib.ru`), archive.org | on НЭБ and Президентская only catalogue cards and whole PDFs, no full-text search: read page by page |
| Moscow province editions: Nistrem 1852, Shramchenko 1890, Avrorin 1899, Penkin 1913 | the 1852 list gives households, souls and the landowner's name | НЭБ | used together they show a village before and after a fire, a sale or an emancipation |
| «Волости и гмины 1890 года» ("Volosts and gminas in 1890") | volost and gmina composition of the Empire | printed | agreed with the Polish geographical dictionary where compared |
| «Указатель населённым местностям Гродненской губернии» (1905) | index of settlements of Grodno province | archive.org | the `_djvu.txt` is unusable (columns mixed); use `_djvu.xml` with word coordinates; OCR loses the first letter in the left column of the left page |
| 1906 place list of Vitebsk province | full lists of volosts, fuzzy search | a searchable version on `familio.org` | |
| Słownik geograficzny Królestwa Polskiego (SGKP) | geographical dictionary in 16 volumes covering Poland and the western provinces: settlement type, powiat, gmina, distance, land area | `dir.icm.edu.pl`, free, full OCR text | see below |
| «Памяць» district volumes (Belarus) | district history and memorial books with a village by village list of names | printed volumes, through a library | a volume has a section per village; it can decode the village codes of a war database |
| Ukrainian archive inventories | full inventories with page-level contents and links to FamilySearch films | `uk.wikisource.org`, namespace `Архів:` | the best finding aid for Ukrainian archives |

### SGKP (`dir.icm.edu.pl`)

The main geographical source for the western provinces, searchable in full text across all volumes (observed
August 2026). Search the whole dictionary to prove a negative or to settle a duplicate: a single occurrence of a
village name in all volumes ("Primerowka, wś, pow. ..., gm. Obrazcowska, <N> w. od ..." in the pattern of the
entry) refutes two hypotheses at once, "there were two villages of this name" and "the archive catalogue misread
it".

## Digital libraries

| library | what it holds | reach | notes |
|---|---|---|---|
| ГПИБ, State Public Historical Library `elib.shpl.ru` | scanned pre-1917 books: memorial books, address calendars, refugee address lists | open page | read the book in the library's viewer; a "too many requests" page (`429`) is a refusal: stop |
| НЭБ, National Electronic Library `rusneb.ru` | gazetteers, memorial books, periodicals | own browser | did not answer from the project's network (2026; a 403 page); a reading room, or a copy through a library |
| Президентская библиотека `prlib.ru` | gazetteers, laws, periodicals | own browser (browser check) | |
| East View `dlib.eastview.com`, `ivis.ru` | Soviet newspapers and journals | human only | free access in the reading rooms of ГПИБ and РГБ: a visit |
| archive.org | memorial books and address calendars of Tver (1844-1916) and Tula (1848-1917) provinces in the collections `CommemorativeBooksTverGubernia`, `CommemorativeBooksTulaGubernia`; gazetteers | open page | `_text.pdf` files have an OCR layer: `pdftotext -layout`; alphabetical indexes at the end of each volume |
| `pskovbook.ru` | Vitebsk province memorial book for 1914 | open page | an independent rescan (volosts, constables) |
| `nlr.ru` (National Library of Russia) | «Весь Ленинград» ("All Leningrad") address books 1922-1935, contents by spread | own browser | |
| Электронекрасовка (Nekrasov library) | newspapers 1939-1946 with recognised text | open page | |
| Jagiellonian Digital Library `jbc.bj.uj.edu.pl` | Polish official gazettes 1917-1939 (`Obwieszczenia Publiczne`, voivodeship gazettes with land lists of gminas), `Monitor Polski`, press | open page (free, no registration) | one issue as a PDF with OCR |
| FBC, Federation of Polish Digital Libraries `fbc.pionier.net.pl` | metadata of all Polish digital libraries | open page | metadata only, no full text |
| CRISPA, Warsaw University Library `crispa.uw.edu.pl` | periodicals missing from JBC | open page | use its own viewer |
| `bcul.lib.uni.lodz.pl` | Łódź University library | own browser | did not answer from the project's network (2026); where the site is available to you, use it in your own browser under its terms |
| Estonian press `dea.digar.ee` (DIGAR) | Estonian newspapers, 1811 to the 2020s, with OCR: obituaries, farm sales, evacuation 1944 | own browser (browser check since November 2026) | |

`tesseract -l rus --psm 11` reads dense pre-reform type only in part; plan for a human or a model to read such
scans.

### OCR traps in digital libraries

- **OCR splits words with spaces.** In JBC a surname appeared as "P r i m e r o w"; a plain `grep` returns zero. Put
  `[\s\-\xad]*` between every pair of letters in the pattern.
- **Two-column gazetteers.** Plain text output mixes the columns; use the word-coordinate XML.
- **Encoding.** Polish PDFs set in CP1250 come out of `pdftotext` as CP1252 (`³` for `ł`, `œ` for `ś`, `¿` for
  `ż`); fix with `text.encode('cp1252').decode('cp1250')`.

## Address books, calendars and printed indexes

- **Памятные книжки and адрес-календари** ("memorial books" and "address calendars") of each province list
  officials, clergy, volost elders, constables and teachers by year. Look for them first on archive.org (with OCR),
  then ГПИБ, then НЭБ. The Pskov regional library's site, which held the Pskov ones, no longer resolves
  (`vivaldi.pskovlib.ru`).
- **City address books** («Весь Петербург», «Весь Ленинград») give address and occupation by year.
- **Refugee lists of the First World War.** ГПИБ's digital library holds parts of a printed list of refugee
  addresses.
- **Some printed works are not online page by page at all.** For them a human reads a PDF or goes to a reading
  room (see `needs-a-human.md`).

## Local history pages

Village and church pages on local history sites often repeat one another and trace back to a single text without
any archive reference: a fire, a number of houses and a date can all come from one such text and be supported by
nothing. Treat them as leads; find the archive reference before you write a fact. A local historian's blog that
names their own archive work is a route to a person, not to an archive (see `needs-a-human.md`).

## Dead library sites: the web archive

For a dead or changed site, ask the Wayback Machine (documented API):
`archive.org/wayback/available?url=<url>` for the nearest snapshot, then `web.archive.org/web/<year>/<url>`; the
list of captured pages under a path is `web.archive.org/cdx/search/cdx?url=<prefix>*`. See `dead-and-moved.md`.
