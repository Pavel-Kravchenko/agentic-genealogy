# Tools

Small Python tools for a family-history project. They are examples of the method, not a product: read a tool before you run it.

All of them work on files on your own machine. None of them queries a genealogy, archive or library site;
`transcribe_audio.py` downloads its speech model once, on first use.

| folder | tools |
|---|---|
| [`local/`](local/README.md) | resolution audit and strips for handwriting, audio transcription with a local Whisper model, coverage of sources by transcripts, a tolerant search over OCR text |
| [`graph/`](graph/README.md) | structural checks of the family graph, duplicate finder and merger, GEDCOM export and import; the schema is in [`graph/SCHEMA.md`](graph/SCHEMA.md) |
| [`privacy/`](privacy/README.md) | deny-list scanner to run before anything is published |

Requirements: Python 3.9 or later. Standard library only, except Pillow (image strips) and `mlx-whisper`
(audio, Apple silicon).

## Rules every tool follows

1. **A zero says how reliable it is.** The OCR search reports a hit, a zero over readable text, or
   "no text" when the files are too poor to support a zero.
2. **Nothing is written without a snapshot.** Tools that change the graph are dry runs unless `--apply`
   is given, and `--apply` copies the graph first. The merge log is appended, never overwritten.
3. **Imported data enters at low confidence** (the default of `gedcom_import.py`; `--confidence medium` is the
   only other choice, for a tree you know was built from documents; `merge_duplicates.py` keeps the confidence
   the imported copy carries). Another person's tree is working notes, not a document. It is written only into
   an event that is entirely empty in our graph (no date, no place, no source, no note). In an event we already
   document no value, style or confidence is changed (the merger only adds the other copy's source where the
   values agree), and what the other tree adds to it is listed in the report.
4. **No silent fallbacks.** Missing or malformed input stops the tool with a message.
5. **File names are compared after Unicode NFC normalisation.**

## Try them

```bash
cd tools/graph
python3 check_graph.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json
python3 merge_duplicates.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json
```

The sample family is invented; its planted problems are listed in
[`examples/sample-family/README.md`](../examples/sample-family/README.md).
