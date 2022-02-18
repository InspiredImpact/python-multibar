from __future__ import annotations

__all__ = ["ProgressContainer", "ProgressbarContainer", "SectorContainer"]

from collections.abc import Sized
from dataclasses import dataclass, field
from typing import Any, Generic, Iterable, List, Literal, TypeVar, Union, cast, overload

from multibar.interfaces.containers import AbstractSeqBasedContainerMixin
from multibar.interfaces.product import AbstractSectorMixin


@dataclass(frozen=True)
class ProgressContainer:
    current: int
    total: int

    @overload
    def percents(self, *, allow_float: Literal[False]) -> int:
        ...

    @overload
    def percents(self, *, allow_float: Literal[True]) -> float:
        ...

    def percents(self, *, allow_float: bool = False) -> Union[int, float]:
        initial = (self.current / self.total) * 100
        if allow_float:
            return initial

        return int(initial)


_AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)


@dataclass(frozen=True, order=True)
class ProgressbarContainer(Sized, Generic[_AbcSectorT_co]):
    length: int
    progress: ProgressContainer
    bar: AbstractSeqBasedContainerMixin[_AbcSectorT_co] = field(repr=False)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ProgressbarContainer):
            return (
                self.progress.current == other.progress.current
                and self.progress.total == other.progress.total
            )

        return NotImplemented

    def __len__(self) -> int:
        return len(self.bar)

    @overload
    def __getitem__(
        self,
        item: int,
    ) -> _AbcSectorT_co:
        ...

    @overload
    def __getitem__(
        self,
        item: slice,
    ) -> Iterable[_AbcSectorT_co]:
        ...

    def __getitem__(
        self,
        item: Union[int, slice],
    ) -> Union[_AbcSectorT_co, Iterable[_AbcSectorT_co]]:
        return self.bar[item]


@dataclass
class SectorContainer(AbstractSeqBasedContainerMixin[_AbcSectorT_co]):
    def __post_init__(self) -> None:
        self._storage: List[_AbcSectorT_co] = []

    def __repr__(self) -> str:
        return "".join(s.name for s in self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    @overload
    def __getitem__(
        self,
        item: int,
    ) -> _AbcSectorT_co:
        ...

    @overload
    def __getitem__(
        self,
        item: slice,
    ) -> Iterable[_AbcSectorT_co]:
        ...

    def __getitem__(
        self,
        item: Union[int, slice],
    ) -> Union[Iterable[_AbcSectorT_co], _AbcSectorT_co]:
        return self._storage[item]

    def put(self, item: AbstractSectorMixin) -> None:
        self._storage.append(cast(_AbcSectorT_co, item))

    @property
    def view(self) -> List[_AbcSectorT_co]:
        return self._storage
