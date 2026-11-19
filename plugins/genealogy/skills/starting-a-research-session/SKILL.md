---
name: starting-a-research-session
description: Use when beginning or resuming work in a family-history project, before any search, edit or answer about ancestors, and again when closing the session - especially when tempted to search right away, when a task description may be stale, or when asked "do we have anything on X"
---

# Starting a research session

## Core principle

A family-history project lives for months and is worked by many sessions and agents that share no memory.
The files are the memory. A session that searches before reading them repeats closed work, and a session
that ends without writing them loses what it found.

## Before the first action

Read in this order. Do not search, edit or answer before step 4.

1. `START_HERE.md` - state of the project, what waits for whom, the do-not list.
2. The last section of `JOURNAL.md` - what the previous session did and where it stopped.
3. `DEAD_ENDS.md` - everything already searched without result, the negative archive replies, the dead
   and repurposed sites. Read the sections that touch today's task completely.
4. `OPEN_QUESTIONS.md` - the entry for today's task, if there is one.

Then check that the description of the task matches the disk. Task descriptions and open-question lines go
stale: a brief may describe the project as it was a week ago. Before acting on "X is missing" or "Y was
never searched":

- search the family graph for the person (given name and surname across the whole file, in every
  spelling and script: Пётр, Петр, Pyotr, Petr; then by full date). A hit under an imported record is a
  duplicate candidate: note it, do not merge in passing;
- search `FACTS.md` and `JOURNAL.md` for the place, the shelf mark, the site;
- only then say "the project does not have this".

Check `git status`. It must be clean before the first edit; if it is not, find out whose changes they are.

When the ledger already closes what you were asked to search, do not repeat the search because it was
asked for. Cite the entry (date, corpus, spellings, control), say what would reopen it and what next to it
is still open, and note the repeated request in the journal.

## During the session

| Event | Where it goes, at once |
|---|---|
| A fact proven by a document | `FACTS.md`, with the shelf mark and the confidence |
| A search without result | `DEAD_ENDS.md`, worded with genre, corpus, years, spellings tried, date |
| A blocked site | `DEAD_ENDS.md` as BLOCKED, never as "nothing found" |
| A question nobody can answer today, or a finding that needs a decision (a probable duplicate, a conflict) | `OPEN_QUESTIONS.md`, with what would answer it and who can; a line in the entry file's queue |
| A technique that cost time to find | `KNOW_HOW.md` |
| A new site or a change in a known site | `SOURCES.md` |

Write each entry when it happens. Findings held in context until the end are lost when a connection drops.

Two documents disagree: record both values and the disagreement. Never smooth a disputed date without a new
document.

## Closing the session

1. Add a dated section to `JOURNAL.md`: what was done, with numbers; what changed in which file; what is left.
2. Update `START_HERE.md` if the state or the queue changed. Remove open-question lines that were closed
   today: a stale line costs the next session a repeated search.
3. Run the graph checks if the graph changed (see the `maintaining-the-family-graph` skill).
4. Commit with an explicit list of paths and a message that says what changed.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Searching first, reading the ledger later | Closed searches are repeated |
| Trusting the task description over the disk | Work is planned on a state that no longer exists |
| "We have nothing on this person" without searching the graph | The person is in the graph under another spelling; the same work is done twice |
| Closing a question in the facts file but leaving the open-question line | The next wave reopens it |
| Writing the journal from memory at the end | Steps are missing from the record, and after a rollback the later steps are lost |
