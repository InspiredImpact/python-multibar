from __future__ import annotations

__all__ = ("ProgressbarAware",)

import abc
import typing

from . import sectors

SectorT = typing.TypeVar("SectorT", bound=sectors.AbstractSector)


class ProgressbarAware(abc.ABC, typing.Generic[SectorT]):
    @abc.abstractmethod
    def add_sector(self, sector: SectorT, /) -> ProgressbarAware[SectorT]:
        ...

    @abc.abstractmethod
    def replace_visual(
        self, sector_pos: int, new_visual: typing.Union[str, bytes], /
    ) -> ProgressbarAware[SectorT]:
        ...

    @property
    @abc.abstractmethod
    def length(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def storage(self) -> typing.Sequence[SectorT]:
        ...
