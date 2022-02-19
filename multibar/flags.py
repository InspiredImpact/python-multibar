__all__ = ["FillFlag"]

import enum
from typing import final


@final
class FillFlag(enum.IntFlag):
    """``int flag``
    The flag that is used to generate the progress bar.

    ClassVars:
    ----------
    (According to the formula)

    FIRST: :class:`int` = 3
        At `three percent`, the first sector of the progress bar is filled.

    LAST: :class:`int` = 97
        At `ninety-seven percent`, the last sector of the progress bar is filled.
    """

    FIRST = 3
    LAST = 97
