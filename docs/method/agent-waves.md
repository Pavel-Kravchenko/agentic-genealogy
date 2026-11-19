# Running waves of subagents

A "wave" is a batch of parallel subagents launched by one coordinating Claude session, each with one narrow
task (read one archive inventory, search one database for one family, transcribe one file). This page collects
what made waves work and what made them fail. The examples are composed illustrations; the patterns come from
real work, the particulars do not.

## When a wave pays off, and when it does not

Pays off, only for material the publisher allows to be read this way (check the terms), and never as a copy of a
database:

- many independent, well-defined tasks: one inventory, one site, one surname each;
- reading a published corpus of inventories, split by volume;
- tasks whose result is a file that the coordinator can check.

Does not pay off:

- anything behind a login, a subscription or a captcha: the researcher uses such sites personally;
- several agents on one site: never more than one agent per site;
- tasks taken from a stale open-questions list: a wave can spend a large share of its budget on lines that
  were closed weeks earlier;
- "blind" machine searches once the obvious ones are exhausted. Launch new waves only from the
  open-questions file.

## Before the wave

**Clean the open-questions list first.** Strike lines already closed, then set tasks. A line without a date
and a state is not a task.

**Check a task against the disk, not against a quotation.** One task quoted a week-old summary ("the full text
of the inventories was never searched") as the reason for a new pass. By then earlier waves had read the
whole published corpus as text and OCR, and the source file itself carried a struck-through "DONE" on the same
line. The agent re-read the whole source file before starting and found it; that took less time than the
repeat pass would have. Rule: when a task cites an old report as the source of
something "unread" or "unchecked", grep the file as it is now before running the full pass again.

**Check for a second session.** Two sessions can work on one project at the same time without knowing of
each other. Before a wave: `ls -lt` over the root and the reports folder to see what changed in the last hours;
check the handover file for duplicated section numbers; if a line in the project memory describes work you did
not do, that is the neighbour: merge both, do not overwrite. Often the seam turns out to be a complement, not a
conflict: one session asks a question the other is answering.

**Take report numbers from `ls`, not from memory.** Once a summary got the number of an existing report.
Number with a margin above the current maximum.

**Collect cancelled leads in a separate file** and give it to agents to read first. Each entry saves
someone a repeated search.

**Check the budget.** A wave of a dozen agents can use a noticeable share of a weekly usage limit within an
hour, and the session limit hits all running agents at once. With less than 20 % of the limit or of the
coordinator's context left, do not launch.

## The brief

An agent told "read the brief of the previous wave" skims it. An agent whose task lists the traps themselves
does not lose an hour on them. Checked in reverse: one agent closed a task on which an earlier agent had
stumbled only because the task said exactly where the earlier one had stumbled.

Every brief contains:

1. **The report file first.** Create the report as the first action, before any search, with a header and a
   status line `Status: IN PROGRESS`, and a list of the sections to come. At the end the status becomes FOUND /
   PARTIAL / EMPTY / BLOCKED.
2. **Write section by section.** Append each finding with its shelf mark immediately (`cat >> report <<'EOF'`),
   never rewrite the whole file in one command, hold at most one finding in memory.
3. **The protocols and traps inline**: which query form works on each site, which one silently returns
   nothing, which site gives false zeros now.
4. **An explicit do-not list**: leads already closed, sources known not to exist, and dead or repurposed domains
   by name (several former archive domains are no longer the institutions' sites).
5. **What it may write**: new files only in its own report and work folders. No edits to the graph, the books
   or the shared summary files. Changes to the graph come as a section "Proposals for the graph" (node,
   field, value, source with shelf mark and leaf, confidence).
6. **Tool discipline**: synchronous calls only, with an explicit `timeout` on every Bash call (up to 600,000
   ms); no background runs; `rm` only with a literal absolute path, one target per call; "do not commit" in
   words.
7. **Access rules**: one site, one request at a time, slowly; no logins, purchases or registrations; never a
   logged-in browser; if a site answers 401, 403 or a captcha, write that down and stop.
8. **The negative-result formula**: "not found in corpus X of genre Y, checked over range Z", never "not found".
9. **The end of the report**: status line, proposals for the graph, what remains (with addresses), and a check
   table (what was checked | result with a number). The final message returns a short summary with numbers and
   the report path.

Why each rule exists:

| rule | what happened without it |
|---|---|
| report first, append at once | many agents of one wave died on API errors, several at the same moment (a network outage). Their last lines announced finds ("Major find in the row", "Now writing the report"): the finds existed and were lost. After the rule, restarted agents finished, and some brought the best finds of the wave. |
| section by section, not one final write | dead agents died on "Now writing the full file" with an empty skeleton on disk |
| no background runs | an agent started with `run_in_background` waits for a notification that never comes |
| explicit `timeout` | Bash calls stalled on the 120-second default |
| "do not commit" in words | one agent committed on its own |
| `rm` with literal paths | wildcards, variables and `$(...)` cannot be checked at the permission prompt, and project media cannot be restored. Better: leave temporary files in the scratchpad |
| traps inside the brief | agents re-discovered known traps and burned the request budget |
| image agents: one or two crops per step | image-heavy agents failed more than any other kind, most of all when many ran in parallel |

A page-by-page walk of a long inventory may need more requests than the brief allows. Stop and report; the
coordinator decides whether to continue, at the same pace, or to hand the inventory to a person.

Intermediate files are capital (kept for your own research, not republished). An agent that reuses the leaves saved by an agent of the previous wave needs
a fraction of its budget.

## Access: one site, one agent, one request at a time

- **One site, one agent, one request at a time, slowly.** Never two agents on one site at once. Stop at the
  first refusal and never retry in a loop.
- **No logged-in browser for agents.** Sites that need a login, a subscription or a captcha are used by the
  researcher personally, in their own browser.
- **Tool quotas are shared by the whole wave.** The harness's web search budget is per session, not per
  agent. Budget per wave.
- **Check what was saved by its format signature.** An HTTP 200 and a plausible size prove nothing: truncated
  files come with status 200, and an HTML page can be saved under a `.jpg` name.

## Concurrency ceilings and rate limits

- The harness ceiling was 20 concurrent subagents (observed 2026). Tasks launched above it silently do not
  start.
- Launch in batches of 8-10 and keep the queue explicit.
- Running agents can fall together on the session rate limit shortly after a second batch is started.
  Wait for the reset, then resume.
- Use freed slots. Reports of a wave often open tasks that were not in its plan: read each report as it lands
  and, if it opens a new direction, put an agent on it at once.

## While the wave runs

- **Check the disk before believing a notification.** A task can come back `failed` while its report on disk is
  almost complete. Task status and result are different things.
- **Never retell an agent's result before its notification has arrived and its file has been read.**
- **Resume a dead agent in its own context; do not restart it.** Send it a message by its id: it remembers
  everything, its file on disk is intact, and it continues from the break. Restarting from zero repeats the
  reading. Message
  pattern: "You died at <step>; on disk there is <file, last section>; the coordinator added section K, do not
  delete it, write after it; remaining: <list>." Load the messaging tool before the wave starts. When an agent
  must be restarted fresh, tell it where its predecessor died and what it had done.
- **Do not write off a task because its agent died.** Most restarted tasks finish at the second or third
  attempt.
- **Check not only what an agent entered but what it said should be removed.** See
  `family-graph-and-gedcom.md#apply-scripts-dry-run-first-refuse-to-run-twice`.

## After the wave

- **Shared files have one writer: the coordinator.** Agents create new files only; the coordinator merges their
  proposals into the graph, the facts file and the open-questions file.
- **The coordinator writes the synthesis itself.** Summary-writing agents die when the API is overloaded, and a
  synthesis needs the judgement that the coordinator already has.
- Strike closed lines from the open-questions file the same day, with the date and the report that closed them,
  so the next wave does not pay for them again.
- Expect new complaints whenever a check's scope grows. That is the first honest look, not a breakage.

## Model choice

| role | model class | why |
|---|---|---|
| coordination, synthesis, decisions about the graph, hard handwriting | strongest available | judgement, merging conflicting reports, difficult hands |
| routine reading (inventories, clear hands), single-site searches | mid-size (for example Sonnet) | clear, bounded tasks, many of them |
| mechanical checks (counting, matching ids, checksums) | small or a script | no judgement needed |

## A sample brief

Adapt names, paths and traps. The cast is fictional.

```markdown
# Wave <N>, task <K>: Primerov family in the 1858 revision of N uezd

You are one agent of a wave. Project root: <project>. Working language of the notes: Russian.

## First action
Create `Reports/<wave>/<K>-primerov-revision-1858.md` with:
  - task (one line), date, `Status: IN PROGRESS`
  - the list of sections you will write: Journal, Findings, Proposals for the graph, What remains, Checks
Then append one section at a time with `cat >> <report> <<'EOF'`. Never rewrite the whole file.
Write each finding the moment you have it. Hold at most one finding in memory.

## Read before any search
- `DEAD_ENDS.md` and `FACTS.md`: grep for Primerov, Примеров, Примеровъ, Primerow, Primerovka.
- the section of `DEAD_ENDS.md` on hypotheses tested and dropped.

## Task
Find Primerov households of the village Primerovka, Obraztsovskaya volost, in the 1858 revision
(fond <F>, opis <O>, delo <D>, leaves 1-240). Read every leaf of the volost; list every Primerov
and every Obraztsov with age, household and leaf.

## Known traps (do not rediscover)
- Leaf number = frame number minus 3 in this file.
- References "aus P. N" point to a leaf of part A of the same book, not to the previous revision.
- The scribe's looped capital letter is often misread as a different given name; compare with the
  same letter elsewhere on the page.
- Spelling variants: Примеров, Примеровъ, Примерав, Прымеров. Search all.

## Do not
- Do not search the 1850 revision; it is closed (see `DEAD_ENDS.md`, entry of <date>).
- Do not use these domains: <dead-domain-1> (no longer the institution's site), <dead-domain-2> (offline).
- Do not edit anything in `Graph/`, `For-the-family/`, or the ledgers in the project root.
- One request at a time, slowly. Do not log in, register or buy. Do not use a logged-in browser.
  On 401/403/captcha: record it, stop that site, do not retry.
- Do not run anything in the background. Give every Bash call an explicit timeout (<= 600000 ms).
- `rm` only with one literal absolute path. Prefer leaving temporary files in your work folder.
- Do not commit.

## Tools
- Python: <path to interpreter>. Normalise file names and paths with unicodedata.normalize("NFC", ...).
- Saved files go to `Work/<wave>/<K>/`, not /tmp. Check each file's format signature after saving.
- Images: one or two crops per step; journal entry after each name read.
- Graph lookups (read only): search by given name + surname across the whole person file, never by id prefix.
- Request limit: about 40 requests, one at a time, and only on a site whose terms of use allow automated
  reading. If the work needs more, stop and report; the coordinator decides.

## Report ending
- Status line: FOUND / PARTIAL / EMPTY / BLOCKED.
- Proposals for the graph: node | field | value | source (shelf mark, leaf/frame, verbatim extract) | confidence.
- What remains, with addresses.
- Checks: what was checked | result with a number (e.g. "leaves read: 240 of 240").
- A negative result names the corpus, genre and range read.
- Final message: three-line summary with numbers and the report path.
```
