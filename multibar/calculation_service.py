import abc
import typing

from . import iterators


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


class ProgressbarCalculationService(CalculationServiceAware):
    def __init__(
        self,
        start_value: typing.Union[int, float],
        end_value: typing.Union[int, float],
        length: int,
    ) -> None:
        self._start_value = start_value
        self._end_value = end_value
        self._length = length

    def calculate_filled_indexes(self) -> iterators.AbstractIterator[int]:
        filled_range = range(round(self.progress_percents / (100 / self._length)))
        return iterators.Iterator(iter(filled_range)).indexes()

    def calculate_unfilled_indexes(self) -> iterators.AbstractIterator[int]:
        filled_range_len = len(tuple(self.calculate_filled_indexes()))
        unfilled_range = range(self._length - filled_range_len)
        return iterators.Iterator(iter(unfilled_range)).indexes(conversion=lambda i: i + filled_range_len)

    @property
    def progressbar_length(self) -> int:
        return self._length

    @property
    def progress_percents(self) -> float:
        return self.get_progress_percentage(self._start_value, self._end_value)

    @property
    def start_value(self) -> typing.Union[int, float]:
        return self._start_value

    @property
    def end_value(self) -> typing.Union[int, float]:
        return self._end_value

    @staticmethod
    def get_progress_percentage(start: int, end: int, /) -> float:
        return (start / end) * 100
