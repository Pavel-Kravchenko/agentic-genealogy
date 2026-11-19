# Repression databases

Databases of victims of Soviet political repression: people shot, imprisoned, exiled and dispossessed as
"kulaks", with their rehabilitation records. Observed from August to November 2026. How to read the reach
classes and the three outcomes: `README.md`. The examples are composed illustrations; the patterns come from
real work, the particulars do not.

## Summary

| site | what it holds | reach | block signature | notes |
|---|---|---|---|---|
| «Открытый список» ("Open List"), `ru.openlist.wiki`; Ukrainian section `ua.openlist.wiki` | 3.35 million record forms of victims | open page (Aug 2026) | neither «Найдено N» nor the not-found block: a challenge page, much smaller than a result page | |
| sinodik.ru (Butovo memorial centre) | 20,761 people shot at the Butovo firing range, with execution orders by day | open page (Aug 2026) | not recorded | more exact on execution dates than «Открытый список» |
| «Бессмертный барак» ("Immortal Barrack"), `bessmertnybarak.com` | 2,803,862 names; books of memory | open page (Aug 2026) | not recorded | a very small page is not proof either way; confirm in a browser |
| «Книга памяти Рязанской области», `memoryazan.ru` | dispossessed families and people convicted under article 58, Ryazan oblast | open page (Aug 2026) | not recorded | searches by name only |
| «Рязанский мартиролог», `stopgulag.org` | victims of repression, Ryazan region | open page (Aug 2026) | not recorded | searches by village name |
| `visz.nlr.ru` | book of memory of victims of repression, Leningrad and Kalinin oblasts | open page (Sep 2026) | not recorded | search by name |
| «Реабілітовані історією», `reabit.org.ua/nbr/` | 371,663 Ukrainian records | open page (Aug-Sep 2026) | none seen | |
| «Книга Пам'яті України», `memory-book.ua` | 1,008,363 names | open page (Aug and Nov 2026) | page without the result block (a silent false zero) | |
| ГДА СБУ (archive of the Security Service of Ukraine) | case files | human only | - | written request only |
| Polish lists: `indeksrepresjonowanych.pl`, `kresy-siberia.org`, `policjapanstwowa.pl` | Polish citizens deported in 1940-1941, camp prisoners, police officers shot in 1940 | open page (Sep 2026) | not recorded | see below |

## «Открытый список» - `ru.openlist.wiki`

**What it holds.** 3.35 million record forms (формуляры) of victims of political repression, built on
published books of memory and archive lists. For ГА РФ (State Archive of the Russian Federation) it is in effect
the inventory of fond 10035 (77,353 cards). The Ukrainian section is `ua.openlist.wiki`; `uk.openlist.wiki` has
never existed. The site is a MediaWiki; use the site's search page (Special:OlSearch).

**Zero signature.** The not-found block, with a hint on how to write the query. **Result signature.** The
caption «Найдено N». **Block signature.** Neither of the two: a challenge page, much smaller than a result page.

**Access.** Use the site's own search page and article pages as a visitor, one request at a time; stop at the
first challenge page (August 2026).

**How to search it.**

- **Search by case number with its letter and without the archive prefix.** «ГА РФ. Д. П-<D>» returns 0,
  «П-<D>» finds the case. A case-number search can restore a whole group case, but **it does not guarantee
  completeness**: some numbers are not indexed. Repeat with place of birth and place of residence.
- **Search both place of birth and place of residence.** For dispossessed peasants the place of birth is often
  empty.
- **The "body" field is the biography**, not the arresting body. There is no field for where and by whom the
  person was arrested; the only slice by authority is the sentencing body. **The filter by arrest date did not
  work (August 2026)**: values were ignored. Check all three arrest slots of a form.
- **Wildcards.** The evidence was contradictory, so test on the spot. Established: `*` must not be inside
  quotes. «"Примеров *"» does not run at all, «Примеров *» returns forms, and the site itself suggests the form
  «"Примеров"*».

**Traps.**

- **Place fields are damaged by OCR**: words broken by stray hyphens and misread letters. One faceted query by
  a village name is never exhaustive.
- **Execution dates in group cases can be inexact.** The form can give the whole group the date of the main
  batch, while the executions ran over several days. Check on sinodik.ru.
- "Presumed relatives" on a page are a guess of the site's engine, not a document.

## sinodik.ru - database of the Butovo memorial centre

20,761 names of people shot at the Butovo firing range near Moscow: cards of the executed and **execution orders
by day**. No login, no captcha (August 2026).

- The site's own search form finds a person; a card links to the day, and all people of one day are on one
  page.
- **More exact than «Открытый список» on execution dates**: a dispute between two dates in a group case can be
  settled here.
- **Spelling trap**: a surname spelled with ы gave records and the same surname with и gave zero (in the
  pattern of Прымеров against Примеров). Try both vowels.
- `martyr.ru` is the site of the parish church of the New Martyrs at Butovo, not of the memorial centre. Its
  lists of the executed are an embedded frame from sinodik.ru. It is useful for reference and contacts.

## «Бессмертный барак» - `bessmertnybarak.com`

2,803,862 names; books of memory, including «Москва, Бутовский полигон» (20,458 records, 1,023 pages) and the
investigation files of the KGB directorate for Moscow and Moscow oblast (about 64,238).

- Search with the site's own form at the `.com` address; the old `.ru` address redirects there (August 2026).
- **A very small page is not proof either way**: confirm in a browser.
- There are no personal pages, only a line in a book. In the alphabetical Butovo book, use the
  alphabetical order to go to the right page.

## Regional books of memory

Many oblasts have their own book of memory of victims of repression; look for the oblast's own title. Examples
and one reference work:

| source | what it holds | how it is searched (Aug 2026) | traps |
|---|---|---|---|
| «Книга памяти Рязанской области», `memoryazan.ru` | **dispossessed peasants, in families, with degrees of kinship**, and people convicted under article 58 | search by surname | searches by name only, not by village |
| «Рязанский мартиролог», `stopgulag.org` | victims of repression of the Ryazan region | one search box over all fields | **searches by village name**; «Ничего не найдено» is printed as text, so the zero is true |
| `visz.nlr.ru` (National Library of Russia) | book of memory of victims of repression, Leningrad and Kalinin oblasts | search by name (Sep 2026) | |
| «Система ИТЛ в СССР» (reference book on the Gulag camps, 1998) | camps, their dates and subordination, with archive notes and the number of personal files | the printed book, through a library | |

## Ukrainian databases

- **«Реабілітовані історією»**, `reabit.org.ua/nbr/`: 371,663 records. No login, no block seen (August 2026).
  Dispossessed and deported peasants without a sentence are mostly not in it.
- **«Книга Пам'яті України»**, `memory-book.ua`: 1,008,363 names, searchable by name and oblast. **A page
  without the result block is not a zero**: it means the search did not run; search again with the site's own
  search button (August 2026).
- **ГДА СБУ** (archive of the Security Service of Ukraine): there is no online index by oblast; only a written
  request.
- For sentences passed on Ukrainian territory, the archive of the Ministry of Internal Affairs of Ukraine (ГДА
  МВС України) is the next address for a written request. More Ukrainian sources: `ukraine.md`.

## Polish databases

| source | what it holds | reach (Sep 2026) |
|---|---|---|
| `indeksrepresjonowanych.pl` (Institute of National Remembrance and the KARTA Centre) | camp prisoners and people deported in 1940-1941, with IPN reference codes | open page, through the search form |
| `kresy-siberia.org`, Wall of Tribute | people deported in 1940-1941 | open page |
| `policjapanstwowa.pl`, «Księga Cmentarna» for Katyn, Kharkiv and Mednoye (PDF), lists of police victims by letter | biographies of all 6,288 prisoners of the Ostashkov camp with their NKVD list number | open page; the PDF text is in the CP1250 encoding |

More on Polish archives: `poland-lithuania-czechia.md`.

## Where the files are not

- **A prisoner's personal file is not in ГА РФ.** The Gulag fond there (Р-9414) holds orders, reports and
  statistics. Personal files and registration cards are in the **information centres of the regional
  directorates of the Ministry of Internal Affairs (ИЦ УМВД) where the camp was located**. Such a centre may
  take requests only through the web form on the regional ministry site, and a negative reply may give no
  article, term or dates.

## Historical facts that keep misleading searches

- **A death certificate issued to relatives in the 1950s may not give the true date of death.** Certificates
  of that period for people shot in 1937-1938 are reported to carry an invented date and cause (not verified
  here against the instruction itself). Expect two dates for the same death, and keep both.
- A published order may postdate an arrest: check dates before attributing a case to an operation.
