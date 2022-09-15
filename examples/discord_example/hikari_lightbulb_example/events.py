from __future__ import annotations

__all__ = ("UserLevelUpdateEvent",)

import typing

import attr
import hikari

if typing.TYPE_CHECKING:
    from examples.discord_example.leveling import users


@attr.define()
class UserLevelUpdateEvent(hikari.Event):
    """Event that dispatches when user level needs to be incremented."""

    app: hikari.traits.RESTAware = attr.field()
    """Hikari app."""

    user: users.User = attr.field()
    """The user whose level needs to be incremented."""
