import asyncio
import unittest
import collections

from bar import ProgressObject, abstract
from bar.utils import PackArgs
from bar.core.ext import from_class
from bar.core.variants import FromClassBase


@from_class(save_callback=True, return_as=2)
class Default:
    # The original function callback will be saved.
    # All values are set as callable objects (because return_as = 2).

    def foo(self) -> str:
        self.now(self, 100)
        self.needed(self, 100)
        self.chars.from_dict(self, {"fill": "+", "line": "-"})
        return "Python"


@from_class(return_as=3)
class MypyClear(FromClassBase):
    # All values are set as awaitable asyncio.Future objects (because return_as = 3).

    async def foo(self) -> None:
        self.now(self, 100)
        self.needed(self, 100)
        self.deque(self, True)
        self.length(self, 10)
        self.chars.from_dict(self, {"fill": "+", "line": "-"})


class FromClassTest(unittest.TestCase):
    def test_default(self) -> None:
        default = Default()
        invoke = default.foo()
        self.assertTrue(callable(default.foo))
        self.assertIsInstance(invoke, PackArgs)
        self.assertIsInstance(invoke.progress.bar, list)
        self.assertIsInstance(invoke.progress.bar[0], abstract.Sector)

    def test_mypy_clear_variable(self) -> None:
        mypy_clear = MypyClear()
        invoke = mypy_clear.foo()
        result = invoke.result()
        self.assertIsInstance(mypy_clear.foo(), asyncio.Future)
        self.assertIsInstance(result, ProgressObject)
        self.assertIsInstance(result.bar, collections.deque)
        self.assertIsInstance(result.bar[0], abstract.Sector)


if __name__ == "__main__":
    unittest.main()
