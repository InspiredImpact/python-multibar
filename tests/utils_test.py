import asyncio
import unittest

from multibar.utils import deprecated, find, to_async, get_percentage


def test_function() -> str:
    return "test"


class UtilsTest(unittest.TestCase):
    def test_deprecation_warning(self) -> None:
        # Will display warning.
        invoke = deprecated("some_new_method", with_invoke=True)(test_function)()
        self.assertEqual(invoke, "test")

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
        from_async = to_async(loop=loop)(test_function)()
        self.assertIsInstance(from_async, asyncio.Future)
        self.assertEqual(loop.run_until_complete(from_async), "test")

    def test_get_percentage(self) -> None:
        # Testing get_percentage() function.
        int_percentage = get_percentage(10, 100)
        self.assertIsInstance(int_percentage, int)
        float_percentage = get_percentage(10, 100, save_float=True)
        self.assertIsInstance(float_percentage, float)


if __name__ == "__main__":
    unittest.main()
