from __future__ import annotations

__all__ = ("FakeProgressbar",)

import typing

from multibar.api import progressbars, sectors


class FakeProgressbar(progressbars.ProgressbarAware[sectors.AbstractSector]):
    def __getitem__(self, item: typing.Any) -> typing.Any:
        return None

    def add_sector(self, sector: sectors.AbstractSector, /) -> FakeProgressbar[sectors.AbstractSector]:
        return self

    def replace_visual(self, sector_pos: int, new_visual: str, /) -> FakeProgressbar[sectors.AbstractSector]:
        return self

    @property
    def length(self) -> int:
        return -1

    @property
    def storage(self) -> typing.Sequence[sectors.AbstractSector]:
        return ()
