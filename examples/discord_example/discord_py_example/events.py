from __future__ import annotations

__all__ = ("UserLevelUpdateEvent",)

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling import users


@dataclasses.dataclass
class UserLevelUpdateEvent:
    """Event that dispatches when user level needs to be incremented."""

    user: users.User
    """The user whose level needs to be incremented."""
