# Telling a block from a true zero

The main rule of this method: on almost every site, being refused looks like an honest empty result. A
research log can easily say "EMPTY" where the search was never let in, and the reverse happens too, an
honest zero taken for a block. No negative result counts until you have checked that the search ran.

The examples are composed illustrations; the patterns come from real work, the particulars do not. Site
observations are from 2026, with the month where it matters. Sites change; recheck the signature before
relying on it.

## 1. Three outcomes, not two

Every request ends in one of three states:

| outcome | what it means | how to record it |
|---|---|---|
| result | the site ran the search and returned records | the records, with the query |
| true zero | the site ran the search and found nothing | `ZERO` + site + exact query + date + corpus searched |
| block | the site did not run the search (captcha, ban, throttling, login wall, broken certificate, intercepted form, script-rendered page) | `BLOCKED` + site + signature seen + date |

A third kind of failure looks like a result: the site ignores a parameter and returns everything or something
unrelated. Treat it as "not run" as well (section 3).

A block is a technical state. It is answered by stopping, by trying again on another day, or by a person in
a browser, never by an archive request, and it does not belong in the list of genuine dead ends.

## 2. Check the length and type of the body, not only the status code

Most blocks come back as HTTP 200. The status code alone tells you almost nothing. For every response, record
and check:

- the status code;
- the body length in bytes;
- the content type and, for HTML, a marker that only a real result page or a real "nothing found" page
  carries;
- for a downloaded file, its format signature (section 4).

A page whose results are drawn by a script can also mislead in the other direction: a plain request for such
a search page shows an empty shell, which is neither a zero nor a block. Search it in a browser.

## 3. Reach and refusal signatures per site

Reach classes: `open page` (a public page reached without a login. An agent reads it only if the site's terms of use and robots
rules allow automated reading, one request at a time; otherwise treat the site as `own browser`), `own browser`
(used by the researcher personally in a browser: it needs a login or a subscription, or it does not serve
automated requests), `human only` (captcha, payment, letter, visit), `dead`. Signatures are generic: what a refusal looks like, so that it is not mistaken for "nothing found".

| site | what it holds | reach | refusal looks like | "nothing found" looks like |
|---|---|---|---|---|
| Services behind a login or a subscription (commercial genealogy services, image viewers of archives, Yandex Archive since October 2026) | trees, record collections, register images | own browser | without the login: a login form, an empty page shell or a very small refusal page, often with status 200. Judge by what the page is, not by the code | none: without the login there is no zero |
| «Открытый список» (Open List, Soviet repression victims) | biographies | open page | a protection challenge page instead of the article | the site's "not found" block with the search-form hint; a result shows «Найдено N» («Знайдено N» in the Ukrainian section). The wiki's own full-text search answers "no form found" to any syntax, which is not an answer of the database |
| ОБД «Мемориал» (WWII losses) | loss records, scans | own browser | a "search in progress" placeholder instead of a result | the site's empty result. In late August 2026 it gave zeros for records that existed: zeros from such days are void. Latin script is not indexed |
| «Память народа» (WWII awards and service) | award sheets, service records | own browser | a 401, or a 403 page «Проверка безопасности»; did not answer from the project's network (September and November 2026) | the site's own empty result page |
| «Дорога памяти» (photos and cards of WWII soldiers) | summary cards | own browser | a result list that does not depend on the query (the whole gallery): the query was not applied | an empty list |
| `gwar.mil.ru` (WWI records portal) | cards, images | own browser | a query whose filter was not applied returns the whole corpus, which looks like a result | an empty list |
| Yaroslavl oblast portal `af.yar-archives.ru` | catalogue, images | own browser | a refusal page instead of the catalogue | `Ничего не найдено` on the search page |
| `memory-book.ua` (Ukrainian WWII memory book) | memory book entries | open page | a page with no result block at all | an explicit "not found" |
| «Бессмертный барак» (repression victims) | biographies | open page | a very small page is not proof either way; confirm in a browser | the site's "not found"; result lists of frequent surnames did not page through completely |
| Jagiellonian Digital Library | Polish gazettes, prints | open page | a connection cut before the file arrives: the file was not read | not recorded |
| `szukajwarchiwach.gov.pl` (Polish State Archives) | catalogue, scans | own browser | a protection page (Sep 2026) | not recorded |
| `metryki.genbaza.pl` | Polish civil register duplicates | own browser (free registration) | a placeholder page without login | not recorded |
| `archyvai.lt` (Lithuanian archives) | catalogue | own browser | 403 | a missing fond number means "not established", not "absent" |
| `lursoft.lv` | Latvian address catalogue | own browser | 403 | not recorded |
| `pakalpojumi.arhivi.gov.lv`, `eresursi.arhivi.gov.lv`, `lenww2.ru`, `melnaisvanags.lv`, `kartes.lu.lv` | Latvian archive services, a WWII Leningrad database, 1930s maps | dead (2026) | no connection or a broken certificate | "not checked", never "absent" |

Agent tools have their own false zeros. The harness's web search tool returns silently empty results once
its budget for the session is used up, so an empty search there is not "nothing exists". A fetch tool can
mis-decode pages in legacy encodings (cp1251): read the raw page for addresses, shelf marks and numbers.

## 4. A downloaded file is proven by its format signature

HTTP 200 and a plausible size prove nothing about a file. A JPEG starts with the bytes `FF D8 FF` and ends
with `FF D9`; a PDF starts with `%PDF`. Check both ends of every image you save.

An example: an HTML error page was saved under a `.jpg` name, and several such "images" had the same size and
the same checksum. Identical size and identical checksum across different records is a second signature of a
fake. In the same way an image viewer can return a login form with status 200: decide by the type of the
body, not by the code.

## 5. Pacing

One site, one agent, one request at a time, slowly. Several agents on one domain multiply the request rate
without anybody seeing the total. Stop at the first refusal and never retry in a loop.

## 6. What to do on a block

1. Stop at the first block signature. Do not retry in a loop.
2. Record it as `BLOCKED`, with the signature you saw (code, length, marker text) and the date. Never record it
   as `ZERO`, and never let it reach a summary as "not found".
3. Hand the site to a person. Sites that need a login or show a captcha are used by the researcher
   personally, in their own browser, under their own account. Whether and when to return to a site is the
   researcher's decision.
4. If the site is down (no connection, 5xx, broken certificate), mark the question "not checked", not
   "absent", and try again on another day.
5. Recheck old zeros against the list of known false-zero periods and signatures before citing them.

## 7. A negative result is only as strong as the volume actually read

- Name the corpus and the record genre in every negative statement (see
  [evidence-rules.md](evidence-rules.md), section 12).
- A zero from a phrase query, a prefix query or a query in the wrong spelling is not a zero for the person
  (see [reading-indexes-and-ocr.md](reading-indexes-and-ocr.md)).
- A zero from machine search over weak OCR is weaker than it looks: in a check against a page-by-page
  reading, it missed files in some inventories.
- A zero from a full-text index that does not index the fields you care about is no zero at all: the ОБД
  full-text search does not index the form fields, which appear only on the scan.
- A zero obtained under a wrong place name, a wrong district or a name the place did not yet have is void.
  The four repeatable reasons that spoil early zeros are a wrong volost name, a wrong uezd, false zeros of a
  database, and a block that looked like a zero.
