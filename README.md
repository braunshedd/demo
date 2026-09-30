# demo

An expense ledger, totalled by category. No dependencies, no network, no build
step — Python 3 and the `unittest` it ships with.

```sh
python3 -m unittest discover -v   # 27 tests, all passing
python3 -m tally ledger.csv       # the sample ledger, reported
```

This is the tree the example pipelines that name `~/code/demo` start from: the
small, healthy project an agent is asked to extend. It plants no defects — that
is `parcel`'s job, and failing tests are `depot`'s. What it has to be is
something a plan can name files in and a test command can pass against, so
`python3 -m unittest discover -v` passing from a clean checkout is the whole of
its contract.

## API

```python
from tally import (
    CATEGORIES, Entry,
    parse_amount, parse_entry, parse_ledger,
    format_cents, totals_by_category, total, largest, format_report,
)
```

- `parse_amount(text)` — a decimal amount as whole cents. At most two decimal
  places; a third is refused rather than rounded.
- `parse_entry(line)` — one `date,category,amount` line as an `Entry`.
- `parse_ledger(text)` — a whole ledger, skipping blanks and `#` comments. A
  bad line raises with its line number.
- `totals_by_category(entries)` / `total(entries)` — the arithmetic, in cents.
- `largest(entries)` — the biggest single entry, first one winning a tie.
- `format_cents(cents)` / `format_report(entries)` — how it is printed.

## Layout

```
tally/parsing.py    the CSV, and the amounts in it
tally/report.py     the arithmetic and the printed shape
tally/cli.py        `python3 -m tally [ledger.csv]`, stdin when omitted
test_parsing.py     one test file per module, at the top level so
test_report.py      `unittest discover` finds them from the repository root
test_cli.py
ledger.csv          a sample fortnight
```

## Things to ask an agent for

The pipelines take the task as a `--var`, and these are sized to finish in one
node and to be provable by the test command:

- a `--category` flag that reports one category only
- a monthly breakdown, grouping by the `YYYY-MM` prefix of the date
- an `average(entries)`, and a line for it in the report
- refusing a negative amount in the ledger, with the line number
