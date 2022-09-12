from __future__ import annotations

__all__ = ("Progressbar",)

import collections
import typing

from multibar.api import progressbars
from multibar.api import sectors


class Progressbar(progressbars.ProgressbarAware[sectors.SectorAware]):
    def __init__(self) -> None:
        self._storage: collections.deque[sectors.SectorAware] = collections.deque()

    def __reversed__(self) -> typing.Iterator[sectors.SectorAware]:
        self._storage.reverse()
        return iter(self._storage)

    def __iter__(self) -> typing.Iterator[sectors.SectorAware]:
        yield from self._storage

    def __repr__(self) -> str:
        return "".join(s.name for s in self._storage)

    def add_sector(self, sector: sectors.SectorAware, /) -> Progressbar[sectors.SectorAware]:
        self._storage.append(sector)
        return self

    def replace_visual(self, sector_pos: int, new_visual: str, /) -> Progressbar[sectors.SectorAware]:
        self._storage[sector_pos].change_name(new_visual)
        return self

    @property
    def length(self) -> int:
        return len(self._storage)

    @property
    def storage(self) -> typing.Iterable[sectors.SectorAware]:
        return self._storage
