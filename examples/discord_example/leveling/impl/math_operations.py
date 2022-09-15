__all__ = ("MathOperations",)

import typing

from examples.discord_example.leveling.api import math_operations


class MathOperations(math_operations.MathOperationsAware):
    """Implementation of math_operations.MathOperationsAware ."""

    __slots__ = ("_base_experience", "_factor")

    def __init__(self, *, base_experience: int = 50, factor: typing.Union[int, float] = 1.1) -> None:
        """
        Parameters
        ----------
        base_experience : int = 50, *
            Base experience multiplier for math operations.

        factor : typing.Union[int, float] = 1.1, *
            Factor for math operations.
        """

        self._base_experience = base_experience
        self._factor = factor

    def get_needed_experience_for(self, current_lvl: int, /) -> int:
        # << inherited docstring from math_operations.MathOperationsAware >>
        return int((self._base_experience * current_lvl) ** self.factor)

    def is_reached_next_level(self, *, current_lvl: int, current_xp: int) -> bool:
        # << inherited docstring from math_operations.MathOperationsAware >>
        return current_xp >= self.get_needed_experience_for(current_lvl)

    @property
    def factor(self) -> float:
        # << inherited docstring from math_operations.MathOperationsAware >>
        return self._factor
