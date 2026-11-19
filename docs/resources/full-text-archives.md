# Full-text bases of digitised documents

Sites that hold scans of archival documents or printed books together with a machine-read text layer, so that
a name can be searched inside the documents themselves. How to read the reach classes and the three outcomes:
`README.md`. The examples are composed illustrations; the patterns come from real work, the particulars do not.

## Summary

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| Yandex Archive (Яндекс.Архив), `yandex.ru/archive` | recognised text of parish registers, confession lists, revision lists and archive inventories from 29 Russian archives | own browser: needs a login since October 2026 | without the login: a redirect to the front page, which is not a zero | only the participating archives listed below |
| epoisk.ru | search over scanned inventories of the Central State Archive of Moscow (ЦГАМ) | open page (Aug 2026) | not recorded | the three outcomes are told apart reliably |
| ГПИБ (State Public Historical Library), `elib.shpl.ru` | scanned printed books: address books, lists, reference works | open page (Sep 2026) | a "too many requests" page (HTTP 429) is a refusal: stop | read full-size pages in the library's own viewer |
| НЭБ (National Electronic Library), `rusneb.ru` | scanned books and periodicals from Russian libraries | own browser | a 403 page | did not answer from the project's network (August 2026) |
| Presidential Library, `prlib.ru` | scanned books and documents | own browser (Aug and Nov 2026) | a browser check page instead of the site | |
| Internet Archive, `archive.org` | scanned printed volumes with OCR: books of memory, gazetteers, commemorative books of provinces | open page and documented API (Aug-Sep 2026) | none observed | prefer the word-coordinate file to the plain-text file for tables |
| «Электронекрасовка» (Nekrasov Library), `electro.nekrasovka.ru` | newspapers 1939-1946 with recognised text | open page (Nov 2026) | not recorded | |
| «Пресса войны», `pressa-voiny.ru` | wartime newspapers | own browser: search closed without login (Nov 2026) | not recorded | |
| «Прожито», `prozhito.org` | diaries | open page (Nov 2026) | the same list for any query | the search did not filter by text when tested (Nov 2026) |

## Yandex Archive (Яндекс.Архив) - `yandex.ru/archive`

**What it holds.** Scans and recognised full text of metrical books (parish registers), confession lists
(исповедные ведомости), revision lists (ревизские сказки) and, often overlooked, the archive inventories
(описи) themselves. No login was needed until October 2026.

**Participating archives (29, as of August-September 2026):** ЦГА Москвы (Central State Archive of Moscow), ЦГАМО
(Central State Archive of Moscow Oblast), the state archives of Irkutsk, Ulyanovsk, Orenburg and Astrakhan
oblasts, Omsk, Vologda, Mordovia, Kuzbass, Chuvashia, Mari El, Yakutia, Novgorod, Adygea, Saratov, North
Ossetia, Primorye, Khabarovsk, Khakassia, Sevastopol, the Yekaterinburg diocese, the Russian State Library,
Ussuriysk, Sakhalin, the Novgorod museum, Dagestan, Karachay-Cherkessia, Yamal-Nenets.

**What it does not index.** Archives not in the list above, for example most central Russian oblast archives
and all Ukrainian archives (August-September 2026). Coverage of Moscow metrical
books was about three quarters, and of Moscow confession lists somewhat more. The recognised text does not
reach back past the 1870s: revision lists and early confession lists are digitised but not recognised, and
have to be read frame by frame.

**Reach.** Since October 2026 the archive needs a login: the researcher reads it in their own browser under
their own Yandex account, where search, scan pages and full-resolution originals work (observed November
2026). Without the login a request is redirected to the front page, which is not a zero.

**Searching inside one file.** The "find in file" box on a file page searches only that file. A short phrase
from the expected entry (a name with the village) is the quickest way to find it; a year in the header or a
month name finds the right page of a long volume.

**Zero signature.** A normal result page that states zero results. A redirect to the front page (no login) is
not a zero.

**Traps.**

- **"Not digitised" and "nothing there" look the same** (September 2026). For an inventory that is not
  digitised, the catalogue shows a file count but lists no files. When walking an archive, compare the number
  of files you collected with the digitised counts the inventories show; only equality proves the walk
  complete.
- **Catalogue titles can be wrong** (September 2026). In one fond, a file titled "no sheet in the inventory"
  with dates that did not match its content was a run of parish registers of a named village; another file carried a misspelt village
  name; in a yearly series the file numbering jumped by about twenty between two consecutive years. Identify
  files by the archive's own printed or spreadsheet index, not by the title.
- **The catalogue dates a file by the inventory, and printed sheet headers can give the wrong year.** In one
  volume of the war years the printed headers still carried a pre-war year. Take the year from the dean's
  certifying signature at the end of each month, or from the switch of the title «крестьянинъ» to
  «Гражданинъ» after February 1917 (September 2026).
- **The text layer scrambles tables.** For a tabular revision list the recognised text mixes up the rows, and
  reading it in order gives plausible nonsense: other people's ages attached to other people. Sort the text
  blocks by their horizontal position into columns, then by vertical position inside each column, and the
  table falls into place; check doubtful cells on the full-size image. In one list this changed a death year
  and an age (September 2026).
- **Do not trust the machine text for numbers.** A handwritten year added to a printed prefix was read as a
  different year, and the running number of an entry was read as the day (November 2026). Read year, day and
  month from the image. For a register without a year in the header, take the year from the annual total at
  the end.
- **The machine text substitutes names.** Names and dates go into the family tree only from the scan.
- **File names of saved images are frame numbers, not sheet numbers.**
- **A saved image can be incomplete.** Open it to the end before relying on it.

## epoisk.ru - search over scanned inventories of ЦГАМ

A search over the scanned inventories of the Central State Archive of Moscow, and a summary table of 173 fonds
of that archive marked for metrical books, confession lists and revision lists. No login. The three outcomes
are told apart reliably (August 2026). Use it to find which inventory to open before searching the documents
themselves.

## ГПИБ (State Public Historical Library of Russia) - `elib.shpl.ru`

**What it holds.** Scans of printed books, including lists and directories that name people (for example
printed lists of First World War refugees with their addresses).

**How to read it.** The library's own viewer shows each page at full size. Read the book there. A "too many
requests" page (HTTP 429) is a refusal: stop (September 2026).

**OCR.** Tesseract (`-l rus --psm 11` gave the most text on a test page) reads dense pre-reform typesetting of
five or six columns only in part: single surnames and place names come through, but row order on
multi-column pages is lost. A surname missing from the OCR is not missing from the page: keep the page link
with every hit and check the scan.

## НЭБ (National Electronic Library) - `rusneb.ru`

Scanned books and periodicals from many Russian libraries. Reach: own browser. It did not answer from the
project's network (August 2026; a 403 page).
Where the site is available to you from where you are, use it in your own browser under its terms; otherwise
the official routes are a written request, a library copy, or a visit (see `README.md`).

## Presidential Library - `prlib.ru`

A browser check page instead of the site in August and November 2026. Own browser: the researcher reads it in
their own browser.

## Internet Archive - `archive.org`

Free and open throughout 2026. Useful volumes found there: the 1905
«Указатель населённым местностям Гродненской губернии» (gazetteer of Grodno province); commemorative books
and address calendars of Tver and Tula provinces with OCR.

**Trap.** For tables, the plain-text OCR file (`_djvu.txt`) mixes the columns. Use the word-coordinate file
(`_djvu.xml`) and rebuild columns from the coordinates. In one gazetteer the OCR also dropped the first letter
of every entry in the left column of the left page (August 2026).

The Internet Archive's Wayback Machine also keeps copies of dead sites; its documented availability and CDX
APIs find the nearest snapshot and list what was captured. A snapshot can be incomplete: one captured book of
memory lacked whole letters of the alphabet, so zeros for surnames under those letters do not count (November
2026).

## «Электронекрасовка» (Nekrasov Library digital collection) - `electro.nekrasovka.ru`

Newspapers of 1939-1946 with recognised text, searchable on the public site (observed November 2026). Trap: a
village name that exists in several regions produces hits about a namesake in another district; check the
district in every hit.

## Other full-text sources and where they are described

- Digitised Estonian newspapers, 1811 to the 2020s (DIGAR, `dea.digar.ee`): see `estonia-latvia.md`. Own
  browser (browser check since November 2026).
- Ukrainian inventories in full text on `uk.wikisource.org` (namespace `Архів:`) and scans on Wikimedia Commons:
  see `ukraine.md`.
- Libraries with scanned printed reference works (Jagiellonian Library and others): see
  `libraries-and-reference.md`.
- War-related newspapers and memoirs: `war-and-losses.md`.
