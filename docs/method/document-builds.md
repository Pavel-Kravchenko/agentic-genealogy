# Building books and reports as .docx

A project can write its books and reports in Markdown and hand them to readers (relatives, an archive) as
Word documents with real margin comments: editorial notes, sources, doubts. Readers comment back in Word. This
page describes the build path and the ways it failed **without an error message**. The examples are composed
illustrations; the patterns come from real work, the particulars do not.

## The build path

Markdown -> flat ODT (`.fodt`, one XML file) with `<office:annotation>` elements -> LibreOffice headless ->
`.docx`:

```
soffice --headless --convert-to docx book.fodt
```

LibreOffice turns ODT annotations into real Word comments; a point comment needs no range plumbing. Do not
build `word/comments.xml` by hand.

The guards below are what a build script should check.

Markdown conventions used: `#` title, `##` to `####` headings 1-3, `>` block quote, `**bold**`, `*italic*`,
`` `mono` ``, and `{{...}}` for a comment anchored at that point in the text.

## Silent failure modes, and the guard for each

| failure | what happened | guard |
|---|---|---|
| a comment containing a blank line | paragraphs are split on blank lines, so the comment was torn in two and part of it lost. In a first build **most comments disappeared**. | mask newlines inside `{{...}}` before splitting; the build asserts `comments emitted == source.count("{{")`. Never remove this assertion. |
| nested comments | notes are long and close far from where they open; a second `{{` inside closes the outer one early | the build fails with "nested comment at line N". Inside a comment: plain text only, shelf marks written as prose. Before inserting `{{`, check the line is not already inside another comment. |
| a comment typed with single braces `{...}` | the guard counts only `{{`, so the note printed as author text. Paragraphs of transcriber's notes stood inside a chapter declared verbatim, for many versions in a row. | after the build the body text must contain no `{{`, no `{`, no `**`. |
| nested markup | backticks inside `**...**` were not expanded and leaked into the text as two literal characters, with the comment count matching and no warning. Neither the comment guard nor the anchor check sees this. | a full count of markup characters in the built `document.xml`; do not put backticks inside bold. |
| a lost `}}` plus a lost `{{` further down | the count stays balanced, and the whole body between the two moved into one margin comment: most of one chapter. | grep a key phrase of the body in `word/document.xml`. Signs of a torn comment: author voice, `####` headings, "Addendum" blocks or tables inside `{{...}}`. Some long comments are legitimate, so read, do not just count. |

The general rule behind all five: **inside a comment, plain text only.**

## The check after every build

Unzip the `.docx` and verify:

1. number of `<w:comment>` == number of `<w:commentReference>` == number of `{{` in the Markdown;
2. the body has no `{{`, no `{`, no `**`, and no orphan backticks;
3. a key phrase from each chapter is present in the body of `word/document.xml`, not only in `comments.xml`.

A small related trap: when notes from the graph are pasted into a generated reference list, join them with
`; `, never with a full stop or a tab (see `family-graph-and-gedcom.md`).

## One clean version per hand-over

Each hand-over to a reader is **one clean `.docx`**: no tracked changes, no parallel "v2-final-final" files.
Corrections from the reader are applied in the next build, and the previous version is kept in a folder of
earlier editions.

A tracked-changes builder is worth writing only on explicit request. It puts `w:ins` around new runs and
around the paragraph mark of a new paragraph, and it relies on one Markdown block producing one Word
paragraph. ODF collapses runs of spaces and drops soft hyphens (U+00AD), so both have to be normalised on the
Markdown side. If you build tracked changes, check both directions: accept-all must give the current text and
reject-all the previous one, word for word.

When a book has moved on to a typeset `.docx` (laid out by hand in Word), the Markdown stops being the source.
Corrections then go into the `.docx` as a new stage, with the table of contents regenerated last, and the
Markdown is not edited without the agreement of the person who decides.

## Snapshot before the first edit

Copy the book file to the earlier-editions folder **as the first command of any session that will edit it**,
named with what comes next and the date ("before <change> (DD.MM)"). Not "I will save at the end": once edits
have gone into the book without a fresh copy, no byte-for-byte rollback remains.
