# -*- coding: utf-8 -*-
"""Tolerant grep over a folder of OCR text files (offline, no network).

Two levels of match per search term (a name root, matched anywhere in a word, case-insensitive):
  exact      the term as typed (a root such as "Примеров" also matches "Примеровка");
  tolerant   the term with ONE letter replaced by a typical OCR confusion (о/0, и/н/п, б/6, д/л,
             Cyrillic/Latin look-alikes; table CONFUSIONS below). One substitution per variant keeps the
             pattern narrow: a pattern that allows everything catches common words.

Coverage is counted too. Typed text gives 0.25-0.40 word-like tokens (words of 4+ letters
among all tokens), handwriting read by OCR 0.07-0.10. A file below --silent-below is "silent"
and one below --weak-below is "weak": a silent OCR is as false a zero as a silent database.

    python3 ocr_tolerant_grep.py ocr_out hits.json --term Примеров --term Образцов

Input: a folder of *.txt files. A file may carry page markers on their own line:
    ===== <name> p.<N> =====
the page of a hit is then N; without markers the page of a hit is the file name.

Outcomes: RESULT (hits printed, JSON written), ZERO (no hits and every file readable),
NO-TEXT (no hits but some files are silent or weak: the zero is not reliable, exit code 3).
"""
import argparse
import glob
import json
import os
import re
import sys

import unicodedata

EXIT_OK, EXIT_INCOMPLETE = 0, 3

# One OCR confusion per variant. Lower-case keys; patterns are matched case-insensitively.
CONFUSIONS = {
    "о": "0oa", "а": "оa", "и": "нпu", "н": "ипh", "п": "н", "б": "6в", "в": "б",
    "д": "л", "л": "д", "г": "т", "т": "г", "е": "э", "э": "е", "с": "co", "к": "k",
    "р": "p", "у": "y", "х": "x", "ж": "х",
}
MARKER = re.compile(r"=====\s+(\S+)\s+(?:стр\.|p\.|page\s*)(\d+)\s+=====", re.I)


def tolerant_pattern(term):
    t = term.lower()
    variants = []
    for i, ch in enumerate(t):
        subs = CONFUSIONS.get(ch)
        if subs:
            variants.append(re.escape(t[:i]) + "[" + re.escape(ch + subs) + "]" + re.escape(t[i + 1:]))
    return re.compile("|".join(variants), re.I) if variants else None


def page_of(lines, i, fallback):
    for j in range(i, -1, -1):
        m = MARKER.match(lines[j])
        if m:
            return m.group(2)
    return fallback


def scan(folder, terms, min_chars, silent_below, weak_below, context_lines):
    files = sorted(glob.glob(os.path.join(folder, "*.txt")))
    if not files:
        raise ValueError("no *.txt files in %s" % folder)
    exact = re.compile("|".join(re.escape(t) for t in terms), re.I)
    tol = [p for p in (tolerant_pattern(t) for t in terms) if p]
    hits, silent, weak, quality = [], [], [], {}
    readable = 0
    for fp in files:
        name = os.path.basename(fp)[:-4]
        txt = unicodedata.normalize("NFC", open(fp, encoding="utf-8", errors="replace").read())
        body = re.sub(r"=====.*?=====", "", txt)
        chars = len(re.sub(r"\s+", "", body))
        tokens = re.findall(r"\S+", body)
        words = [w for w in tokens if re.fullmatch(r"[^\W\d_]{4,}", w)]   # letters of any script
        share = len(words) / len(tokens) if tokens else 0.0
        quality[name] = round(share, 3)
        if chars < min_chars or share < silent_below:
            silent.append({"file": name, "chars": chars, "share": round(share, 3)})
        elif share < weak_below:
            weak.append({"file": name, "chars": chars, "share": round(share, 3)})
        else:
            readable += 1
        lines = txt.split("\n")
        for i, ln in enumerate(lines):
            if ln.startswith("====="):
                continue
            m = exact.search(ln)
            level = "exact"
            if not m:
                for p in tol:
                    m = p.search(ln)
                    if m:
                        level = "tolerant"
                        break
            if not m:
                continue
            ctx = " ".join(x.strip() for x in lines[max(0, i - context_lines):i + context_lines + 1]
                           if x.strip() and not x.startswith("====="))
            hits.append({"file": name, "level": level, "match": m.group(0),
                         "page": page_of(lines, i, name), "line": ln.strip(), "context": ctx[:500]})
    summary = {"files": len(files), "readable": readable, "weak": len(weak), "silent": len(silent),
               "hits": len(hits), "exact": sum(h["level"] == "exact" for h in hits),
               "tolerant": sum(h["level"] == "tolerant" for h in hits)}
    return summary, silent, weak, quality, hits


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder", help="folder of OCR *.txt files")
    ap.add_argument("out_json", help="where to write the result JSON")
    ap.add_argument("--term", action="append", required=True,
                    help="search term, a name root; repeat for several")
    ap.add_argument("--min-chars", type=int, default=200, help="files with fewer characters are silent (default 200)")
    ap.add_argument("--silent-below", type=float, default=0.10, help="word-like token share below this = silent (default 0.10)")
    ap.add_argument("--weak-below", type=float, default=0.20, help="share below this = weak (default 0.20)")
    ap.add_argument("--context-lines", type=int, default=3, help="lines of context each side (default 3)")
    ap.add_argument("--force", action="store_true", help="overwrite out_json if it exists (default: refuse)")
    a = ap.parse_args()
    if os.path.exists(a.out_json) and not a.force:
        sys.exit("%s already exists; choose another path or pass --force" % a.out_json)
    if not (0 <= a.silent_below <= a.weak_below <= 1):
        raise ValueError("need 0 <= --silent-below <= --weak-below <= 1")
    summary, silent, weak, quality, hits = scan(
        a.folder, a.term, a.min_chars, a.silent_below, a.weak_below, a.context_lines)
    with open(a.out_json, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "silent": silent, "weak": weak, "quality": quality,
                   "hits": hits}, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False))
    if hits:
        print("RESULT: %d hits (%d exact, %d tolerant)" % (summary["hits"], summary["exact"], summary["tolerant"]))
        return EXIT_OK
    if silent or weak:
        print("NO-TEXT: no hits, but %d silent and %d weak files: this zero is not reliable; "
              "check the scans" % (len(silent), len(weak)), file=sys.stderr)
        return EXIT_INCOMPLETE
    print("ZERO: no hits in %d readable files (OCR errors beyond one confusion per word can still hide a name)"
          % summary["readable"])
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
