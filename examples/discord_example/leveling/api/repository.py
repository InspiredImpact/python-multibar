from __future__ import annotations

__all__ = ("UserRepositoryAware",)

import abc
import typing

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling import users


class UserRepositoryAware(abc.ABC):
    """Interface for user repository implementations."""

    __slots__ = ()

    @abc.abstractmethod
    async def get_user_by_id(self, identifier: users.UserID, /) -> typing.Optional[users.User]:
        """Returns User entity if exists.

        !!! note
            If user is not found, will return builtins.None.

        Parameters
        ----------
        identifier : users.User, /
            Id of user to get.
        """
        ...

    @abc.abstractmethod
    async def add_user(self, user: users.User, /) -> None:
        """Adds user to data.

        Parameters
        ----------
        user : users.User, /
            User to add.
        """
        ...

    @abc.abstractmethod
    async def increase_xp_for(self, identifier: users.UserID, xp_amount: int, /) -> None:
        """Increases user xp.

        Parameters
        ----------
        identifier : users.UserID, /
            ID of user to increase xp for.

        xp_amount : int, /
            Amount of xp to increase for.
        """
        ...
