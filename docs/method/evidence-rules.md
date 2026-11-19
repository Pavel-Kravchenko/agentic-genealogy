# Rules of evidence and identification

These rules were each paid for at least once in a family-history project run with Claude agents. The
examples are composed illustrations; the patterns come from real work, the particulars do not. They use an
invented cast (the Primerov, Obraztsov, Näidis and Paraugs families, the village of Primerovka).

## 1. The document comes first

- A fact enters the record from a document image: a register entry, a form, a census list, a certificate.
  An index entry, a search snippet, a catalogue line, somebody's tree and a relative's memory each say where
  to look; none of them is the fact.
- When two papers about one person disagree, ask first who held the pen. In one archive folder a form was
  filled in from the applicant's own words, and a certificate from the volost executive committee stated
  origin and kinship in another hand, by another office, from its own lists. The certificate carried the
  proof of kinship in several files; the forms of the same files gave ages that differed from it by a year
  or two, systematically. Prefer the paper written by an outsider from records over a self-declaration, and for
  dates prefer a direct record of the date over an age.
- A retelling by a living relative is checked against the document images before it enters the record.
- When a document is found unreadable, that is a result. Write "not readable" and why, rather than a guess.
  Nothing marked "probably" goes into the narrative text.

## 2. A surname and a given name are not identifiers

- In one parish, namesakes with the same given name are the norm. A tree importer that matched persons by
  name produced, on several men called Ivan Primerov, merge conflicts that did not exist and a false fact;
  they survived through several agent waves and generated an open question about an anomaly that did not exist.
- A personal file of a "Pyotr Ivanovich Primerov" matched the surname, the given name and the patronymic,
  was ordered more than once as "ours", and turned out to belong to a man from a volost at the other end of the
  country. The rule bought with it: a file belongs to the family when the volost and the estate match, not
  the name.
- One man's file can carry several spellings of his surname, in more than one script. Any rule of the type
  "one letter means ours, two letters means strangers" is unsafe and was withdrawn.
- When comparing your graph with an exported tree, match persons only by the export's unique id (`_UID` in
  GEDCOM exports). Equal name, even name plus year, is not identity.
- A spelling that looks close can be a different family: every index line of a look-alike surname came from
  another region, and gravestone records agreed.

## 3. Telling namesakes apart: household first, age last

Age in a questionnaire is weak by construction. Household members, parish and confession are strong.

The case that set the rule: a conclusion rested on an "Anna" in one file and an "Anna Ivanovna", several
years older, in another being one woman, with the gap explained as the usual looseness of stated ages, which
on its own would have been fair. The identity broke on the household: one woman lived with a child, the
other's form listed no children. Parish and confession then confirmed it.

A second case, with almost everything matching: a bride with the same given name and surname as an ancestor,
born a few days apart in the same year. Three things separated them: she was entered as a spinster, while
the ancestor married that year as a widow; her father had another given name and another status; and the
groom was someone else. Read quickly, she would have been taken for the ancestor.

A more dangerous trap matched village, given name and wife's name at once: a second
"Primerovka" in another province where another Ivan lived with his wife Anna. Order of checks before
building on an identity:

1. household members (spouse, children with ages, parents and their status, alive or dead);
2. parish, volost or estate of registration;
3. confession;
4. only then dates and ages.

A link found only by "full name + year + village", with no patronymic of the father and no family
composition on the cards, is not a namesake trap yet, but it carries the risk of one: mark it as such.

## 4. Unproven identity stays as separate persons

When a document may concern a person already in the graph but the identity is not proven:

- enter the document's people as new, separate persons, with only what the document says directly;
- link them to the existing persons as "presumed kinship", confidence "low";
- do not merge until a new document or a direct word from the family settles it;
- do not touch the dates of the existing person; record the disagreement in its dispute field.

When the family member who owns the research decides a kinship ("make them the parents"), execute it in the
graph: merge the placeholder persons into the documented ones, confidence "medium", source "decision of
<family member>, <date>", and keep the competing versions in the dispute field or the list of withdrawn claims.

## 5. Never smooth a disputed date

- A disputed date stays disputed until a new document arrives. Keep both values with their sources.
- Where a document disagrees with a gravestone or with family memory, print both.
- Common reasons two dates differ, each seen in the project:
  - a tree gives the date the civil act was registered, the register gives the date of the event; checked
    on the certificates themselves, the register was right each time;
  - a death record issued to relatives decades after a repression case can show a date that is not the
    date of death; ask the archive that holds the case file which date it records;
  - an "impossible" date that belongs to a namesake (two men with the same name and patronymic in one
    family line; the contradiction lived in the project for a long time before it was split).
- When a surname turns out to have been misread, reread every document of that family for the same name.
  Put the confirmed spelling into the variants with its document; do not change the main name.

## 6. Kinship stated by a living relative is recorded as stated

A living family member's statement decides kinship where documents are silent; a calculation over dates or
over the graph does not override it. An agent
computed a kinship from the graph that a family member contradicted. When much of a graph came from somebody
else's exported tree, the graph is a party in such a dispute, not the judge. Record the kinship as said, from
whose point of view it was said, and if a calculation is needed, ask one plain question instead of
publishing a conclusion.

## 7. Somebody else's tree is working notes, not testimony

- Open the tree's "Sources" tab before counting it as independent evidence. If it says
  `Geni World Family Tree`, it may be your own tree come back through third hands.
- Open the "Revisions" tab: a surname can be changed several times in a tree without a source or a date ever
  being added.
- Circular confirmation: a profile whose only "source" is an exported tree is not documented, even when the
  links already sit in your graph. The task is to check those links, not to attach more to them.
- In Latvian trees the "maiden name" is often the name of the farm (the Paraugi farm giving "Paraugs").
  Compare with the family's farm in the revision list; if they match, keep it as a variant with a note, not as
  the surname.
- Dates in other trees that repeat an already disproved date from another tree are checked against the
  withdrawn ones before use.
- Geocoders spoil places in imported trees while the original text survives in a note. One nonexistent place
  node appeared dozens of times and glued several distant places together; the farms of one parish
  collapsed into a town; a home village was replaced by the volost centre in many events. Do not trust
  coordinates for persons born before the war; read the original place string.

## 8. Places in a Soviet-era form are given in the grid of the day it was filled in

A person filling in a form names the village in the administrative grid current at the time of filling, not
at the time of birth. Proven twice on different branches:

- "Primerovka" with the name of a volost that existed for only a few years in the 1920s, for a birth before
  the First World War. The real address at the time of birth was a different volost of a
  different uezd.
- "Primerovka, N district" of a city region, which was correct only because for a few years in the 1930s the
  village really belonged to that district.

The register is always older than the form. Before writing to an archive, fix the name of the place for the
year of the event from the published lists of populated places («Списки населённых мест»), or the query is
bound to return a true zero. The same trap works for reforms: a village sat in another volost until about
the turn of the century, and a later reform moved settlements between communes; records
before the reform lie under the old unit.

## 9. Calendars and double dates

- Julian against Gregorian: the difference is constant, 12 days until 28 February 1900 and 13 days from
  1 March 1900.
- A double date in a Lutheran personal register (Estonia) is birth and baptism, not old and new style.
  Checked on a few dozen date pairs from one register: the gaps ranged from none to several months, which no
  calendar produces. Twins had different gaps; some entries were made when Estonia already used the new
  style; and a 12-day gap fell in a year when the calendar difference was already 13.
  Take the first date as birth. A transcription that called these old and new style had to be corrected,
  and the wrong reading would have shifted the dates of dozens of persons.

## 10. Read status words literally

Latvian `Knechts` (farmhand) and `Wirths` (farm owner, host) look alike in old handwriting. Read the word
that is written, and check a doubtful letter against the same letter in neighbouring words by the same scribe.

## 11. Secondary sources without an imprint

A newspaper clipping without the paper's title and date, a typed family list without author, a page from an
unnamed book: such sources give disputed dates only. They can point to a document; they cannot settle one.

## 12. Every negative conclusion names the record genre and the corpus searched

An index covers one genre of record, not all of them. "There are no Primerovs in N uezd" was true for the
parish registers and false for the recruits' service lists, where they appear.

- Right: "he is not in the parish registers of the migrant colony of N-uezd natives in the city, for the
  years those registers cover".
- Wrong: "he is not anywhere".

Check what an archive actually looked at before treating its negative reply as closing the question. One
negative reply did not cover the question asked: the file consulted held lists for a whole province, and the
reply concerned the part for a neighbouring uezd, not the family's. Do not send the same request again to a
door that has answered no, but do not count an answer to a different question.

A negative conclusion is only as strong as the volume actually read. Searching a catalogue for one literal
year missed a file whose title gave a range of years around it.

## 13. Before saying "we do not have this", search your own graph

Agents can write that a name "does not occur in the project" about persons who are in the graph, and such
claims travel into the fact file and the drafts before anyone notices. The check is one
command over the full person file, searching by surname and given name tokens. Lists derived from the graph
(per-person sheets) are incomplete: one man had fewer children on his sheet than in the graph.

Before adding new persons, search by name tokens and by full date across the whole graph, not by an id prefix.
An agent adding a couple of dozen persons from a family list searched by its own id prefix and missed that
the imported tree held the same family under other prefixes and even under names without a surname; most of
them became duplicates. Run the duplicate finder before entering new persons, not after.

## 14. Agent waves: two lessons about stale inputs

- A task description can describe the disk as it was a week earlier. One wave was launched to grep a corpus
  "never read in full"; earlier waves had already read every file, and the quoted source file had
  the line struck through with "done" next to it. Before executing a task that cites an old report or file,
  open the current file on disk and search it, not the quotation in the task.
- Rolling a graph back to a snapshot silently cancels every change made after it: a batch of restored place values
  was lost that way and only a full audit noticed. After a rollback, replay each later step from the log, not
  from memory.

## 15. A letter to a living person is written by a person

A private person owes the family nothing, and a long composed text asks a great deal of them. The agent
prepares the facts and two or three questions; the researcher writes the message in their own words,
briefly, and says plainly that AI helped to prepare it. Archives are different: their correspondence is
formal, and a detailed request works there.
