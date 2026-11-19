# War and military-loss databases

Databases of soldiers, losses, awards, prisoners of war and burials for the First World War, the Winter War
(1939-1940) and the Second World War, as observed from August to November 2026. How to read the reach classes
and the three outcomes: `README.md`. Most of the large databases below are run by the Russian Ministry of
Defence; this guide describes only what a visitor sees on them and the official routes. Sites of ministries of
defence are classed `own browser`: the researcher searches them personally, in their own browser. The examples are
composed illustrations; the patterns come from real work, the particulars do not.

## Summary

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| ОБД «Мемориал» (Generalised Data Bank "Memorial"), `obd-memorial.ru` | Red Army loss reports, burial records, books of memory, search questionnaires, repatriation files | own browser (Aug-Nov 2026) | placeholder «Идет поиск» ("search in progress") that never resolves | false zeros in late Aug 2026; no Latin script |
| «Подвиг народа» ("Feat of the People"), `podvignaroda.ru` | award sheets and award card files | own browser (Aug 2026) | a 403 page | card files have no scans here |
| «Память народа» ("Memory of the People"), `pamyat-naroda.ru` | everything of the two above plus unit documents (war diaries), conscription books | own browser | 401, or a 403 page «Проверка безопасности» ("security check") | did not answer from the project's network (September and November 2026); more records than ОБД |
| `poisk.re` | search over card data from the Central Archive of the Ministry of Defence (ЦАМО), captured German prisoner cards | open page (Sep-Nov 2026) | a "too many requests" page (429) is a refusal: stop | three-word queries give a false zero |
| «Дорога памяти» ("Road of Memory"), `1418museum.ru` | summary cards with dates, places and portraits | own browser (Sep-Nov 2026) | not a block: if the search term is not applied, the site shows the whole gallery | `foto.pamyat-naroda.ru` redirects here |
| gwar.mil.ru, «Памяти героев Великой войны 1914-1918» | 41.5 million First World War documents of the Russian State Military History Archive | own browser (Aug-Nov 2026) | not recorded | |
| ВИПЦ, `v-ipc.ru` | combined database of 41 sources: books of memory, Polish and Belarusian burial lists, ОБД burials | open page (Nov 2026) | not recorded | search by place of birth works |
| «Саксонские мемориалы» (Saxon Memorials Foundation), `ru.stsg.de` | Soviet prisoners of war in Saxony, including the Zeithain camp | open page (Nov 2026) | not recorded | Cyrillic and Latin both work |
| `pobediteli.ru` | register of Second World War veterans alive in 2005, by region and letter | open page (Aug and Nov 2026) | not recorded | |
| `moypolk.ru`, `polk.ru` | portals of relatives: stories, search requests, unawarded medals | open page (Nov 2026) | «Много запросов» ("too many requests") on `moypolk.ru` is a refusal: stop | |
| `memory.mil.by`, `partizany.by`, `memory.grsu.by` | Belarusian databases of the fallen, burials and partisans | own browser (Nov 2026) | not recorded | `memory.mil.by` is a site of the Belarusian Ministry of Defence; `memory.grsu.by` is small |
| `winterwar.karelia.ru` | losses of the Winter War | open page (Nov 2026) | not recorded | substring search |

## ОБД «Мемориал» - `obd-memorial.ru`

**What it holds.** Red Army losses (unit reports, military registration office reports), burial records,
published books of memory, search questionnaires filled in by relatives (анкеты розыска), and repatriation files
from the State Archive of the Russian Federation (ГА РФ).

**What it does not index.**

- **Latin script** is not indexed at all (August 2026).
- **The fields of a search questionnaire** are not in the full text: the field post address from the last
  letter, statements of fellow soldiers and the circumstances of death are visible **only on the scan**. Always
  open the scan.
- **The ГА РФ and РГВА (Russian State Military Archive) layers** are not in the full text at all; their cards
  are not found by the site's search.
- **Award files** of ЦАМО are not shown by ОБД (November 2026); look in «Подвиг народа».

**How a visitor searches it.** The search form is one full-text field; the separate fields (surname, given name
and so on) were removed (August 2026). The result appears after a short wait: the page first shows the
placeholder «Идет поиск». If the placeholder never turns into a result, the search did not run.

**Zero signature.** An empty result list while a control query in the same sitting returns records. **Block
signature.** The placeholder «Идет поиск» that never resolves.

**Traps.**

- **False zeros in late August 2026.** Queries that had returned records one day returned none the next; all
  zeros of those days were void.
- **Abbreviated names in the record are not found by the full name** (November 2026). A record entered as
  "Primerov Iv. Petr." is not found by «Примеров Иван Петрович». A zero counts only together with the slices
  "surname + given name" and "surname + place".
- **One bare surname is not exhaustive.** A bare surname query can return a few dozen records and still miss
  cards of the person sought that turn up under "surname + oblast" and "surname + village". Build the corpus
  from the union of slices.
- **Neighbouring cards in an alphabetical ЦАМО file are not neighbours in life**: those files are bound in
  alphabetical order from all over the USSR. In the conscription books of district military registration
  offices, however, the neighbours on a sheet are people from the same village.

## «Подвиг народа» - `podvignaroda.ru`

**What it holds.** Award sheets with their scans, and award card files (the anniversary card file and the
award card file).

**What it does not index.** The cards of the two card files showed no scans on this site (checked on a few
records, August 2026). Look for those scans on «Память народа».

**How a visitor searches it.** The site's own search form, a single full-text field; no captcha (August 2026).
A result gives surname, given name, patronymic, date of birth, place of conscription, award, and the fond,
inventory and file.

## «Память народа» - `pamyat-naroda.ru`

**What it holds.** The losses of ОБД, the awards of «Подвиг народа», and in addition unit documents (war diaries,
orders, maps) and conscription books; it **returned more than ОБД** on the same people. Conscription books can
give a date and place of call-up that no other source has.

**Reach.** Own browser. It did not answer from the project's network (September and November 2026; a 401, or a 403 page
«Проверка безопасности»). Where the site is available to you, use it in your own browser under its terms:
search by name and save the card and the scan of each hit. Its unit-documents section can be searched by fond and inventory
number in the site's own form. The official route for ЦАМО records is a written request to ЦАМО
(`russia-regional-archives.md`).

## `poisk.re`

Search over card data from ЦАМО. Its search also covers captured German prisoner-of-war cards (stalag, prisoner
number, date and place of capture, ЦАМО shelf mark; observed September-November 2026).

- **False zero on a three-word name** (September 2026): surname + given name + patronymic returned "not found"
  for a record that the two-word query surname + given name found. Search with two words, then filter by
  patronymic.
- Place and year cannot be part of the query. For a common surname, query surname + a rare patronymic.
- Long result lists are truncated: narrow the query.
- A "too many requests" page (429) is a refusal: stop (November 2026).

## «Дорога памяти» - `1418museum.ru`

`foto.pamyat-naroda.ru` redirects to `1418museum.ru`. If the search term is not applied, the site **shows the
whole gallery**: a false result that looks like a long list of hits (August 2026). Use the site's own search box. Cards are summaries assembled from several documents and
carry no shelf marks; they can carry a portrait photograph and an award (November 2026).

## gwar.mil.ru - «Памяти героев Великой войны 1914-1918»

**What it holds.** 41.5 million documents of the Russian State Military History Archive (РГВИА) on the First
World War, in 11 card files: losses, hospitals, burials, captivity, awards, service records. No login; as a site
of the Ministry of Defence it is used by the researcher in their own browser.

**Zero signature.** An empty result list for a search that ran.

**Traps.**

- **The same place is recorded in different forms.** Search the place in every field the search form offers,
  then merge the lists.
- **Matching is fuzzy.** A search for one volost name also returned other volosts with similar names. Exact
  matches come first, so the end of the exact block shows whether the slice is exhausted.
- **A phrase query loses about half the corpus** (September 2026). Search one word, filter the results, and
  draw no negative conclusion from a phrase.
- **One person appears under several spellings.** In one volost a noticeable share of cards were persons already
  counted under another spelling.
- **Some cards carry a numeric village code instead of a name.** The codes are not explained on the site. They
  can be decoded by matching the people under a code against the village-by-village name lists of printed
  district books of memory («Памяць» volumes, see `belarus.md`). Confirm a decoded village code on several people
  before using it.
- The card gives only volost and uezd; the scan of a hospital admission notice adds age, marital status,
  occupation before the war and place of residence. Open the scan before identifying a person.

**Official route.** Questions the database does not answer go to РГВИА as a written request.

## Second World War: other databases

| site | what it holds | how it is searched (observed) | notes |
|---|---|---|---|
| ВИПЦ, `v-ipc.ru` | combined base of 41 sources: books of memory (for example Ulyanovsk and Leningrad oblasts), Polish and Belarusian burial lists, ОБД burials | the site's search form (Nov 2026) | place of birth works as a search key; not every region's books are included, so check its list of sources; its cemetery search finds places, not people |
| «Саксонские мемориалы», `ru.stsg.de` | Soviet prisoners of war, Zeithain camp | search by surname, 50 records per page (Nov 2026) | Cyrillic and Latin |
| `soldat.ru` reference pages | field post numbers 1943-1945, hospital locations | plain pages (Nov 2026) | field post stations of 1941 are not there |
| `rkkawwii.ru` | composition and combat path of divisions | plain pages (Nov 2026) | |
| `pobediteli.ru` | veterans alive in 2005 | by region and letter | |
| `moypolk.ru` | relatives' portal | a relatives' portal: read it page by page | |
| `polk.ru` | search requests and medals waiting for their owners | plain pages | |
| `sgvavia.ru` forum | aviation losses, researchers' threads | guest search works (Nov 2026) | |
| `memory.mil.by`, `partizany.by`, `memory.grsu.by` | Belarusian fallen and burials, partisans | the sites' own search forms, in the researcher's own browser (Nov 2026) | see `belarus.md` |
| «Имена из солдатских медальонов», vols. 1-10 | names read from soldiers' identity capsules | the published volumes (Nov 2026) | |

Further databases from the same navigator that answered in November 2026: `brest-fortress.by`,
`batyrlarga-tagzym.kz`, `baza.onagradah.ru` (awards), `polkrf.ru`, `9may.my1.ru`, `warheroes.ru`,
`rgaspi.info` (partisans), `krdar.kaisa.ru` (Caucasus), `mosopolchenie.ru` (Moscow people's militia),
`cgako.ru`, `sar-archive.ru`, `iremember.ru`, and databases of evacuees of Chelyabinsk, the Komi-Permyak
district and Novosibirsk.

## Prisoners of war

| source | what it holds | notes |
|---|---|---|
| `poisk.re` | captured German cards of Soviet prisoners | see above |
| `ru.stsg.de` | prisoners in Saxony | see above |
| `kzlager.net` | camp prisoners | |
| published books of the dead of Buchenwald, Dora, Mauthausen, Neuengamme, Dachau, Stukenbrock | camp death registers | |
| `krigsgraver.no` | war graves in Norway | |
| `digitalarkivet.no` | Norwegian archives: Soviet prisoner files | the catalogue opens without login, but the files are "Browse scans / Not searchable": a name is found only by reading the scans (Sep 2026) |
| `soldat.ru` | prisoner list | |
| `dbases.archive74.ru` | prisoners; district registration offices | |
| `permgaspi.ru` | prisoners | |

German holdings on Soviet prisoners: `germany.md`.

## Winter War (1939-1940)

- `winterwar.karelia.ru`: opens directly; search by substring (November 2026).
- Award decrees of 1940: six PDF files on `aroundspb.ru/awards_1940.html`; they give no year or place of birth.
- Kronos: an xlsx data set on Zenodo (record 12793574).
- `raatteentie.heninen.net`, `permgaspi.ru/db/finland`, `151sp.eu`: further lists of losses.
- These are all lists of the dead, the missing and the decorated. A man who came back without an award should
  not be in any of them, so a zero here says nothing about service.
- A written request to the Russian State Military Archive (РГВА) needs the district registration office and
  the unit number.

## The navigator «Найди предков. 1939-1945»

A published guide by E. Brozovskaya (update of April 2026) collects about 380 links to Second World War sources
by region and type.

**Did not answer from the project's network (November 2026):** `pamyat-naroda.ru`, `warsearch.ru`,
`goskatalog.ru`, `spbarchives.ru` with its subdomains, `vov.mos.ru`, `polk.mos.ru`, `victims.rusarchives.ru`,
`vbd-voenkor.ru`, `gato.tularegion.ru`, `kremnik.ru`, `22june.mil.ru`, `archive.mil.ru`, `bitva.kursk.ru`,
`slava-sibiryakam.ru`, `world-war.ru`, `yar-archives.ru`, `mari-plen.ru`, `tsdahou.archives.gov.ua`,
`martyrology.org.ua`. Where a site is available to you, use it in your own
browser under its terms; otherwise a written request (the official route for state archives), a library copy or
a visit.

**Search closed without login:** `forum.patriotcenter.ru`, `pressa-voiny.ru`. `prlib.ru` showed a browser check
(own browser); `prozhito.org` did not filter by text when tested (November 2026).

**Links from the navigator that no longer lead to the original resource (November 2026):** `obd-memorial-3.ru`
(domain expired), `tastorona.su` (no longer the institution's site, observed November 2026), `kolomnapomnit.ru`
(parked), `лицапобеды.рус` (hosting panel), `poisk-pobeda.ru` (no longer the institution's site, observed November
2026), `ponyrimuseum.ucoz.ru` (did not answer, HTTP 404, November 2026). Do not open or cite them. The full list:
`dead-and-moved.md`.
