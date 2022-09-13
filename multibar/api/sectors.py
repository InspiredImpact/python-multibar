from __future__ import annotations

__all__ = ("AbstractSector",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class AbstractSector(abc.ABC):
    __slots__ = ("_name", "_is_filled", "_position")

    def __init__(self, name: str, is_filled: bool, position: int) -> None:
        self._name = name
        self._is_filled = is_filled
        self._position = position

    @abc.abstractmethod
    def add_to_progressbar(self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /) -> SelfT:
        ...

    @abc.abstractmethod
    def change_name(self, value: str, /) -> AbstractSector:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        ...
