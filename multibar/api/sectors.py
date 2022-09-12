from __future__ import annotations

__all__ = ("AbstractSector",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class AbstractSector(abc.ABC):
    __slots__ = ("_name", "_is_filled", "_position")

    def __init__(self, name: typing.Union[str, bytes], is_filled: bool, position: int) -> None:
        self._name = name
        self._is_filled = is_filled
        self._position = position

    @abc.abstractmethod
    def add_to_progressbar(self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /) -> SelfT:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> typing.Union[str, bytes]:
        ...

    @abc.abstractmethod
    def change_name(self, value: typing.Union[str, bytes], /) -> AbstractSector:
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        ...
