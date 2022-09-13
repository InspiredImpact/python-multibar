from __future__ import annotations

__all__ = ("FakeSector",)

import typing

from multibar.api import sectors

if typing.TYPE_CHECKING:
    from multibar.api import progressbars


class FakeSector(sectors.AbstractSector):
    def add_to_progressbar(self, progressbar: progressbars.ProgressbarAware[FakeSector], /) -> FakeSector:
        return self

    def change_name(self, value: str, /) -> FakeSector:
        return self

    @property
    def name(self) -> str:
        return ""

    @property
    def is_filled(self) -> bool:
        return False

    @property
    def position(self) -> int:
        return -1
