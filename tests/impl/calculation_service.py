import typing

__all__ = ("FakeCalculationService",)

from multibar import iterators
from multibar.api import calculation_service


class FakeCalculationService(calculation_service.AbstractCalculationService):
    def calculate_filled_indexes(self) -> iterators.AbstractIterator[int]:
        return iterators.Iterator(iter(()))

    def calculate_unfilled_indexes(self) -> iterators.AbstractIterator[int]:
        return iterators.Iterator(iter(()))

    @property
    def progressbar_length(self) -> int:
        return -1

    @property
    def progress_percents(self) -> float:
        return float("NaN")

    @staticmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        return float("NaN")
