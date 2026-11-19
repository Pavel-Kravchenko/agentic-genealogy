# Transcribing handwriting and audio

How the project turned photographs of handwritten documents (parish registers, letters, a family notebook,
questionnaires, certificates) and voice recordings of relatives into text that can be cited. The examples
are composed illustrations; the patterns come from real work, the particulars do not. Numbers that describe
tools, cameras and messengers are as observed in 2026.

## The bottleneck is resolution, not the model

In a family corpus, **most page images had a long side of exactly 1280 px**.
That is the signature of a messenger compressing an image sent "as a photo" (observed with Telegram and
WhatsApp in 2026). A parish register page at 1280 px gives about 40 px per line of cursive. The transcripts
made from these images carried many `[illegible]` marks.

No software repairs this. Re-photographing does.

Targets used from then on:

| what is photographed | long side, minimum | good |
|---|---|---|
| A4 sheet (certificate, letter, questionnaire) | 2500 px | 3500-4000 px |
| register page, A3 | 3500 px | 5000 px |

Rule of thumb: one line of cursive needs **at least 100 px of height**. Transkribus asks for at least
300 dpi, which is about 2500 px on A4.

Check resolution before reading anything. A small script that prints, per file, the long side and a verdict
(good / tolerable / re-shoot) and writes the re-shoot list to a file saves hours: every file on that list
will produce its own crop of illegible marks.

PDFs from a home archive can be the best material in the corpus: scans at 200 ppi can be better than phone
photographs that went through a messenger. Extract them without recompression: when a page holds exactly one raster image, take it out as is (`pdfimages -all`);
when the page is vector or made of several pieces, render it (`pdftoppm -r 300`). A pixel threshold tuned for
phone photographs will mark these PDF pages "tolerable"; ignore the threshold for them. Do not run letters
through `pdftotext`: scanned PDFs have no text layer.

## Sending files: where most resolution is lost

| channel | how to send |
|---|---|
| Telegram | only "Send as file". On desktop untick "Compress image"; on iPhone choose "File" in the attachment menu, not "Photo". Otherwise exactly 1280 px. |
| WhatsApp | only as "Document". Ordinary sending compresses even more. |
| AirDrop, Google Drive, Yandex Disk, e-mail | no compression, send as is. |
| iCloud Photos with "Optimise storage" | check that the original is exported, not the preview. |

HEIC (the iPhone default) is fine; convert it on the computer (on macOS `sips` does it).

Keep the file names the relatives' devices gave. Transcripts and the media list cite documents by file name,
and renaming breaks every link already written. Put each new batch in its own folder named by content and
date of arrival.

## How to photograph a page

A 12-megapixel phone camera gives 4032 x 3024 px, about 350 dpi when the page fills the frame. That is enough.

- One page per frame. A whole open book in one frame drops to about 245 dpi and cursive starts to break up.
- The page fills the frame. Pixels spent on the table are lost to the text.
- Camera parallel to the sheet, straight from above. An angle gives a trapezoid and slanted lines.
- Flatten the sheet (glass, rulers along the edges). The hump in the middle of a book blurs exactly what lies
  in it.
- Diffuse light, flash off. A flash reflection on glossy paper or ink eats a whole line. A window on a cloudy
  day or two lamps from the sides work best. No shadow of the photographer on the page.
- No filters. "Document", "black and white" or "enhance contrast" modes in scanner apps turn pale ink white.
  Contrast can be raised later, reversibly, by a script.
- Do not crop or rotate on the phone. Let the computer rotate by EXIF.

A flatbed scanner beats a phone: 400-600 dpi, "colour photo" mode (not "text", not "document"), no automatic
contrast, saved as TIFF or PNG, or JPEG at maximum quality.

## EXIF orientation: transpose, do not rotate

Phone photographs of a notebook typically carry **EXIF orientation 6**. A note saying "all frames are rotated
by 90 degrees, rotate them with `sips -r 90`" is wrong. `sips -r` rotates the pixels but keeps the
orientation tag, so a viewer rotates the image a second time.

The correct step is `PIL.ImageOps.exif_transpose`: the page stands up as a 3024 x 4032 portrait with
horizontal text and needs no further turning.

## Reading in overlapping strips

On images that cannot be re-shot, cutting the page helps. The preparation script
(`tools/local/htr_prep.py`) cuts each page into **eight horizontal strips with 20 % overlap**, raises the contrast automatically and stretches each strip to
1500 px wide. It adds no pixels, but the model's vision encoder spends many more patches on the same letter.
On a 1280 px register page, one strip showed the names of the parish clergy, which the earlier whole-page
transcript did not contain at all. The 20 % overlap shows a line at a strip boundary twice, so it cannot be
lost.

What worked best for difficult handwriting, in falling order of yield:

1. `exif_transpose` instead of rotating pixels.
2. One line per crop at full resolution (about 2000 px wide); disputed words enlarged 8 to 12 times. Dark lines
   brightened separately. Reading the whole page at once is clearly worse.
3. For overwritten strokes: a threshold sweep and a stroke-width map (distance transform). This separates a
   later retracing from the original writing. On one page it showed that an age figure was two digits written
   over each other, the outer one written second.
4. Compare a doubtful letter with the same letter in neighbouring words of the same hand. That is how "d" and
   "b" were told apart in one disputed verb.

For agents reading images: one or two crops per step, with a pause, and a journal entry after each name read.
Image-heavy agents failed more often than any other kind (see `agent-waves.md`).

## Marking conventions

- `[?]` after a word: read, but unsure.
- `[illegible]`: not read.
- Pre-reform Russian spelling is kept as written (`ѣ`, `і`, final `ъ`).
- Names, villages and volosts are **never corrected to something plausible**. Write what is visible and mark it
  `[?]`.
- What is marked "probably" does not go into the book text. This discipline saved several readings in the
  three-reader test below.
- An honest negative is a result. Of the dark places in one notebook, a few were closed as unreadable. One place
  has no coherent reading: the sentence is unfinished in the original. There is no coherent reading to find.

## Several independent readings, and what their disagreement tells

A family notebook was read three times:

| reading | how | result |
|---|---|---|
| first | continuous, whole text | full draft |
| second | two independent readers | dozens of disagreements |
| third | narrow, only the dark places | most dark places resolved |

**The third reader corrected the second where the second was certain.** In a few places the second reader
had overwritten the first reading with the confidence mark "firm", and in each of them the first reading was
right.

Rules that follow:

- A reader's confidence is not a document. A disagreement between two readings is closed by a third look at
  the image, not by vote and not by seniority.
- Commercial HTR is a second opinion, never a replacement. For pre-1917 Russian registers one often
  suggested service is Transkribus (Russian models for late 19th and early 20th century hands). A cloud
  service receives the images you send. Do not send documents about living people without their consent, and
  check where the provider stores data. The places where its output disagrees with yours are the list of places
  to look at again by eye.
- A looped capital letter of one scribe was read by unfamiliar eyes as a different, common given name more
  than once. Check every such reading against the same letter elsewhere on the same page.
- Before rejecting another researcher's reading of a record, open the image yourself. In one case a genealogy
  site held a link to exactly the right frame.

## Check place names against a gazetteer

Read is not the same as existed. When the strip pipeline was tested on a register page, the letters that
emerged did **not** match any known volost of the two uezds concerned. Check every village and volost name
against a gazetteer or a list of administrative units for the period before it enters the graph.

## Two traps in reading the content

**A double date in a Lutheran personal register was birth and baptism, not Old Style and New Style.** Checked
on the date pairs of one parish book. The calendar difference is constant: 12 days, 13 from 1 March 1900. The
gaps in the book ranged from none to several months, which is not a calendar. Two arguments decide it: some
entries were made when the country already used the New Style, so a double date by calendar was impossible;
and a "matching" pair of +12 days fell where the difference was already 13. Take the first date as the birth. The error would have been
expensive: dozens of persons' dates would have shifted, and the earlier transcript had in fact asserted Old
Style / New Style.

**Two women of the same name are told apart by household, not by age.** Age in a questionnaire is weak
evidence by design; household, parish of registration and religion are strong (the case is in
[evidence-rules.md](evidence-rules.md), section 3).

## Transcribing audio

Record a conversation only with the knowledge and consent of everyone who speaks in it, and say at the start of
the recording that it is being recorded. The law on recording differs from country to country; check the one
that applies to you.

Transcribing locally, what failed: `whisper-large-v3` **brought the machine down** by exhausting its memory, and the model cache was
left holding only the model's `config.json`, because the download never finished.

What worked:

- A Python 3.12 virtual environment (`uv venv --python 3.12`, then `uv pip install mlx-whisper`), model
  `mlx-community/whisper-large-v3-turbo` (1.6 GB download).
- `language="ru"`, an `initial_prompt` listing the family surnames and place names you expect, and
  `condition_on_previous_text=False`. Without the last setting one recognition error is carried through the
  whole file.
- **One file at a time.** A smaller model variant (turbo) transcribes much faster and needs far less memory
  than the large one. Each result (`.txt` with timestamps in seconds, and `.json`) is written to disk at once, and a rerun skips files already
  done.
- Video: extract the sound first with `ffmpeg -vn -ac 1 -ar 16000` to WAV, then the same.

**Never edit the transcript.** It is a source. Recognition errors (misheard surnames, place names) are listed
in the report that accompanies it, with the timestamp. Where a relative's account differs from a civil register
or another document, write the discrepancy out side by side; do not reconcile it.

**Recordings forwarded by e-mail can arrive with two extra bytes.** `.m4a` files forwarded through one
web-mail service would not open in `ffmpeg` ("moov atom not found") or `afinfo`, and `file` called them "data".
The cause was `0d 0a` (`\r\n`) in front of the `ftypM4A` signature at the very start of the file, a forwarding
artefact. `tail -c +3 file > copy` repairs it; the content is intact. Check with `xxd -l 16` before blaming the
recording or the model. Earlier recordings from the same phone were clean: it depends on the forwarding path
(observed 2026).

## Coverage: what has been transcribed

Counting what remains untranscribed is a script, and it has two traps.

**Count by checksum, not by file name.** An inventory of the remainder sent a batch of "untranscribed"
frames to work; all of them were byte-identical duplicates of frames already read. When
Telegram forwards an album, a photo can land on disk twice, once named with a sequence number
(`photo_6_<date>_<time>.jpg`) and once with a timestamp (`photo_<date>_<time>.jpg`). A name comparison does
not see the pair; `md5` does.

**Normalise file names to NFC before comparing.** macOS returns file names in decomposed Unicode (NFD): the
Cyrillic letters `й` and `ё` are a base letter plus a combining mark, while the same letters in a transcript are
precomposed (NFC). Without normalisation any name containing them is **never** found in the text. The coverage check falsely
reported as untranscribed a file that was discussed two paragraphs earlier in the same document. Details and the one-line fix are in
`family-graph-and-gedcom.md#file-names-on-macos-nfd`.

Two more conventions: a transcript reproduces the document, a report retells it; photographs get an inventory
entry (who, where, captions verbatim), not a transcript. A negative result ("not mentioned") is only as strong
as the volume that was read, so state the range of pages or frames.

## What not to install

- Kraken, eScriptorium, TrOCR: training your own model pays off from hundreds of pages in **one** hand. A family
  archive is a mix of many hands.
- Do not re-shoot what the resolution check already marks "good" (archive copies are often already
  large enough).
- Do not delete the working strips until the transcript has been moved into the sources folder.
