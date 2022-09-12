from __future__ import annotations
import abc
import typing
import collections

from . import sectors

SectorT = typing.TypeVar("SectorT", bound=sectors.AbstractSector)


class ProgressbarAware(abc.ABC, typing.Generic[SectorT]):
    @abc.abstractmethod
    def add_sector(self, sector: SectorT, /) -> ProgressbarAware[SectorT]:
        ...

    @abc.abstractmethod
    def replace_visual(self, sector_pos: int, new_visual: str, /) -> ProgressbarAware[SectorT]:
        ...

    @property
    @abc.abstractmethod
    def length(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def storage(self) -> typing.Sequence[SectorT]:
        ...


class Progressbar(ProgressbarAware[sectors.AbstractSector]):
    def __init__(self) -> None:
        self._storage: collections.deque[SectorT] = collections.deque()

    def __reversed__(self) -> typing.Iterator[SectorT]:
        self._storage.reverse()
        return iter(self._storage)

    def __iter__(self) -> typing.Iterator[SectorT]:
        yield from self._storage

    def __repr__(self) -> str:
        return "".join(s.name for s in self._storage)

    def add_sector(self, sector: sectors.AbstractSector, /) -> Progressbar[sectors.AbstractSector]:
        self._storage.append(sector)
        return self

    def replace_visual(self, sector_pos: int, new_visual: str, /) -> Progressbar[sectors.AbstractSector]:
        self._storage[sector_pos].change_name(new_visual)
        return self

    @property
    def length(self) -> int:
        return len(self._storage)

    @property
    def storage(self) -> typing.Iterable[sectors.AbstractSector]:
        return self._storage
