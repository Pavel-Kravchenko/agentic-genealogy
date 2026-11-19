---
name: searching-a-source
description: Use when querying any genealogy database, archive catalogue, name index, full-text search or digitised collection for a person or place - especially when a search returns nothing, returns suspiciously little, returns HTTP 200 with an odd page, or when about to write "not found", "no records" or "does not exist"
---

# Searching a source

## Core principle

A search has three outcomes, not two: a result, a true zero, and a block. A block almost always looks like
a true zero. And a true zero is a statement about one record genre in one corpus under one spelling, never
about a person.

## Before the query

1. Read the dead-ends ledger for this person, place and site. Do not repeat a closed search; do not knock
   again on an archive that has answered in the negative, unless its reply did not cover the question asked
   (another district or other years).
2. Establish the place name and jurisdiction valid in the year of the event. A Soviet-era form names the
   birthplace in the administrative grid of the day the form was filled in, which may not have existed when
   the person was born. Use a gazetteer of that period.
3. List the spellings. Vary the distortions of the root, not the grammatical cases: Примеров, Примерав,
   Прымеров, Primerow, Przymierow. Test two case forms first; if they return the same set, the index
   lemmatises and case forms are wasted queries. Prefix truncation with `*` rarely works; verify it on a known hit.
4. Before the 1880s many parish registers of peasants carry no surname. Search by given name + patronymic
   + wife's given name.

## Running the query

- Query only an `open page`: a public page reached without a login. An agent reads it only if the site's
  terms of use and robots rules allow automated reading; otherwise treat the site as `own browser`. A site
  that needs a login or a subscription, or that does not serve automated requests, is `own browser`: no agent
  queries it; hand it to the researcher, who uses it personally in their own browser. A captcha, a
  payment, a letter or a visit is `human only`.
- Before an agent reads a site, the researcher checks that the site's terms of use and robots rules do not
  forbid automated reading. If they do, or if it is unclear, treat the site as `own browser`.
- One site, one agent, one request at a time, slowly. Stop at the first refusal and never retry in a loop.
- Search with one word and filter locally. Adding words to narrow a query can silently drop much of the
  corpus. Never draw a negative conclusion from a phrase query.
- Extra search fields often rank and do not filter. Count by the last page that is still about your place,
  not by the counter.
- A name index may be cut at a fixed number of rows without saying so. Page through to the end and compare
  with the stated total.

## Reading the answer: result, zero or block

Check the length and type of the body, not only the status code.

| Sign | Meaning |
|---|---|
| The site's own "nothing found" marker is present | True zero for this query |
| HTTP 200 with a very small body, a login form, a search form with no results, a "checking your browser" page, an empty application shell | Block |
| No result cards and no "nothing found" marker | Block or failure, not zero |
| 403, 429, 503 on images while pages answer | Block or maintenance |
| A saved `.jpg` that is an HTML page | Failed file. Verify the format signature (JPEG starts `FFD8`, ends `FFD9`), not the status or the size |

Prove that the search ran before you trust a zero: run a control query that must return something (a
common surname) in the same session, with the same parameters. When there is no time for the control,
record `ZERO, control not run`: it closes nothing until the control has been run.

A database answers only for what it covers. A true zero in a list of repression victims, of war dead or of
one province's registers says nothing about a person who was never in that category or that province.
State the coverage in the entry.

When asked for a yes or no that the three outcomes cannot give, answer "not established", say which sites
gave a real answer, and say what would settle it.

On a block: stop. Do not retry, and do not look for another way in. Record BLOCKED with the date and the
signature, and hand the site to the researcher, who decides whether and how to use it in their own
browser: name the site, the exact query, the spellings to try and what a real result page looks like.

## Reading what you found

- The full-text layer does not index everything. Fields of a form, marginal notes and whole archive layers
  are visible only on the scan. "Not in the database" means "not in the indexed text".
- OCR misreads printed years (the handwritten last digit, sometimes the decade) and whole names. Take
  names and dates from the image only. Date a sheet by the file's own dating or a duplicate copy.
- Grep over saved OCR text gives false zeros: words are broken by spaces and hyphens. Put `[\s\-]*` between
  letters and use tolerant classes for known confusions.
- A catalogue dates a file by the inventory, not by the document.

## Recording the outcome

A result goes to the facts file with its shelf mark. Everything else goes to the dead-ends ledger in this form:

```
<date>. <site/corpus>, <record genre>, <years covered>: searched <spellings>; control query <word> returned
<n>; result: ZERO | BLOCKED (<signature>). Closes: <exactly what>. Does not close: <other genres, other
spellings, other jurisdictions>. Reopen if: <condition>.
```

Right: "in the parish registers of N uezd indexed on this site for 1860-1917 there is no Primerov under
five spellings". Wrong: "he is nowhere".

## Red flags

Stop and re-read this skill when you are about to write any of these:

- "No records exist" after one spelling or one site
- "The site returned nothing" without having seen its nothing-found marker
- "Not found, so the family story is wrong"
- "Probably blocked, I will try a different way in"
- "The index has him aged 40, so the year of birth is ..." without opening the image
