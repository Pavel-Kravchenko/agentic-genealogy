#!/usr/bin/env python3
"""Prepare scans for reading handwriting: a resolution verdict and overlapping strips.

    python3 htr_prep.py audit [options] PATH [PATH ...]      resolution report: legible, or re-shoot
    python3 htr_prep.py prep  [options] --out DIR PATH [...] cut every page into strips, with a manifest
    python3 htr_prep.py selftest                              self-check on synthetic images

PATH is an image file, a PDF or a folder (searched recursively). The model, not this script, reads
the strips: `prep` writes the strips and a manifest.md into DIR/<file name>/ and the transcription
is typed into the manifest, strip by strip.

A PDF is a source like a jpg: its pages are extracted into DIR/_pdf/ and then handled one by one.
A page with exactly one embedded raster is extracted as is, without re-encoding.

Requirements: Python 3.9+, Pillow. PDF input needs poppler (`pdfinfo`, `pdfimages`, `pdftoppm`).
HEIC input needs macOS `sips`. File names are compared after NFC normalisation.
`prep` refuses to write into a strip folder that already holds a manifest.md (a transcription may have been
typed into it) unless --force is given, and refuses two inputs of one file name. With --force the old strips
(p01.jpg, p02.jpg, ...) of that folder are removed and the previous manifest is kept as manifest.bak.md
(manifest.bak2.md, ... on later runs; a backup is never overwritten), so a typed transcription is not lost.
Resolution decides legibility: a handwritten line needs about 100 px of height; a low-resolution scan
is fixed by re-shooting, not by a model.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

STRIPS = 8            # strips per page
OVERLAP = 0.20        # overlap of neighbouring strips, share of the strip height
TARGET_W = 1500       # width the strip is enlarged to
MAX_UPSCALE = 3.0     # beyond this enlargement is pure blur
BAD, OK = 1500, 2500  # long side of the page: below BAD re-shoot, below OK tolerable
PDF_DPI = 300         # render resolution for a PDF page that has no single embedded raster
JPEG_QUALITY = 92
AUTOCONTRAST_CUTOFF = 1

IMG_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic"}
EXTS = IMG_EXTS | {".pdf"}
RASTER = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".jp2", ".ppm", ".pgm", ".pbm"}   # what pdfimages writes

PDF_ORIGIN = {}       # page extracted from a PDF -> (source pdf, page number)


def nfc(s):
    return unicodedata.normalize("NFC", s)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("%s failed (%s): %s"
                           % (cmd[0], " ".join(cmd[1:]), r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout.decode("utf-8", "replace")


def images(targets, work, pdf_dpi=PDF_DPI):
    """Pages to work on. A PDF is expanded page by page (see pdf_pages); copies of one PDF count once."""
    seen, out = set(), []
    for t in targets:
        p = Path(t)
        if not p.exists():
            raise FileNotFoundError("no such file or folder: %s" % t)
        found = (sorted(q for q in p.rglob("*") if q.suffix.lower() in EXTS) if p.is_dir()
                 else ([p] if p.suffix.lower() in EXTS else []))
        for q in found:
            pdf = q.suffix.lower() == ".pdf"
            key = hashlib.md5(q.read_bytes()).hexdigest() if pdf else q.resolve()
            if key not in seen:
                seen.add(key)
                out.extend(pdf_pages(q, work, pdf_dpi) if pdf else [q])
    return out


def pdf_page_count(pdf):
    for line in run(["pdfinfo", str(pdf)]).splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    raise RuntimeError("pdfinfo did not give a page count: %s" % pdf)


def pdf_image_counts(pdf):
    """Number of raster images on each page, from pdfimages -list."""
    counts = {}
    for line in run(["pdfimages", "-list", str(pdf)]).splitlines()[2:]:
        f = line.split()
        if len(f) > 2 and f[2] == "image":
            counts[int(f[0])] = counts.get(int(f[0]), 0) + 1
    return counts


def pdf_pages(pdf, work, dpi=PDF_DPI):
    """Pages of a PDF as separate images in work/_pdf/. A page with exactly one raster is extracted as
    is (pdfimages -all); a vector page or one made of several pieces is rendered whole at `dpi`."""
    n = pdf_page_count(pdf)
    digest = hashlib.md5(pdf.read_bytes()).hexdigest()[:8]
    dst = work / "_pdf" / ("%s-%s" % (pdf.stem, digest))
    ready = sorted(q for q in dst.iterdir() if q.suffix.lower() in RASTER) if dst.is_dir() else []
    if len(ready) == n:
        for i, q in enumerate(ready, 1):
            PDF_ORIGIN[q.resolve()] = (pdf, i)
        return ready

    dst.mkdir(parents=True, exist_ok=True)
    counts = pdf_image_counts(pdf)
    out = []
    for page in range(1, n + 1):
        tmp = Path(tempfile.mkdtemp())
        try:
            if counts.get(page) == 1:
                run(["pdfimages", "-all", "-f", str(page), "-l", str(page), str(pdf), str(tmp / "i")])
            else:
                run(["pdftoppm", "-jpeg", "-r", str(dpi), "-f", str(page), "-l", str(page), str(pdf), str(tmp / "i")])
            got = [q for q in sorted(tmp.iterdir()) if q.suffix.lower() in RASTER]
            if len(got) != 1:
                raise RuntimeError("%s, page %d: expected one image, got %s"
                                   % (pdf.name, page, [q.name for q in got] or "nothing"))
            final = dst / ("%s-p%03d%s" % (pdf.stem, page, got[0].suffix.lower()))
            shutil.move(str(got[0]), str(final))
            PDF_ORIGIN[final.resolve()] = (pdf, page)
            out.append(final)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return out


def load(path):
    """Open a scan with EXIF orientation applied. Pillow cannot read HEIC: convert with macOS sips."""
    from PIL import Image, ImageOps
    if path.suffix.lower() == ".heic":
        with tempfile.TemporaryDirectory() as td:          # the converted copy does not outlive this call
            tmp = Path(td) / (path.stem + ".jpg")
            r = subprocess.run(["sips", "-s", "format", "jpeg", str(path), "--out", str(tmp)], capture_output=True)
            if r.returncode != 0 or not tmp.exists():
                raise RuntimeError("sips could not open HEIC %s: %s" % (path, r.stderr.decode("utf-8", "replace").strip()))
            img = ImageOps.exif_transpose(Image.open(tmp))
            img.load()
            return img
    return ImageOps.exif_transpose(Image.open(path))


def bands(height, strips=STRIPS, overlap=OVERLAP):
    """Strip borders (top, bottom). They overlap and cover the whole height without gaps."""
    step = height / float(strips)
    pad = step * overlap
    return [(max(0, int(round(i * step - pad))), min(height, int(round((i + 1) * step + pad))))
            for i in range(strips)]


def verdict(w, h, bad=BAD, ok=OK):
    m = max(w, h)
    return "reshoot" if m < bad else ("tolerable" if m < ok else "good")


def origin(src):
    """Where the page came from: (path, page number). For a PDF the PDF itself, not the cache file."""
    got = PDF_ORIGIN.get(Path(src).resolve())
    return (str(got[0]), got[1]) if got else (str(src), None)


def manifest(src, w, h, scale, rows, bad, ok):
    src_path, src_page = origin(src)
    L = ["# %s" % src.name, "",
         "Original: `%s`%s  " % (src_path, ", page %d" % src_page if src_page else ""),
         "Resolution: %dx%d (%s), strips enlarged x%.1f" % (w, h, verdict(w, h, bad, ok), scale), "",
         "Read the strips in order; they overlap, so a line at a seam appears twice.",
         "Mark an uncertain word `[?]`, an unreadable one `[illegible]`.", ""]
    for name, top, bottom, sw, sh in rows:
        L += ["## %s - rows %d-%d px, %dx%d" % (name, top, bottom, sw, sh), "", "```", "", "```", ""]
    return "\n".join(L)


def prep(paths, work, strips=STRIPS, overlap=OVERLAP, target_w=TARGET_W, max_upscale=MAX_UPSCALE,
         bad=BAD, ok=OK, force=False):
    from PIL import Image, ImageOps
    made = []
    targets = {}
    for src in paths:                    # refuse before anything is written
        dst = work / nfc(src.stem)
        key = str(dst).casefold()        # one folder on a file system that ignores case
        if key in targets:
            raise SystemExit("two inputs share the file name '%s' (%s and %s); rename one" % (src.stem, targets[key], src))
        targets[key] = src
        if (dst / "manifest.md").exists() and not force:
            raise SystemExit("%s already holds a manifest.md (a transcription may be typed into it); "
                             "not overwriting. Use --force to replace it." % dst)
    for src in paths:
        img = load(src)
        w, h = img.size
        dst = work / nfc(src.stem)
        dst.mkdir(parents=True, exist_ok=True)
        if force:       # old strips go; the previous manifest (a typed transcription) is kept, never overwritten
            for old in dst.iterdir():
                if re.fullmatch(r"p\d{2,}\.jpg", old.name):
                    old.unlink()
            if (dst / "manifest.md").exists():
                bak, n = dst / "manifest.bak.md", 1
                while bak.exists():
                    n += 1
                    bak = dst / ("manifest.bak%d.md" % n)
                os.replace(dst / "manifest.md", bak)
        # enlarge only: a page wider than target_w (PDF pages arrive so) is not shrunk
        scale = max(1.0, min(target_w / float(w), max_upscale))
        rows = []
        for i, (top, bottom) in enumerate(bands(h, strips, overlap), 1):
            strip = ImageOps.autocontrast(img.crop((0, top, w, bottom)), cutoff=AUTOCONTRAST_CUTOFF)
            if scale > 1:
                strip = strip.resize((int(strip.width * scale), int(strip.height * scale)), Image.LANCZOS)
            name = "p%02d.jpg" % i
            strip.convert("RGB").save(dst / name, quality=JPEG_QUALITY)
            rows.append((name, top, bottom, strip.width, strip.height))
        (dst / "manifest.md").write_text(manifest(src, w, h, scale, rows, bad, ok), encoding="utf-8")
        made.append((src, dst, len(rows)))
    return made


def audit(paths, bad=BAD, ok=OK):
    rows = []
    for p in paths:
        w, h = load(p).size            # an unreadable file raises: no silent "error" row
        rows.append((p, w, h, verdict(w, h, bad, ok)))
    rows.sort(key=lambda r: (r[3] != "reshoot", str(r[0])))
    return rows


def selftest():
    from PIL import Image
    b = bands(1000, strips=8, overlap=0.2)
    assert b[0][0] == 0 and b[-1][1] == 1000, b
    assert all(b[i][1] > b[i + 1][0] for i in range(len(b) - 1)), "no overlap"
    assert all(b[i][0] < b[i + 1][0] for i in range(len(b) - 1)), "order broken"
    assert bands(1000, strips=8, overlap=0)[3] == (375, 500), bands(1000, strips=8, overlap=0)[3]

    tmp = Path(tempfile.mkdtemp())
    try:
        work = tmp / "htr"
        src = tmp / "page.png"
        Image.new("RGB", (600, 1200), (240, 235, 220)).save(src)
        (made,) = prep([src], work)
        assert made[2] == STRIPS, made
        tiles = sorted((work / "page").glob("p*.jpg"))
        assert len(tiles) == STRIPS, tiles
        w0, h0 = Image.open(tiles[0]).size
        assert w0 == TARGET_W, w0
        assert h0 > 1200 // STRIPS, h0
        assert "reshoot" in (work / "page" / "manifest.md").read_text(encoding="utf-8")
        try:
            prep([src], work)
        except SystemExit as e:
            assert "not overwriting" in str(e), e
        else:
            raise AssertionError("prep overwrote an existing manifest.md without --force")
        assert prep([src], work, force=True)[0][2] == STRIPS
        # --force: stale strips are removed, the previous manifest (with a typed transcription) is kept
        mf = work / "page" / "manifest.md"
        mf.write_text(mf.read_text(encoding="utf-8") + "\nTYPED TEXT\n", encoding="utf-8")
        assert prep([src], work, strips=6, force=True)[0][2] == 6
        assert len(sorted((work / "page").glob("p*.jpg"))) == 6, "stale strips left: %s" % sorted((work / "page").glob("p*.jpg"))
        kept = lambda: [b.name for b in sorted((work / "page").glob("manifest.bak*.md"))
                        if "TYPED TEXT" in b.read_text(encoding="utf-8")]
        assert len(kept()) == 1, "typed transcription lost: %s" % kept()
        assert "TYPED TEXT" not in mf.read_text(encoding="utf-8"), "new manifest still holds the old text"
        assert prep([src], work, strips=6, force=True)[0][2] == 6       # a further --force overwrites no backup
        assert len(kept()) == 1, "a later --force destroyed the kept transcription: %s" % kept()
        assert audit([src])[0][3] == "reshoot"
        if shutil.which("pdfinfo"):
            pdf = tmp / "letter.pdf"
            page = Image.new("RGB", (1700, 2338), (250, 248, 245))
            page.save(pdf, save_all=True, append_images=[page])
            pages = images([pdf], work)
            assert len(pages) == 2, pages
            assert Image.open(pages[0]).size == (1700, 2338), Image.open(pages[0]).size
            assert origin(pages[0]) == (str(pdf), 1), origin(pages[0])
            assert len(images([pdf, pdf], work)) == 2, "a copy of the same PDF must not double the pages"
        else:
            print("pdfinfo not found: PDF part of the self-check skipped")
    finally:
        shutil.rmtree(tmp)
    print("self-check passed")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Prepare scans for reading handwriting.")
    ap.add_argument("command", choices=["audit", "prep", "selftest"])
    ap.add_argument("paths", nargs="*", help="image files, PDFs or folders")
    ap.add_argument("--out", help="working folder (required for prep; audit writes reshoot.txt there if given)")
    ap.add_argument("--strips", type=int, default=STRIPS, help="strips per page (default: %(default)s)")
    ap.add_argument("--overlap", type=float, default=OVERLAP, help="strip overlap, share of height (default: %(default)s)")
    ap.add_argument("--target-width", type=int, default=TARGET_W, help="width strips are enlarged to (default: %(default)s)")
    ap.add_argument("--max-upscale", type=float, default=MAX_UPSCALE, help="largest enlargement factor (default: %(default)s)")
    ap.add_argument("--bad", type=int, default=BAD, help="long side below this: reshoot (default: %(default)s)")
    ap.add_argument("--ok", type=int, default=OK, help="long side below this: tolerable (default: %(default)s)")
    ap.add_argument("--force", action="store_true", help="prep: replace a strip folder that already holds a manifest.md; its old strips are "
                         "removed and the previous manifest is kept as manifest.bak.md (never overwritten)")
    ap.add_argument("--pdf-dpi", type=int, default=PDF_DPI, help="render resolution for PDF pages without a single raster")
    args = ap.parse_intermixed_args(argv)

    if args.command == "selftest":
        return selftest()
    if not args.paths:
        ap.error("give at least one PATH")
    if args.command == "prep" and not args.out:
        ap.error("prep needs --out")
    if args.bad >= args.ok:
        ap.error("--bad must be smaller than --ok")
    scratch = None
    if args.out:
        work = Path(args.out)
    else:                                                  # audit without --out: pages rendered from PDFs are temporary
        scratch = tempfile.TemporaryDirectory(prefix="htr_prep_")
        work = Path(scratch.name)
    try:
        return execute(args, work)
    finally:
        if scratch:
            scratch.cleanup()


def execute(args, work):
    paths = images(args.paths, work, args.pdf_dpi)
    if not paths:
        raise SystemExit("no images found in: %s" % ", ".join(args.paths))

    if args.command == "audit":
        rows = audit(paths, args.bad, args.ok)
        counts = {}
        for _, _, _, v in rows:
            counts[v] = counts.get(v, 0) + 1
        for p, w, h, v in rows:
            path, page = origin(p)
            print("%-10s %5dx%-5d %s%s" % (v, w, h, nfc(path), " (page %d)" % page if page else ""))
        print("\nTotal: " + ", ".join("%s %d" % kv for kv in sorted(counts.items())))
        bad = [p for p, _, _, v in rows if v == "reshoot"]
        if bad and args.out:
            work.mkdir(parents=True, exist_ok=True)
            out = work / "reshoot.txt"
            out.write_text("\n".join(str(p) for p in bad) + "\n", encoding="utf-8")
            print("Re-shoot list: %s" % out)
        return 0

    for src, dst, n in prep(paths, work, args.strips, args.overlap, args.target_width, args.max_upscale,
                            args.bad, args.ok, args.force):
        print("%s -> %s (%d strips)" % (src.name, dst, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
