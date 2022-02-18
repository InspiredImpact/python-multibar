__all__ = ["NoneType", "NotImplementedType"]

from typing import Final, Type, Any

NoneType: Final[Type[Any]] = type(None)
NotImplementedType: Final[Type[Any]] = type(NotImplemented)
