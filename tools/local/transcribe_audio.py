#!/usr/bin/env python3
"""Transcribe audio recordings with mlx-whisper, one file at a time, result on disk at once.

    python3 transcribe_audio.py --language ru --out OUT_DIR recording1.m4a recording2.m4a video.mp4

For each input it writes OUT_DIR/<name>.txt (lines "[seconds] text") and OUT_DIR/<name>.json.
Inputs that already have a non-empty .txt are skipped. If only an empty .txt or a .json exists, the tool
refuses before doing any work, because writing would replace that file (it also refuses two inputs that
share a file name); --force replaces the transcripts
(and re-transcribes inputs that are otherwise skipped). A video (.mp4 .mov .mkv) is first converted
to a 16 kHz mono wav with ffmpeg in a temporary folder that is removed afterwards; no wav is written to
OUT_DIR and ffmpeg never overwrites a file.

Use it only on recordings made with the knowledge and consent of everyone recorded.

Requirements: Apple-silicon Mac, Python 3.9+, `pip install mlx-whisper`, ffmpeg for video input.
The first run downloads the model from the Hugging Face hub (about 1.6 GB for the default turbo model).
Larger models need much more memory; run one file at a time.
Do not edit the transcript by hand to "correct" it: mark doubtful passages in a separate note.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import unicodedata

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
VIDEO_EXTS = (".mp4", ".mov", ".mkv")


def transcribe_all(out_dir, inputs, language, model=DEFAULT_MODEL, prompt=None, force=False):
    for src in inputs:
        if not os.path.isfile(src):
            raise FileNotFoundError("input not found: %s" % src)
    stems = [unicodedata.normalize("NFC", os.path.splitext(os.path.basename(src))[0]) for src in inputs]
    seen = {}
    for src, stem in zip(inputs, stems):       # refuse before any work: one stem would be written twice
        if stem.casefold() in seen:
            raise SystemExit("two inputs share the file name '%s' (%s and %s); rename one"
                             % (stem, seen[stem.casefold()], src))
        seen[stem.casefold()] = src
    import mlx_whisper     # imported here so that --help works without the package
    if not force:                  # refuse before any model is loaded or any file is written
        for stem in stems:
            txt = os.path.join(out_dir, stem + ".txt")
            if os.path.exists(txt) and os.path.getsize(txt) > 0:
                continue           # finished earlier, skipped below
            for target in (txt, os.path.join(out_dir, stem + ".json")):
                if os.path.exists(target):
                    raise SystemExit("%s already exists and would be overwritten; "
                                     "move it away or pass --force" % target)
    os.makedirs(out_dir, exist_ok=True)
    for src, stem in zip(inputs, stems):
        txt = os.path.join(out_dir, stem + ".txt")
        if not force and os.path.exists(txt) and os.path.getsize(txt) > 0:
            print("exists:", stem)
            continue
        kwargs = {"path_or_hf_repo": model, "language": language,
                  "condition_on_previous_text": False, "verbose": False}
        if prompt:
            kwargs["initial_prompt"] = prompt
        with tempfile.TemporaryDirectory(prefix="transcribe_") as tmp:
            audio = src
            if src.lower().endswith(VIDEO_EXTS):
                audio = os.path.join(tmp, stem + ".wav")
                subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", audio],
                               check=True)
            r = mlx_whisper.transcribe(audio, **kwargs)
        with open(os.path.join(out_dir, stem + ".json"), "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
        with open(txt, "w", encoding="utf-8") as f:
            for s in r["segments"]:
                f.write("[%.0f] %s\n" % (s["start"], s["text"].strip()))
        print("done:", stem, len(r["segments"]), "segments")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Transcribe audio with mlx-whisper, file by file.")
    ap.add_argument("inputs", nargs="+", help="audio or video files")
    ap.add_argument("--out", required=True, help="output folder")
    ap.add_argument("--language", required=True, help="spoken language code, e.g. ru, de, en, et")
    ap.add_argument("--model", default=DEFAULT_MODEL, help="model repo (default: %(default)s)")
    ap.add_argument("--prompt", default=None,
                    help="optional text that primes the decoder, e.g. a list of place names and surnames spoken in the recording")
    ap.add_argument("--force", action="store_true",
                    help="replace existing .txt and .json transcripts (default: refuse, and skip inputs with a non-empty .txt)")
    args = ap.parse_intermixed_args(argv)
    transcribe_all(args.out, args.inputs, args.language, args.model, args.prompt, args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
