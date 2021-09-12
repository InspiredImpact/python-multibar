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

import abc
import typing


__all__: typing.Sequence[str] = (
    "Sector",
    "SectorFactoryABC",
)


class SectorFactoryABC(abc.ABC):
    """``|ABC class|``

    Abstract class, currently used in:

    * :class:`FillSectorFactory`
    * :class:`LineSectorFactory`

    Abstract methods:
    -----------------
    create_sector: :class:`Sector`
        Returns the bar progress sector object.
    """

    @abc.abstractmethod
    def create_sector(self, emoji: str, position: int) -> typing.Any:
        ...


@typing.runtime_checkable
class Sector(typing.Protocol):
    """``|runtime protocol|``

    Protocol class for runtime checks. ("ABC")

    Example of usage:
    -----------------
    ```py

    from multibar.abstract import Sector
    from multibar import ProgressBar, ProgressTemplates

    progress_bar = ProgressBar(10, 100)
    progress = progress_bar.write_progress(**ProgressTemplates.ADVANCED)
    for i in progress.bar:
        print(isinstance(i, Sector))

    True
    ...
    ```
    """

    __slots__ = ()

    @property
    def emoji_name(self) -> str:
        raise NotImplementedError

    @emoji_name.setter
    def emoji_name(self, new: str) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_discord_emoji(self) -> bool:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def position(self) -> int:
        raise NotImplementedError
