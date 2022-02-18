__all__ = ["Sector"]

from typing import Any

from multibar.interfaces.product import AbstractSectorMixin
from multibar.regex import DISCORD_EMOJI_REGEX


class Sector(AbstractSectorMixin):
    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Sector):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.name)

    def is_discord_emoji(self) -> bool:
        return DISCORD_EMOJI_REGEX.match(self.name) is not None
