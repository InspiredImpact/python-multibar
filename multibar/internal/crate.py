from __future__ import annotations

__all__ = ["ProgressContainer", "ProgressbarContainer", "SectorContainer"]

from collections.abc import Sized
from dataclasses import dataclass, field
from typing import Any, Generic, Iterable, List, Literal, TypeVar, Union, cast, overload

from multibar.interfaces.collections import Comparable
from multibar.interfaces.containers import AbstractSeqBasedContainerMixin
from multibar.interfaces.product import AbstractSectorMixin


@dataclass(frozen=True)
class ProgressContainer:
    """``dataclass``
    Class that represents current progress state.

    Parameters:
    -----------
    current: :class:`int`
        Current progress value.

    total: :class:`int`
        Needed progress value.
    """

    current: int
    total: int

    @overload
    def percents(self, *, allow_float: Literal[False]) -> int:
        """If :allow_float: False, will return :class:`int`"""

    @overload
    def percents(self, *, allow_float: Literal[True]) -> float:
        """If :allow_float: True, will return :class:`float`"""

    def percents(self, *, allow_float: bool = False) -> Union[int, float]:
        """``sync method``
        Returns percentage of current progress.

        Parameters:
        -----------
        allow_float: :class:`bool`
            If True, will return :class:`float`, otherwise - :class:`int`.
        """
        initial = (self.current / self.total) * 100
        if allow_float:
            return initial

        return int(initial)


_AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)


@dataclass(frozen=True, order=True)
class ProgressbarContainer(Comparable, Sized, Generic[_AbcSectorT_co]):
    """``dataclass``
    Class that represents progressbar state.

    Parameters:
    -----------
    length: :class:`int`
        Length of progress bar.

    state: :class:`ProgressContainer`
        Progress state.

    bar: :class:`AbstractSeqBasedContainerMixin[_AbcSectorT_co]`
        Progress bar container.
    """

    length: int
    state: ProgressContainer
    bar: AbstractSeqBasedContainerMixin[_AbcSectorT_co] = field(repr=False)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ProgressbarContainer):
            return self.state.current == other.state.current and self.state.total == other.state.total

        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.state.current, self.state.total))

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
    """``dataclass``
    Simple implementation of sequence-based Sector container.
    """

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
