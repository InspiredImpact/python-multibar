from __future__ import annotations

__all__ = ("ProgressbarAware",)

import abc
import collections.abc
import typing

from . import sectors

SectorT = typing.TypeVar("SectorT", bound=sectors.AbstractSector)


class ProgressbarAware(abc.ABC, typing.Generic[SectorT]):
    """Interface for progressbar implementations."""

    __slots__ = ()

    @typing.overload
    @abc.abstractmethod
    def __getitem__(self, item: slice) -> collections.abc.Sequence[SectorT]:
        ...

    @typing.overload
    @abc.abstractmethod
    def __getitem__(self, item: int) -> SectorT:
        ...

    @abc.abstractmethod
    def __getitem__(self, item: typing.Any) -> typing.Any:
        """Returns sector object if item is instance of int,
        or sequence of sectors if item is instance of slice."""
        ...

    @abc.abstractmethod
    def add_sector(self, sector: SectorT, /) -> ProgressbarAware[SectorT]:
        """Adds sector to progressbar.

        Parameters
        ----------
        sector : SectorT, /
            Sector to add.

        Returns
        -------
        Self
            The progressbar object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def replace_display_name_for(
        self, sector_pos: int, new_display_name: str, /
    ) -> ProgressbarAware[SectorT]:
        """Replaces sector display name.

        Parameters
        ----------
        sector_pos : int, /
            To find sector by index to change.

        new_display_name : str, /
            New display name value.

        Returns
        -------
        Self
            The progressbar object to allow fluent-style.
        """
        ...

    @property
    @abc.abstractmethod
    def length(self) -> int:
        """
        Returns
        -------
        int
            Length of the progressbar.
        """
        ...

    @property
    @abc.abstractmethod
    def sectors(self) -> collections.abc.Sequence[SectorT]:
        """
        Returns
        -------
        collections.abc.Sequence[SectorT]
            Sequence of sectors.
        """
        ...
