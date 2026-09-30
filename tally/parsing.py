"""Reading expense entries out of the CSV the ledger is kept in."""

from dataclasses import dataclass

CATEGORIES = ("groceries", "transport", "rent", "utilities", "other")


@dataclass(frozen=True)
class Entry:
    """One line of the ledger: what was spent, on what, and when."""

    date: str
    category: str
    cents: int


def parse_amount(text):
    """Parse a decimal amount of currency into whole cents.

    Accepts at most two decimal places, because a third would have to be
    rounded and a ledger that rounds silently is a ledger that does not
    balance. Raises `ValueError` on anything else.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("amount is empty")
    whole, _, fraction = cleaned.partition(".")
    if len(fraction) > 2:
        raise ValueError(f"amount has more than two decimal places: {text!r}")
    try:
        units = int(whole)
    except ValueError:
        raise ValueError(f"invalid amount: {text!r}") from None
    if not fraction:
        return units * 100
    if not fraction.isdigit():
        raise ValueError(f"invalid amount: {text!r}")
    return units * 100 + int(fraction.ljust(2, "0"))


def parse_entry(line):
    """Parse one `date,category,amount` line into an `Entry`.

    Raises `ValueError` naming the problem: a line with the wrong number of
    fields, an unknown category, or an amount `parse_amount` refuses.
    """
    fields = [field.strip() for field in line.split(",")]
    if len(fields) != 3:
        raise ValueError(f"expected 3 fields, got {len(fields)}: {line!r}")
    date, category, amount = fields
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category!r}")
    return Entry(date=date, category=category, cents=parse_amount(amount))


def parse_ledger(text):
    """Parse a whole ledger, skipping blank lines and `#` comments.

    The line number is added to the message of anything `parse_entry` raises,
    so a bad ledger says where it went wrong rather than only what.
    """
    entries = []
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            entries.append(parse_entry(stripped))
        except ValueError as err:
            raise ValueError(f"line {number}: {err}") from None
    return entries
