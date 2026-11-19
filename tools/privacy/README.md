# Privacy scanner

`pii_scan.py` checks text before it leaves a private family-history project.

```bash
# 1. deny-list from your own graph (schema: tools/graph/SCHEMA.md) plus a free-form file of other names
python3 pii_scan.py build --persons /path/to/Graph/persons.json --extra /path/to/private/extra-names.txt \
        --deny /path/outside/the/publication/denylist.json

#    build refuses to overwrite an existing deny-list (add --force to replace it) and refuses to write it
#    inside this repository ("the deny-list holds private names: write it outside this repository")

# 2. scan what you are about to publish; exit code 1 on any hit
python3 pii_scan.py scan ./public-folder --deny /path/outside/denylist.json --allow /path/outside/allow.txt

# 3. read every proper noun the scanner cannot know about
python3 pii_scan.py inventory ./public-folder
```

What it catches: every word of every name, family group and name variant in the graph and every
capitalised word of every place, in any Russian inflection (endings are stripped), in four
transliterations of Cyrillic (English, simplified, German, scholarly), with Latin diacritics folded;
and anything shaped like a shelf mark, for example an archive reference code with three numbers (`EAA.`, `ERA.`
and similar prefixes), three numbers joined by hyphens, or `fond N, opis N`.

`scan` reads every file under the given paths, whatever its extension. Text that is not UTF-8 is read as
UTF-16 (with a byte order mark) or as cp1251. A binary file (an image, a PDF, an archive) cannot be read: it
is listed as `NOT SCANNED` and `scan` exits 1 until you have looked at the file yourself and added
`unscanned@<end of its path>` to the allow file. A clean result therefore never hides an unread file.

What it does not catch: people who are not in your graph and not in your extra file, small places
written differently from the graph, photographs, file metadata, and stories recognisable without a
name. Step 3 and a human reading are part of the check.

The first scan is noisy on purpose: given names, provinces and common words that collide with a
surname stem are all reported. Read the hits, and put what you accept into the allow file with a
reason after `#`. `token@path-suffix` allows a token in one file only (for example your own name in
`LICENSE`).

See it fail before you trust it: plant a real surname in a copy of one file and confirm exit code 1.

Run on the sample family (every name there is invented, so every hit is expected):

```bash
python3 pii_scan.py build --persons ../../examples/sample-family/persons.json --deny /tmp/deny.json
python3 pii_scan.py scan ../../examples/sample-family/README.md --deny /tmp/deny.json   # hits, exit 1
```

Two traps that were found while building it: Unicode NFKD folding turns Cyrillic `й` into `и`, so
adjectival forms in `-ский` stopped matching until Cyrillic was normalised separately from Latin; and
ISO dates look like `fond-inventory-file` shelf marks, so full dates are excluded from that pattern.
