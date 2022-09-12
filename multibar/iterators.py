from __future__ import annotations

import abc
import typing

T_co = typing.TypeVar("T_co", covariant=True)


class AbstractIterator(typing.Generic[T_co], abc.ABC):
    __slots__ = ()

    def __iter__(self) -> typing.Iterator[T_co]:
        return self

    @abc.abstractmethod
    def __next__(self) -> T_co:
        ...

    @typing.overload
    def indexes(self) -> AbstractIterator[int]:
        ...

    @typing.overload
    def indexes(
        self,
        *,
        start: int,
        conversion: typing.Optional[typing.Callable[[T_co], typing.Any]],
    ) -> AbstractIterator[int]:
        ...

    @typing.final
    def indexes(
        self,
        *,
        start: int = 0,
        conversion: typing.Optional[typing.Callable[[T_co], typing.Any]] = None,
    ) -> AbstractIterator[int]:
        return _ConvertableIndexIterator(self, start=start, conversion=conversion)


class Iterator(AbstractIterator[T_co]):
    __slots__ = ("_iterator",)

    def __init__(self, iterator: typing.Iterator[T_co], /) -> None:
        self._iterator = iterator

    def __iter__(self) -> Iterator[T_co]:
        return self

    def __next__(self) -> T_co:
        return next(self._iterator)


class _ConvertableIndexIterator(typing.Generic[T_co], AbstractIterator[int]):
    __slots__ = ("_iterator", "_iteration_n", "_conversion")

    def __init__(
        self,
        iterator: AbstractIterator[T_co],
        *,
        start: int,
        conversion: typing.Optional[typing.Callable[[T_co], typing.Any]],
    ) -> None:
        self._iterator = iterator
        self._iteration_n = start
        self._conversion = conversion

    def __next__(self) -> int:
        index, _ = self._iteration_n, self._iterator.__next__()
        self._iteration_n += 1
        if self._conversion is not None:
            index = self._conversion(index)
        return index
