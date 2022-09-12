from __future__ import annotations

import abc
import typing

from . import signatures
from . import progressbars
from . import sectors
from . import utils
from . import calculation_service as math_operations

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


class ProgressbarWriter(ProgressbarWriterAware[sectors.AbstractSector]):
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        *,
        sector_cls: typing.Optional[sectors.AbstractSector],
        progressbar_cls: typing.Optional[progressbars.ProgressbarAware],
        signature_cls: typing.Optional[signatures.ProgressbarSignatureProtocol],
        calculation_service: typing.Optional[math_operations.CalculationServiceAware],
    ) -> None:
        ...

    def __init__(
        self,
        *,
        signature: typing.Optional[signatures.ProgressbarSignatureProtocol] = None,
        sector_cls: typing.Optional[typing.Type[sectors.AbstractSector]] = None,
        progressbar_cls: typing.Optional[typing.Type[progressbars.ProgressbarAware]] = None,
        calculation_service: typing.Optional[typing.Type[math_operations.CalculationServiceAware]] = None,
    ) -> None:
        self._signature = utils.none_or(signatures.Signature(), signature)
        self._sector_cls = utils.none_or(sectors.Sector, sector_cls)
        self._progressbar_cls = utils.none_or(progressbars.Progressbar, progressbar_cls)
        self._calculation_service = utils.none_or(math_operations.ProgressbarCalculationService, calculation_service)

    @classmethod
    def from_signature(
        cls, signature: signatures.ProgressbarSignatureProtocol, /
    ) -> ProgressbarWriter[sectors.Sector]:
        ...

    @typing.final
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> typing.Optional[progressbars.Progressbar[sectors.AbstractSector]]:
        sig = self._signature
        sector_cls = self._sector_cls
        progressbar = self._progressbar_cls()
        calculation_service = self._calculation_service(start_value, end_value, length)

        for sector_index in calculation_service.calculate_filled_indexes():
            progressbar.add_sector(
                sector_cls(name=sig.middle.on_filled, is_filled=True, position=sector_index)
            )

        for sector_index in calculation_service.calculate_unfilled_indexes():
            progressbar.add_sector(
                sector_cls(name=sig.middle.on_unfilled, is_filled=False, position=sector_index)
            )

        return progressbar

    def bind_signature(
        self, signature: signatures.ProgressbarSignatureProtocol, /
    ) -> ProgressbarWriter[sectors.Sector]:
        self._signature = signature
        return self

    @property
    def signature(self) -> signatures.ProgressbarSignatureProtocol:
        return self._signature

    @property
    def sector_cls(self) -> typing.Type[sectors.AbstractSector]:
        return self._sector_cls

    @property
    def progressbar_cls(self) -> typing.Type[progressbars.ProgressbarAware]:
        return self._progressbar_cls

    @property
    def calculation_cls(self) -> typing.Type[math_operations.CalculationServiceAware]:
        return self._calculation_service
