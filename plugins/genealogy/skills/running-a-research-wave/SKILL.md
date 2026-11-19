---
name: running-a-research-wave
description: Use when dispatching several subagents in parallel for genealogy searches, transcription or verification, when writing a subagent brief for such work, when a subagent died, timed out or reported failure, or when deciding whether a wave of agents is worth launching at all
---

# Running a research wave

## Core principle

A wave multiplies whatever is in the brief, including its mistakes and its stale facts. The coordinator's
work is the brief before the wave and the disk after it. An agent's report is a claim; the file it wrote
is the result.

## Before launching

1. **Is a wave warranted?** Launch one only for leads listed in the open-questions file that are
   independent of each other. Leads that arrive in a message are first reconciled with the open
   questions and the dead-ends ledger: narrow each to the part that is still open, and drop a lead with
   nothing open and machine-searchable left. When no such directions remain, a wave produces repeated
   zeros. Do not launch with less than a fifth of your own context left: you must still read the
   results. Asked to launch anyway, write the briefs to disk and start the wave from a fresh session;
   say so plainly, deadline or not.
2. **Clean the open-questions list and compare the task list with the disk.** A stale line becomes a
   wasted agent.
3. **Only sites whose terms of use and robots rules allow automated reading, checked by the researcher
   before the wave. One site, one agent, one request at a time, slowly; stop at the first refusal.** Never
   give two agents the same domain.
4. **No logged-in browser for agents.** Sites behind a login, a subscription or a captcha are not part of
   a wave. Leads that need them go to the human queue ("Waits for the researcher" in the entry file), and
   the researcher works them personally.
5. **Take free report numbers from a directory listing**, not from memory.
6. **Concurrency.** Batches of 8-10. Start the second batch as agents of the first finish. A dying agent
   can leave an empty stub, so reports are written section by section.

## The brief

Each brief stands alone. Put the protocols and the traps into it, not a pointer to them: otherwise agents
rediscover what is known and burn the request budget. Use `brief-template.md` in this skill's directory.
It must contain:

- the goal and "done when";
- input paths, the output path, the exact report file name;
- **report file first**: created as the first action with `Status: IN PROGRESS`; every finding appended
  at once with its shelf mark; written section by section, never the whole file in one command; final
  status FOUND / PARTIAL / EMPTY / BLOCKED;
- what is already known and already closed for this lead, copied from the ledgers;
- the per-site protocol: which public page to use, that the researcher confirmed its terms and robots rules
  allow automated reading, the refusal signature, the control query, and the pacing rule (one request at a time, slowly, stop at the first refusal, never retry in a loop);
- an explicit **do-not list**: dead and repurposed domains by name, closed archives, sites reserved for
  another agent, no commits, no deletions except by literal path, no background jobs, no other agents;
- synchronous tool calls with an explicit timeout;
- the model: the strongest model for coordination and for hard handwriting, a mid-size model for routine
  reading and single-site searches.

Shared limits belong in the brief too: a web-search tool can have one quota for the whole wave, and when
it runs out the other agents lose search without knowing why.

## While it runs and after

- **Check the disk before believing a notification.** A task can report `failed` while its report file is
  almost complete, and report success with an empty file.
- **Never retell a result before the notification has arrived and the file has been read.**
- **Resume a dead agent in its own context** with a message of the form "you died at <step>; on disk there
  is <what>; remaining: <what>". Restarting from zero repeats the reading. On a rate-limit error of the
  model service, wait for the reset, then resume.
- **Verify saved files by format signature.** HTTP 200 and a plausible size do not prove a file: truncated
  images come with status 200, and an HTML page can be saved under a `.jpg` name.
- **Check not only what an agent entered but what it said should be removed and did not remove.** A
  finding without its execution looks closed and is worse than no finding.
- **The coordinator writes the synthesis.** Shared files (facts, dead ends, open questions, graph) have
  one writer; agents write only their own new files.
- **When the scope of a check widens, expect new complaints.** That is the first honest look at data
  nobody examined, not a regression.

## Quick reference

| Situation | Action |
|---|---|
| Agent silent, no notification | Wait; read its report file, not its transcript |
| Status `failed`, file nearly full | Use the file; resume for the remainder |
| Two leads on one site | One agent takes both, in sequence |
| Site needs login or captcha | Not in the wave; goes to the human queue |
| Agent returns "nothing found" | Did its control query run? Is the block signature absent? |
| Agent proposes graph changes | Coordinator applies them by script after reading the evidence |
