__all__ = ("ProgressbarCalculationService",)

import typing

from multibar import iterators
from multibar.api import calculation_service


class ProgressbarCalculationService(calculation_service.AbstractCalculationService):
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
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        return (start / end) * 100
