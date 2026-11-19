# Estonia and Latvia: archives, catalogues and image portals

Resources for ancestors from the former Estland, Livland and Courland provinces (today Estonia and Latvia),
including Estonians and Latvians who moved into the Russian interior. Every statement about site behaviour is an
observation with its month, not a guarantee. The examples are composed illustrations; the patterns come from real
work, the particulars do not. Reach classes used below:

- **open page**: a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser`.
- **own browser**: used by the researcher personally in a browser: it needs a login or a subscription, or it does not serve automated requests (for example, it shows a browser check).
- **human only**: needs payment, signature or a reading room.
- **dead**: does not answer or never existed.

## Estonia: National Archives (Rahvusarhiiv)

### Overview

| site | what it holds | reach | zero signature | notes |
|---|---|---|---|---|
| AIS catalogue `ais.ra.ee` | inventories of all Estonian fonds: file titles, shelf marks, "Digiteeritud" (digitised) flag | open page | see traps below | no frame list in AIS |
| Saaga `ra.ee/dgs/explorer.php` | structure of fonds and inventories; image viewer | catalogue: open page; images: own browser (free VAU login) | | |
| Name index of personal books (nimreg) | surname, shelf mark, page and frame number in Lutheran personal books | open page | real zero: the "Leiti sarnased nimed" (similar names) block is empty too | results in pages of 100 |
| Data registers `ra.ee/apps/andmed/` | six sets: revision lists (shelf mark by estate and year), estates, volosts, name register of manor fonds, Album Academicum (Tartu students 1918-1944) | open page | | German names in inverted form |
| Name-giving database `ra.ee/apps/onomastika/` | who received which surname, where, in 1826 (Livland) and 1835 (Estland) | open page | | no wildcards |
| DIGAR press `dea.digar.ee` | full text of Estonian newspapers, 1811 to the 2020s | own browser (browser check since November 2026) | | |
| Cemetery register `kalmistud.ee` | burials: birth, death and burial dates, plot neighbours | open page (search form) | a result list without your filter applied is not "no records" | no gravestone photos |

### AIS catalogue

- Search by shelf mark (reference code, with `*` as a mask) on its own; combined with a title or a free-text query
  the reference code was ignored (September 2026). Search by words in the title works separately.
- The general search box with a shelf mark returned a normal page with the line `Otsing: (puudub)`: a silent zero
  that looks like "no such file" (September 2026). Use the reference-code search.
- Tell a zero from a hit by the presence of result rows, never by the look of the page.
- A file that exists in AIS but has no images gives "Page was not found" when opened by shelf mark in Saaga. That
  means "not digitised", not a typing error (November 2026).
- Inventories store the **normalised** spelling of surnames (e.g. `Naidis`, not the older `Näiddis` written in the
  source). A search under the source spelling can miss files that the normalised form finds.
- File titles can truncate a surname (a two-syllable name stored as its first syllable plus the patronymic).
  Once one file of a family is found, read the neighbouring entries of the same inventory, not only surname hits.
- Shelf marks take a slash before a sub-unit: `EAA.<fond>.<series>.<item>/<sub>`. A hyphen or dot in that place is
  not accepted.
- The old AIS address is dead; AIS moved to a new interface (August 2026).
- Fonds useful for migrants: **ERA.36** (option files of 1920-1923, people who opted for Estonian citizenship from
  Soviet Russia); **EAA.527** (Livland Treasury Chamber) and **EAA.178** (Estland Treasury Chamber), which handled
  the registration and departure of peasants from the tax estate; **EAA.924** (passports and transfers). File numbers
  quoted in old documents can be an office's own registry numbers, not archival file numbers.
- Livland province was split between today's Estonia and Latvia. For a provincial institution such as the
  treasury chamber, check both the Estonian archive and LVVA in Riga.

### Saaga images (own browser, VAU login)

- The catalogue is open to everyone; images and the list of frames need a free **VAU** account (`ra.ee/vau`,
  registration by e-mail or Google sign-in). The researcher registers, signs in and views the images in their own
  browser.
- In the explorer, the **Viitekood** / "Reference code" field (the second field, not `Üldotsing`) opens a file by
  shelf mark. The window title shows the file title, often with the applicant's name.
- Change frames with the frame-number field: the "next" arrow skipped frames silently (September 2026).
- The viewer does not zoom above 100 %: enlarge a screenshot instead.
- The researcher downloads the frames they need with the viewer's download button.

### Frame, file and sheet are three different numbers

- The viewer's frame index is not the image file number, and the gap between them is not constant within a file;
  "repeated shot" images are separate files (November 2026).
- The frame number is not the sheet (folio) number either: offsets of a few frames occur, and a frame can carry
  sheet numbers written over crossed-out older ones. Identify a sheet by its stamped number and its header, not by
  the viewer counter.
- Frame numbers given by the nimreg index matched the viewer's frame numbers on the files checked (September 2026).
- A frame reference copied from someone else's tree can be off by a few frames and open the neighbouring household.
  Check every frame through the index, and record in your notes whether a number is a frame or a file number.

### nimreg: name index of Lutheran personal books

- Search by surname, choosing county and parish in the form. Columns: Nimi / Viitekood / Fond / Säilik / Algus /
  Lõpp / Lehekülg / **Kaader** (frame).
- Covers **personal books (Personalbücher) only**; church registers of births, marriages and deaths are not
  indexed there. Given names are mostly empty: it gives the surname and the place in the book.
- Wildcards `*` and `?` work. If the "Leiti sarnased nimed" block is also empty, the surname is really absent.
- **Results come in pages of 100 rows, and the first page did not say that more existed** (September 2026). Go to
  the last page before counting.
- **Spellings are indexed separately, without normalisation** (the opposite of AIS): `Näiddis` and `Naidis` are
  separate entries, and the archive's normalised form may give nothing. Query every variant and add the results.

### Data registers and the name-giving database

- German estate names are stored inverted: search `<Estate>hof, Alt-`, not `Alt-<Estate>hof`. Estate names repeat
  across counties; the register row shows estate, parish and county, so filter by all three.
- The name-giving database has separate fields for the spelling in the source and the normalised form; they are
  different searches. No wildcards. It settles where and when a family received its surname, and the etymology of
  the name.

### Reading Estonian and Livonian records

- **A double date in a Lutheran personal book is birth and baptism, not Julian and Gregorian.** The calendar gap is
  constant (12 days, 13 from 1 March 1900), but the gaps in one book ranged from none to many months, and entries of
  the 1920s were made when Estonia already used the new style. Take the first date as
  birth.
- Families in a Livonian revision list are numbered by their household in the previous revision. All members of
  one family can carry the same family number while living on several farms. Search by family number, not by farm.
- Before reading a personal-book volume frame by frame, check its start year: a volume that begins after the family
  left the estate can never hold them.
- Personal books often open with a register of estates and villages ("Register von Gebiethen und Dörfern":
  estate, farm, page). Start there. Livonian peasants had no surnames before 1826.
- Two women with the same name and close ages are separated by household composition, parish and confession, not
  by age: an age gap of several years can look like normal error while the children listed show two people.

### Ordering instead of reading yourself

The archive takes requests for copies of frames and for genealogical research; turnaround was a few weeks
(noted August 2026).

### DIGAR: Estonian newspapers

- Full-text search of Estonian newspapers with date filters and phrase search; 25 results per page. From November
  2026 the site shows a browser check, so the researcher searches it in their own browser.
- Useful genres: marriage intention notices ("Perekonnaseisu teateid", 1922-1944), lists of optants returning from
  Russia (1920s), official notices of the 1860s-1880s (passports, searches, auctions). Some surnames are also
  common nouns and flood the results.
- Geneanet also holds DIGAR's name index (see "Indexes on commercial sites" below).

### Other Estonian resources

- **August Nigol, "Eesti asundused ja asupaigad Venemaal", Tartu 1918** (in the 1918 spelling "Wenemaal"):
  `ida.aule.ee/raamatud/nigol1918_orig.pdf`, 95 pages, clean text layer. A list of the 313 Estonian settlements in
  the Russian Empire with volosts, distance to stations, households, year of foundation and origin of settlers.
  Portal of sources: `ida.aule.ee`.
- **kalmistud.ee cemetery register**: search with the site's form; a result list shown without your filter applied
  is not "no records" (November 2026).

### Never existed

`geni.ee`, `nimi.ee`, `saaga.ee` (not the archive's service; the archive's Saaga is under `ra.ee`), `rahvusarhiiv.ra.ee`, `isik.ra.ee`,
`ra.ee/erakonnad`. These names come up in generated text; do not cite them.

## Latvia

### Overview

| site | what it holds | reach | notes |
|---|---|---|---|
| Raduraksti `raduraksti.arhivi.lv` (LVVA) | Lutheran and other church books, revision lists, 1897 census | catalogue: open page; images: own browser (free registration) | no search by personal name |
| Place-name register `vietvardi.lgia.gov.lv` | all Latvian place names, including single farms | open page | |
| `ciltskoki.lv` | family trees | own browser | |

### Raduraksti

- The catalogue is open without login, with the shelf mark of each file ("<fond>. fonds <opis>. uzskaites
  saraksta <file>. lieta"). Images need a free account; the researcher registers and views them in the browser
  (September 2026).
- The catalogue is organised by collection: church books, revision lists (for about 1,600 estates), the 1897
  census by volost. Its search covers collection titles only, never personal names: browse by parish, year and
  section.
- **Frame numbering has gaps**: a file can jump from frame 1 to frame 5. A gap is not a lost page.
- **The portal catalogue is incomplete.** If a file you expect is missing, ask the archive before concluding that
  the book does not survive.
- **Registers after 1901 were kept on printed Russian forms**; that is the official copy.
- Catalogue cards sometimes give the wrong language of a book.
- The old image domain `img1.lvva-raduraksti.lv` returns **410 Gone** (September 2026). Links to it in exported
  trees are dead; the old link still carries the fond, inventory and file numbers, so the shelf mark can still be
  read from it.
- **1834 revision lists**: the cross-reference "aus P. N" means page or household N of part A of the same book,
  "P.B N" part B; it does not point to the previous revision. Within one book the sheet number differed from the
  frame number by a constant offset; check that offset for each book.
- **1897 census**: one file can cover a whole county, and it may not hold every enumeration district of a volost.
  Use the volost header bands ("Pagasts/Волость") to tell "file missing" from "household missing".
- An earlier revision (1811, 1816, 1826) for an estate may be absent from the portal altogether; then only LVVA in
  Riga can settle it, by letter or in person.

### Reading Latvian church books

- Handwriting traps: a "4" with an open loop reads as "7"; a looped capital "F" can be read as "A". Check a single
  doubtful reading against the same scribe's letters on the same page.
- German and Latvian place names do not map by sound: a German name that sounds like one Latvian parish may belong
  to another. A place gazetteer is the judge of a place name, not the ear.
- Parishes and volosts were split and renamed after 1918. A farm that a family tree places in a parish created in
  the 1920s is recorded in the books of the older parish it was split from.
- Farm names in trees may be unattested or mangled. The place-name register settles it: it gives name, type
  (`viensēta` = single farm), parish, municipality, status and coordinates. A farm name written in Russian in a
  family document usually corresponds to `<Name> mājas` ("the <Name> houses", e.g. the Paraugi farm). The register
  can also show that a remembered farm name exists nowhere in Latvia.

### Trees and exports from Familio

- Familio exports can carry Raduraksti frame references in a note field; the old image links are dead (410), but
  the shelf mark is recoverable (see above). Open the frame yourself before rejecting someone else's reference.
- For the date-qualifier observation in Familio GEDCOM see `genealogy-services.md`.

## Indexes on commercial sites

- **FamilySearch** holds indexes such as "Latvia BMD 1854-1909", "Latvia Census 1854-1897" (Raduraksti material
  with a name search; coverage for a given parish can stop decades before 1909) and "Estonia, Census, Tax and House Lists"
  (Saaga revision lists). It needs the researcher's own login.
- **Geneanet** carries these FamilySearch index collections and the DIGAR name index; it works in the researcher's own
  browser, with full record cards for Premium subscribers only. The search form does not accept Cyrillic.
- **MyHeritage** had no Latvian church-book index in September 2026.
- Other people's trees are working notes, not evidence. Before counting one as an independent confirmation, open
  its sources tab: a tree citing "Geni World Family Tree" may be your own data come back through third hands.

## Lessons for the region

- A zero from an index is a zero only after a control: the similar-names block (nimreg), result rows (AIS), the
  last page of the results (nimreg), every spelling variant (nimreg, DIGAR).
- AIS normalises spellings; nimreg and DIGAR do not. Use the normalised form in AIS and all source forms in the
  others.
