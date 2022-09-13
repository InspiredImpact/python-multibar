__all__ = ("ProgressbarCalculationService",)

import collections.abc
import typing

from multibar.api import calculation_service


class ProgressbarCalculationService(calculation_service.AbstractCalculationService):
    def calculate_filled_indexes(self) -> collections.abc.Iterator[int]:
        filled_range = range(round(self.progress_percents / (100 / self._length)))
        return iter(filled_range)

    def calculate_unfilled_indexes(self) -> collections.abc.Iterator[int]:
        filled_range_len = len(tuple(self.calculate_filled_indexes()))
        unfilled_range = range(self._length - filled_range_len)
        return map(lambda i: i + filled_range_len, unfilled_range)

    @property
    def progress_percents(self) -> float:
        return self.get_progress_percentage(self._start_value, self._end_value)

    @staticmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        return (start / end) * 100
