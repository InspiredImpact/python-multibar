from __future__ import annotations

__all__ = ("AbstractCalculationService",)

import abc
import typing

if typing.TYPE_CHECKING:
    from multibar import iterators


class AbstractCalculationService(abc.ABC):
    __slots__ = ("_start_value", "_end_value", "_length")

    def __init__(
        self,
        start_value: typing.Union[int, float],
        end_value: typing.Union[int, float],
        length: int,
    ) -> None:
        self._start_value = start_value
        self._end_value = end_value
        self._length = length

    @abc.abstractmethod
    def calculate_filled_indexes(self) -> iterators.AbstractIterator[int]:
        ...

    @abc.abstractmethod
    def calculate_unfilled_indexes(self) -> iterators.AbstractIterator[int]:
        ...

    @property
    @abc.abstractmethod
    def progressbar_length(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def progress_percents(self) -> float:
        ...

    @staticmethod
    @abc.abstractmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        ...

    @property
    def start_value(self) -> typing.Union[int, float]:
        return self._start_value

    @property
    def end_value(self) -> typing.Union[int, float]:
        return self._end_value

    @property
    def length_value(self) -> int:
        return self._length
