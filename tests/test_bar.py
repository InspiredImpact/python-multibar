import asyncio
import unittest
import collections

# tests
from bar import abstract, ProgressObject

# user
from bar import ProgressBar, ProgressBlanks


class BarTest(unittest.TestCase):
    def test_simple_bar(self) -> None:
        bar = ProgressBar(10, 100, length=10)
        self.assertEqual(bar.length, 10)
        self.assertIsInstance(bar.percents, int)
        self.assertIsInstance(bar.needed, int)
        self.assertIsInstance(bar.now, int)
        progress = bar.write_progress(**ProgressBlanks.DEFAULT)
        self.assertIsInstance(progress, ProgressObject)
        self.assertIsInstance(progress.bar, list)
        self.assertIsInstance(progress.bar[0], abstract.Sector)

    def test_advanced_bar(self) -> None:
        bar = ProgressBar(10, 100, length=15, deque=True)
        progress = asyncio.run(
            bar.async_write_progress(
                ProgressBlanks.ADVANCED,
            )
        )
        self.assertIsInstance(progress.bar, collections.deque)


if __name__ == "__main__":
    unittest.main()
