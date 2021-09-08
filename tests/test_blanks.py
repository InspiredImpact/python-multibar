import unittest

from multibar import ProgressBlanks


class BlanksTest(unittest.TestCase):
    def test_default_blanks(self) -> None:
        self.assertEqual(
            ProgressBlanks.DEFAULT,
            {"fill": "█", "line": "●"},
        )

    def test_advanced_blanks(self) -> None:
        self.assertEqual(
            ProgressBlanks.ADVANCED,
            {
                "fill": "█",
                "line": "●",
                "start": "◄",
                "end": "►",
                "unfilled_start": "◁",
                "unfilled_end": "▷",
            },
        )


if __name__ == "__main__":
    unittest.main()
