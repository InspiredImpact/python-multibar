from __future__ import annotations

__all__ = ("ProgressbarWriterAware",)

import abc
import typing

from . import signatures
from . import progressbars
from . import sectors
from . import calculation_service as math_operations

SectorT = typing.TypeVar("SectorT", bound=sectors.SectorAware)


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
    ) -> typing.Optional[progressbars.ProgressbarAware[SectorT]]:
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
    ) -> typing.Optional[progressbars.ProgressbarAware[SectorT]]:
        ...

    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> typing.Optional[progressbars.ProgressbarAware[SectorT]]:
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
    def progressbar_cls(self) -> typing.Type[progressbars.ProgressbarAware]:
        ...

    @property
    @abc.abstractmethod
    def calculation_cls(self) -> typing.Type[math_operations.CalculationServiceAware]:
        ...
