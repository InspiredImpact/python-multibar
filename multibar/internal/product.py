__all__ = ["Sector"]

from typing import Any

from multibar.interfaces.product import AbstractSectorMixin
from multibar.regex import DISCORD_EMOJI_REGEX


class Sector(AbstractSectorMixin):
    """Class that represents basic implementation of Sector."""

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Sector):
            return self.name == other.name
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)

    def is_discord_emoji(self) -> bool:
        """Returns True, if regex match is not None."""
        return DISCORD_EMOJI_REGEX.match(self.name) is not None
