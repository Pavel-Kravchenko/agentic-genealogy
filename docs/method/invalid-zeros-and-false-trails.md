# Invalid zeros and false trails: the recurring patterns

This page collects the ways a search goes wrong in a family-history project run with agents, as recorded in a
dead-ends ledger (see [dead-ends.md](dead-ends.md)). Each pattern gives how it looks, why it is wrong, how to
catch it, and the rule that prevents it.

The examples are composed illustrations; the patterns come from real work, the particulars do not.

| # | Pattern |
|---|---|
| 1 | Zero from a search that never ran (block, outage, ignored parameter) |
| 2 | Zero from one spelling |
| 3 | Zero from the wrong jurisdiction or the wrong year's place name |
| 4 | Zero from an index that covers one genre |
| 5 | Zero (or false hit) from OCR and machine text |
| 6 | A reply that covers less than the question |
| 7 | Namesake in the same village or parish |
| 8 | Namesake village or district in another province |
| 9 | A tree that copied our own data (circular confirmation) |
| 10 | A hypothesis kept alive by an age match |
| 11 | A catalogue date or frame number that is not the document's |
| 12 | Errors that live in reports and briefs, not in the sources |
| 13 | A document of another kind taken for ours |
| 14 | Geocoder damage to places |

The most frequent in practice are patterns 1, 4 and 8. Pattern 1 matters most for agents: when a ledger is
first marked up, a large share of its "closed" entries turn out to be technical locks rather than absences of
documents, and in any long run of agent searches a noticeable share of outcomes are "resource not reachable"
or "search does not work", which a careless agent records as zeros.

## 1. A zero from a search that never ran

**How it looks.** An empty result list, a page with no links, an HTTP 200. The agent writes "not found".

**Why it is wrong.** Most refusals look like an empty result, not like an error. Typical shapes:

| What the agent sees | What it really is |
|---|---|
| HTTP 200 with a captcha page and no record links | Data present; the site needs a human in a browser |
| A redirect to a login form | The images are behind registration; the catalogue may still be open to anonymous reading |
| An image gallery with no file links | Images for registered users only; the catalogue with full references may be open |
| A timeout, no HTTP status, or a 5xx error | Host may be alive; the pages simply were not read |
| 403, a security-check page, or a search engine's captcha | A refusal of automated requests, not an absence |
| An agent harness's web search returns nothing | A shared search quota used up, not an answer |
| A redirect to the front page with an almost empty body | A block on that page type |
| "No record found" for any query | The site's own search box replaced by another form; not an answer of the database |

Other forms: a database outage that returns 0 for every query for a day or two; a search parameter that the
portal silently ignores, so every "zero" got that way is void; a web-archive snapshot of a printed book that
lacks whole letters of the alphabet; a site that serves a person in a browser while refusing an agent.

The positive signature is worth recording too: some sites return an honest zero as a page of a fixed, small
shape. Knowing what a true zero looks like on a site lets a reader tell it from a refusal.

**How to catch it.** Control queries in the same session: the same query that returned records the day before;
a common surname that returns its usual count; a known record that must be found. And read the raw response
instead of the agent's summary.

**Rule.** Do not count an empty result as negative before checking that the search ran. Every zero sits next to
a control from the same session. A zero without a control is recorded as `[TECHNICAL]` until proven otherwise.
Keep a table of refusal signatures per site with the month observed. At the first refusal, stop: one site, one
request at a time, no retries in a loop; what needs a login or a captcha goes to the researcher's own browser.

## 2. A zero from one spelling

**How it looks.** "Primerov: 0 in the archive." Or an archive letter answering for one spelling.

**Why it is wrong.** Spellings drift between clerks, alphabets, archives and indexes, and indexes split forms
that a person would treat as one. Typical cases:

- A typed document spells the surname with a different final letter (Примерот), not covered by any spelling
  tried before.
- A database spells it with a soft sign the searcher did not use, and returns an "honest but empty" zero.
- An archive inventory normalises the spelling (w to v): a report records "no files for Primerow", while there
  are several dozen under the normalised form.
- One family's single file shows several forms of the surname for one man, so a rule such as "one letter =
  ours, two letters = others" has to be cancelled.
- A sibilant variant: one form gives a fraction of the records of the other, and the oldest layer of records
  exists only under the second. Searching the "correct" form cuts off the oldest generation.
- A clerk's distortion with a different vowel gives a zero in the entire archive.
- Case forms of rare surnames are not lemmatised: the genitive returns 0, the nominative a few records.
- The full-text index splits one word into separate dictionary groups: `Primerov`, `Primer` and `Primerovy` are
  three corpora, and the unrequested third can hold a whole unknown man of the family. A volost name can have a
  dozen forms in one index, some of them machine distortions.
- A surname recorded under the grandfather's name: the man is missed under the family surname.
- A commercial collection's surname search loses records; one turns up only by given name plus village.

A different kind: **the surname does not yet exist**. Early peasant registers in many regions carry no
surnames at all. Search by "given name + patronymic + wife's name", or by farm name.

The reverse also holds and saves time: some full-text indexes normalise the old hard sign, yat and dotted i, so
a surname returns the same count with and without them. Variants that the index already merges need not be
searched separately.

**How to catch it.** Read the scan instead of the index; save the result pages you read for each spelling
and check them by hand; note which spelling each archive normalises to.

**Rule.** Never search by one spelling. Minimum: with and without the -ov/-ova ending, all case stems,
sibilant and final-consonant variants, the archive's Latin normalisation, and the surname of the grandfather.
Record the spellings tried in the entry; the untried ones are the condition for reopening. Do not search by
prefix in an index that matches word forms: a truncated stem returns many unrelated hits.

## 3. A zero from the wrong jurisdiction or the wrong year's place name

**How it looks.** "Nothing for Primerovka in the files of Obraztsovskaya volost."

**Why it is wrong.** Administrative units moved, merged and were renamed; archives hold what their territory
held at the time, not today. Typical cases:

1. The village belonged to another volost until some date; every search for the earlier years under the later
   volost name is a search under a name that did not exist for the village. The correction does not
   automatically carry to the neighbouring village.
2. Task briefs give the wrong higher unit (powiat, uezd) for a commune; everything searched under it is
   searched in the wrong place. Several communes can share nearly the same name; the filter that works is the
   higher unit in its grammatical form as printed, not the commune name.
3. A reform moved settlements between communes; their earlier files lie with the abolished commune.
4. A uezd belonged to a neighbouring province for part of the period; the records are in the other province's
   archive.
5. A Soviet-era form names a birthplace by the administrative grid current when the form was filled, which may
   be a unit that did not exist in the birth year.
6. A parish was split off from its neighbour later, so farm names "of the new parish" are in the old parish's
   books.
7. A place name enters the project's lists through an error in a brief.

Custody cases (the place is right, the archive is not): a branch archive whose holdings start after 1917; a
national archive that does not hold a province kept in a regional archive; an archive that holds a uezd's
registers only to some year, with later years in another province's archive; recruit records kept centrally
rather than in the provincial city; a consistory copy missing from the consistory fond.

**How to catch it.** Read the official gazettes, use printed gazetteers of the period, read the archive's own
published guide. Settler colonies and estate settlements are often missing from official place lists; period
monographs on such settlements and the estate name in the gazetteer can explain the gap.

**Rule.** Write every place in an entry under its name **of that year**, with the higher unit. Before searching
a range of years, establish the boundary changes inside it. Filter records by the higher unit, not by the
commune name. Do not request records by a unit that did not exist in the year of the event.

## 4. A zero from an index that covers one genre

**How it looks.** "Not in the database." The database was searched correctly and completely.

**Why it is wrong.** The database never held that kind of person. Typical cases:

| Index or corpus | What it covers | Why the zero says nothing |
|---|---|---|
| A national name index of church books | Church personal books | Not revision lists, not other confessions |
| An international tracing archive's online index | Camps, persecution, forced labour of civilians, displaced persons | Prisoner-of-war personnel cards are mostly elsewhere |
| A national repression database | Repression on that country's territory in a given period | A person arrested elsewhere or earlier cannot be in it |
| Repression databases in general | Political articles | A sentence under an economic article is in none of them |
| Second World War databases | Post-1917 records | Weight zero for a man born in the 19th century |
| City-of-arrival registers | Migrants who left | Say nothing about those who stayed |
| Parish registers of a migrant community in a city | Its churches and years | A zero does not mean he never lived in that city |
| A modern place-name register | Modern names | Keeps only a small fraction of vanished farms |
| An online index of a record collection | The indexed part | An index zero is not an image zero |
| Death record of an adult | No column for parents | Cannot name the father |
| A mirror of a large collection | Part of the collections | A whole archive can be missing; a mirror's zero is not the collection's |

One case goes the other way and is a warning against over-generalising a genre: gazette notices of land
consolidation were judged "never name participants" after a few notices of one subfamily; a second subfamily
prints owner lists. The verdict was lifted.

**How to catch it.** Read what the database says about itself; run a positive control (the village is well
represented by another family's records); ask "could this person be here at all, by age, territory and
genre?".

**Rule.** Every negative names its genre. Before searching, write down why the person could be in this corpus.
Give each zero a weight (zero, low, medium, meaningful), and say why.

## 5. A zero, or a false hit, from OCR and machine text

**How it looks.** No hit in the full text; or a hit whose year, name or age is wrong.

**Why it is wrong.** The recognised text layer is a machine reading, and the search snippet is a further machine
layer on top. Typical cases:

1. A printed year on a form misread, including the tens digit; proved with consistory duplicates.
2. OCR substitutes one given name for another.
3. Search snippets wrong in several ways: a patronymic replaced; "mother of the deceased" instead of the
   deceased; "months" instead of "years"; two families from one sheet merged; a name changed by one letter.
4. A fuzzy search reports dozens of hits; the machine text of the scans contains the name once.
5. The recognised layer covers a small share of the papers, so a zero in it is weak.
6. A database's full text does not index the form fields; what is "not in the database" may be on the image.
7. A typewriter types a Latin numeral with a Cyrillic letter of the same shape, and a month is misread.
8. A fetch tool's summary of a page in a legacy encoding gives wrong addresses.
9. A name misread several times the same way; comparing the scribe's own hand on the same page fixes it.
10. A misread age or status word creates a person or a storyline that never existed and has to be removed.

**How to catch it.** Open the scan; compare duplicates of the same record; compare against the column layout of
the sheet; read the page itself instead of a summary.

**Rule.** Take no fact from a snippet. Take years and headings from the scan or from the file's dating, not from
the printed form heading. Read ages without a "months" mark only from the scan. Take addresses, shelf marks and
numbers from the page itself, never from a summary. Before declaring a contradiction, compare the word with the
same scribe's hand on the same page.

## 6. A reply that covers less than the question

**How it looks.** An official letter: "no information".

**Why it is wrong.** An archive answers the question it read and looks through the volume it judges enough.
Only a few replies close anything for good, and those that do usually carry content (a document, an act of
destruction), not a silence. Ways a reply covers less than the question:

- it covers one district's part of a file that covers the whole province, while the family lived in another;
- it searches one spelling;
- it searches one confession's registers and asks for clarification on the others: "not searched", not
  "not found";
- it answers that a settlement "is not listed" in the official gazetteer, which is true and does not answer the
  question (see pattern 3);
- it answers for federal archives only, leaving regional, departmental and registry-office holdings untouched;
- it searches by name, while the request asked for a full pass by village (the person may be recorded in
  someone else's household, as a servant or a lodger);
- the series survives only for a few years, for which the person was the wrong age;
- it forwards the request to another body without an answer of its own.

A sound negative states its limits: a registry office that searched all its books for the whole period asked
closes that district and no other. That is the model of a useful negative.

Bookkeeping traps come with the letters: two letters of one archive can carry the same outgoing number; a
standard phrase in a reply can be a template, not a lead. And a reply can carry weight beyond its words: an
archive searching for one child that finds other children of the same father in the same books proves the
surname is readable there, which makes the zero for that child meaningful.

**How to catch it.** Compare the reply with the inventory of the file it names, re-read the request, and read
the reply's scan rather than a summary.

**Rule.** Record every reply with what was asked, what was answered, what volume was searched, and a separate
column "does it really close anything". Note "not searched" separately from "not found". Re-ask with the whole
file, all spellings and the place under its name of the year. A reply that did not cover the question asked is
recorded as such, without blame.

## 7. A namesake in the same village or parish

**How it looks.** A record with the right given name, surname, village and an age within a year.

**Why it is wrong.** In a village, given names and surnames repeat across households. Typical cases:

- a full namesake from the same village, whose later life is fully documented and is not ours;
- a woman with the same name, surname and birth year in the same parish, entered as a spinster while ours
  married that year as a widow; her father differs in name and status;
- a girl born to parents with the same names as ours a few months after our girl (one mother does not give
  birth twice in a few months);
- two girls of the same name born in the same month in the same parish to two other couples;
- a man linked to our family by a tree, who belongs to another of two same-named fathers in the parish;
- a family whose surname differs from ours by one capital letter on a spread;
- two men with the same full name and patronymic: an "impossible" date belongs to the other;
- a boy from the neighbouring village with the right name and father's surname who died in childhood.

The opposite risk is also real: relatives accepted as ours on "name + year + village" alone, because the cards
carry neither the father's name nor the household.

**How to catch it.** By the discriminators: father's name and status, marital status, farm name, household
composition, church, the column a line sits in.

**Rule.** The surname is not an identifier. Membership of a record in the family is proved by volost and manor
(or farm, or household), not by name. Each namesake that cost time goes into section 6 of `DEAD_ENDS.md` with
its discriminator, so the next reader does not repeat it.

## 8. A namesake village or district in another province

**How it looks.** All hits for the village name come from somewhere.

**Why it is wrong.** Place names repeat. The worst case: a village called Primerovka in another province, where
an Ivan lived with a wife Anna. Other forms: every gazette hit for the village name is a namesake manor or
settlement elsewhere; several villages of one name in neighbouring districts; communes of near-identical
names in different higher units; two churches of the same dedication in one province; a surname query in which
almost every hit comes from one namesake village elsewhere; a catalogue heading that means a workers'
settlement, not a construction site; an archive section named after a street, not after the province; a
village with a second name ("also called ..."); an estate village and a state-peasant village with the same
name, whose surname sets do not overlap.

**How to catch it.** Check the higher unit in every line (volost, uezd, powiat, voivodeship), the church,
coordinates of the period, the full gazetteer.

**Rule.** Never search a village without its higher unit. Filter on the higher unit's word. Record the
discriminator for every namesake place.

## 9. A tree that copied our own data

**How it looks.** A second source confirming our version.

**Why it is wrong.** The second source descends from the first. Typical cases: a hypothesis rests on an online
tree and an inscription on a photograph, and the inscription turns out to have no documentary source of its
own, so the version has one channel, not two; the only "source" for a branch is an export of another tree
service; tree data on several sites are echoes of one large tree; printed trees found among family papers are
an earlier export of the project's own graph; a relative's "memory" of a surname comes from a tree; graph nodes
are held up by one tree alone.

**How to catch it.** Ask each source where it came from; find the common ancestor of two "independent"
confirmations.

**Rule.** An online tree is not a document; in the family's texts its data are introduced as "according to the
family tree". There is no presumption that our graph is better either: the tree may be right where our value
was computed, and wrong where we hold a civil record. Count channels, not mentions.

## 10. A hypothesis kept alive by an age match

**How it looks.** "Right name, right year: it is probably him."

**Why it is wrong.** Ages in the period are approximate and namesakes common. Typical cases: the same-parish
namesake of pattern 7; the only database man of the right name, who turns out younger than his supposed
daughter; several girls of one name born on one manor within a few years, some struck off firmly and some only
by absence of trace; several men of the right name born in the right year, which an online card cannot
separate; a namesake of the right birth year who died as an infant; an "elder son" who never existed (age
misread); a pair of brothers whose age gap fits while their patronymics differ.

**How to catch it.** By a second identifier: father, household, place of origin, or a mechanism (a person cannot
be older than his father's marriage, cannot be in a list before his birth).

**Rule.** An age match only keeps a candidate on the list. It never promotes one. Write "not excluded" and the
missing identifier, and keep the candidates listed by name in `OPEN_QUESTIONS.md`.

## 11. A catalogue date or frame number that is not the document's

**How it looks.** "The file is dated <year>", "sheet <n>", "recruits of <year>".

**Why it is wrong.** Typical cases: a catalogue dates a file by its inventory, while the sheets carry their own
dates; the first year a fond survives is read as the year of a record; a search for the literal year misses a
file whose heading gives a range; a date on a record card is the sentence date, not the date of death (the
death line can be empty for one person and filled for another in the same format); a tree gives the
registration date of a civil act, not the event date; the date of death and the date of the act differ; a
snippet frame is a spread, so frame and sheet numbers are offset; an image viewer numbers a page differently
from the file, so the same page is read twice as two pages; a volume begins after the family left, so its
silence says nothing about them.

**How to catch it.** Read the sheet, use duplicates, count frames against sheet numbers, compare with a
neighbour's record of the same form.

**Rule.** The year of a sheet comes from the sheet or from a duplicate, never from the catalogue or the printed
form. Record frame and sheet separately, and the viewer index separately from the file number. Write both dates
when the event and its registration differ.

## 12. Errors that live in reports and briefs

**How it looks.** A fact everyone "knows", repeated in every brief.

**Why it is wrong.** Typical cases: a wrong conclusion of one report ("no revision lists of the uezd in the
full text") is never entered in a reference file and is copied into each later brief, while the archive's own
inventory shows the revisions digitised and open; earlier reports name websites that never existed; a place
name enters the project's place list from a brief; an estimate of work left ("half read, half left") is wrong
because nobody counted.

**Rule.** An error that lives only in task briefs cannot be killed until it is written into a reference file.
Briefs cite `DEAD_ENDS.md`, `FACTS.md` and `OPEN_QUESTIONS.md`, never another brief.

## 13. A document of another kind taken for ours

**How it looks.** The catalogue title promises exactly what we need.

**Why it is wrong.** Typical cases: a fond catalogued as a district registry office that holds a village
church's registers; files thought to be second copies of one church that belong to other churches; a card file
described as one group of people that holds another; transport lists taken for personal files; a column in a
file treated as independent evidence that was itself copied; and the cases of patterns 5, 9, 11 and 14.

**Rule.** Order and cite a file by what its pages show, not by its catalogue title. Record the correction in the
ledger so the title does not mislead again.

## 14. Geocoder damage to places

**How it looks.** Coordinates and modern place names on every event of the graph.

**Why it is wrong.** An automatic geocoder of a family-tree service replaces places with its best match.
Typical cases: one non-existent village node glues together several different places far apart; the farms of
one parish collapse into one town; a family village is replaced by the volost centre; a village is overwritten
by the nearest district town. The original wording usually survives in the event notes.

**Rule.** Do not trust coordinates of pre-war persons. Restore places only from the original note; never fill
an empty place with a "dump" node or an inferred value.
