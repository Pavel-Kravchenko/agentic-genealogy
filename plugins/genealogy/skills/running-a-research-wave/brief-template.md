# Brief for agent <NN>: <one-line goal>

All names below are from an invented example family. Replace everything in angle brackets.

## Goal

Find <record genre> for <person: Ivan Petrovich Primerov, born about 1874, village Primerovka,
Obraztsovskaya volost, N uezd, <province>> in <corpus/site>.

**Done when:** the report file ends with one of FOUND / PARTIAL / EMPTY / BLOCKED and, for FOUND and
PARTIAL, every finding has its shelf mark, sheet or frame number and a saved image or a verbatim quotation.

## Your files

- Report (create it as your FIRST action): `<project>/Reports/<wave>/<NN>-<topic>.md`
  First lines:
  ```
  # <NN>. <topic>
  **Status:** IN PROGRESS
  Sections: 1 What was asked - 2 What was searched - 3 Findings - 4 Zeros and blocks - 5 Proposed changes
  ```
- Working folder for saved files: `<project>/Work/<wave>/<NN>/`
- Append every finding to the report the moment you have it. Write the report section by section. Never
  hold results in memory to write at the end, and never write the whole file in one command.

## What is already known (do not rediscover)

- <facts from FACTS.md that concern this lead, each with its source>
- <spellings already known: Примеров, Примерав, Прымеров, Primerow>

## What is already closed (do not repeat)

- <entries copied from DEAD_ENDS.md: site, genre, years, spellings, date>
- <negative archive replies and exactly what each covers>

## How to search <site>

- Query: <the site's public search page, used as a visitor uses it>. The researcher has checked that this
  site's terms of use and robots rules allow automated reading; if the site says otherwise, stop and report
  BLOCKED.
- Pace: one request at a time, slowly. Stop at the first refusal and do not retry. This site is yours
  alone in this wave.
- Control query: run `<common surname>` first; expect about <n> results. If the control fails, stop:
  the outcome is BLOCKED, not EMPTY.
- Block signature: <status, "a very small page" or "a login form", marker text>. True zero: <the site's own nothing-found marker>.
- Search one word and filter locally. Try the spelling variants listed above. Test two case forms before
  cycling through cases.
- Names and dates only from the image, never from the index or OCR. Where the source has no image,
  quote the database fields verbatim and mark the finding "database field only".
- Verify every saved file by its format signature (JPEG `FFD8` ... `FFD9`, PDF `%PDF`).
- A record is a match only if <birth year, place, patronymic> agree with the facts above. List every
  rejected namesake with the reason.

## Do not

- Do not open or cite these domains (dead, or no longer the institution's site): <list>.
- Do not touch these sites (reserved for other agents or for the human): <list>.
- Do not use a logged-in browser. Do not log in, register or pay. Do not try to get past a captcha, a
  login or a block.
- Do not edit the graph, the facts file, the ledgers or any shared file. Put proposals in section 5.
- Do not commit. Do not delete anything except your own temporary files, by literal path, one per command.
- Do not start background jobs or other agents. Every tool call synchronous, with a timeout of <n> seconds.
- Web search budget for you: <n> calls.

## Model

<The strongest model for coordination and hard handwriting | a mid-size model for routine reading and single-site searches.>
If a page is beyond you, report the frame and stop; the coordinator decides who reads it.

## Report sections

1. **What was asked** - one paragraph.
2. **What was searched** - table: site/corpus | genre | years | spellings | queries run | control result.
3. **Findings** - each: verbatim text, shelf mark, sheet/frame, saved file, confidence, which namesakes
   were excluded and how.
4. **Zeros and blocks** - each worded with genre, corpus, years, spellings, date; what it closes and what
   it does not.
5. **Proposed changes** - additions and removals for the graph and the ledgers, each with its evidence.

Final line of the report: `**Status:** FOUND | PARTIAL | EMPTY | BLOCKED`.
