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

import typing
import asyncio
import functools
import collections
import dataclasses

from multibar import abstract
from multibar.utils import PackArgs
from multibar.bases import ProgressBase
from multibar.flags import FillFlag, MusicBarFlag
from multibar.sectors import FillSectorFactory, LineSectorFactory, SectorBase

if typing.TYPE_CHECKING:
    from multibar.core.variants import Bar, CharsSnowflake, MusicChars


__all__: typing.Sequence[str] = (
    "ProgressBar",
    "ProgressObject",
    "MusicBar",
)


T = typing.TypeVar("T")
VT = typing.TypeVar("VT")  # Value type


@dataclasses.dataclass(eq=False)
@functools.total_ordering
class ProgressObject:
    """``|dataclass|``

    Object with bar, percents and length attributes.
    (All comparison operations are performed based on 'percentages: :class:`int`').

    Features:
    ---------
    __iadd__: :class:`PackArgs`
        Add a callback function to ProgressObject.

    __call__: :class:`ProgressObject`
        Return self.

    __len__: :class:`int`
        Length of the progress bar.

    __iter__: :class:`typing.Iterator[str]`
        Will iterate over attributes.

    __getitem__: :class:`abstract.Sector`
        Return the object of the ProgressObject.bar.

    __reversed__: :class:`ProgressObject`
        Will turn over the ProgressObject.bar.

    __eq__: :class:`bool`
        Compares current percentages with another number.
    # And the rest of the comparison operations...

    Properties:
    -----------
    as_dict: :class:`dict`
        Returns all attributes by a dictionary.

    """

    bar: Bar
    length: int
    percents: int
    now: typing.Optional[int]
    needed: typing.Optional[int]

    def __iadd__(self, other: typing.Any) -> PackArgs:
        return PackArgs(progress=self, callback=other)

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> ProgressObject:
        return self

    def __len__(self) -> int:
        return len(self.bar)

    def __eq__(self, other: int) -> bool:  # type: ignore[override]
        return self.percents == other

    def __lt__(self, other: int) -> bool:
        return self.percents < other

    def __iter__(self) -> typing.Iterator[str]:
        attrs = dict(self.__dict__)
        return iter(attrs)

    def __getitem__(self, item: int) -> SectorBase:
        return self.bar[item]

    def __reversed__(self) -> ProgressObject:
        if isinstance(self.bar, list):
            self.bar = self.bar[::-1]
        else:
            self.bar.rotate()
        return self

    def __str__(self) -> str:
        return "".join(i.emoji_name for i in self.bar)

    def as_dict(self) -> typing.Dict[str, VT]:
        return {k: getattr(self, k) for k in self.__dict__}


class ProgressBar(ProgressBase):
    """``|main class|``

    The main class that is used throughout the project to work with the progress bar.

    Parameters:
    -----------
    now: :class:`int` [Positional only]
        Current progress parameter.

    needed: :class:`int` [Positional only]
        Total progress parameter.

    length: :class:`int` [Keyword only]
        Length of the progress bar.

    deque: :class:`int` [Keyword only]
        If True, it will return a Deque[Sector] object instead of a List[Sector].

    Raises:
    -------
    :class:`errors.MissingRequiredArguments`:
        If <now> is None or <needed> is None.

    :class:`errors.BadValueSpecified`:
        If ([length] < 0) OR (<now> > <needed>).
    """

    def __init__(
        self,
        now: typing.Optional[int] = None,
        needed: typing.Optional[int] = None,
        /,
        *,
        length: int = 20,
        deque: bool = False,
    ) -> None:
        self.now = now
        self.needed = needed
        self.length = length
        self.deque = deque

        self._check_locals(**locals())

        self.percents: int = int((now / needed) * 100)  # type: ignore[operator] #mypy doesn't see logic of check_locals
        self.__fill_factory: abstract.SectorFactoryABC = FillSectorFactory()
        self.__empty_factory: abstract.SectorFactoryABC = LineSectorFactory()

    def write_progress(
        self,
        *,
        fill: str,
        line: str,
        unfilled_start: typing.Optional[str] = None,
        start: typing.Optional[str] = None,
        unfilled_end: typing.Optional[str] = None,
        end: typing.Optional[str] = None,
    ) -> ProgressObject:
        """``|method|``

        Synchronous method for generating progress bar.

        Parameters:
        -----------
        fill: :class:`str` [Keyword only]
            Emoji, which will fill the progress bar.

        line: :class:`str` [Keyword only]
            Unfilled progress bar emoji.

        unfilled_start: :class:`typing.Optional[str]` [Keyword only]
            Unfilled start emoji of progress bar.

        start: :class:`typing.Optional[str]` [Keyword only]
            Start emoji of progress bar.

        unfilled_end: :class:`typing.Optional[str]` [Keyword only]
            Unfilled end emoji of progress bar.

        end: :class:`typing.Optional[str]` [Keyword only]
            End emoji of progress bar.

        Returns:
        --------
        :class:`ProgressObject`
        """
        bar: Bar = [] if not self.deque else collections.deque()
        # We fill first with `fill` characters.
        for i in range(rest := (round(self.percents / (100 / self.length)))):
            bar.append(self.__fill_factory.create_sector(emoji=fill, position=i))

        for i in range(self.length - rest):
            bar.append(self.__empty_factory.create_sector(emoji=line, position=i + rest))

        # Add `unfilled_start` if it is specified and none of the sectors is yet filled.
        if unfilled_start is not None and self.percents < FillFlag.FIRST:
            bar[0].emoji_name = unfilled_start

        # Otherwise, if `start` is specified, it will be added to the beginning.
        elif self.percents >= FillFlag.FIRST and start is not None:
            bar[0].emoji_name = start

        # If `unfilled_end` is specified and the last sector is not filled, then the
        # corresponding character will be added to the end of the progress bar.
        if unfilled_end is not None and self.percents < FillFlag.LAST:
            bar[-1].emoji_name = unfilled_end

        # Otherwise, if end is specified, the character corresponding to the
        # given argument will be appended to the end of the progressbar.
        elif self.percents >= FillFlag.LAST and end is not None:
            bar[-1].emoji_name = end

        return ProgressObject(
            length=self.length,
            percents=self.percents,
            bar=bar,
            now=self.now,
            needed=self.needed,
        )

    async def async_write_progress(
        self,
        chars: CharsSnowflake,
        /,
        *,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> ProgressObject:
        """``|coro|``

        Asynchronous method for generating progress bar.

        Parameters:
        -----------
        chars: :class:`CharsSnowflake` [Positional only]
            Dictionary with chars for the progress bar.

        loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` [Keyword only]
            Loop for running code in executor.

        Returns:
        --------
        :class:`ProgressObject`
        """
        loop = loop or asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(self.write_progress, **chars))


class MusicBar(ProgressBase):
    """``|main class|``

    The main class for generating a "music bar".

    Parameters:
    -----------
    now: :class:`int`
        Current progress (| Current music time).

    needed: :class:`int`
        Necessary progress (| Total music time).

    length: :class:`int`
        Length of the progress bar.

    deque: :class:`bool`
        If True, it will return a Deque[Sector] object instead of a List[Sector].

    Raises:
    -------
    :class:`errors.MissingRequiredArguments`:
        If <now> is None or <needed> is None.

    :class:`errors.BadValueSpecified`:
        If ([length] < 0) OR (<now> > <needed>).
    """

    def __init__(
        self,
        now: int,
        needed: int,
        /,
        *,
        length: int = 20,
        deque: bool = False,
    ) -> None:
        self.now = now
        self.needed = needed
        self.length = length
        self.deque = deque

        self._check_locals(**locals())

        self.percents: int = int((now / needed) * 100)
        self.__line_factory = LineSectorFactory()
        self.__fill_factory = FillSectorFactory()

    def write_progress(
        self,
        *,
        line: str,
        current: str,
    ) -> ProgressObject:
        """``|method|``

        Synchronous method for generating music bar.

        Parameters:
        -----------
        line: :class:`str` [Keyword only]
            Emoji line of music bar.

        current: :class:`str` [Keyword only]
            Emoji (dot), which will be installed in place of the current progress.

        Returns:
        --------
        :class:`ProgressObject`
        """
        bar: Bar = [] if not self.deque else collections.deque()
        for i in range(rest := (round(self.percents / (100 / self.length)))):
            bar.append(self.__line_factory.create_sector(emoji=line, position=i))

        if rest == self.length:
            bar[-1] = self.__fill_factory.create_sector(emoji=current, position=rest)
        else:
            bar.append(self.__fill_factory.create_sector(emoji=current, position=rest))

        for i in range(self.length - len(bar)):
            bar.append(
                self.__line_factory.create_sector(emoji=line, position=i + rest + MusicBarFlag.CORRECT_START)
            )
        return ProgressObject(
            length=self.length,
            percents=self.percents,
            bar=bar,
            now=self.now,
            needed=self.needed,
        )

    async def async_write_progress(
        self,
        chars: MusicChars,
        /,
        *,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> ProgressObject:
        """``|coro|``

        Asynchronous method for generating music bar.

        Parameters:
        -----------
        chars :class:`MusicChars` [Positional only]
            Dictionary with emoji for music bar.

        loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` [Keyword only]
            Loop for running code in executor.

        Returns:
        --------
        :class:`ProgressObject`
        """
        loop = loop or asyncio.get_event_loop()
        return await loop.run_in_executor(None, functools.partial(self.write_progress, **chars))
