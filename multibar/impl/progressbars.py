from __future__ import annotations

__all__ = ("Progressbar",)

import typing

from multibar.api import progressbars, sectors


class Progressbar(progressbars.ProgressbarAware[sectors.AbstractSector]):
    __slots__ = ("_storage",)

    def __init__(self) -> None:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        self._storage: list[sectors.AbstractSector] = []

    def __getitem__(self, item: typing.Any) -> typing.Any:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        if not isinstance(item, (int, slice)):
            return NotImplemented
        return self._storage[item]

    def __reversed__(self) -> typing.Iterator[sectors.AbstractSector]:
        """Returns reversed progressbar."""
        self._storage.reverse()
        return iter(self._storage)

    def __repr__(self) -> str:
        """Returns string representation of progressbar."""
        return "".join(s.name for s in self._storage)

    def add_sector(self, sector: sectors.AbstractSector, /) -> Progressbar:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        self._storage.append(sector)
        return self

    def replace_display_name_for(self, sector_pos: int, new_display_name: str, /) -> Progressbar:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        self._storage[sector_pos].change_name(new_display_name)
        return self

    @property
    def length(self) -> int:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return len(self._storage)

    @property
    def sectors(self) -> list[sectors.AbstractSector]:
        # << inherited docstring for multibar.api.progressbars.ProgressbarAware >>
        return self._storage
