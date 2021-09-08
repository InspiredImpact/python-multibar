"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import re
import abc
import typing

from multibar import abstract


__all__: typing.Sequence[str] = (
    "FillSectorFactory",
    "LineSectorFactory",
    "FillSector",
    "EmptySector",
    "SectorBase",
)


class FillSectorFactory(abstract.SectorFactoryABC):
    """``|class|``

    The factory that creates objects of the :class:`FillSector`.
    """

    def create_sector(self, emoji: str, position: int) -> FillSector:
        """``|function|``

        Method that creates an object of the class :class:`FillSector`.

        Parameters:
        -----------
        emoji: :class:`str`
            Emoji for a certain part of the progress bar.

        position: :class:`int`
            Item position in the progress bar.

        Returns:
        --------
        :class:`FillSector`
        """
        return FillSector(emoji=emoji, idx=position)


class LineSectorFactory(abstract.SectorFactoryABC):
    """``|class|``

    The factory that creates objects of the :class:`EmptySector`.
    """

    def create_sector(self, emoji: str, position: int) -> EmptySector:
        """``|function|``

        Method that creates an object of the class :class:`EmptySector`

        Parameters:
        -----------
        emoji: :class:`str`
            Emoji for a certain part of the progress bar.

        position: :class:`int`
            Item position in the progress bar.

        Returns:
        --------
        :class:`EmptySector`
        """
        return EmptySector(emoji=emoji, idx=position)


class SectorBase:
    """``|class|``

    Base class with a set of basic methods for further work with sectors.

    # FillSector and EmptySector inherit from this class

    Parameters:
    -----------
    emoji: :class:`str`
        Emoji for a certain part of the progress bar.

    idx: :class:`int`
        Item position in the progress bar.

    Features:
    ---------
    __str__: str(SectorBase) | SectorBase
        Returns a specific progress bar emoji.

    __repr__: repr(SectorBase)
        Development information.

    __call__: SectorBase(**kwargs)
        Returns the object of the current class instance.

    ABC methods:
    ------------
    __bool__:
        A required dunder method that all subclasses must implement.

    Properties:
    -----------
    emoji_name: :class:`str`
        Getter: emoji_name
        Setter: emoji_name = other
        Emoji for a certain part of the progress bar.

    is_discord_emoji: :class:`bool`
        Will return True if regex detects that this is a discord emoji by template.

    position: :class:`int`
        Item position in the progress bar.
    """

    def __init__(self, *, emoji: str, idx: int) -> None:
        self.__emoji = emoji
        self.__idx = idx

    def __str__(self) -> str:
        return self.__emoji

    def __repr__(self) -> str:
        return (
            f'<Sector.{re.split(r"(?=[A-Z])", self.__class__.__name__)[1]}'
            f"(emoji={self.emoji_name}, position={self.position})>"
        )

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> SectorBase:
        return self

    @abc.abstractmethod
    def __bool__(self) -> bool:
        ...

    @property
    def emoji_name(self) -> str:
        return self.__emoji

    @emoji_name.setter
    def emoji_name(self, new: str) -> None:
        self.__emoji = new

    @property
    def is_discord_emoji(self) -> bool:
        return re.match(r"^<(a|):.+?:\d+>$", self.__emoji) is not None

    @property
    def position(self) -> int:
        return self.__idx


class FillSector(SectorBase):
    """``|class|``

    Class of the filled sector of the progress bar.

    Features:
    ---------
    __bool__:
        Returns True (because the sector is full).
    """

    def __bool__(self) -> bool:
        return True


class EmptySector(SectorBase):
    """``|class|``

    Empty sector of the progress bar.

    Features:
    ---------
    __bool__:
        Returns False (because the sector is empty).
    """

    def __bool__(self) -> bool:
        return False
