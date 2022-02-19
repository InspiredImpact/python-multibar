__all__ = ["NoneType", "NotImplementedType"]

from typing import Any, Final, Type

NoneType: Final[Type[Any]] = type(None)
NotImplementedType: Final[Type[Any]] = type(NotImplemented)
