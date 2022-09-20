# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implementation of progressbar interfaces."""
from __future__ import annotations

__all__ = ("Progressbar",)

import typing

from returns.primitives.hkt import Kind1, SupportsKind1

from multibar.api import progressbars as abc_progressbars
from multibar.api import sectors as abc_sectors

SectorT = typing.TypeVar("SectorT", bound=abc_sectors.AbstractSector)
_NewValueType = typing.TypeVar("_NewValueType", bound=abc_sectors.AbstractSector)
_InstanceKind = typing.TypeVar("_InstanceKind", bound="Progressbar[typing.Any]")


class Progressbar(SupportsKind1["Progressbar[typing.Any]", SectorT], abc_progressbars.ProgressbarAware[SectorT]):
    """Implementation of abc_progressbars.ProgressbarAware[SectorT].

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    __slots__ = ("_storage",)

    def __init__(self) -> None:
        self._storage: typing.MutableSequence[SectorT] = []

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Sectors count.
        """
        return len(self._storage)

    def __getitem__(self, item: typing.Any) -> typing.Any:
        """Returns sector object if item is instance of int,
        or sequence of sectors if item is instance of slice.

        Returns
        -------
        typing.Any
            Any value depending on context and implementation.
            If item is instance of (int, slice), will return sequence
            of sectors or sector object.
        """
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
        """Applies callback for every sector in progressbar.

        !!! info
            Returns new progressbar object.

            It is a type-hint safe operation for mypy. That allows you to
            pass extended implementations of interfaces or abscractions,
            given the support of the underlying api.

        !!! abstract
            You can skip this block, if you don't use type-hints.

            We use HKT in this case so that you can add new methods to sectors,
            but at the same time they would support the abstract class api.

            An example of behavior in pseudocode:
            ??? example "Expand pseudocode example"
                ```py
                >>> progressbar = progressbarwriter.write(value, value)
                ...
                >>> class ExtendedImpl(AbstractSector):  # Your extended implementation
                >>>     def __init__(self, sector_obj: AbstractSector) -> None:
                ...         super().__init__(sector_obj.name, sector_obj.is_filled, sector_obj.position)
                ...         self._origin = sector_obj
                ...
                >>>     def extended_method(self) -> None:
                ...         ...
                ...
                ...    # Other abstraction api implementation.
                ...
                >>> new_progressbar = progressbar.map(lambda s: ExtendedImpl(s))
                >>> new_progressbar.sectors[0].extended_method()  # Mypy happy.
                ```

            It is worth clarifying that this implementation has not yet been finalized
            and may be changed in future versions (and even without HKT at all).
            You can leave your opinion about this in the issues of the project.

        Returns
        -------
        Progressbar[_NewValueType]
            New instace of progressbar with your sector objects.
            But it would differ from the usual implementation in
            that mypy does not throw an error in this case.
        """
        return self.set_new_sectors(callback(s) for s in self._storage)

    @classmethod
    def set_new_sectors(
        cls,
        new_value: typing.Iterable[_NewValueType],
        /,
    ) -> Progressbar[_NewValueType]:
        """Sets new sectors in progressbar.

        !!! info
            Returns new progressbar object.

            It is a type-hint safe operation for mypy. That allows you to
            pass extended implementations of interfaces or abscractions,
            given the support of the underlying api.

        !!! abstract
            You can skip this block, if you don't use type-hints.

            We use HKT in this case so that you can add new methods to sectors,
            but at the same time they would support the abstract class api.

            An example of behavior in pseudocode:
            ??? example "Expand pseudocode example"
                ```py
                >>> progressbar = progresswriter.write(value, value)  # Sectors doesn't have .extend_method()
                >>> sectors = IterableOverYourExtendedSectors(...)  # Extended sectors with .extend_method()
                >>> new_progressbar = progressbar.set_new_sectors(sectors)  # Sectors have .extend_method()
                >>> new_progressbar.sectors[0].extend_method()  # Mypy happy.
                ```

            It is worth clarifying that this implementation has not yet been finalized
            and may be changed in future versions (and even without HKT at all).
            You can leave your opinion about this in the issues of the project.

        Parameters
        ----------
        new_value : collections.abc.Iterable[_NewValueType], /
            Iterable over new sector objects. For example of behavior see `info` block.

        Returns
        -------
        Progressbar[_NewValueType]
            New instace of progressbar with your sector objects.
            But it would differ from the usual implementation in
            that mypy does not throw an error in this case.
        """
        # Alternative to cls[_NewValueType](), to avoid mypy "is not indexable" error.
        bar = typing.cast(Progressbar[_NewValueType], cls())
        for new_sector in new_value:
            bar.add_sector(new_sector)
        return bar

    def for_each(self, consumer: typing.Callable[[SectorT], typing.Any], /) -> None:
        """Pass each sector to a given consumer.

        Parameters
        ----------
        consumer : typing.Callable[[SectorT], typing.Any], /
            Function to apply for progressbar sectors.

        Returns
        -------
        None
        """
        for sector in self._storage:
            consumer(sector)

    def add_sector(self: _InstanceKind, sector: abc_sectors.AbstractSector, /) -> _InstanceKind:
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
        self._storage.append(sector)
        return self

    def replace_display_name_for(self, sector_pos: int, new_display_name: str, /) -> Progressbar[SectorT]:
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
        self._storage[sector_pos].change_name(new_display_name)
        return self

    @property
    def length(self) -> int:
        """
        Returns
        -------
        int
            Length of the progressbar.
        """
        return len(self._storage)

    @property
    def sectors(self) -> typing.MutableSequence[SectorT]:
        """
        Returns
        -------
        collections.abc.Sequence[SectorT]
            Sequence of sectors.
        """
        return self._storage
