from __future__ import annotations

__all__ = ("SectorAware",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class SectorAware(abc.ABC):
    @abc.abstractmethod
    def add_to_progressbar(self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /) -> SelfT:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> typing.AnyStr:
        ...

    @abc.abstractmethod
    def change_name(self, value: str, /) -> SectorAware:
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        ...
