# Sample family

A fictional family of 19 people over four generations, built from invented names (Primerov, Obraztsov,
Näidis, Paraugs). Every person, date, place and shelf mark is made up; shelf marks are placeholders
(`fond <F>, opis <O>, delo <D>`). `persons.json` and `links.json` follow
[tools/graph/SCHEMA.md](../../tools/graph/SCHEMA.md).

| generation | people |
|---|---|
| 1 | Ivan Petrovich Primerov and Anna Petrovna (née Obraztsova) |
| 2 | Pyotr Ivanovich Primerov and Maria Ivanovna (née Obraztsova); Anna Ivanovna and Pyotr Ivanovich Obraztsov |
| 3 | Ivan Petrovich Primerov (b. 1895) and Anna Paraugs; Maria Petrovna Primerova and Jaan Näidis; two Obraztsov children; one more Primerova daughter |
| 4 | Pyotr and Maria, children of Ivan and Anna Paraugs; Mari and Juhan Näidis |

Planted cases, so that every tool has something to find:

| case | where | which tool finds it |
|---|---|---|
| Duplicate pair: `primerov-pyotr-ivanovich-1921` (Cyrillic) and `ext-primerow-pyotr-ivanovich` (Latin, from an imported tree), same birth date | persons | `merge_duplicates.py` lists it, `--apply` merges it |
| Disputed date, both values kept: `obraztsova-anna-petrovna`, birth `1899-04-17` (baptism entry) against 1898 (gravestone) | `birth.confidence` `disputed`, `disputes` | `check_graph.py` reports it as a field state |
| Person known only by given name and patronymic: `maria-petrovna-godmother`, no surname, no dates, linked as `GODPARENT` | persons, links | `check_graph.py` counts two absent events; the exporter writes a name without a surname |
| Estonian script: `naidis-jaan`, `naidis-mari`, `naidis-juhan` (ä), two of them with Cyrillic variants | persons | export and import keep the diacritic; the matcher folds `ä` to `a` for comparison |
| Old Style date: `primerov-pyotr-ivanovich` and `primerova-maria-ivanovna-1872`, `style` `OS`; the New Style date is in `notes` | `birth.style` | the exporter adds "Date in Old Style." to the event note |
| Mother aged 54 at a birth: `primerova-anna-petrovna-1926` | links | `check_graph.py` finding |
| Child born two years after the mother's death: `obraztsov-ivan-petrovich` | links | `check_graph.py` finding |
| Approximate and bounded dates: `~1838`, `before 1931` | dates | parsed by `check_graph.py` and exported as `ABT` and `BEF` |

Try it from `tools/graph/`:

```
python3 check_graph.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json
python3 merge_duplicates.py --persons ../../examples/sample-family/persons.json --links ../../examples/sample-family/links.json
```

The sample is structurally valid on purpose (0 errors). To see errors, copy the files and break a link, for
example set a `to` to an id that does not exist. Run `--apply` on a copy, not on the example.
