#!/usr/bin/env python3
"""Which source files are not yet transcribed.

    python3 source_coverage.py --sources SOURCES_DIR --transcripts TRANSCRIPTS_DIR [TRANSCRIPTS_DIR ...]

Exit code 0 when every source file is covered, 1 when some are not, 2 on bad input.

Two rules:

1. Count by checksum, not by name. A messenger can store one photo twice, once under a sequence
   number and once under a timestamp name. A comparison by name does not see such pairs and
   overstates the remainder. Files with the same md5 form one group, and the group is covered when
   ANY of its names is covered.
2. Only a transcript counts. The covering texts are the .md and .txt files under the --transcripts
   folders: a transcript reproduces the document, a report only retells it, so a report must not be
   passed as a transcript folder.

A group is covered when a covering text names any file name of the group (with or without extension)
or one of its archive reference numbers. References are found by a regular expression (--ref-pattern);
transcribers refer to an image by scan number and shelf mark, not by a long file name.

File names are normalised to NFC before comparison. macOS stores names in NFD, with a letter such as
"й" or "ä" split into base and combining mark, while the text of a transcript has the composed form.
Without normalisation every such name is never found.

Requirements: Python 3.9+, standard library only.
"""
import argparse
import hashlib
import os
import re
import sys
import unicodedata

DEFAULT_EXTS = ".jpg,.jpeg,.png,.pdf,.tif,.tiff,.heic,.webp"
DEFAULT_REF_PATTERN = r"\d{6,}|[A-Z]{2,4}\.\d+\.\d+\.\d+"
MIN_KEY_LEN = 4          # shorter keys would match everywhere


def nfc(s):
    return unicodedata.normalize("NFC", s)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def covering_text(transcript_dirs):
    """All .md and .txt files under the transcript folders, joined, NFC."""
    parts, n = [], 0
    for d in transcript_dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if f.lower().endswith((".md", ".txt")):
                    with open(os.path.join(root, f), encoding="utf-8") as fh:   # malformed UTF-8 raises
                        parts.append(fh.read())
                    n += 1
    return nfc("\n".join(parts)), n


def groups_by_checksum(sources, exts):
    groups = {}
    for root, _, files in os.walk(sources):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                p = os.path.join(root, f)
                groups.setdefault(md5_of(p), []).append(os.path.relpath(p, sources))
    return groups


def uncovered(groups, text, ref_re):
    missing = []
    for files in groups.values():
        keys = set()
        for f in files:
            name = os.path.basename(f)
            keys.add(name)
            keys.add(os.path.splitext(name)[0])
            keys |= set(ref_re.findall(name))
        keys = {nfc(k) for k in keys}
        if not any(k in text for k in keys if len(k) >= MIN_KEY_LEN):
            missing.append(files)
    return missing


def main(argv=None):
    ap = argparse.ArgumentParser(description="List source files that no transcript mentions.")
    ap.add_argument("--sources", required=True, help="folder with the original files (searched recursively)")
    ap.add_argument("--transcripts", required=True, nargs="+", help="folder(s) with transcripts (.md, .txt)")
    ap.add_argument("--exts", default=DEFAULT_EXTS, help="extensions of source files (default: %(default)s)")
    ap.add_argument("--ref-pattern", default=DEFAULT_REF_PATTERN,
                    help="regular expression for archive reference numbers inside file names (default: %(default)s)")
    args = ap.parse_args(argv)

    for d in [args.sources] + args.transcripts:
        if not os.path.isdir(d):
            print("not a folder: %s" % d, file=sys.stderr)
            return 2
    exts = {e.strip().lower() for e in args.exts.split(",") if e.strip()}
    text, n_texts = covering_text(args.transcripts)
    if n_texts == 0:
        print("no .md or .txt files under the transcript folders: %s" % ", ".join(args.transcripts), file=sys.stderr)
        return 2
    groups = groups_by_checksum(args.sources, exts)
    if not groups:
        print("no source files with extensions %s under %s" % (args.exts, args.sources), file=sys.stderr)
        return 2
    missing = uncovered(groups, text, re.compile(args.ref_pattern))

    total = sum(len(v) for v in groups.values())
    dup = sum(len(v) - 1 for v in groups.values() if len(v) > 1)
    print("files %d, unique %d, duplicates %d, covering texts %d" % (total, len(groups), dup, n_texts))
    if missing:
        print("\nNOT TRANSCRIBED: %d" % len(missing))
        for files in sorted(missing):
            print("  " + nfc(files[0]) + ("  (+%d identical)" % (len(files) - 1) if len(files) > 1 else ""))
        return 1
    print("\nnothing left to transcribe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
