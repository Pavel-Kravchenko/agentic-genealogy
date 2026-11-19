# The approach

How we run family-history research with Claude agents, and why it is organised this way. The details of
each part are in `docs/method/`; the per-site knowledge is in `docs/resources/`.

## What the work looks like

A family asks who their people were. The material is scattered: a few certificates and photographs at
home, memories of the oldest relatives, parish registers and revision lists in archives of several
countries, war and repression databases, other people's online trees. Most of it is handwritten, in
several languages and scripts, indexed badly or not at all.

An agent is good at a large part of this: reading catalogues and finding aids, running many spelling
variants through an index, reading a register page line by line, keeping a ledger, cross-checking a claim
against two hundred pages of notes. It is bad at knowing what it does not know: an empty answer from a
blocked site looks to it like "no such person", and a record with the right name looks like the right
person. The method below exists to contain those two failures.

## Six principles

1. **The document comes first.** A fact is what a document says, with its shelf mark. Memory, other
   people's trees and inference are recorded as what they are. When two sources disagree, both values
   stay until a new document decides.

2. **The files are the memory.** Sessions and agents share nothing except the project folder. One entry
   file says where things stand; a journal records each session; and five ledgers hold what is known
   (facts), what was searched in vain (dead ends), what is still open (open questions) and how each
   source behaves (sources, know-how). A session reads them before it searches and writes them as it goes.

3. **Three outcomes, not two.** Every search ends in a result, a true zero or a block. A zero is trusted
   only when the search is proven to have run, and it is worded with the record genre, the corpus, the
   years and the spellings, because that is all it closes.

4. **Names are not identifiers.** Identity is proven by a document or by household, parish and confession
   agreeing; unproven identity stays as two persons with a weak link.

5. **Polite access.** Where a site's terms of use and robots rules allow it, an agent may read its public
   pages the way a visitor does: one site at a time, one request at a time, slowly, stopping at the first
   refusal. Checking those terms, and the law that applies to you, is your responsibility; when in doubt,
   use the site yourself in your browser. Sites behind a login, a subscription or a
   captcha are used by the researcher personally, in their own browser. A refusal, a captcha or a paywall
   is where the agent stops and a person decides what happens next.

6. **People decide.** The owners of the family story decide what a document changes, what is said about
   the living, and what is published. The agent prepares the analysis and asks. Letters to private people
   are written by a person. Deleting, pushing, publishing, sending, paying and logging in are the
   researcher's decisions.

## The loop

```
read the ledgers
   -> pick a lead from the open questions
      -> establish the place and jurisdiction for the year of the event; list the spellings
         -> search (one site, one thread), prove the search ran
            -> read the image, transcribe verbatim, verify what will be used
               -> analysis without edits: what it says, what it changes, what stays open; "enter it?"
                  -> on a yes: scripted entry with snapshot and checks
                     -> update facts, dead ends, open questions, journal; commit
```

When many independent leads exist, the search step fans out into a wave of subagents, each with its own
site and its own report file, and the coordinator reads the files and writes the synthesis.

## What agents did well, and where they failed

Observed over several months of one project:

- They read finding aids and inventories that the archives publish for reading, page by page, and ran many
  spelling variants of a query.
- They found the dead and repurposed domains that search engines and language models keep recommending.
- They produced false zeros in numbers, until "prove the search ran" became a rule.
- They merged namesakes on a matching age and recomputed a kinship that a living relative had stated
  correctly.
- They write long, composed letters. A message to a private person is therefore written by the researcher,
  who says plainly that AI helped to prepare it; the agent supplies the facts and the questions.
- They died mid-task when the API connection dropped, taking unwritten findings with them, until "report
  file first, append at once" became a rule.

Each rule in the skills is there because its absence cost something. The catalogue of these costs is
`docs/errors-and-solutions.md`.

## What still needs a person

Logging in, solving a captcha, paying an archive, sitting in a reading room, photographing a page
properly, telephoning a registry office, talking to the oldest relative, writing to a stranger, and
deciding what may be said about the living. The method treats this as a queue with a clear hand-over, not
as an obstacle to route around. See `docs/resources/needs-a-human.md`.
