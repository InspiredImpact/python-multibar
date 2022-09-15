from __future__ import annotations

__all__ = ("User",)

import dataclasses
import typing

import typing_extensions

UserID: typing_extensions.TypeAlias = int


@dataclasses.dataclass
class User:
    """User entity."""

    id: UserID
    level: int
    xp: int

    @classmethod
    def from_dict(cls, mapping: typing.MutableMapping[typing.Any, typing.Any], /) -> User:
        """Alternative constructor from dict.

        Parameters
        ----------
        mapping : typing.MutableMapping[typing.Any, typing.Any], /
            Mapping with data to initialize.
        """

        return cls(**mapping)

    @classmethod
    def from_identifier(cls, identifier: UserID, /) -> User:
        """Alternative constructor from user id.

        Parameters
        ----------
        identifier : UserID, /
            User ID to initialize.
        """

        return cls(id=identifier, level=1, xp=0)

    def lvlup(self) -> None:
        """Handles levelup."""

        self.level += 1
        self.xp = 0
