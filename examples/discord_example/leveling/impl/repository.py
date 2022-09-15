__all__ = ("JSONUserRepository", "CachedJSONUserRepository")

import dataclasses
import logging
import typing

import aiofiles
import ujson

from examples.discord_example.leveling import users, utils
from examples.discord_example.leveling.api import repository

_LOGGER = logging.getLogger(__name__)


class JSONUserRepository(repository.UserRepositoryAware):
    """Implementation of repository.UserRepositoryAware ."""

    __slots__ = ("_json_fp",)

    def __init__(self, *, json_fp: str) -> None:
        """
        Parameters
        ----------
        json_fp : str, *
            JSON file path.
        """

        self._json_fp = json_fp

    async def get_user_by_id(self, identifier: users.UserID, /) -> typing.Optional[users.User]:
        # << inherited docstring from repository.UserRepositoryAware >>
        async with aiofiles.open(self._json_fp, "r+") as users_io:
            _LOGGER.info(
                "Accessing to <%s> data. Getting user <%s> by id.",
                self._json_fp,
                identifier,
            )

            state_now = ujson.loads(await users_io.read())

        try:
            user_dict = state_now[str(identifier)]
        except KeyError:
            return None

        user_dict["id"] = identifier
        return users.User.from_dict(user_dict)

    async def add_user(self, user: users.User, /) -> None:
        # << inherited docstring from repository.UserRepositoryAware >>
        user_dict = dataclasses.asdict(user)
        identifier = str(user_dict.pop("id"))

        async with aiofiles.open(self._json_fp, "r+") as users_io:
            _LOGGER.info(
                "Accessing to <%s> data. Adding user <%s> to data.",
                self._json_fp,
                identifier,
            )

            state_now = ujson.loads(await users_io.read())
            if identifier in state_now:
                return

            state_now[identifier] = user_dict
            await utils.dump_json_async(users_io, state_now)

            _LOGGER.info(
                "UserID <%s> successfully inserted into data with level %s, exp %s.",
                identifier,
                user.level,
                user.xp,
            )

    async def increase_xp_for(self, identifier: users.UserID, xp_amount: int, /) -> None:
        # << inherited docstring from repository.UserRepositoryAware >>
        identifier = str(identifier)

        async with aiofiles.open(self._json_fp, "r+") as users_io:
            _LOGGER.info(
                "Accessing to <%s> data. Increasing user <%s> experience: %s.",
                self._json_fp,
                identifier,
                xp_amount,
            )

            state_now = ujson.loads(await users_io.read())
            state_now[identifier]["xp"] += xp_amount
            await utils.dump_json_async(users_io, state_now)


class CachedJSONUserRepository(JSONUserRepository):
    """Primitive implementation of cached JSON user repository."""

    def __init__(self, **kwargs: typing.Any) -> None:
        """
        Parameters
        ----------
        kwargs : typing.Any
            Any superclass keyword init arguments.
        """

        super().__init__(**kwargs)
        self._cache = {}  # Primitive cache

    async def get_user_by_id(self, identifier: users.UserID, /) -> typing.Optional[users.User]:
        # << inherited docstring from repository.UserRepositoryAware >>
        if identifier not in self._cache:
            user = await super().get_user_by_id(identifier)
            if user is None:
                return

            self._cache[identifier] = user
            return user

        return self._cache[identifier]

    async def add_user(self, user: users.User, /) -> None:
        # << inherited docstring from repository.UserRepositoryAware >>
        if user.id in self._cache:
            return

        await super().add_user(user)
        self._cache[user.id] = user

    async def increase_xp_for(self, user_id: users.UserID, xp_amount: int, /) -> None:
        # << inherited docstring from repository.UserRepositoryAware >>
        if user_id not in self._cache:
            return

        self._cache[user_id].xp += xp_amount
