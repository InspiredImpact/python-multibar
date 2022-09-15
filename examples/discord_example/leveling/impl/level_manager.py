from __future__ import annotations

__all__ = ("UserLevelingManager",)

import logging
import random
import typing

from returns.io import IO

from examples.discord_example.leveling import users
from examples.discord_example.leveling.api import level_manager

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling.api import math_operations, unit_of_work

_LOGGER = logging.getLogger(__name__)


class UserLevelingManager(level_manager.UserLevelingManagerAware):
    """Implementation of level_manager.UserLevelingManagerAware ."""

    __slots__ = ("_uow", "_math", "_xp_per_message")

    def __init__(
        self,
        *,
        uow: unit_of_work.AbstractUserUnitOfWork,
        math: math_operations.MathOperationsAware,
        xp_per_message: tuple[int, int] = (1, 5),
    ) -> None:
        """
        Parameters
        ----------
        uow : unit_of_work.AbstractUserUnitOfWork, *
            Unit of work implementation.

        math : math_operations.MathOperationsAware, *
            Math operations implementation.

        xp_per_message : tuple[int, int] = (1, 5), *
            XP per message diapason : tuple(from, to).
        """

        self._uow = uow
        self._math = math
        self._xp_per_message = xp_per_message

    def user_reached_next_level(self, user: users.User, /) -> bool:
        # << inherited docstring from level_manager.UserLevelingManagerAware >>
        reached = self._math.is_reached_next_level(
            current_lvl=user.level,
            current_xp=user.xp,
        )
        if reached:
            _LOGGER.info(
                "User with id <%s> reached new lvl: %s",
                user.id,
                user.level + 1,
            )

        return reached

    def random_xp(self) -> IO[int]:
        # << inherited docstring from level_manager.UserLevelingManagerAware >>
        return IO(random.randint(*self._xp_per_message))

    @property
    def uow(self) -> unit_of_work.AbstractUserUnitOfWork:
        # << inherited docstring from level_manager.UserLevelingManagerAware >>
        return self._uow

    @property
    def math(self) -> math_operations.MathOperationsAware:
        # << inherited docstring from level_manager.UserLevelingManagerAware >>
        return self._math
