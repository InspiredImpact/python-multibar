from __future__ import annotations

__all__ = ("AbstractSector",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class AbstractSector(abc.ABC):
    """Abstraction for sector implementations."""

    __slots__ = ("_name", "_is_filled", "_position")

    def __init__(self, name: str, is_filled: bool, position: int) -> None:
        """Slotted abstraction, that bounded to the arguments.

        Parameters
        ----------
        name : str
            Sector display name.

        is_filled : bool
            Sector filled value.

        position : int
            Sector position in the progressbar.
        """
        self._name = name
        self._is_filled = is_filled
        self._position = position

    @abc.abstractmethod
    def add_to_progressbar(self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /) -> SelfT:
        """Adds sector self to progressbar.

        Parameters
        ----------
        progressbar : progressbars.ProgressbarAware[SelfT], /
            Progressbar to add self for.

        Returns
        -------
        Self
            The sector object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def change_name(self, new_display_name: str, /) -> AbstractSector:
        """Changes sector display name.

        Parameters
        ----------
        new_display_name : str, /
            New display name to set.

        Returns
        -------
        Self
            The sector object to allow fluent-style.
        """
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Returns
        -------
        str
            Sector display name.
        """
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        """
        Returns
        -------
        str
            Sector filled value.
        """
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        """
        Returns
        -------
        str
            Sector position in the progressbar.
        """
        ...
