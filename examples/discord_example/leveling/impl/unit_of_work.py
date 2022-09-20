from __future__ import annotations

__all__ = ("JSONUserUnitOfWork",)

import logging

import aiofiles
import ujson

from examples.discord_example.leveling import users, utils
from examples.discord_example.leveling.api import unit_of_work
from examples.discord_example.leveling.impl import repository

_LOGGER = logging.getLogger(__name__)


class JSONUserUnitOfWork(unit_of_work.AbstractUserUnitOfWork):
    """Implementation of unit_of_work.AbstractUserUnitOfWork ."""

    __slots__ = ("_json_fp", "_products")

    def __init__(
        self,
        *,
        json_fp: str,
        repo: repository.JSONUserRepository,
    ) -> None:
        """
        Parameters
        ----------
        json_fp: str, *
            JSON file path.

        repo: repository.JSONUserRepository, *
            User repository implementation.
        """

        self._json_fp = json_fp
        self._products = repo

    async def handle_lvlup_for(self, identifier: users.UserID, /) -> None:
        # << inherited docstring from unit_of_work.AbstractUserUnitOfWork >>
        identifier = str(identifier)

        async with aiofiles.open(self._json_fp, "r+") as users_io:
            _LOGGER.info(
                "Accessing to <%s> data. Handling user lvlup <%s> to data.",
                self._json_fp,
                identifier,
            )

            state_now = ujson.loads(await users_io.read())
            state_now[identifier]["level"] += 1
            state_now[identifier]["xp"] = 0
            await utils.dump_json_async(users_io, state_now)

    @property
    def products(self) -> repository.JSONUserRepository:
        # << inherited docstring from unit_of_work.AbstractUserUnitOfWork >>
        return self._products
