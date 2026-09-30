"""Turning parsed entries into the numbers someone asked for."""

from .parsing import CATEGORIES


def format_cents(cents):
    """Format whole cents as a decimal amount, always with two places."""
    sign = "-" if cents < 0 else ""
    whole, remainder = divmod(abs(cents), 100)
    return f"{sign}{whole}.{remainder:02d}"


def totals_by_category(entries):
    """Total spend per category, in cents.

    Only categories that appear are returned, so an empty ledger totals to an
    empty mapping rather than to a row of zeroes.
    """
    totals = {}
    for entry in entries:
        totals[entry.category] = totals.get(entry.category, 0) + entry.cents
    return totals


def total(entries):
    """The whole ledger's spend, in cents."""
    return sum(entry.cents for entry in entries)


def largest(entries):
    """The single largest entry, or `None` when there are none.

    Ties go to the entry that appears first, which keeps the answer stable
    under a re-ordering that did not change any amount.
    """
    if not entries:
        return None
    return max(entries, key=lambda entry: entry.cents)


def format_report(entries):
    """The report as printed: a line per category, then the total.

    Categories come out in the order `CATEGORIES` declares rather than in the
    order they were spent in, so two ledgers can be read side by side.
    """
    totals = totals_by_category(entries)
    lines = []
    for category in CATEGORIES:
        if category in totals:
            lines.append(f"{category:<12}{format_cents(totals[category]):>10}")
    lines.append(f"{'total':<12}{format_cents(total(entries)):>10}")
    return "\n".join(lines)
