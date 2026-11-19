# Poland, Lithuania and Czechia: archives, digital libraries and databases

Resources for ancestors from the western provinces of the Russian Empire (Congress Poland, the Lithuanian and
Belarusian lands under Polish rule 1921-1939) and for Czech and Slovak links (legionnaires, Prague). Statements about
site behaviour are observations with their month. The examples are composed illustrations; the patterns come from
real work, the particulars do not. Reach classes: **open page** (a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser`), **own browser** (used by the researcher personally in a browser: login, registration,
subscription, or no automated requests served, for example a browser check), **human only**, **dead**; see
[README.md](README.md).

## Poland

### Overview

| site | what it holds | reach | notes |
|---|---|---|---|
| Słownik geograficzny Królestwa Polskiego (SGKP) `dir.icm.edu.pl` | geographical dictionary, 16 volumes, 1880-1902: every village, estate and gmina of the former Polish-Lithuanian lands, with full OCR text | open page | the main gazetteer for Grodno province too |
| Jagiellonian Digital Library (JBC) `jbc.bj.uj.edu.pl` | official gazettes and press: `Obwieszczenia Publiczne` 1917-1939, `Poleski Dziennik Wojewódzki` 1922-1939, `Monitor Polski` | open page (free, no registration) | OCR splits words |
| Federation of Polish Digital Libraries (FBC) `fbc.pionier.net.pl` | metadata of all Polish digital libraries | open page | metadata only |
| CRISPA (Warsaw University Library) `crispa.uw.edu.pl` | press absent from JBC (e.g. `Tygodnik Handlowy`) | open page | full-text search closed |
| `nazwiska-polskie.pl` | surname counts from the PESEL register | open page | needs a control |
| `policjapanstwowa.pl` | "Księga Cmentarna" for Katyń, Kharkiv and Mednoye (PDF) and lists of police victims | open page | PDFs in CP1250 |
| `indeksrepresjonowanych.pl` (IPN / KARTA) | camp prisoners and people deported 1940-1941, with IPN shelf marks | open page (search form) | |
| `kresy-siberia.org` Wall of Tribute | people deported 1940-1941 | open page | |
| `metryki.genbaza.pl` | images of the civil duplicates of church registers held by the National Archive in Kraków | own browser (free registration) | without login a placeholder image ("brick") |
| `szukajwarchiwach.gov.pl` | catalogue and scans of Polish state archives | own browser (browser check) | |
| `genealodzy.pl` (Geneteka) | name indexes by parish | own browser (browser check, September 2026) | an empty parish is not a zero |
| `bcul.lib.uni.lodz.pl` | Łódź University digital library | own browser | did not answer from the project's network (2026); where the site is available to you, use it in your own browser under its terms |

### Słownik geograficzny Królestwa Polskiego

- The site's full-text search covers all 16 volumes at once, and a page's OCR text can be opened from the result.
- Searching all volumes is the way to prove a negative. A village name that occurs exactly once in the whole
  dictionary settles both "there were two villages of this name" and "the catalogue misread it".
- Entries give the kind of place (wś = village), powiat, gmina, distance to the powiat town and land area; that is
  often the only printed link between a village and its volost.

### JBC, FBC and CRISPA

- JBC gives an issue as a PDF with OCR, read with `pdftotext -layout`. The voivodeship gazettes of 1938-1939 carry
  land lists by gmina, household by household with plot areas.
- **JBC's OCR splits words with spaces** ("P r i m e r o w"), so a plain grep returns a false zero. Use a regular
  expression with `[\s\-\xad]*` between every pair of letters.
- FBC searches metadata, not full text; use it to find issues that the full-text search of one library misses.
- CRISPA: use its own viewer.

### Surname counts: nazwiska-polskie.pl

- A surname page that exists means the surname is in the PESEL register; "not found" means it is not.
- **A control is required** before "not found" can be read: run two surnames known to exist first.

### Victims of 1939-1941 repressions

- **Księga Cmentarna** (Katyń, Kharkiv, Mednoye) PDFs from `policjapanstwowa.pl` use a CP1250 font, but `pdftotext`
  outputs CP1252: `³` stands for `ł`, `œ` for `ś`, `¿` for `ż`. Repair with
  `text.encode('cp1252').decode('cp1250')`. A biography line ending "L. <list>/<part> (<position>), <case>" means NKVD
  transport list number, part, position on the list, and NKVD case number; the dates of the lists are in the
  introduction of each volume.
- **Indeks Represjonowanych** cards give the position in the Księga Cmentarna and the IPN signature of the list
  (`IPN BU <...>`): a ready reference for a request to the IPN.
- `kresy-siberia.org` Wall of Tribute: people deported 1940-1941.

### Church and civil registers

- Lesser Poland (Małopolska) example: parish copies in the Kraków Curia archive end about 1889; civil duplicates of
  1810-1911 are in the National Archive in Kraków (one fond), with images on `metryki.genbaza.pl` (free registration;
  without login every image is a placeholder "brick").
- `szukajwarchiwach.gov.pl` is used by a person in a browser.
- An empty Geneteka index for a parish means the parish has not been indexed, not that it holds no record.

## Lithuania

- **LVIA** (Lithuanian State Historical Archives, Vilnius). The Orthodox diocese of Grodno was founded only in
  1900; before that, Grodno province parishes belonged to the Lithuanian consistory in Vilna, so the consistory's
  second copies of registers are expected in LVIA.
- **Fond 605** (Vilna, before 1900 Lithuanian, Orthodox consistory): its Grodno series stops in the 1860s, and some
  deaneries are absent altogether (2026). **Fond 634** holds Uniate records up to 1839.
- Catalogue at `archyvai.lt`; part of the registers is digitised and open at `epaveldas.lt`. Both are used by
  a person in a browser.

## Czechia

| site | what it holds | reach | notes |
|---|---|---|---|
| `csol.cz` (formerly legie100) | Czechoslovak legionnaires database of the Military History Institute (VÚA-VHA) | open page | the result list was shifted by one position against the cards (2026): confirm on the card |
| `digi.nacr.cz/prihlasky2/` | Prague police residence registrations (přihlášky) 1850-1914 | open page (search form) | diacritics are mandatory: a name typed without its háček finds nothing |
| `katalog.ahmp.cz` | Prague City Archives catalogue; house-right records are a fond inside it, not a separate database | open page | parish registers (matriky) by parish only |
| National Library `kramerius5.nkp.cz` | digitised periodicals (Kramerius) | open page | part of the periodicals is under a DNNT licence (restricted) |
| Moravian Library Kramerius | digitised periodicals | own browser | did not open in September 2026; recheck later |
