from __future__ import annotations

__all__ = ("Progressbar",)

import typing

from multibar.api import progressbars, sectors


class Progressbar(progressbars.ProgressbarAware[sectors.AbstractSector]):
    def __init__(self) -> None:
        self._storage: list[sectors.AbstractSector] = []

    def __getitem__(self, item: typing.Any) -> typing.Any:
        if not isinstance(item, (int, slice)):
            return NotImplemented
        return self._storage[item]

    def __reversed__(self) -> typing.Iterator[sectors.AbstractSector]:
        self._storage.reverse()
        return iter(self._storage)

    def __iter__(self) -> typing.Iterator[sectors.AbstractSector]:
        yield from self._storage

    def __repr__(self) -> str:
        return "".join(s.name for s in self._storage)

    def add_sector(self, sector: sectors.AbstractSector, /) -> Progressbar:
        self._storage.append(sector)
        return self

    def replace_visual(self, sector_pos: int, new_visual: str, /) -> Progressbar:
        self._storage[sector_pos].change_name(new_visual)
        return self

    @property
    def length(self) -> int:
        return len(self._storage)

    @property
    def storage(self) -> typing.Sequence[sectors.AbstractSector]:
        return self._storage
