from __future__ import annotations

__all__ = ("ProgressbarAware",)

import abc
import collections.abc
import typing

from returns.primitives.hkt import Kind1

from . import sectors

if typing.TYPE_CHECKING:

    class SupportsGetitem(typing.Protocol):
        def __getitem__(self, item: typing.Any) -> typing.Any:
            ...


SectorT = typing.TypeVar("SectorT", bound=sectors.AbstractSector)
_NewValueType = typing.TypeVar("_NewValueType", bound=sectors.AbstractSector)
_InstanceKind = typing.TypeVar("_InstanceKind", bound="ProgressbarAware[typing.Any]")


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
    def __len__(self) -> int:
        """Returns sectors count."""
        ...

    @classmethod
    @abc.abstractmethod
    def set_new_sectors(
        cls: typing.Type[_InstanceKind],
        new_value: collections.abc.Iterable[_NewValueType],
        /,
    ) -> Kind1[_InstanceKind, _NewValueType]:
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
            >>> progressbar = progresswriter.write(value, value)  # Sectors doesn't have .extend_method()
            >>> sectors = IterableOverYourExtendedSectors(...)  # Extended sectors with .extend_method()
            >>> new_progressbar = progressbar.set_new_sectors(sectors)  # Sectors have .extend_method()
            >>> new_progressbar.sectors[0].extend_method()  # Mypy happy.

            It is worth clarifying that this implementation has not yet been finalized
            and may be changed in future versions (and even without HKT at all).
            You can leave your opinion about this in the issues of the project.

        Parameters
        ----------
        new_value : collections.abc.Iterable[_NewValueType], /
            Iterable over new sector objects. For example of behavior see `info` block.

        Returns
        -------
        Kind1[_InstanceKind, _NewValueType]
            New instace of progressbar with your sector objects.
            But it would differ from the usual implementation in
            that mypy does not throw an error in this case.
        """
        ...

    @abc.abstractmethod
    def map(
        self: _InstanceKind,
        callback: typing.Callable[[SectorT], _NewValueType],
        /,
    ) -> Kind1[_InstanceKind, _NewValueType]:
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
            progressbar = progressbarwriter.write(value, value)

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

            It is worth clarifying that this implementation has not yet been finalized
            and may be changed in future versions (and even without HKT at all).
            You can leave your opinion about this in the issues of the project.
        """
        ...

    @abc.abstractmethod
    def for_each(self, consumer: typing.Callable[[SectorT], typing.Any], /) -> None:
        """Pass each sector to a given consumer.

        Parameters
        ----------
        consumer : typing.Callable[[SectorT], typing.Any], /
            Function to apply for progressbar sectors.
        """
        ...

    @abc.abstractmethod
    def add_sector(self: _InstanceKind, sector: sectors.AbstractSector, /) -> _InstanceKind:
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
    def sectors(self) -> collections.abc.MutableSequence[SectorT]:
        """
        Returns
        -------
        collections.abc.Sequence[SectorT]
            Sequence of sectors.
        """
        ...
