from __future__ import annotations

__all__ = ("Sector",)

import typing

from multibar.api import sectors

if typing.TYPE_CHECKING:
    from multibar.api import progressbars


class Sector(sectors.SectorAware):
    def __init__(self, name: typing.AnyStr, is_filled: bool, position: int) -> None:
        self._name = name
        self._is_filled = is_filled
        self._position = position

    def add_to_progressbar(self: Sector, progressbar: progressbars.ProgressbarAware[Sector], /) -> Sector:
        progressbar.add_sector(self)
        return self

    def change_name(self, value: str, /) -> Sector:
        self._name = value
        return self

    @property
    def name(self) -> typing.AnyStr:
        return self._name

    @property
    def is_filled(self) -> bool:
        return self._is_filled

    @property
    def position(self) -> int:
        return self._position
