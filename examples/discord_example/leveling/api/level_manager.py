from __future__ import annotations

__all__ = ("UserLevelingManagerAware",)

import abc
import typing

from returns.io import IO

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling import users
    from examples.discord_example.leveling.api import math_operations, unit_of_work


class UserLevelingManagerAware(abc.ABC):
    """Interface for user leveling manager implementations."""

    __slots__ = ()

    @abc.abstractmethod
    def user_reached_next_level(self, user: users.User, /) -> bool:
        """Returns True, if user reaches new lvl by xp.
        A level of abstraction higher than leveling.api.math_operations.MathOperationsAware .

        Parameters
        ----------
        user : users.User, /
            User to check.
        """
        ...

    @abc.abstractmethod
    def random_xp(self) -> IO[int]:
        """Returns random xp to add."""
        ...

    @property
    @abc.abstractmethod
    def uow(self) -> unit_of_work.AbstractUserUnitOfWork:
        """Unit of work implementation."""
        ...

    @property
    @abc.abstractmethod
    def math(self) -> math_operations.AbstractMathOperations:
        """Math operations implementation."""
        ...
