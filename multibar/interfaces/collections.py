__all__ = ["Comparable", "Representable"]

import abc
from typing import Any


class Representable(abc.ABC):
    @abc.abstractmethod
    def __repr__(self) -> str:
        ...


class Comparable(abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...

    @abc.abstractmethod
    def __hash__(self) -> int:
        ...
