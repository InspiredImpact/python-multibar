import unittest

from multibar import ProgressTemplates


class TemplatesTest(unittest.TestCase):
    """``|test case|``

    All tests related to the templates in our module.
    """

    def test_default_blanks(self) -> None:
        """Default template testing"""
        self.assertIsInstance(ProgressTemplates.DEFAULT, dict)

    def test_advanced_blanks(self) -> None:
        """Advanced template testing"""
        self.assertIsInstance(ProgressTemplates.ADVANCED, dict)


if __name__ == "__main__":
    unittest.main()
