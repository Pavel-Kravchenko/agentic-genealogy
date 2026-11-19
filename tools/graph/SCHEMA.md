# Graph schema: persons and links

The family graph is two JSON files. `persons.json` is a list of person objects, `links.json` a list of
link objects. All tools in this folder read and write exactly this schema. `check_graph.py` checks the structural parts of it: unique ids, the required person fields, `sex`, the event `confidence` values and `high` only with a `source`, readable dates, link types, dangling ids, links to oneself, SPOUSE written twice, the link `confidence` values and `high` only with a `source`, and ancestor cycles. It does not check `style`, the link keys `source` and `note`, or that `disputes` is filled where an event is `disputed` (it reports an empty `disputes` there as a field state).
UTF-8, one JSON document per file. Names stay in the script of the source (Cyrillic, Latin with
diacritics); only the keys and the enumerated values are English.

## Persons

| key | type | required | meaning |
|---|---|---|---|
| `id` | string | yes | Unique, stable, never reused. Lower-case Latin with hyphens, for example `primerov-ivan-petrovich`. Nodes created by `gedcom_import.py` get the prefix `ext-`. |
| `name` | string | yes | Display name as one string: surname, given name, patronymic, in the order of the source. A maiden name goes in brackets: `Примерова Анна Петровна (дев. Образцова)`. A person known only by given name and patronymic is written that way, without a surname. |
| `variants` | list of strings | yes | Other spellings and other-script forms of the name. May be empty. |
| `sex` | `"m"` or `"f"` | yes | Anything else is an error. |
| `family` | string | yes | Surname group in its masculine form (`Примеров`), or `""` when no surname is known. The exporter uses it to find the surname inside `name`. |
| `birth` | event object or `null` | yes | `null` means "no birth event in the graph" (a state, not an error). |
| `death` | event object or `null` | yes | Same. |
| `disputes` | list of strings | yes | One sentence per open dispute, giving both values and where each comes from. May be empty. Required wherever an event has confidence `disputed`. |
| `notes` | string | no | Free text. |
| `sources` | list of strings or `null` | no | Sources of the person as a whole. Event sources go in the event. |
| `external_ids` | object or `null` | no | `{source name: id in that source}`, for example `{"external": "node-17"}`. The importer uses it to recognise a person it has seen before; the merger refuses to merge two nodes that carry different ids from the same source. |

Further keys are kept untouched by the tools but are not defined here.

### Event object (`birth`, `death`)

| key | type | meaning |
|---|---|---|
| `date` | string or `null` | See "Dates". `null` or `""` when no date is known. |
| `style` | `""` or `"OS"` | `"OS"`: the date is written in the Old Style (Julian) calendar, exactly as the document gives it. `""`: as written, calendar not stated or New Style. The exporter adds a note for `"OS"`. |
| `place` | string | Place as the source gives it. `""` when unknown. |
| `confidence` | `"high"`, `"medium"`, `"low"` or `"disputed"` | `high` requires a `source`. `disputed` means documents disagree; the values go in the person's `disputes`, and the field is not "corrected". |
| `source` | string | The document: its kind and a placeholder or real shelf mark. `""` when none. |

### Dates

A date is a string: `1861-03-09`, `1938-07`, `1868` (day, month and year are optional from the right).
Qualifiers, written in front of the date or as a range:

| written | meaning | GEDCOM |
|---|---|---|
| `~1838` | approximately | `ABT 1838` |
| `before 1931` | no later than | `BEF 1931` |
| `after 1925` | no earlier than | `AFT 1925` |
| `between 1781 and 1784` | in the range | `BET 1781 AND 1784` |
| `1760/61` | dual year (year-start change) | `1760/61` |

The parser also reads GEDCOM abbreviations (`ABT`, `CAL`, `EST`, `BEF`, `AFT`, `BET ... AND ...`) and the
Russian qualifiers `около`, `ок`, `до`, `после`, `между ... и ...` as input aliases. A date that is none of
these is an error. Years outside 1500-2100 are errors.

## Links

| key | type | required | meaning |
|---|---|---|---|
| `from` | string | yes | `id` of the first person. |
| `type` | string | yes | One of the types below. |
| `to` | string | yes | `id` of the second person. |
| `confidence` | `"high"`, `"medium"` or `"low"` | yes | `high` requires a `source`. |
| `source` | string | yes | The document for the link; `""` when none. |
| `note` | string | yes | Free text; `""` when none. |

| type | direction | meaning |
|---|---|---|
| `PARENT` | parent -> child | Birth parent. At most two per child; more is reported as a finding. |
| `ADOPTIVE_PARENT` | parent -> child | Adoptive or step parent. Counts for the cycle check, not for the "two parents" and "same-sex parents" checks. |
| `SPOUSE` | either way | Marriage or partnership. Symmetric: write it once; writing both directions is an error. |
| `HALF_SIBLING` | either way | Half-sibling where the shared parent is not in the graph. |
| `GODPARENT` | godparent -> godchild | Godparent at a baptism. |
| `GUARANTOR` | guarantor -> person | Guarantor or surety named in a record (for example at a marriage). |
| `POSSIBLE_KIN` | either way | Relationship suspected but not documented. Use confidence `low`. |

A link to a non-existent id, a link from a person to itself and an unknown type are errors. A cycle of
`PARENT` and `ADOPTIVE_PARENT` links (an ancestor who is their own descendant) is an error.

## Example

```json
{
 "id": "primerov-pyotr-ivanovich",
 "name": "Примеров Пётр Иванович",
 "variants": [],
 "sex": "m",
 "family": "Примеров",
 "birth": {"date": "1868-05-12", "style": "OS", "place": "Primerovka",
           "confidence": "high", "source": "baptism entry, parish register, fond <F>, opis <O>, delo <D>"},
 "death": {"date": "1934-03-02", "style": "", "place": "Primerovka",
           "confidence": "medium", "source": "family memory"},
 "disputes": [],
 "notes": "Date of birth is Old Style (Julian); the New Style date is 1868-05-24."
}
```

```json
{"from": "primerov-ivan-petrovich", "type": "PARENT", "to": "primerov-pyotr-ivanovich",
 "confidence": "high", "source": "baptism entry, parish register, fond <F>, opis <O>, delo <D>", "note": ""}
```
