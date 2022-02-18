__all__ = ["AbstractSectorMixin"]

import abc

from multibar.interfaces.collections import Comparable, Representable


class AbstractSectorMixin(Comparable, Representable, abc.ABC):
    __slots__ = ("name", "position", "empty")

    def __init__(self, name: str, position: int, empty: bool) -> None:
        self.name = name
        self.position = position
        self.empty = empty
