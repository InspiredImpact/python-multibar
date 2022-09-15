__all__ = ("AbstractCalculationService",)

import abc
import collections.abc
import typing


class AbstractCalculationService(abc.ABC):
    """An abstraction that represents a service for mathematical operations
     on the progress bar.

    Currently, implemented in:
        - multibar.impl.calculation_service.ProgressbarCalculationService
    """

    __slots__ = ("_start_value", "_end_value", "_length")

    def __init__(
        self,
        start_value: typing.Union[int, float],
        end_value: typing.Union[int, float],
        length: int,
    ) -> None:
        """Slotted abstraction, that bounded to the arguments.

        Parameters
        ----------
        start_value : typing.Union[int, float]
            Start value (current progress) for progressbar math operations.

        end_value : typing.Union[int, float]
            End value (needed progress) for progressbar math operations.

        length : int
            Length of progressbar for progressbar math operations.
        """
        self._start_value = start_value
        self._end_value = end_value
        self._length = length

    @abc.abstractmethod
    def calculate_filled_indexes(self) -> collections.abc.Iterator[int]:
        """Returns iterator over progressbar filled sector indexes.
        This method is implemented for a more comfortable calculation
        of the position of the sector in the progress bar.

        Returns
        -------
        collections.abc.Iterator[int]
            Iterator over progressbar filled sector indexes.
        """
        ...

    @abc.abstractmethod
    def calculate_unfilled_indexes(self) -> collections.abc.Iterator[int]:
        """Returns iterator over progressbar unfilled sector indexes.
        This method is implemented for a more comfortable calculation
        of the position of the sector in the progress bar.

        Returns
        -------
        collections.abc.Iterator[int]
            Iterator over progressbar unfilled sector indexes.
        """
        ...

    @property
    @abc.abstractmethod
    def progress_percents(self) -> float:
        """Returns current progress percentage.

        Returns
        -------
        float
            Float progress percentage.
        """
        ...

    @staticmethod
    @abc.abstractmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        """Alternative staticmethod to get progress percentage.

        Parameters
        -----------
        start : typing.Union[int, float]
            Start value (current progress) for progressbar math operations.

        end : typing.Union[int, float]
            End value (needed progress) for progressbar math operations.
        """
        ...

    @property
    def start_value(self) -> typing.Union[int, float]:
        """
        Returns
        -------
        typing.Union[int, float]
            Start value (current progress) for progressbar math operations.
        """
        return self._start_value

    @property
    def end_value(self) -> typing.Union[int, float]:
        """
        Returns
        -------
        typing.Union[int, float]
            End value (needed progress) for progressbar math operations.
        """
        return self._end_value

    @property
    def length_value(self) -> int:
        """
        Returns
        -------
        int
            Length of progressbar for progressbar math operations.
        """
        return self._length
