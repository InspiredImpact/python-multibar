from __future__ import annotations

__all__ = ["SphinxSectorFactory"]

from dataclasses import dataclass
from typing import Any, Generic, Type, TypeVar

from multibar.interfaces.product import AbstractSectorMixin

_AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)


@dataclass
class SphinxSectorFactory(Generic[_AbcSectorT_co]):
    bind: Type[_AbcSectorT_co]

    @classmethod
    def from_bind(
        cls: Type[SphinxSectorFactory[_AbcSectorT_co]],
        *,
        sector_type: Type[_AbcSectorT_co],
    ) -> SphinxSectorFactory[_AbcSectorT_co]:
        return cls(
            bind=sector_type,
        )

    def rebind(
        self,
        *,
        sector_type: Type[_AbcSectorT_co],
    ) -> None:
        if not issubclass(sector_type, AbstractSectorMixin):
            raise TypeError("Sector must be subclass of :class:`AbstractSectorMixin`")

        self.bind = sector_type

    def create_product(
        self,
        name: str,
        position: int,
        *args: Any,
        empty: bool = False,
        **kwargs: Any,
    ) -> _AbcSectorT_co:
        return self.bind(
            *args, name=name, position=position, empty=empty, **kwargs,
        )
