from __future__ import annotations

__all__ = ["Sentinel", "MISSING", "MissingOr"]

from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    MutableMapping,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
)

if TYPE_CHECKING:

    class _SentinelProto(Protocol):
        def __new__(cls: Type[Any]) -> _SentinelProto:
            ...

        def __repr__(self) -> str:
            ...

        def __bool__(self) -> Literal[False]:
            ...

        def __copy__(self) -> Sentinel:
            ...

        def __deepcopy__(self, memodict: MutableMapping[int, Any]) -> Sentinel:
            ...


class Sentinel:
    def __init__(self, name: str, *, repr: Optional[str] = None) -> None:
        self.__name = name
        self.__repr = f"<{name}>" if repr is None else repr

    def __repr__(self) -> str:
        return self.__repr

    def __bool__(self) -> Literal[False]:
        return False

    def __copy__(self) -> Sentinel:
        return self

    def __deepcopy__(self, memodict: MutableMapping[int, Any]) -> Sentinel:
        memodict[id(self)] = self
        return self

    @classmethod
    def new(cls, name: str, *, repr: Optional[str] = None) -> _SentinelProto:
        sentinel = cls(name, repr=repr)
        setattr(sentinel, "__new__", lambda cls_: sentinel)
        return sentinel


MISSING = Sentinel.new("MISSING")

T = TypeVar("T")
MissingOr = Union[T, Sentinel]
