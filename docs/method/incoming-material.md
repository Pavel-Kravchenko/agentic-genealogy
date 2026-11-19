# Taking in new material

What happens when something new arrives: an archive copy, a scan from a relative, a photograph, an e-mail
with a recording, or a relative's spoken statement. The procedure has two steps, and the first one changes
nothing. The examples are composed illustrations; the patterns come from real work, the particulars do not.

The reason for the split: the person who decides settles what a document changes **before** the graph and the
summary files are touched; and a change made by a script with a snapshot can be checked and
undone.

## Step 1: analysis, no edits

Open the file itself first. A forwarded message can carry unrelated requests and the wrong attachment: a
message can ask for one thing while its attachment is another. If the file does not match the message, do the main work on what arrived and ask for the right file under "needs you".

When two versions of a document arrive (an original and one with corrections), decide which is
which by content: size, number of images and comments, the program that made it, its date. Not by what the
message says. In one case the file called "edited" was the original, and the corrections were in a much smaller
file from the day before. Look for the second file in the same download folder, and state the mapping in the
first report.

The analysis has four parts:

1. **What it says, verbatim.** A transcript of the relevant lines with the shelf mark and leaf
   (`fond <F>, opis <O>, delo <D>, leaf N`), unreadable parts marked `[?]` or `[illegible]`. See
   `transcription.md`.
2. **What it changes.** A table: place (person, chapter, date) | what the book or graph says now | what the
   document says | proposed wording for the person who decides.
3. **What stays open.** Questions the document raises or does not settle.
4. **"Enter it into the project?"** Asked, not assumed.

Nothing in the book changes without the explicit word of the person who decides. An identity that the
document does not prove stays as separate nodes.

If a relative reports "X is missing on the sheet", first look up X in the full person file and extract the text
of the printed sheet. On a tall ancestor sheet a sibling can stand far from the brothers and sisters; then the
answer is an explanation, not an edit.

Exception: when the person who decides says "enter it" directly, analysis and entry are one step, and the
book is changed by that decision.

## Step 2: entry, after consent

1. **File the original.** Copy it into the sources folder and compare its `md5` with the copy in the download
   or "to sort" folder. Every attachment goes in, even one that only confirms what is known.
2. **Transcribe and inventory.** A transcript for text; for photographs an inventory line with captions
   verbatim and unreadable parts marked `[?]` or `[illegible]`.
3. **Graph script.** A small script kept with the batch: a dry run without a flag, `--apply` with a snapshot of
   the graph, and a second run that refuses ("node already exists"). Search for duplicates across the whole graph
   before adding nodes. Details in `family-graph-and-gedcom.md`.
4. **Checks.** The structure check and the duplicate finder must give the same findings as before the edit.
5. **Journal.** A dated section in the facts file, the open-questions file, the work journal and the
   start-here file.
6. **Two commits.** First the graph snapshots taken before the edit, then the entry itself. Name the paths
   explicitly; never stage the whole tree, other people's untracked work may be lying in it.

Corrections that arrive as a series of messages are collected verbatim into one file and applied by one
script, followed by one rebuild, after the sender has finished.

## What the reply contains

- what changed, with numbers;
- the places in the book that the person who decides has to settle;
- for that person: the updated `.docx` and the rebuilt ancestor and descendant sheets, with the list of files to
  forward;
- "needs you": what only the researcher can do (a decision, a missing file, a re-shoot).

## Spoken statements and memories

A relative's statement is material like any other. It is written down verbatim with date and speaker, and it
decides kinship where documents are silent. Where it disagrees with a document (a date on a gravestone against a
register, a remembered year against a certificate), both are kept and printed; the disagreement is not
smoothed. Recordings, made with the consent of everyone recorded, follow `transcription.md#transcribing-audio`; the transcript is never edited.
