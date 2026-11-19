# Reading full-text indexes and OCR text

Full-text search over digitised registers, inventories and gazettes finds what manual reading would take
months to find, and it fails silently in ways that look exactly like "this person is not there". The patterns
below were observed in 2026 on Yandex Archive (Яндекс.Архив, handwritten Russian registers with machine
reading), on Soviet archive inventories run through `tesseract`, on Polish official gazettes in PDF and on war
memorial databases. The examples are composed illustrations; the patterns come from real work, the
particulars do not. They use the invented Primerov family.

## 1. An index splits one word into unrelated lemma groups

A lemmatising index does not merge different roots that handwriting and machine reading produce. These are not
grammatical cases; they are distinct "words" for the index.

- `Primerov`, `Primer`, `Primerovy` returned three separate corpora. In the third, which nobody had asked for,
  sat a whole unknown man of the family.
- The name of one volost came back in about a dozen forms (spelling variants of the adjective plus two machine
  distortions of the root).
- One spelling of a surname gave roughly a third as many records as another, and the whole layer before the
  mid-1880s sat under the second only. Searching the "correct" spelling cut off the older layer completely.

How to search:

- Vary the distortions of the root, not the grammatical cases. Case endings of one root (masculine genitive,
  instrumental, pre-reform endings) fall into one lemma; several case forms of one stem gave one and the same
  result list.
- Not every surname is split. For some, case forms give identical results. Test two forms of this particular
  surname before running a full list of variants.
- Truncation as a prefix did not work on Yandex Archive: a prefix query returned only unrelated hits.
  Test it on a known hit before relying on it anywhere.
- Some normalisation does happen: the final hard sign `ъ`, the letter yat and the dotted `i` are folded.
  A surname with and without the final `ъ` gave the same records both ways.
- Yandex Archive did not AND the words of a query: a full name and patronymic returned over a hundred
  thousand hits. Only a single rare word form works as a query.
- A search meant for one inventory must be shown to be limited to that inventory: a page that only filled
  the search box and drew no scoped result list gives no "zero for this inventory".
- Diacritics matter where the site keeps them: on a Czech archive form `Přimerov` and `Primerov` are different
  queries.
- Some sites print the count in another language section with another word: the Ukrainian section of
  «Открытый список» (Open List, a database of victims of Soviet repression) prints «Знайдено N», not
  «Найдено N». A reader that waits for the Russian word counts every honest Ukrainian result as a block.

## 2. Before the 1880s, search without surnames

Before the mid-1880s, register entries for peasants mostly carry no surname at all. Search with the combination
given name + patronymic + wife's name: "Ivan Petrov" (Ivan son of Pyotr) with "wife Anna". This combination
reached decades further back than the surname searches.

## 3. OCR errors on printed years

Printed register forms have the century and decade printed and the last digit written in by hand. Machine
reading loses the handwritten digit and sometimes the printed decade:

- last digit: a handwritten `2` read as `8`, `3` as `7`, `0` as `6`; in one file the headers came out as several
  different years where every leaf was from one year;
- decade: checked against consistory duplicates, a printed "186-" header could belong to the 1870s or 1880s.

Take the year of a leaf from the duplicate copy or from the dating of the file, not from the printed header.
A handwritten `4` with an open loop reads as `7`: recheck years in that hand.

## 4. OCR on carbon-copy typescripts

Soviet archive inventories from the 1950s are often second or third carbon copies. On them `tesseract -l rus`
made three substitutions, each of which kills a hit completely (found September 2026):

- `3` read as `5` or `8` in numbers (a file numbered 13 becomes "18" or "15"). A search by file number does
  not work at all.
- `Ж` read as `Л` in names: a name beginning with `Ж` comes out with `Л`. A full pass can miss the very file
  it is looking for for this reason.
- A whole line drops out: on a smudged page the village is not recognised in any spelling.

What to do: search with tolerant expressions instead of an exact root: a character class for the known
confusion at the start (`[ЖЛЗ3]` for a name beginning with `Ж`), alternatives for a doubtful letter
(`римеров|римерав|рымеров`, `[ПН]р[иы]мер`), and a short stem in the middle of the word rather than the whole
word. Reconstruct a file number from its neighbours: inventories run in
sequence, and the order of lines does not lie even when the digits do. Check everything that goes into a
letter against the image, for example `pdftoppm -r 200 -png -f N -l N file.pdf page`.

Consequence for old runs: a negative result of a machine search over such OCR is weaker than it looks. A recheck
of a few inventories found misses. Rerunning every file may not be worth it, but such zeros cannot be cited as
"checked".

## 5. Tolerant regular expressions for grep over downloaded OCR

- Words in downloaded OCR are broken by spaces and hyphenation. Put `[\s\-]*` between letters:
  `П[\s\-]*р[\s\-]*и[\s\-]*м[\s\-]*е[\s\-]*р[\s\-]*о[\s\-]*в`. This applies to any downloaded OCR, not
  only to the Polish gazettes where it was found.
- Combine with character classes for known confusions (section 4) and with alternatives for root
  distortions (section 1).
- On macOS file names come back in Unicode NFD; a regular expression written in NFC silently matches nothing.
  Normalise names and paths with `unicodedata.normalize("NFC", ...)` before matching.
- Polish PDFs set in CP1250 come out of `pdftotext` read as CP1252: `³` for `ł`, `œ` for `ś`, `¿` for `ż`.
  Fix with `text.encode('cp1252').decode('cp1250')` before searching.
- Pages served in cp1251: a fetch tool can mis-decode them (it returned wrong postal addresses of an
  archive). Read the raw page and convert it (`iconv -f cp1251`) instead.

## 6. Tables read by OCR come out in the wrong order

The text layer of Yandex Archive for tabular documents (revision lists) mixed up the order of rows (observed
2026): read in sequence, the list gives plausible nonsense, other people's ages for other people.
The working method: where the recognised blocks come with their position on the page, sort them by X, cut
into columns, sort by Y inside each column, and the table falls into place. Then check every doubtful cell
against a crop of the full-size image. In one revision list this caught a death year that the text layer
gave several years off and a misread age.

## 7. Place indexes damaged by OCR

Printed place indexes suffer the same way: hyphenation inside words ("Prime-rovka"), letter swaps (`Т` read as
`Г`), and one place name returned in several distorted forms. Full-text search catches only part of the
occurrences; reading the whole file page by page remains irreplaceable.

## 8. Namesake places eat the results

- One village name existed in several communes of the same region, and all of them turned up in one issue of
  the Polish official gazette. A commune misattributed to the wrong county in the agents' task descriptions
  filtered out many finds. The fix: filter results by the county word (the
  genitive "pow. <county>" in the gazette line), not by the commune name.
- A surname query returned several hundred records, all but one from a namesake village in another
  province.
- A Latvian archive section titled with a province name ("Vitebskas") held house registers of the street of
  that name in Riga.
- A catalogue keyword that names a large construction project returned only the settlement of the same name.
- A namesake village in another province had its own Ivan with his own wife Anna (see
  [evidence-rules.md](evidence-rules.md), section 3).

## 9. Query narrowing silently loses half the corpus

Observed on a First World War records portal, September 2026:

- a volost name searched as a phrase returned about half as many cards as the same name searched as one word;
- two search fields with different labels ("volost" and "place") returned identical results, record for
  record;
- matching is very loose: one volost name also returned other, unrelated volost names that share a few
  letters.

Rule: search one word, filter locally, and never draw a negative conclusion from a phrase query.

## 10. Catalogue descriptions and dates against the scan

- A catalogue title can be wrong about what a file is. A fond listed as "civil registration of N district"
  held parish registers of a village church over several decades. Two files listed as second copies of one
  city church came from two other churches.
- A catalogue date given as a range is missed by a search for one year inside the range.
- A frame number in a viewer is not a leaf number: in one register the offset was a few frames.
- In a Czech legionnaires' listing the content was shifted by one position against the ids; check each card.
- In a war memorial database one person had two cards with different places of birth.

## 11. Names and dates only from the image

A search snippet is machine markup and can be wrong. Proven cases from Yandex Archive snippets: a surety's
patronymic substituted; "mother of the deceased" where the record was of the deceased woman herself;
"months" where the image said years; two families on one leaf glued together; a priest's surname changed
by one letter. Copy no fact from a snippet. Open the scan, check the position of blocks by column, and read an
age without the abbreviation for "months" only on the image.

In ОБД «Мемориал» (the Russian database of Second World War losses), Latin script is not indexed at all, and
the full-text search does not index the fields of the form: a military address, the testimony of comrades and
the circumstances of death are visible only on the image. Anything once recorded as "not in the database"
needs a check of the scans.

A general search engine is not a source either: asked about a rare surname, it returned ten results about an
unrelated software product.

## 12. Reading a manuscript: readers disagree

One family notebook was read three times. The second reading, by two independent readers, disagreed in
dozens of places; a third, narrow reading worked through the dark places and resolved most of them. In a few
places the third reader corrected the second where the second had marked a reading as certain, and in each
of them the first reading had been right. A reader's confidence is not a document. A disagreement between two
readings is closed by a third look at the image, not by a vote or by seniority.

Techniques, in order of return:

1. `PIL.ImageOps.exif_transpose` instead of rotating pixels.
2. Crop one line at full resolution (about 2000 px) and enlarge the doubtful word 8 to 12 times.
3. For overwritten strokes, a threshold sweep and a stroke-width map (distance transform) separate a later
   overwriting from the original writing. On one page this showed that an age digit was two digits written
   over each other, the outer one written second.
4. Compare a doubtful letter with the same letter in neighbouring words of the same hand. This also settles a
   name against a series: compare with the same scribe's other entries.

A few places stayed closed as unreadable. One place has no coherent reading: the sentence is unfinished in the
original. Looking for a coherent reading there is pointless.
