from __future__ import annotations

__all__ = ("ProgressbarWriterAware",)

import abc
import typing

from . import calculation_service as math_operations
from . import progressbars, sectors, signatures

SectorT = typing.TypeVar("SectorT", bound=sectors.AbstractSector)


class ProgressbarWriterAware(abc.ABC, typing.Generic[SectorT]):
    @classmethod
    @abc.abstractmethod
    def from_signature(
        cls, signature: signatures.ProgressbarSignatureProtocol, /
    ) -> ProgressbarWriterAware[SectorT]:
        ...

    @typing.overload
    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> progressbars.ProgressbarAware[SectorT]:
        ...

    @typing.overload
    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int,
    ) -> progressbars.ProgressbarAware[SectorT]:
        ...

    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> progressbars.ProgressbarAware[SectorT]:
        ...

    @abc.abstractmethod
    def bind_signature(
        self, signature: signatures.ProgressbarSignatureProtocol, /
    ) -> ProgressbarWriterAware[SectorT]:
        ...

    @property
    @abc.abstractmethod
    def signature(self) -> signatures.ProgressbarSignatureProtocol:
        ...

    @property
    @abc.abstractmethod
    def sector_cls(self) -> typing.Type[SectorT]:
        ...

    @property
    @abc.abstractmethod
    def progressbar_cls(self) -> typing.Type[progressbars.ProgressbarAware[SectorT]]:
        ...

    @property
    @abc.abstractmethod
    def calculation_cls(self) -> typing.Type[math_operations.AbstractCalculationService]:
        ...
