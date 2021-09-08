import asyncio
import unittest
import collections

from bar.utils import PackArgs, ignored
from bar import Progress, ProgressTools, ProgressObject


class _TestDefault(Progress):
    # All values are set as ProgressObject (because default return_as = 1).

    async def foo(self) -> None:
        # Both synchronous and asynchronous are supported.
        # (Recommended to use asynchronous).
        self.chars({"fill": "++", "line": "--"})
        self.length(10)
        self.now(40)
        self.needed(100)

    def baz(self) -> None:
        self.now(10)
        self.needed(100)
        self.deque(True)  # Will return a collections.deque object instead of builtins.list.


class _TestAdvanced(Progress, save_callback=True, return_as=2):
    # All values are set as callable objects (because return_as = 2).

    async def foo(self) -> str:
        self.chars({"fill": "+", "line": "-"})
        self.now(40)
        self.needed(100)
        return "Python"

    def foo2(self) -> None:
        self.copy("foo")

    @ignored
    def baz(self, a: int, b: int) -> int:
        return a + b


class _TestWithTools(Progress, ProgressTools, return_as=3):
    # All values are set as awaitable asyncio.Future objects (because return_as = 3).

    async def foo(self) -> None:
        self.chars(self.to_dict(fill="+", line="-"))  # `to_dict` tool
        self.now(10)
        self.needed(100)


class InheritanceTest(unittest.TestCase):
    def test_inheritance_default(self) -> None:
        default = _TestDefault()
        self.assertIsInstance(default.foo, ProgressObject)
        self.assertIsInstance(default.baz, ProgressObject)
        self.assertIsInstance(default.baz.bar, collections.deque)

    def test_inheritance_advanced(self) -> None:
        advanced = _TestAdvanced()
        self.assertTrue(callable(advanced.foo))
        self.assertIsInstance(advanced.foo(), PackArgs)
        self.assertIsInstance(advanced.foo2(), PackArgs)
        self.assertEqual(advanced.baz(1, 2), 3)

    def test_inheritance_with_tools(self) -> None:
        with_tools = _TestWithTools()
        self.assertTrue(with_tools.can_run("foo"))
        self.assertIsInstance(with_tools.foo(), asyncio.Future)


if __name__ == "__main__":
    unittest.main()
