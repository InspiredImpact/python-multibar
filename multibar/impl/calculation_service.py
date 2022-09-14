__all__ = ("ProgressbarCalculationService",)

import collections.abc
import typing

from multibar.api import calculation_service


class ProgressbarCalculationService(calculation_service.AbstractCalculationService):
    def calculate_filled_indexes(self) -> collections.abc.Iterator[int]:
        # << inherited docstring for multibar.api.calculation_service.AbstractCalculationService >>
        filled_range = range(round(self.progress_percents / (100 / self._length)))
        return iter(filled_range)

    def calculate_unfilled_indexes(self) -> collections.abc.Iterator[int]:
        # << inherited docstring for multibar.api.calculation_service.AbstractCalculationService >>
        filled_range_len = len(tuple(self.calculate_filled_indexes()))
        unfilled_range = range(self._length - filled_range_len)
        return map(lambda i: i + filled_range_len, unfilled_range)

    @property
    def progress_percents(self) -> float:
        # << inherited docstring for multibar.api.calculation_service.AbstractCalculationService >>
        return self.get_progress_percentage(self._start_value, self._end_value)

    @staticmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        # << inherited docstring for multibar.api.calculation_service.AbstractCalculationService >>
        return (start / end) * 100
