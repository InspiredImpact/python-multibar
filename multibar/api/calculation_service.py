__all__ = ("CalculationServiceAware",)

import abc
import typing

from .. import iterators


class CalculationServiceAware(abc.ABC):
    __slots__ = ()

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

    @property
    @abc.abstractmethod
    def start_value(self) -> typing.Union[int, float]:
        ...

    @property
    @abc.abstractmethod
    def end_value(self) -> typing.Union[int, float]:
        ...

    @staticmethod
    @abc.abstractmethod
    def get_progress_percentage(start: int, end: int, /) -> float:
        ...
