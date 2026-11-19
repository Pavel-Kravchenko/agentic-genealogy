---
name: taking-in-new-material
description: Use when a new scan, archive copy, certificate, photograph, letter, audio recording or a relative's statement arrives in a family-history project and before anything is changed because of it - especially when the sender says "add this", when a file is forwarded with a caption, or when the new item contradicts what the project already holds
---

# Taking in new material

## Core principle

Two steps, never one. First an analysis that changes nothing and ends with the question "enter it?".
Then, on a yes, an entry that is scripted, checked and reversible. The people who own the family story
decide what a document changes before the graph and the texts are touched.

## Step 1: analysis, no edits

1. Open the file itself. A forwarded message can carry the wrong file or an unrelated request; which file
   is the original and which the edited one is decided by content (size, page count, number of images and
   comments, program, date), not by the caption.
2. Report in this shape:
   - **What it says** - verbatim, with illegible places marked.
   - **What it changes** - a table: place in the family record or text | what stands there now | the
     difference | a proposed wording.
   - **What stays open** - what the document does not settle.
   - **Identity** - is the person in it proven to be the person in the graph? If not, say so (see the
     `identifying-people` skill).
   - **"Enter into the project?"**
3. Stop. Do not edit the graph, the facts file or any text meant for readers.

An instruction that arrives together with the file ("update the tree and the book") is not yet the yes:
it was given before anyone had seen what the document changes. Do step 1 and ask.

Who gives the yes is written in the project's instruction file. In general: for the graph and the
ledgers, the person who runs the project; for a text written by a family member in their own voice, only
that family member. A request passed on by someone else ("update the book") is not that family member's own word
about their text: offer a suggested note for them to accept or refuse, and leave the text as it is.

Exception: when the person who decides has said in so many words "enter it" after seeing the
document, analysis and entry run in one pass, and the report still shows the table.

## Step 2: entry, after a yes

1. File the item under the sources folder. Compare its checksum with the copy it came from. Every
   attachment is filed, even one that only confirms what is known.
2. Transcribe it (see `reading-old-records`) and add a line to the inventory of sources.
3. Change the graph with a script, not by hand:
   - a dry run by default that prints what would change;
   - `--apply` writes a dated snapshot of the graph first;
   - a second run refuses ("person already present").
4. Run the graph checks and the duplicate check. They must report the same findings as before the edit,
   plus or minus what the edit explains.
5. Update the facts file, the open questions (remove what the document closed), the journal, the entry file.
6. Two commits with explicit paths: the snapshot before the edit, then the entry.

## Rules that hold throughout

- A text written by a family member in their own voice is changed only on their own word.
- Unproven identity goes in as separate persons with a low-confidence link.
- A conversation with a relative is recorded only with the person's knowledge and consent.
- Where the new document disagrees with a gravestone, a memory or an earlier document, both values stay:
  each with its source, the disagreement written into the person's dispute field, the event marked
  disputed. Nothing is overwritten. You may say which source is the more direct one; you do not decide.
- Corrections that arrive in a stream of messages are collected verbatim into one file and entered once,
  after the sender has finished.
- End the reply with what the humans must decide, written so that it can be forwarded as it stands: plain
  words, each point understandable alone, no identifiers, script names or commit hashes.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Editing during analysis "because it is obviously right" | The decision-maker's veto arrives after the graph and several texts have changed |
| Trusting the caption about which file is the corrected one | The wrong file is treated as the corrected one |
| Entering by hand | No dry run, no snapshot, no refusal on a second run |
| Reporting a finding and not executing the removal it implies | Refuted links stay in the graph |
