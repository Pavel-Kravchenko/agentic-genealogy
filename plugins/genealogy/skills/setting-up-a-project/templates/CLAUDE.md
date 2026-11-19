# <Project name> - rules for Claude

<Two lines: what this project is, whose family story it is, the working language.>

**Session start:** `START_HERE.md`, then the last section of `JOURNAL.md`. `DEAD_ENDS.md` before any search.

**Git:** `git status` clean before the first edit; commit after checks, with an explicit list of paths
(never `git add -A`). Media are not tracked.

**The family's rules (do not re-litigate):**
- Living people: <year of birth only; children by given name only; no patronymics or dates unless they
  supplied them>.
- <Whose voice the book or memoir is in>; its text changes only on that person's word.
- Where a document and a gravestone or a memory disagree: <keep and print both>.
- <Any rule on shelf marks in reader-facing text, units, references between chapters>.

**Facts:** the document comes first. Kinship stated by a living relative is recorded as stated and not
recomputed. Never smooth a disputed date without a new document. Invent nothing: when there is no source,
say so.

**Scripts:** normalise file names and paths with `unicodedata.normalize("NFC", ...)`. Find people in the
graph by given name and surname across the whole file, not by id prefix. Run the duplicate check before
entering anyone.

**Subagents:** report file as the first action, appended section by section; no background jobs; a
logged-in browser is never handed to agents; agents read only sites whose terms of use and robots rules
allow automated reading; one site, one agent, one request at a time, stop at the first
refusal; sites that need a login or a subscription, or that do not serve automated requests, are used by
the researcher personally; at most <8-10> at once; resume a dead agent in its own context. A new wave only
for leads in `OPEN_QUESTIONS.md`.

**Tools:** <interpreter path; audio transcription tool; which sites the researcher uses only in their own browser>.

**Decisions for the researcher:** deleting, pushing, publishing, sending, paying, logging in and rewriting
history are done only on the researcher's explicit word.
