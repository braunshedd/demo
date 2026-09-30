import unittest

from tally.parsing import Entry, parse_amount, parse_entry, parse_ledger


class TestParseAmount(unittest.TestCase):
    def test_reads_a_whole_number_as_cents(self):
        self.assertEqual(parse_amount("12"), 1200)

    def test_reads_two_decimal_places(self):
        self.assertEqual(parse_amount("12.50"), 1250)

    def test_pads_a_single_decimal_place(self):
        self.assertEqual(parse_amount("12.5"), 1250)

    def test_ignores_surrounding_whitespace(self):
        self.assertEqual(parse_amount("  3.07 "), 307)

    def test_refuses_a_third_decimal_place(self):
        with self.assertRaises(ValueError):
            parse_amount("1.005")

    def test_refuses_something_that_is_not_a_number(self):
        with self.assertRaises(ValueError):
            parse_amount("twelve")

    def test_refuses_an_empty_amount(self):
        with self.assertRaises(ValueError):
            parse_amount("   ")


class TestParseEntry(unittest.TestCase):
    def test_reads_a_line(self):
        self.assertEqual(
            parse_entry("2026-01-04,groceries,12.50"),
            Entry(date="2026-01-04", category="groceries", cents=1250),
        )

    def test_refuses_an_unknown_category(self):
        with self.assertRaises(ValueError):
            parse_entry("2026-01-04,sundries,12.50")

    def test_refuses_the_wrong_number_of_fields(self):
        with self.assertRaises(ValueError):
            parse_entry("2026-01-04,groceries")


class TestParseLedger(unittest.TestCase):
    def test_skips_blank_lines_and_comments(self):
        entries = parse_ledger(
            "# january\n"
            "2026-01-04,groceries,12.50\n"
            "\n"
            "2026-01-05,transport,3.20\n"
        )
        self.assertEqual([entry.category for entry in entries], ["groceries", "transport"])

    def test_names_the_line_a_bad_entry_is_on(self):
        with self.assertRaises(ValueError) as caught:
            parse_ledger("2026-01-04,groceries,12.50\n2026-01-05,sundries,1.00\n")
        self.assertIn("line 2", str(caught.exception))

    def test_an_empty_ledger_parses_to_nothing(self):
        self.assertEqual(parse_ledger(""), [])


if __name__ == "__main__":
    unittest.main()
