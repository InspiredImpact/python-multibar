__all__ = ("MathOperationsAware",)

import abc
import typing


class MathOperationsAware(abc.ABC):
    """Interface for all math operation implementations."""

    __slots__ = ()

    @abc.abstractmethod
    def get_needed_experience_for(self, current_lvl: int, /) -> int:
        """Returns total xp for specific level.

        Parameters
        ----------
        current_lvl : int, /
            Level to calculate xp for.
        """
        ...

    @abc.abstractmethod
    def is_reached_next_level(self, *, current_lvl: int, current_xp: int) -> bool:
        """Returns True, if user reaches new lvl by xp.

        Parameters
        ----------
        current_lvl : int, *
            Level for calculation.

        current_xp : int, *
            Current xp for calculation.
        """
        ...

    @property
    @abc.abstractmethod
    def factor(self) -> typing.Union[int, float]:
        """Factor for math operations."""
        ...
