# Local tools

Four tools that run on the researcher's own machine and query no website; `transcribe_audio.py` downloads
its speech model once, on first use. All paths are arguments.

| tool | what it does | requirements |
|---|---|---|
| `htr_prep.py` | Resolution verdict for scans (`audit`) and overlapping enlarged strips of each page (`prep`) | Python 3.9+, Pillow; poppler for PDF; macOS `sips` for HEIC |
| `transcribe_audio.py` | Transcribes recordings with mlx-whisper, file by file | Apple-silicon Mac, `pip install mlx-whisper`, ffmpeg for video |
| `ocr_tolerant_grep.py` | Searches a folder of OCR text for a name, tolerating typical OCR confusions, and says when a zero is unreliable | Python 3.9+, standard library |
| `source_coverage.py` | Lists source files that no transcript mentions, counting identical files once | Python 3.9+, standard library |

## htr_prep.py

```
python3 htr_prep.py audit --out work/htr scans/
python3 htr_prep.py prep  --out work/htr scans/page-01.jpg           # add --force to redo a page
python3 htr_prep.py selftest
```

`audit` prints one line per page, worst first: `reshoot` when the long side is under 1500 px, `tolerable`
under 2500 px, `good` otherwise (`--bad`, `--ok`), and a total. With `--out` the pages to re-shoot are
written to `reshoot.txt`. A handwritten line needs about 100 px of height; a low-resolution scan is fixed by
re-shooting at full size (a messenger's "as photo" option typically caps the long side at 1280 px), not by a
model.

`prep` cuts each page into 8 strips (`--strips`) that overlap by 20 % (`--overlap`), applies auto-contrast
and enlarges each strip to 1500 px width (`--target-width`, never more than `--max-upscale` 3.0, never
shrinking). It writes `work/htr/<name>/p01.jpg ... p08.jpg` and `manifest.md` with one empty block per strip,
in which the transcription is typed. A strip folder that already holds a `manifest.md` is not overwritten
unless `--force` is given; with `--force` the old strips (`p01.jpg`, `p02.jpg`, ...) of that page are removed and the previous manifest is kept as `manifest.bak.md` (`manifest.bak2.md`, ... on later runs; a backup is never overwritten), so a typed transcription is not lost. Orientation comes from the EXIF tag. A PDF is split into pages first
(into `work/htr/_pdf/`); copies of the same PDF are counted once.

Process PDFs from unknown senders only with an up-to-date poppler.

Expected output for a 1280 x 1706 page: `letter_low.png -> work/htr/letter_low (8 strips)`; strips about 1500 px wide and 300-350 px high.

## transcribe_audio.py

```
python3 transcribe_audio.py --language ru --out transcripts/ audio/interview1.m4a audio/interview2.m4a
python3 transcribe_audio.py --language et --prompt "parish X, Näidis" --out transcripts/ video.mp4
```

Use it only on recordings made with the knowledge and consent of everyone recorded.

Writes `transcripts/<name>.txt` (`[seconds] text`, one line per segment) and `.json`; inputs with a
non-empty `.txt` are skipped. If only an empty `.txt` or a `.json` exists, the tool refuses before doing any
work, and it refuses two inputs that share a file name (`talk.m4a` and `talk.mp4`); `--force` replaces existing transcripts and re-transcribes skipped inputs. A video's sound is
extracted by ffmpeg into a temporary folder that is removed afterwards (no `.wav` is left in the output
folder, and ffmpeg never overwrites a file). `--language` is required: a wrong language gives plausible nonsense. `--prompt`
primes the decoder with names and places that occur in the recording. Default model
`mlx-community/whisper-large-v3-turbo` (about 1.6 GB, downloaded on first use). Larger models need much more memory;
run one file at a time. Pass only model repositories you trust to `--model`: the weights of any repository
named there are downloaded and loaded. Do not correct the transcript by
hand; keep doubtful passages in a separate note.

## source_coverage.py

```
python3 source_coverage.py --sources sources/ --transcripts transcripts/ notes/transcribed/
```

Groups the files under `--sources` by md5, so one photo stored twice under different names counts once. A
group is covered when any `.md` or `.txt` file under the `--transcripts` folders names any of its file names
(with or without extension) or one of its reference numbers (`--ref-pattern`, default
`\d{6,}|[A-Z]{2,4}\.\d+\.\d+\.\d+`). File names are normalised to NFC first: macOS stores a letter such as
"й" in decomposed form, the transcript has the composed form, and without normalisation such names are
never found. Pass only real transcripts: a report that retells a document must not count as one.

Exit code 0 when all is covered, 1 when files remain, 2 on a missing folder or no texts. Example output:

```
files 4, unique 3, duplicates 1, covering texts 1

NOT TRANSCRIBED: 1
  box1/untouched.png
```

## ocr_tolerant_grep.py

```
python3 ocr_tolerant_grep.py ocr_out hits.json --term Примеров --term Образцов
```

An existing `hits.json` is not overwritten unless `--force` is given.

Offline grep over a folder of OCR `.txt` files, two levels: exact (the term as typed, matched anywhere in a
word, so a root finds inflected forms) and tolerant (the term with one letter replaced by a typical OCR
confusion: о/0, и/н/п, б/6, д/л, Cyrillic and Latin look-alikes; edit `CONFUSIONS` in the script). One
substitution per variant keeps the pattern narrow; a pattern that allows everything matches common words.

Coverage is the offline counterpart of a block signature: the share of word-like tokens (words of 4 or more
letters among all tokens). Typed text gives 0.25-0.40, handwriting read by OCR 0.07-0.10. Files below
`--silent-below` (0.10) are silent, below `--weak-below` (0.20) weak. No hits and any silent or weak file gives
`NO-TEXT` (exit 3): that zero is not reliable. No hits and all files readable gives `ZERO`. Page markers are
optional: a line `===== <name> p.<N> =====` gives hits their page, otherwise the page is the file name. With
one text file per page, silent counts refer to pages.

Expected output: a one-line JSON summary, then `RESULT: N hits (E exact, T tolerant)`; the JSON file holds the
hits with file, page, matched text, line and context, plus the coverage lists.
