import asyncio
import unittest

from bar.utils import deprecated, find, to_async


def deprecated_function() -> str:
    return "bar"


def sync_function() -> str:
    return "sync"


class UtilsTest(unittest.TestCase):
    def test_deprecation_warning(self) -> None:
        # Will display warning.
        invoke = deprecated("some_new_method", with_invoke=True)(deprecated_function)()
        self.assertEqual(invoke, "bar")

    def test_find_once(self) -> None:
        # Finding the first match.
        sequence = ("string", False, "", 0, True, 1)
        self.assertEqual(find(lambda v: not v, sequence), False)

    def test_find_multiple(self) -> None:
        # Finding all matches.
        sequence = ("string", False, "", 0, True, 1)
        self.assertEqual(find(lambda v: not v, sequence, get_all=True), [False, "", 0])

    def test_to_async(self) -> None:
        # From sync function to :class:`asyncio.Future` (Awaitable)
        loop = asyncio.get_event_loop()
        from_async = to_async(loop=loop)(sync_function)()
        self.assertIsInstance(from_async, asyncio.Future)
        self.assertEqual(loop.run_until_complete(from_async), "sync")


if __name__ == "__main__":
    unittest.main()
