from __future__ import annotations

__all__ = ("Sector",)

import typing

from multibar.api import sectors

if typing.TYPE_CHECKING:
    from multibar.api import progressbars


class Sector(sectors.AbstractSector):
    def add_to_progressbar(self: Sector, progressbar: progressbars.ProgressbarAware[Sector], /) -> Sector:
        # << inherited docstring for multibar.api.sectors.AbstractSector >>
        progressbar.add_sector(self)
        return self

    def change_name(self, new_display_name: str, /) -> Sector:
        # << inherited docstring for multibar.api.sectors.AbstractSector >>
        self._name = new_display_name
        return self

    @property
    def name(self) -> str:
        # << inherited docstring for multibar.api.sectors.AbstractSector >>
        return self._name

    @property
    def is_filled(self) -> bool:
        # << inherited docstring for multibar.api.sectors.AbstractSector >>
        return self._is_filled

    @property
    def position(self) -> int:
        # << inherited docstring for multibar.api.sectors.AbstractSector >>
        return self._position
