import asyncio
import unittest
import collections

from multibar import abstract, ProgressObject, ProgressBar, ProgressTemplates, MusicBar, MusicTemplates


class BarTest(unittest.TestCase):
    """``|test case|``

    All tests related to the basic classes like ProgressBar, MusicBar in our module.
    """

    def test_progressbar(self) -> None:
        """ProgressBar testing"""

        # Testing ProgressBar instance attributes.
        bar = ProgressBar(10, 100, length=10)
        self.assertEqual(bar.length, 10)
        self.assertIsInstance(bar.percents, int)
        self.assertIsInstance(bar.needed, int)
        self.assertIsInstance(bar.now, int)

        # Testing ProgressObject instance attributes.
        progress = bar.write_progress(**ProgressTemplates.DEFAULT)
        self.assertIsInstance(progress, ProgressObject)
        self.assertIsInstance(progress.bar, list)
        self.assertIsInstance(progress.bar[0], abstract.Sector)

    def test_musicbar(self) -> None:
        """MusicBar testing"""

        # Testing MusicBar instance attributes.
        bar = MusicBar(20, 360, length=10)
        self.assertEqual(bar.length, 10)
        self.assertIsInstance(bar.percents, int)
        self.assertIsInstance(bar.needed, int)
        self.assertIsInstance(bar.now, int)

        # Testing ProgressObject instance attributes.
        progress = bar.write_progress(line="-", current="o")
        self.assertIsInstance(progress, ProgressObject)
        self.assertIsInstance(progress.bar, list)
        self.assertIsInstance(progress.bar[0], abstract.Sector)

    def test_async_progressbar(self) -> None:
        """ProgressBar async progress testing"""

        # Testing ProgressBar instance attributes.
        bar = ProgressBar(10, 100, length=15, deque=True)
        self.assertEqual(bar.length, 15)
        self.assertIsInstance(bar.percents, int)
        self.assertIsInstance(bar.needed, int)
        self.assertIsInstance(bar.now, int)

        # Testing ProgressObject instance attributes.
        progress = asyncio.run(
            bar.async_write_progress(
                ProgressTemplates.ADVANCED,
            )
        )
        self.assertIsInstance(progress, ProgressObject)
        self.assertIsInstance(progress.bar, collections.deque)
        self.assertIsInstance(progress.bar[0], abstract.Sector)

    def test_async_musicbar(self) -> None:
        """MusicBar async progress testing"""

        # Testing MusicBar instance attributes.
        bar = MusicBar(10, 100, length=15, deque=True)
        self.assertEqual(bar.length, 15)
        self.assertIsInstance(bar.percents, int)
        self.assertIsInstance(bar.needed, int)
        self.assertIsInstance(bar.now, int)

        # Testing ProgressObject instance attributes.
        progress = asyncio.run(bar.async_write_progress(MusicTemplates.CHARS))
        self.assertIsInstance(progress, ProgressObject)
        self.assertIsInstance(progress.bar, collections.deque)
        self.assertIsInstance(progress.bar[0], abstract.Sector)


if __name__ == "__main__":
    unittest.main()
