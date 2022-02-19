import argparse
import sys
from typing import Any, List

from multibar import ProgressBar


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generating progress bars in cli.")
    parser.add_argument(
        "simple",
        action="store_true",
        help="Writing simple bar with only :fill: and :line: chars.",
    )
    parser.add_argument(
        "--current",
        type=int,
        help="Current progress value.",
    )
    parser.add_argument(
        "--total",
        type=int,
        help="Needed progress value.",
    )
    parser.add_argument(
        "--length",
        type=int,
        help="ProgressBar length.",
    )
    parser.add_argument(
        "--chars",
        nargs="+",
        help="""
        ProgressBar chars in order:
        1) fill
        2) line
        3) start
        4) end
        5) unfilled_start
        6) unfilled_end
        """,
    )
    return parser


def _reinsert_chars(initial: List[Any]) -> List[Any]:
    chars = [None] * 6
    for idx, char in enumerate(initial):
        del chars[idx]
        chars.insert(idx, char)

    return chars


def parse_results(namespace: Any) -> str:
    chars = _reinsert_chars(namespace.chars)

    bar = ProgressBar(
        namespace.current,
        namespace.total,
        length=namespace.length,
    )
    # chars from order
    progress = bar.write_progress(
        fill=chars[0],
        line=chars[1],
        start=chars[2],
        end=chars[3],
        unfilled_start=chars[4],
        unfilled_end=chars[5],
    )

    return str(progress.bar)


if __name__ == "__main__":
    result = parse_results(create_parser().parse_args())
    sys.stdout.write(result + "\n")
