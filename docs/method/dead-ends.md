# The dead-ends ledger

A family-history project run with agents produces far more negative results than positive ones: zeros far
outnumber finds, and a noticeable share of the "zeros" are sites that did not answer or searches that did not
work. Without a ledger, the zeros are forgotten, and the next session (or the next agent, or the researcher a
month later) runs the same searches again. Worse, a zero that was never valid gets repeated as a fact.

The ledger is a plain Markdown file, `DEAD_ENDS.md` (template in
[setting-up-a-project/templates](../../plugins/genealogy/skills/setting-up-a-project/templates/DEAD_ENDS.md)),
read at the start of every session **before any search is planned**. A wave of agents is briefed from it: each
brief names the entries that cover the agent's ground.

This page explains what the ledger is for, how it is divided, how an entry is worded so that it stays true,
how a closed entry is reopened, and how the ledger relates to `OPEN_QUESTIONS.md` and `FACTS.md`. Worked
entries close the page. The recurring kinds of failure are collected separately in
[invalid-zeros-and-false-trails.md](invalid-zeros-and-false-trails.md).

The examples are composed illustrations; the patterns come from real work, the particulars do not.

## The one rule

**Absence from an index is not absence of the person.** An index covers one genre of record, not all of them.
Parish registers do not list recruits; service records do not list infants; a database of the repressed does
not list people sentenced under an economic article; a database of the war dead does not list those who came
home. Every negative result in the ledger is therefore written in five parts:

1. what was searched for;
2. where exactly: database or archive, fond and series as placeholders, range of years, **genre** of record;
3. how much: number of files, sheets, records, result pages, and spellings tried;
4. the result;
5. what the result means, and **what it does not mean**.

Good: "Not in the parish registers of the Primerovka church, births 1881-1895: every result page read, all
spellings of the volost name tried." Bad: "He is nowhere." The first sentence is still true a year later. The
second tends to turn false within a week, and one whole section of the ledger (invalid zeros) consists of such
cases.

A second rule follows from the first: **a negative archive reply is not the absence of the document.** An
archive answers the question it read, and looks through the volume it judged sufficient. Each reply is
recorded with exactly what it covers.

## Why agents need it more than people do

Agents start each session without memory. They also report a failed search in the same confident register
as a successful one, and a blocked request often looks like an empty result (see the companion page). The
ledger has to absorb three kinds of damage that are specific to agentic work:

- **zeros from searches that never ran**: a captcha page returned with HTTP 200, a refusal answered with an
  empty redirect, a database outage that returned 0 for every query. The prohibition "do not count an empty
  result as negative before checking that the search ran" is usually written only after it has cost a batch of
  false zeros;
- **errors that live only in briefs**: a wrong conclusion from one agent's report is copied into every later
  brief and never enters the reference files, so nobody can find and correct it. The rule: an error that lives
  only in task briefs cannot be killed until it is written into a reference file;
- **invented resources**: agents' reports can name websites that never existed, or misspell real ones. Later
  agents spend time checking them.

## Sections and what goes in each

The ledger has eight fixed sections, followed by dated additions (one heading per working day or per wave),
which keep the same entry format.

| § | Section | What belongs there |
|---|---|---|
| 0 | How to read this file | The five-part rule, the warning that some old zeros are invalid, the marker table |
| 1 | Closed for good | Directions searched to the bottom. Read the report, do not repeat the search |
| 2 | Closed for one genre | An honest but narrow zero; each entry names the neighbouring genre that stays open |
| 3 | Zeros that turned out invalid | Earlier zeros that were wrong, grouped by mechanism: wrong place name, wrong district, false database zero, block that looked like a zero, wrong spelling |
| 4 | Negative archive replies | One table row per letter: archive, date, what was asked, what was searched, what it really closes |
| 5 | Dead, moved and non-existent resources | Repurposed domains and non-resolving domains are `[TECHNICAL]` (the archive behind them lives: write a letter, try a web archive); only an address that never existed is `[FINAL]` |
| 6 | False trails and namesakes | Not empty but full of other people: namesake persons, namesake places, documents mistaken for ours. Each entry names the **discriminator** (father's name and status, marital state, district, church, the column a line sits in) |
| 7 | Hypotheses tested and dropped | One table row per hypothesis with what refuted it. Refuted, not merely unconfirmed; an open fork is marked as a fork, with the condition that would settle it |
| 8 | Prohibitions | Short imperative rules, each paid for with lost time or data |

### Markers

Each entry starts with a marker so that a technical lock is never read as the absence of a document.

| Marker | Meaning |
|---|---|
| `[FINAL]` | No future condition will make this route answer: the object does not exist physically, the record form never contains the item sought, or the hypothesis was refuted by a **mechanism**, not by a missing record |
| `[CONDITIONAL · removable]` | Closure is temporary: page-by-page reading, a new request, the right spelling, new digitisation or access will lift it |
| `[CONDITIONAL · genre]` | Closure is permanent but narrow: one genre, one database, one threshold, a few surviving years. The route itself never reopens, but the question can be reached through a neighbouring genre |
| `[TECHNICAL]` | Not absence of a document but absence of access: captcha, refusal, broken certificate, a search form that no longer belongs to the institution, domain not resolving. Fixed by the researcher in a browser, a web archive or a letter, not by an archive search |

When a ledger is first marked up this way, the usual surprise is how few entries are final: many "closed"
entries turn out to be remaining work, and a good part are not dead ends at all but locks. An inventory should
also look for **entries with no route around them named at all**, and mark them "a hole in the inventory, not
in the work", so that they are distinguished from genre-bound entries whose route around is named but not yet
worked.

Section 6 (namesakes, namesake places, foreign documents) takes no marker: these are not dead ends but traps.

Later status words used in the dated sections: `[CLOSED TO THE BOTTOM]` (searched completely, with the
corpus named after a dot, for example `· <service name>`), `[DEAD END LIFTED <date>]`, `[PREVIOUS CONCLUSION
CANCELLED]`, `[NAMESAKE TRAP]`, `[NEW · recorded <date>]`.

### Section 2: closed for one genre while another stays open

Often the most valuable section. The zero is honest but narrow. Each entry ends with the genre or address to
try instead. The model entry lists several corpora, all empty, and states **the weight of each zero
separately**:

- a full-text archive index: every hit for the surname on every result page read; weight low, because the
  corpus covers registers of the cities migrants went to, not the village;
- a First World War card index: the surname is there, none from the right district; weight low, because a man
  born decades before the war hardly appears in its losses by age;
- a memorial book compiled village by village: the surname occurs nowhere; weight **medium and meaningful**:
  by then the family no longer lived in that village;
- Second World War databases; weight **zero**: all these genres start after 1917, and the person sought was
  born long before.

### Section 4: negative archive replies

One row per letter, in a table with the marker in the first cell:

`marker and condition | archive | date and number of the reply | what was asked | what the archive searched | does it really close anything`

The last column is the main one. Typically only a few replies close anything for good. The others close one
district, one parish and a few years, one spelling, one genre with a few surviving years, or "federal archives
only". The reply's outgoing number is kept in the private ledger so nobody orders the same search twice; in
shared examples it is replaced by `<no.>`.

### Section 8: prohibitions

Short imperatives, numbered, each tied to the entry or incident that paid for it. Examples:

- Do not count an empty result as negative before checking that the search ran.
- Do not state a negative without genre and volume.
- Do not search by one spelling of the surname. Minimum: with and without the ending, all case stems, with the
  sibilant variants, in the archive's own Latin normalisation.
- Do not search by prefix or truncation in an index that matches word forms.
- Do not search for the literal year in inventory headings; expand the ranges.
- Do not take a fact from a search snippet, or a year from the printed form heading; only from the scan.
- Do not open the repurposed domains, and do not cite them.
- Do not write to an archive about a fond that does not exist; do not write to an archive about a province it
  does not hold.
- Do not request a birth record by a volost that did not yet exist in the birth year.
- Do not give one site to several agents at once; one site, one request at a time, stop at the first refusal.
- Do not spend a shared web-search quota where reading the page directly will do.
- Do not take addresses, shelf marks or numbers from a summarised page; only from the page itself.
- Do not give subagents background mode: an agent that waits for a notification that never comes stops without
  a report.
- Do not treat an online family tree as a document; do not assume our own graph is better either.

## How to word an entry so that it stays true

An entry is true if a reader a year later can tell exactly which ground it covers. Each entry carries:

| Element | Example | Why |
|---|---|---|
| Genre of record | "parish registers, births only" | A zero in one genre says nothing about another |
| Corpus | "full-text layer of the archive portal", "the online index, not the images" | An index, a mirror and the images are three different corpora |
| Years | "1881-1886, 1888-1895" | The ledger expands ranges; never "around 1890" |
| Place under its name **of that year** | "volost A (before <year>), volost B (after)" | Boundaries moved; a search by the later name finds nothing earlier |
| Spellings tried | "Primerov, Примеровъ, Primerow, Przymierow; not tried: Прымеров" | The untried spellings are the condition for reopening |
| Volume | "every result page, all records written out" | Distinguishes a sample from a complete pass |
| Proof that the search ran | "control query for a common surname returned its usual count in the same session" | Distinguishes a zero from a block |
| Positive control | "the village is well represented: several hundred records for another family of it" | A zero is convincing only if the corpus is known not to be empty for that place |
| Date of the search | "observed <month year>" | Sites change; a zero ages |
| What would reopen it | "a request to the registry office of the neighbouring districts" | Turns the entry into a task when conditions change |
| Source | the report or session log that holds the raw output | Read the report instead of repeating the search |

The control query deserves emphasis. In the best entries every zero sits next to a number that proves the tool
was working at the time: a common surname that returned its usual count, or a known record found in the same
session. A good entry reads "the zero is honest: in the same session the same tools returned live results for
other queries". Without that sentence the entry is `[TECHNICAL]` until proven otherwise.

## Reopening an entry and marking the correction

The ledger never deletes a line. When a closure turns out wrong, or its condition is met:

1. **Strike the old text through** (`~~...~~`) and leave it in place, so that a reader who remembers the old
   claim finds why it fell.
2. **Add a new line directly below** with a dated status word: `[DEAD END LIFTED <date>]`, `[PREVIOUS
   CONCLUSION CANCELLED]`, or "**Correction <date>:** ... was: '...'". Quote the old wording after "was:".
3. **Name the evidence** that reopened it (the document, the report) and the **reason the old conclusion was
   wrong** (one subfamily of notices read and generalised; a portal that served its catalogue after all).
4. **Carry the consequence**: "searching surnames in these notices is meaningful, but only in this
   subfamily".
5. **Update the marker table** in § 0 and any entry that cited the old conclusion.

When a condition is met by work rather than refuted, the entry says so in its first cell ("CLOSED <date>: file
read; the condition 'file not read' is removed") and records what the work closed, including the surprise: a
single file may close questions nobody expected it to, and leave open the ones it was ordered for.

## The ledger and the other files

Three of the project's files are easy to confuse.

| File | Holds | Changes when |
|---|---|---|
| `FACTS.md` | Established facts with their document and date of entry | A document establishes something |
| `OPEN_QUESTIONS.md` | What is still open, with the next concrete step and its cost | A question is opened, narrowed or closed |
| `DEAD_ENDS.md` | What was searched and not found, and what was wrongly believed | A search ends empty, a reply arrives, a trail proves false |

The rules between them:

- **A new wave of agents is planned only from `OPEN_QUESTIONS.md`**, never from the ledger. The ledger removes
  ground; it does not assign it. Once the open questions hold no blind machine directions any more, no new
  wave is started without a named question.
- **Before planning, every candidate step is checked against the ledger.** If an entry covers it, the step is
  dropped or rewritten to target exactly the entry's condition for reopening.
- A `[CONDITIONAL]` entry whose route around is named but not worked is **work, not a dead end**: it has a twin
  line in `OPEN_QUESTIONS.md`.
- When a fact enters `FACTS.md` and contradicts an entry, the entry is reopened (struck and dated) in the same
  step. An entry such as "the surname is not in the registers" falls the day a godparent line from those
  registers enters the facts file.
- A hypothesis leaves `OPEN_QUESTIONS.md` for section 7 only when it is refuted, with the refuting document. An
  unresolved fork stays open, and both readings stay in the family's texts side by side.

## Worked entries

Composed illustrations with the invented cast; shelf marks are placeholders.

### Section 1: closed for good

**1. A list read to the bottom, with false recognitions.**

> `[CLOSED TO THE BOTTOM · <month year>]` **Household list of a rural commune, `fond <F>, opis <O>, delo <D>`:
> read in full, none of ours.** All digitised frames, every name written out one by one. Zero for Primerov
> (Примеров, Примеровъ, Primerow) and Obraztsov in every spelling.
> False recognitions waiting for the next reader: a few names that resemble ours at first sight; each checked
> under magnification, all different surnames.
> The task "write out everyone born in the province" cannot be done on this file: the form has no birthplace
> column. Strike it from the plans.
> Still alive in this file: the last sheet is not a list but a covering note that refers to a second list; that
> list is not online. That is an address for a letter, not a dead end.

**2. Closed by mechanism.**

> `[FINAL]` **Confession lists, `fond <F>, opis <O>, delo <D>`: no Näidis household.** Read frame by frame; the
> manor section complete, households without a gap. Not chance: the volume **begins years after** the family
> left the parish (departure documented in another file). They could not meet in this book. The zero says
> nothing about the family, only about the volume's dates. Do not open again.

### Section 2: closed for one genre

**3. Genre closed, neighbour genre already worked.**

> `[CONDITIONAL · genre]` **Obraztsov in N uezd: parish registers.** Closed: parish registers, all surviving
> years. Open and already productive: recruit lists, `fond <F>`, where an Obraztsov from a neighbouring village
> is found. The old formula "no Obraztsovs in N uezd" holds for registers only.
> **Correction <date>:** "no Obraztsovs in the registers" is refuted: an Obraztsov from Primerovka stands as
> godfather in the births of one year of those registers. The zero rested on search indexes; nobody had read the
> books themselves. What remains closed is "not in the indexes".

**4. Record form lacks the field.**

> `[CONDITIONAL · genre]` **Death record of Maria Primerova.** The death record of an adult has **no column for
> parents**, so it cannot answer who her father was, whatever is found. Open instead: her marriage record,
> `fond <F>, opis <O>, delo <D>`.

### Section 3: invalid zeros

**5. Wrong place name for the year.**

> **Primerovka belonged to Obraztsovskaya volost until about 1900**, when that volost was merged into a larger
> one. Everything searched for the earlier years under the later volost name was searched
> under a name that did not then exist for this village. Recheck those zeros under both names. Do not carry the
> correction to the neighbours without checking: the next village may already have belonged to the later volost.

**6. A zero from one spelling.**

> **Primerov: a typed document spells it Примерот.** None of the spellings tried before covered this form. On the
> same scan a month written in Latin numerals was typed with a Cyrillic letter of the same shape and read as a
> different month.

### Section 4: negative archive replies

**7. Four rows of the replies table.**

| Marker and condition | Archive | Date and no. | Asked | Searched | Does it close anything |
|---|---|---|---|---|---|
| `[CONDITIONAL · removable]` One district closed, thoroughly. Condition: ask the neighbouring districts | District registry office | `<date>`, `<no.>` | Death of Pyotr Primerov | All its books for the whole period asked | **Yes, for its district.** Says nothing of neighbours |
| `[CONDITIONAL · removable]` Reply covered one part of the file. Condition: re-ask for the N uezd part | Provincial archive | `<date>`, `<no.>` | The Primerov family in a province-wide list | Only the part of the list for another uezd | **No.** The family lived in N uezd |
| `[CONDITIONAL · removable]` One spelling. Condition: re-ask under three forms | Regional archive | `<date>`, `<no.>` | Birth of Ivan Primerov, one parish, a few years | That parish, those years, "Primerov" only | **For this parish and these years, yes.** Примеровъ and Primerow not checked |
| `[FINAL]` Physical absence, with its act | National archive | `<date>`, `<no.>` | Recruit lists of N uezd for the decade asked | The fond inventory | **Closes, with content:** the files for those years were destroyed; the reply cites the act. A document, not a silence |

### Section 6: false trails and namesakes

**8. Namesake in the same parish, nearly accepted.**

> ⚠ **Anna Primerova, frame `<id>` of a marriage register: NOT our Anna.** Given name, surname and year of
> birth all match. Three things differ: she is entered as a spinster, while ours married that year as a widow; her
> father has another name and another status; the groom is a stranger. A quick reader will take her for ours.
> Do not.

### Section 7: hypotheses tested and dropped

**9. Refuted by a mechanism, and a fork.**

| Marker | Hypothesis | What refuted it |
|---|---|---|
| `[FINAL]` | "Anna was born in Primerovka" | Excluded by mechanism, not by search: by the period gazetteer the village was founded after her birth |
| `[FINAL]` | "The earliest year in the reply is the year the Obraztsovs were recruited" | **That year is the first for which the fond survives**, not the year of a record. A man born later cannot stand in that list. Corrected in the family's texts with a note |
| `[CONDITIONAL · removable]` A fork, not a refutation: patronymics differ. Condition: a document naming the father | "Ivan Obraztsov is Maria's grandfather" | A relative's recollection fits, the age gap fits, but the patronymics differ: status `probable` for kinship and `disputed` for configuration; not into the family's texts as fact |

### Dated additions

**10. A zero with its control.**

> `[CONDITIONAL · machine databases]` **Pyotr Obraztsov is found nowhere.** Zero in the war-dead database (full
> name: 0; surname and given name: a handful, none with the right patronymic), in the awards databases and in
> the First World War index. **The zero is honest: in the same session the same tools returned live results for
> other queries.** Condition: the name comes only from a person sheet; only a paper from home or the village
> registers can close it, not a machine search.

**11. Weight of a modern register.**

> `[CONDITIONAL · genre]` **Latvian place-name register: the Paraugi farm is not confirmed.** Read strictly:
> this is absence from a **modern** index, which keeps only a small fraction of the farms that disappeared.
> The negative weighs almost nothing. Route: pre-war maps and parish books.

**12. A technical lock, dated.**

> `[CONDITIONAL · access]` **The full-text archive portal stopped answering search pages from `<date>`.** Every
> page redirects to the portal's front page with an almost empty body, including sheets that opened before.
> This is a block, not a zero. Not done because of it: one parish file read through. Condition: the portal
> answers again, or the researcher reads the file in their own browser.

**13. A reopened genre verdict.**

> ~~`[CONDITIONAL · genre]` **Land-consolidation notices in an official gazette.** A few notices read in full.
> The form does not name participants: a property of the genre, not a gap in digitisation.~~
>
> **`[DEAD END LIFTED <date>]` Land-consolidation notices: corrected, was "the genre does not name
> participants".** It does. The earlier conclusion was drawn from one subfamily of notices (opening and closing
> of proceedings) and missed a second, which prints name lists of owners with their areas. Consequence:
> searching surnames in consolidation notices is meaningful, but only in that subfamily; the notices read
> before were of the other kind.
