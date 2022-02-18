from __future__ import annotations

__all__ = ["AbstractSeqBasedContainerMixin"]

import abc
from collections.abc import Sized
from typing import (
    TYPE_CHECKING,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

from multibar.interfaces.collections import Representable

if TYPE_CHECKING:
    from types import TracebackType

T_co = TypeVar("T_co", covariant=True)


class AbstractSeqBasedContainerMixin(Representable, Sized, abc.ABC, Generic[T_co]):
    @abc.abstractmethod
    def __getitem__(
        self,
        item: Union[int, slice],
    ) -> Union[Iterable[T_co], T_co]:
        ...

    def __enter__(self) -> AbstractSeqBasedContainerMixin[T_co]:
        return self

    @overload
    def __exit__(self, exc_type: None, exc_val: None, exc_tb: None) -> None:
        ...

    @overload
    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.finalize()

    def finalize(self) -> None:
        ...

    @abc.abstractmethod
    def put(self, item: T_co) -> None:
        ...

    @property
    @abc.abstractmethod
    def view(self) -> Iterable[T_co]:
        ...
