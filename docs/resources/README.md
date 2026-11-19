# How to read the resource guides

These guides list the online sources that a researcher of ancestors from the former Russian Empire and the
USSR meets most often: what each one holds, what it does not index, who can reach it, how its "nothing found"
differs from a refusal, and the traps in reading its results. They are field notes, not a catalogue: every
behaviour is dated, and any of them can change the next week.

The examples are composed illustrations; the patterns come from real work, the particulars do not.

## Reach classes

Each site carries one of four reach classes, or a dated note where it did not answer. The class says who can get an answer out of the site, not whether
the site is good.

| class | meaning | what to do |
|---|---|---|
| open page | a public page reached without a login. An agent reads it only if the site's terms of use and robots rules allow automated reading; otherwise treat the site as `own browser` | where the terms allow it, read it one request at a time, slowly, and stop at the first refusal |
| own browser | used by the researcher personally in a browser: it needs a login or a subscription, or it does not serve automated requests | the researcher uses it personally, in their own browser, as a normal user, and saves what they find |
| human only | the site needs a captcha, a payment, a reading room or a letter | write down exactly what the person should search for or ask, and hand it over |
| dead | the domain is gone, parked, or now serves somebody else's content | do not open or cite it; look for a copy in the Internet Archive |

Whether a site's terms of use allow automated reading is for the researcher to check before an agent reads it;
when in doubt, use the site in a browser.

A site can move between classes. Yandex Archive (see `full-text-archives.md`) was an open page until October
2026 and needs a login since then. Before relying on a class, run one control query whose answer you already know.

These guides describe only what a visitor sees and the official routes. They do not describe how to get past
a login, a captcha, a firewall, a geographic block or a paywall. Where a site needs a human, the guide says so
and says what the human can do there: a form, a written request, a visit.

## The three outcomes of a search (and the fourth)

A query to an online index has three possible outcomes, and they must be kept apart in every log:

1. **Result**: one or more records came back.
2. **True zero**: the site was reached, the search ran, and nothing matched.
3. **Block**: the site did not let the request through, or the search did not run.

The central lesson: **on most sites a block looks exactly like a true zero.** A refused request often comes
back as an ordinary-looking page with no record cards, an empty result list, a login form or a "search in
progress" placeholder. It is easy to write "nothing found" where the site simply refused, and the opposite
mistake happens too. So:

- Judge the page by what it contains: its size compared with a normal result page, and the presence of the
  element that the site prints only on a real empty result. Do not judge by the absence of cards alone.
- Each guide gives, per site, the **block signature** (what a refusal looks like) and the **zero signature**
  (what a real empty result looks like). A zero is counted only when the zero signature is present.
- Before counting zeros, run a **control query** with a name that must be in the index (a very common surname
  such as Иванов works on most Russian sites). If the control returns nothing, every zero of that session is
  void.
- A site can also return false zeros for reasons of its own. ОБД «Мемориал» returned nothing for queries that
  had returned records the day before (late August 2026); all zeros of those days had to be thrown away.

A fourth outcome showed up often enough to get its own label: **the search does not work** (a search term is
silently ignored, so the page shows the whole collection, or always the first page). Observed in November 2026
on sites listed in one published war-research navigator, it was a small but real share.

## An index covers one genre of document, not a person

"Not in the index" never means "not in the records". Every online index covers one kind of document from one
set of archive holdings: parish registers of one province, award sheets, loss reports, recruit lists. A
negative finding must name the index, the document genre and the corpus: "no Primerov in the indexed parish
registers of N uezd, 1850-1900", not "no Primerovs in N uezd". A family absent from the indexed parish
registers of a district can turn up in the recruit lists of the same district.

Three more rules follow from the same point:

- **Full text does not index the fields of a form.** On ОБД «Мемориал» the full-text search does not read the
  fields of a search questionnaire (the last field post address, the statements of fellow soldiers, the
  circumstances of death): only the scan shows them. Always open the scan, not only the card.
- **One query is never exhaustive.** Spelling variants, abbreviated given names, OCR damage in place names and
  fuzzy matching all lose records. Build the corpus from several slices (surname alone, surname + region,
  surname + village) and merge them.
- **A phrase can lose half the corpus.** On gwar.mil.ru a volost name searched as a phrase returned about half
  of what the same name returned as one word (observed September 2026). Query with one word and filter the
  results; draw no negative conclusion from a phrase query.

## Dating of observations

Every statement about a site is dated: "observed <month> 2026", or "2026" where the month was not recorded. The observations were made between
August and November 2026. Where two observations disagree, the later one wins and the guide says what changed. A
behaviour without a date in the guide should be read as "observed at least once in 2026, not rechecked".

Pacing: one site at a time, one request at a time, slowly; stop at the first refusal and never retry in a loop.
A site that did not answer from the project's network is reached through the official route the guide names:
where the site is available to you, use it in your own browser under its terms; otherwise a written request, a
library copy, a visit, or a person in the country who uses the archive's services under its rules. Do not use a
VPN or a proxy to get round a block.

## Harness traps that look like site behaviour

- Web search through an agent harness can have a per-session limit shared by parallel agents; when it runs
  out, an agent loses search without an error it can understand (observed 2026).
- A fetch tool that converts pages to text gave two wrong postal addresses of an archive from a page in the
  windows-1251 encoding. Read addresses, shelf marks and numbers from the page itself, decoded explicitly.
- A web search engine answered a query for a rare surname with ten results about unrelated software: an empty
  search can come back as confident noise.
- Save every page you read to disk at once, for your own research; do not republish saved pages. Re-reading a
  saved page is free; asking the site again is not.

## The guides

| file | content |
|---|---|
| `full-text-archives.md` | full-text bases of digitised documents: Yandex Archive, ГПИБ (State Public Historical Library), НЭБ (National Electronic Library), Internet Archive volumes, digitised newspapers |
| `war-and-losses.md` | First and Second World War databases: ОБД «Мемориал», «Подвиг народа», «Память народа», gwar.mil.ru, prisoner-of-war and burial databases, Winter War sources |
| `repression.md` | databases of victims of political repression: «Открытый список», sinodik.ru, «Бессмертный барак», regional books of memory, Ukrainian and Polish lists |
| `russia-regional-archives.md` | Russian state archives by region |
| `belarus.md` | Belarusian archives and sources |
| `estonia-latvia.md` | Estonian and Latvian archives and sources |
| `ukraine.md` | Ukrainian archives and sources |
| `poland-lithuania-czechia.md` | Polish, Lithuanian and Czech sources |
| `germany.md` | German archives, including prisoner-of-war records |
| `genealogy-services.md` | commercial and community genealogy services |
| `libraries-and-reference.md` | libraries, gazetteers and printed reference works |
| `dead-and-moved.md` | dead, moved and repurposed domains |
| `needs-a-human.md` | sources that only a person can use, and what to ask them to do |
