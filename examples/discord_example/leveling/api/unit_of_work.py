from __future__ import annotations

__all__ = ("AbstractUserUnitOfWork",)

import abc
import typing

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling import users
    from examples.discord_example.leveling.api import repository as abc_repository


class AbstractUserUnitOfWork(abc.ABC):
    """Abstraction for all user unit of work implementation."""

    __slots__ = ()

    def __enter__(self) -> AbstractUserUnitOfWork:
        return self

    def __exit__(self, *args: typing.Any) -> None:
        """Stub for with syntax."""
        pass

    @abc.abstractmethod
    async def handle_lvlup_for(self, identifier: users.UserID, /) -> None:
        """Levels up the user.

        Parameters
        ----------
        identifier : users.UserID, /
            User ID to level up for.
        """
        ...

    @property
    @abc.abstractmethod
    def products(self) -> abc_repository.UserRepositoryAware:
        """Returns user repository implementation."""
        ...
