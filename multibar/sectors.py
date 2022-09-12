from __future__ import annotations
import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class AbstractSector(abc.ABC):
    @abc.abstractmethod
    def add_to_progressbar(
        self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /
    ) -> SelfT:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> typing.AnyStr:
        ...

    @abc.abstractmethod
    def change_name(self, value: str, /) -> AbstractSector:
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        ...


class Sector(AbstractSector):
    def __init__(self, name: typing.AnyStr, is_filled: bool, position: int) -> None:
        self._name = name
        self._is_filled = is_filled
        self._position = position

    def add_to_progressbar(
        self: Sector, progressbar: progressbars.ProgressbarAware[Sector], /
    ) -> Sector:
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
