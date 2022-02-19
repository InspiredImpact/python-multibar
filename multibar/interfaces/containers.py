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

T = TypeVar("T")


class AbstractSeqBasedContainerMixin(Representable, Sized, abc.ABC, Generic[T]):
    """``abc mixin``
    Class that is abstract mixin for subclassing
    (creating custom Container implementations).
    """

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> Iterable[T]:
        ...

    @abc.abstractmethod
    def __getitem__(
        self,
        item: Union[int, slice],
    ) -> Union[Iterable[T], T]:
        ...

    def __enter__(self) -> AbstractSeqBasedContainerMixin[T]:
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
        """``sync method``
        Called in `__exit__` method.
        """

    @abc.abstractmethod
    def put(self, item: T) -> None:
        """``abc method``
        Puts item to storage.

        Parameters:
        -----------
        item: :class:`~T`
            Any item to storage.
        """

    @property
    @abc.abstractmethod
    def view(self) -> Iterable[T]:
        """``abc method``
        Returns iterator over :class:`~T`
        """
