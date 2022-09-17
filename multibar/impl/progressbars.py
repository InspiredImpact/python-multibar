from __future__ import annotations

__all__ = ("Progressbar",)

import typing

from returns.primitives.hkt import Kind1, SupportsKind1

from multibar.api import progressbars as abc_progressbars
from multibar.api import sectors as abc_sectors

SectorT = typing.TypeVar("SectorT", bound=abc_sectors.AbstractSector)
_NewValueType = typing.TypeVar("_NewValueType", bound=abc_sectors.AbstractSector)
_InstanceKind = typing.TypeVar("_InstanceKind", bound="Progressbar[typing.Any]")


class Progressbar(
    SupportsKind1["Progressbar[typing.Any]", SectorT], abc_progressbars.ProgressbarAware[SectorT]
):
    __slots__ = ("_storage",)

    def __init__(self) -> None:
        self._storage: typing.MutableSequence[SectorT] = []

    def __len__(self) -> int:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return len(self._storage)

    def __getitem__(self, item: typing.Any) -> typing.Any:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        if not isinstance(item, (int, slice)):
            return NotImplemented
        return self._storage[item]

    def __reversed__(self) -> typing.Iterator[SectorT]:
        """Returns reversed progressbar."""
        self._storage.reverse()
        return iter(self._storage)

    def __repr__(self) -> str:
        """Returns string representation of progressbar."""
        return "".join(s.name for s in self._storage)

    def map(
        self: Kind1[_InstanceKind, SectorT],
        callback: typing.Callable[[SectorT], _NewValueType],
        /,
    ) -> Progressbar[_NewValueType]:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return self.set_new_sectors(callback(s) for s in self._storage)

    @classmethod
    def set_new_sectors(
        cls,
        new_value: typing.Iterable[_NewValueType],
        /,
    ) -> Progressbar[_NewValueType]:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        # Alternative to cls[_NewValueType](), to avoid mypy "is not indexable" error.
        bar = typing.cast(Progressbar[_NewValueType], cls())
        for new_sector in new_value:
            bar.add_sector(new_sector)
        return bar

    def for_each(self, consumer: typing.Callable[[SectorT], typing.Any], /) -> None:
        for sector in self._storage:
            consumer(sector)

    def add_sector(self: _InstanceKind, sector: abc_sectors.AbstractSector, /) -> _InstanceKind:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        self._storage.append(sector)
        return self

    def replace_display_name_for(self, sector_pos: int, new_display_name: str, /) -> Progressbar[SectorT]:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        self._storage[sector_pos].change_name(new_display_name)
        return self

    @property
    def length(self) -> int:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return len(self._storage)

    @property
    def sectors(self) -> typing.MutableSequence[SectorT]:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return self._storage
