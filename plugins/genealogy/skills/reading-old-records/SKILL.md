---
name: reading-old-records
description: Use when transcribing or reading a photographed or scanned handwritten record (parish register, revision list, census sheet, letter, certificate), a carbon-copy typescript, or an audio recording of a relative - especially when text is illegible, when a scan came through a messenger, or when a reading must carry a name or a date into the family record
---

# Reading old records

## Core principle

The bottleneck is resolution, not the model. No tool repairs a page that was compressed before it reached
you; a new photograph does. And a transcription reproduces the document: it never corrects, completes or
interprets it.

## Step 1: audit the image before reading

- Long side exactly 1280 px is the signature of messenger compression ("sent as photo", not "as file").
  A register page at 1280 px leaves about 40 px per line of cursive; a line needs about 100 px of height,
  a page about 2,500 px on the long side.
- If the image is under that: read what can be read, mark the rest, and ask for a re-shoot. Say exactly how:
  one page per frame, daylight without flash, camera parallel to the page, sent as a file or through a
  cloud link; with the neighbouring pages and the title page of the volume, which date the entry and
  show the clerk's hand.
- Fix orientation by the EXIF tag (`PIL.ImageOps.exif_transpose`), not by rotating pixels with a tool that
  leaves the tag in place.
- Check for duplicates by checksum before transcribing: a messenger album saves the same picture twice
  under two names.

## Step 2: read in strips

Do not read a whole page at once. Cut it into overlapping horizontal strips (8 strips with 20% overlap
works for a register page), apply autocontrast, enlarge each to about 1,500 px wide. The overlap shows
each boundary line twice so that no line is lost. For a hard word, crop the single line at full resolution,
lighten dark lines, and enlarge a doubtful word 8 to 12 times. The repository's `tools/local/htr_prep.py` does the cutting.

## Step 3: transcribe verbatim

- Keep the original spelling, abbreviations, line order and column structure.
- Unreadable text: `[illegible]`; an uncertain reading: the reading followed by `[?]`; a digit that may be
  one of two: `189[7/9]`. Never fill a gap from what "must" be there or from what such entries usually say.
- A transcription is never brought into line with another document. When the certificate says 1899 and
  the register digit is unclear, the transcription keeps the unclear digit and the disagreement is
  recorded as a comparison in the notes.
- A reading supplied by someone else, with no image in front of you, is their reading: label it so and
  do not pass it on as verified.
- Your own remarks go in a separate notes section, never inside the transcription.
- A tabular record (revision list, census sheet) is transcribed as a table, with the printed column
  headings, because the meaning of a number is its column.
- Frame number is not sheet number, and neither is the file number. Record all that you know.

## Step 4: verify what will be used

Every name, date and place that goes into the family record is checked a second time:

- Read the page independently two or three times (fresh context each time) and compare. Where the readings
  agree, the confidence is real; where they differ, the difference marks exactly the words that need a
  human or a better image. Do not vote: resolve from the image or leave it marked.
- Check place names against a gazetteer of the period and names against the same clerk's other entries.
- Printed year on a form with a handwritten last digit: date the sheet by the file or a duplicate copy.
- Watch for look-alike digits in the clerk's hand (an open-looped 4 read as 7) and re-check years.

## Typescript and OCR

Carbon copies of mid-century inventories defeat OCR in stable ways: `3` becomes `5` or `8` in numbers,
`Ж` becomes `Л`, and a smeared line drops out entirely. Search with tolerant patterns, restore a file
number from its neighbours (inventories are sequential), and check by eye on the page image everything
that goes into a letter or a request.

## Audio

- A conversation with a relative is recorded only with the person's knowledge and consent.
- Transcribe locally. The large Whisper model can exhaust memory on a laptop; a smaller variant (for
  example turbo) is much faster and needs far less memory. Transcribe one file at a time.
- Do not edit the transcript. List recognition errors and discrepancies with documents in a separate
  report; do not reconcile them.

## Coverage

What is transcribed and what is not is counted by checksum, with file names normalised to Unicode NFC
before comparison (macOS returns names decomposed, and a name with й or ё then never matches).

## What not to do

- Do not train or install a custom handwriting model for a mixed pile of hands: it pays off from hundreds
  of pages of one hand.
- Do not run `pdftotext` on photographed letters and report "no text": there is no text layer.
- Do not summarise in place of transcribing. The report retells; the transcription reproduces.
