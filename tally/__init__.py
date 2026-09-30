"""tally — total an expense ledger by category.

Three modules: `parsing` reads the CSV, `report` does the arithmetic, `cli`
is the command line over both.
"""

from .parsing import CATEGORIES, Entry, parse_amount, parse_entry, parse_ledger
from .report import format_cents, format_report, largest, total, totals_by_category

__all__ = [
    "CATEGORIES",
    "Entry",
    "parse_amount",
    "parse_entry",
    "parse_ledger",
    "format_cents",
    "format_report",
    "largest",
    "total",
    "totals_by_category",
]
