__all__ = ["NoneType", "NotImplementedType"]

from typing import Any, Final, Type

SENTIEL = object()
NoneType: Final[Type[Any]] = type(None)
NotImplementedType: Final[Type[Any]] = type(NotImplemented)
