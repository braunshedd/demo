"""The command line: `python3 -m tally <ledger.csv>`, or the ledger on stdin."""

import argparse
import sys

from .parsing import parse_ledger
from .report import format_report


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tally", description="Total an expense ledger by category."
    )
    parser.add_argument(
        "ledger",
        nargs="?",
        help="the CSV to read; the ledger is read from stdin when omitted",
    )
    return parser


def main(argv=None):
    """Run the CLI, returning the process exit code.

    A ledger the parser refuses is an exit code of 1 and a message on stderr,
    never a traceback: this is the surface a shell node checks.
    """
    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    if args.ledger is None:
        text = sys.stdin.read()
    else:
        try:
            with open(args.ledger, encoding="utf-8") as handle:
                text = handle.read()
        except OSError as err:
            print(f"error: {err}", file=sys.stderr)
            return 1
    try:
        entries = parse_ledger(text)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1
    print(format_report(entries))
    return 0
