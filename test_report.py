import unittest

from tally.parsing import Entry
from tally.report import format_cents, format_report, largest, total, totals_by_category

LEDGER = [
    Entry(date="2026-01-04", category="groceries", cents=1250),
    Entry(date="2026-01-05", category="transport", cents=320),
    Entry(date="2026-01-06", category="groceries", cents=880),
]


class TestFormatCents(unittest.TestCase):
    def test_always_prints_two_decimal_places(self):
        self.assertEqual(format_cents(1200), "12.00")
        self.assertEqual(format_cents(1205), "12.05")

    def test_prints_a_negative_amount_with_its_sign(self):
        self.assertEqual(format_cents(-450), "-4.50")


class TestTotals(unittest.TestCase):
    def test_sums_each_category(self):
        self.assertEqual(totals_by_category(LEDGER), {"groceries": 2130, "transport": 320})

    def test_omits_categories_that_do_not_appear(self):
        self.assertEqual(totals_by_category([]), {})

    def test_totals_the_whole_ledger(self):
        self.assertEqual(total(LEDGER), 2450)


class TestLargest(unittest.TestCase):
    def test_finds_the_largest_entry(self):
        self.assertEqual(largest(LEDGER), LEDGER[0])

    def test_has_no_largest_entry_in_an_empty_ledger(self):
        self.assertIsNone(largest([]))

    def test_a_tie_goes_to_the_first_entry(self):
        tied = [
            Entry(date="2026-01-04", category="rent", cents=500),
            Entry(date="2026-01-05", category="other", cents=500),
        ]
        self.assertEqual(largest(tied), tied[0])


class TestFormatReport(unittest.TestCase):
    def test_reports_categories_in_declaration_order_then_the_total(self):
        self.assertEqual(
            format_report(LEDGER).splitlines(),
            [
                "groceries        21.30",
                "transport         3.20",
                "total            24.50",
            ],
        )

    def test_an_empty_ledger_reports_a_zero_total(self):
        self.assertEqual(format_report([]).splitlines(), ["total             0.00"])


if __name__ == "__main__":
    unittest.main()
