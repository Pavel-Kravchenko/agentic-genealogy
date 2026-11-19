#!/usr/bin/env python3
"""Privacy scan before anything derived from a family-history project is published.

Builds a deny-list from your own family graph (surnames, name variants, places) and from an optional
file of extra tokens (correspondents, researchers, tree owners), then scans every file that reads as
text for those tokens in any inflection and in several transliterations, and for anything shaped like a
shelf mark. Text that is not UTF-8 is read as UTF-16 (with a byte order mark) or cp1251. A binary file
(an image, a PDF) cannot be read: it is listed as NOT SCANNED and makes `scan` exit 1 until you have
looked at it yourself and added `unscanned@<end of its path>` to the allow file.

  pii_scan.py build --persons persons.json [--extra extra.txt] --deny denylist.json [--force]
  pii_scan.py scan PATH [PATH ...] --deny denylist.json [--allow allow.txt]
  pii_scan.py inventory PATH [PATH ...]

`scan` exits 1 on any hit that is not in the allow file and on any file it could not read. Keep the deny-list and the allow file OUTSIDE
what you publish. The scanner knows only what is in your graph and your extra file: read the output of
`inventory` (every capitalised or non-Latin token that is not a dictionary word) yourself as well.
Before trusting a clean scan, plant a real surname in a copy and see the scan fail.

`build` refuses to overwrite an existing deny-list unless --force, and refuses to write the deny-list
into the repository that holds this script (the deny-list holds private names).

Allow file: one token per line, `#` starts a comment; `token@path-suffix` allows the token only in files
whose path ends with that suffix. Python 3.9+, standard library only.
"""
import argparse, json, os, re, sys, unicodedata

# Cyrillic -> Latin, four schemes: the same surname is spelt differently in English, simplified,
# German and scholarly sources.
BGN = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
       "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
       "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ъ": "", "ы": "y",
       "ь": "", "э": "e", "ю": "yu", "я": "ya", "і": "i", "ѣ": "e", "ї": "yi", "є": "ye", "ў": "u"}
SIMPLE = dict(BGN, **{"й": "j", "х": "h", "ц": "c", "щ": "sch", "ю": "ju", "я": "ja"})
GERMAN = dict(BGN, **{"в": "w", "ж": "sch", "з": "s", "й": "j", "х": "ch", "ц": "z", "ч": "tsch",
                      "ш": "sch", "щ": "schtsch", "ю": "ju", "я": "ja"})
SCHOLARLY = dict(BGN, **{"ж": "z", "х": "h", "ц": "c", "ч": "c", "ш": "s", "щ": "sc", "ю": "u", "я": "a",
                         "й": "j"})
SCHEMES = [BGN, SIMPLE, GERMAN, SCHOLARLY]

# Endings stripped from Cyrillic words so that inflected forms match (longest first).
ENDINGS = ["ского", "ская", "ской", "ский", "ское", "скую", "ских", "ским", "ович", "евич", "овна", "евна",
           "ова", "ева", "ина", "ого", "ый", "ий", "ая", "ое", "ые", "ов", "ев", "ин", "а", "о", "и", "ы",
           "е", "ь", "я", "й"]
MIN_STEM = 4          # shorter Cyrillic stems are ignored
MIN_LATIN = 5         # shorter Latin transliterations are ignored

SHELFMARK = re.compile(
    r"(EAA|ERA|LVVA|LVA)\.?\s?\d+[.\-]\d+[.\-]\d+"                 # Estonian / Latvian reference codes
    r"|\b\d{2,5}[\-–/]\d{1,3}[\-–/]\d{1,5}\b"                       # three numbers joined by hyphens
    r"|(?:[Фф]\.|fond|f\.)\s*[A-Za-zА-Яа-я\-]*\d+\s*,?\s*(?:[Оо]п\.|opis|op\.)\s*\d+", re.I)
ISO_DATE = re.compile(r"(1[5-9]|20)\d\d-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def fold_latin(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("ł", "l").replace("ø", "o").replace("ß", "ss").replace("đ", "d")


def is_cyrillic(w):
    return bool(re.search(r"[а-яёіїєў]", w.lower()))


def norm(w):
    """One normaliser for both sides. Cyrillic keeps й (NFKD would turn it into и)."""
    return w.lower().replace("ё", "е") if is_cyrillic(w) else fold_latin(w)


def _strip(w):
    for e in ENDINGS:
        if w.endswith(e) and len(w) - len(e) >= MIN_STEM:
            return w[:len(w) - len(e)]
    return w


def stem(w):
    """Strip up to two endings: Примеровского -> Примеров -> Пример, the same stem as Примеров."""
    return _strip(_strip(w.lower().replace("ё", "е")))


def transliterations(st):
    return {"".join(scheme.get(c, c) for c in st) for scheme in SCHEMES}


def words(s):
    return re.findall(r"[A-Za-zÀ-ɏА-Яа-яЁёІіЇїЄєЎў'’\-]{3,}", nfc(s))


def repo_root():
    """The repository this script ships in (tools/privacy/pii_scan.py -> its grandparent), or None."""
    here = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(here)
    return os.path.dirname(parent) if os.path.basename(parent) == "tools" else None


def build(persons_path, extra_path, deny_path, force=False):
    root = repo_root()
    target = os.path.realpath(deny_path)
    if root and os.path.commonpath([root, target]) == root:
        sys.exit("the deny-list holds private names: write it outside this repository")
    if os.path.exists(deny_path) and not force:
        sys.exit("%s already exists; choose another path or pass --force" % deny_path)
    persons = json.load(open(persons_path, encoding="utf-8"))
    if not isinstance(persons, list) or not persons:
        sys.exit("persons file must be a non-empty JSON list (see tools/graph/SCHEMA.md)")
    names, places, extra = set(), set(), set()
    for p in persons:
        names.update(words(p["name"]))
        names.update(words(p.get("family") or ""))
        for v in p.get("variants") or []:
            names.update(words(v))
        for ev in ("birth", "death"):
            place = (p.get(ev) or {}).get("place") or ""
            places.update(w for w in words(place) if w[0].isupper())
    if extra_path:
        for line in open(extra_path, encoding="utf-8"):
            extra.update(words(line.split("#")[0]))
    with open(deny_path, "w", encoding="utf-8") as f:
        json.dump({"names": sorted(names), "places": sorted(places), "extra": sorted(extra)},
                  f, ensure_ascii=False, indent=0)
    print("names %d, places %d, extra %d -> %s" % (len(names), len(places), len(extra), deny_path))
    print("Given names, patronymics, provinces and common words are in the list too: put the ones you")
    print("accept into an allow file after reading the first scan.")


def load(deny_path, allow_path):
    deny = json.load(open(deny_path, encoding="utf-8"))
    allow = set()
    if allow_path:
        for line in open(allow_path, encoding="utf-8"):
            line = line.split("#")[0].strip()
            if not line:
                continue
            if "@" in line:
                tok, suffix = line.split("@", 1)
                allow.add(norm(tok) + "@" + suffix)
            else:
                allow.add(norm(line))
    patterns = {}                                   # stem or transliteration -> source token
    for kind in ("names", "places", "extra"):
        for tok in deny[kind]:
            if is_cyrillic(tok):
                st = stem(tok)
                if len(st) < MIN_STEM:
                    continue
                patterns.setdefault(st, kind + ":" + tok)
                for t in transliterations(st):
                    if len(t) >= MIN_LATIN:
                        patterns.setdefault(t, kind + ":" + tok)
            else:
                f = fold_latin(tok)
                if len(f) >= MIN_STEM:
                    patterns.setdefault(f, kind + ":" + tok)
    return patterns, allow


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
                for f in files:       # every file: a file left out by its extension would hide a leak
                    if f != ".DS_Store":
                        yield os.path.join(root, f)
        elif os.path.exists(p):
            yield p
        else:
            sys.exit("no such path: " + p)


def allowed(token, path, allow):
    if token in allow:
        return True
    return any(a.startswith(token + "@") and path.endswith(a.split("@", 1)[1]) for a in allow if "@" in a)


def read_text(fp):
    """-> (text, note). UTF-8 first; UTF-16 when a byte order mark says so; a file without NUL bytes that is
    not UTF-8 is read as cp1251 (legacy Cyrillic text, old GEDCOM exports). (None, reason) for a binary file."""
    with open(fp, "rb") as f:
        data = f.read()
    try:
        return data.decode("utf-8"), ""
    except UnicodeDecodeError:
        pass
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            return data.decode("utf-16"), "read as UTF-16"
        except UnicodeDecodeError:
            pass
    if b"\0" not in data:
        return data.decode("cp1251", errors="replace"), "read as cp1251"
    return None, "binary"


def scan(paths, deny_path, allow_path):
    patterns, allow = load(deny_path, allow_path)
    hits = nfiles = unread = accepted = 0
    for fp in iter_files(paths):
        text, note = read_text(fp)
        if text is None:        # fail closed: a file nobody read is not a clean file
            if allowed(norm("unscanned"), fp, allow):
                accepted += 1
                print("%s: not scanned (binary), accepted in the allow file" % fp)
            else:
                unread += 1
                print("%s: NOT SCANNED (binary: an image, a PDF, an archive). Look at it yourself, then add "
                      "`unscanned@<end of its path>` to the allow file" % fp)
            continue
        if note:
            print("%s: %s" % (fp, note))
        lines = nfc(text).split("\n")
        nfiles += 1
        for i, line in enumerate(lines, 1):
            for w in set(words(line)):
                f = norm(w)
                if allowed(f, fp, allow):
                    continue
                src = None
                if is_cyrillic(f):
                    src = patterns.get(stem(f))
                elif f in patterns:
                    src = patterns[f]
                else:                               # Latin: a transliterated stem plus a short ending
                    for n in range(len(f), MIN_LATIN - 1, -1):
                        if f[:n] in patterns and n >= max(MIN_LATIN, len(f) - 4):
                            src = patterns[f[:n]]
                            break
                if src:
                    hits += 1
                    print("%s:%d: NAME %s  <- %s" % (fp, i, w, src))
            for m in SHELFMARK.finditer(line):
                if ISO_DATE.fullmatch(m.group(0)) or allowed(norm(m.group(0)), fp, allow):
                    continue
                hits += 1
                print("%s:%d: SHELFMARK %s" % (fp, i, m.group(0)))
    print("scanned %d files, %d hits; not scanned: %d (accepted in the allow file: %d)"
          % (nfiles, hits, unread + accepted, accepted))
    return 1 if hits or unread else 0


def inventory(paths):
    dictionary = set()
    if os.path.exists("/usr/share/dict/words"):
        dictionary = {w.strip().lower() for w in open("/usr/share/dict/words")}
    else:
        print("no /usr/share/dict/words: every capitalised token is listed", file=sys.stderr)
    counts = {}
    for fp in iter_files(paths):
        text, note = read_text(fp)
        if text is None:
            print("%s: not read (binary)" % fp, file=sys.stderr)
            continue
        text = nfc(text)
        for w in words(text):
            f = fold_latin(w)
            if is_cyrillic(w) or (w[0].isupper() and f not in dictionary and f.rstrip("s") not in dictionary):
                counts[w] = counts.get(w, 0) + 1
    for w, n in sorted(counts.items(), key=lambda x: (is_cyrillic(x[0]), x[0].lower())):
        print("%4d  %s" % (n, w))
    print("unique tokens: %d" % len(counts))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build the deny-list from the family graph")
    b.add_argument("--persons", required=True)
    b.add_argument("--extra", help="text file with extra names and places, free form")
    b.add_argument("--deny", required=True, help="output deny-list (keep it private)")
    b.add_argument("--force", action="store_true", help="overwrite an existing deny-list (default: refuse)")
    s = sub.add_parser("scan", help="scan files or folders; exit 1 on hits")
    s.add_argument("paths", nargs="+")
    s.add_argument("--deny", required=True)
    s.add_argument("--allow")
    v = sub.add_parser("inventory", help="list capitalised and non-Latin tokens that are not dictionary words")
    v.add_argument("paths", nargs="+")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.persons, a.extra, a.deny, a.force)
    elif a.cmd == "scan":
        sys.exit(scan(a.paths, a.deny, a.allow))
    else:
        inventory(a.paths)


if __name__ == "__main__":
    main()
