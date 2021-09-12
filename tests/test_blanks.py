import unittest

from multibar import ProgressTemplates


class BlanksTest(unittest.TestCase):
    def test_default_blanks(self) -> None:
        self.assertEqual(
            ProgressTemplates.DEFAULT,
            {"fill": "█", "line": "●"},
        )

    def test_advanced_blanks(self) -> None:
        self.assertEqual(
            ProgressTemplates.ADVANCED,
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
