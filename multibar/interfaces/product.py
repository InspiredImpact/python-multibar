__all__ = ["AbstractSectorMixin"]

import abc

from multibar.interfaces.collections import Comparable, Representable


class AbstractSectorMixin(Comparable, Representable, abc.ABC):
    """``abc mixin``
    Class that is abstract mixin for subclassing
    (creating custom Sector implementations).

    Parameters:
    -----------
    name: :class:`str`
        Sector name parameter.

    position: :class:`int`
        Sector position in progressbar.

    empty: :class:`bool`
        For empty sectors used :line: emoji (and unfilled_start, unfilled_end if passed).
    """

    __slots__ = ("name", "position", "empty")

    def __init__(self, *, name: str, position: int, empty: bool) -> None:
        self.name = name
        self.position = position
        self.empty = empty
