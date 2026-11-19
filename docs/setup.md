# Setup

What we used, how to install the skills, and how to arrange a project. Versions and limits are as
observed in 2026.

## What you need

| Component | Used for | Notes |
|---|---|---|
| Claude Code (terminal, desktop app or IDE extension) | the agent, subagents, file and shell access | any recent version; plugin commands below were checked on 2.1.328 |
| A project folder under git | the shared memory of all sessions | text is tracked, media are not (see the template `.gitignore`) |
| Your own web browser | sites that need a login or a subscription | you use them yourself, as a normal user; the agent does not log in anywhere |
| Python 3.9 or later | the offline tools in `tools/` (none of them queries a genealogy, archive or library site; `transcribe_audio.py` downloads its speech model once, on first use) | standard library, plus Pillow for image strips |
| `mlx-whisper` (Apple silicon) or another local Whisper | transcribing recorded conversations | the turbo model; file by file |
| LibreOffice (`soffice`) | building `.docx` with real comments from markdown | optional, for books and reports |
| `poppler` (`pdftotext`, `pdftoppm`), `tesseract` with the language packs you need | reading PDFs of inventories, OCR of typescript | OCR output is a lead, never a source |

Hardware: everything ran on a laptop. The large Whisper model exhausted its memory; the turbo model did
not.

## Install the skills

From a clone of this repository:

```bash
claude plugin validate ./plugins/genealogy        # last line: Validation passed
claude --plugin-dir ./plugins/genealogy           # load for one session
```

Or register the repository as a marketplace and install the plugin:

```bash
claude plugin marketplace add ./agentic-genealogy   # the path of your clone
claude plugin install genealogy@agentic-genealogy
```

The skills then appear as `/genealogy:<skill-name>` and Claude loads them on its own when a task matches.
To use single skills without the plugin, copy a skill's directory into `~/.claude/skills/` (all projects)
or `<project>/.claude/skills/` (one project).

| Skill | Use it when |
|---|---|
| `setting-up-a-project` | starting a project or giving structure to a pile of material |
| `starting-a-research-session` | beginning, resuming or closing a session |
| `searching-a-source` | querying any database, index or catalogue |
| `identifying-people` | deciding whether two records are one person |
| `reading-old-records` | transcribing handwriting, typescript or audio |
| `taking-in-new-material` | a new scan, copy, photo or statement arrives |
| `writing-to-archives-and-people` | preparing a request or a message |
| `running-a-research-wave` | dispatching parallel subagents |
| `maintaining-the-family-graph` | changing the data file, GEDCOM, duplicates |
| `checking-privacy-before-sharing` | anything is about to leave the private project |

## Set up a project

Ask Claude to use `/genealogy:setting-up-a-project`, or do it by hand: create the folder tree described in
that skill, copy the starter files from `plugins/genealogy/skills/setting-up-a-project/templates/`
(rename `gitignore` to `.gitignore`), and fill in `CLAUDE.md` and `START_HERE.md`.

The roles of the files:

| File | Role | Read |
|---|---|---|
| `CLAUDE.md` | standing rules, loaded into every session | automatically |
| `START_HERE.md` | state, queue, do-not list | first, every session |
| `JOURNAL.md` | dated history of sessions | last section, every session |
| `DEAD_ENDS.md` | searched and not found; negative replies; dead sites | before any search |
| `OPEN_QUESTIONS.md` | unresolved leads | when choosing work |
| `FACTS.md` | what documents prove | when writing or checking |
| `SOURCES.md` | per-site knowledge for your regions | before querying a site |
| `KNOW_HOW.md` | techniques | when stuck |

Seed your `SOURCES.md` from `docs/resources/` and your `KNOW_HOW.md` from `docs/method/`, then keep them
current: sites change, and your own dated observation beats ours.

## Permissions and safety settings

- Allow read-only shell commands and the project's own scripts; keep deletions and pushes behind a prompt.
  Deletions use literal paths, one target per command: scans and recordings cannot be recreated.
- Do not hand a logged-in browser to agents.
- Keep passwords and login data out of git (the template `.gitignore` excludes the usual file names; check
  yours) and out of agent briefs.
- Back up `Sources/` outside git.

## Limits we ran into

| Limit | Observed | What to do |
|---|---|---|
| Parallel subagents | harness ceiling 20; running agents can fall together on the session rate limit shortly after a second batch starts | batches of 8-10; second batch as the first finishes |
| Web search tool | 200 calls per session, shared by all agents of a wave | give each agent a budget in its brief |
| Web fetch tool on pages in legacy encodings (cp1251) | returned wrong postal addresses | take addresses, shelf marks and numbers from the raw HTML |
| Coordinator context | a wave returns more than can be read with under a fifth of the context left | do not launch a wave late in a session |
| Network location | some state sites did not answer from the project's network | record per site what was observed, with month and year; the official alternative is a written request or a visit |
| Sessions behind logins | some expire overnight, some last days | check before assuming; the researcher logs in again |

## Working languages

The agent works in the family's language. The sources covered in `docs/resources/` are in Russian (pre-
and post-reform spelling), Ukrainian, Belarusian, Polish, Latvian, Estonian and German. Keep search terms in the original
script; keep transliterations as name variants, since each archive and country spells the same surname
differently.
