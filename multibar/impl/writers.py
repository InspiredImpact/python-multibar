from __future__ import annotations

__all__ = ("ProgressbarWriter",)

import typing

from . import signatures
from . import progressbars
from . import sectors
from . import calculation_service as math_operations
from multibar import utils
from multibar.api import writers as abc_writers
from multibar.api import sectors as abc_sectors

if typing.TYPE_CHECKING:
    from multibar.api import signatures as abc_signatures
    from multibar.api import progressbars as abc_progressbars
    from multibar.api import calculation_service as abc_math_operations


class ProgressbarWriter(abc_writers.ProgressbarWriterAware[abc_sectors.SectorAware]):
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        *,
        sector_cls: typing.Optional[abc_sectors.SectorAware],
        progressbar_cls: typing.Optional[abc_progressbars.ProgressbarAware],
        signature: typing.Optional[abc_signatures.ProgressbarSignatureProtocol],
        calculation_service: typing.Optional[abc_math_operations.CalculationServiceAware],
    ) -> None:
        ...

    def __init__(
        self,
        *,
        sector_cls: typing.Optional[abc_sectors.SectorAware] = None,
        progressbar_cls: typing.Optional[abc_progressbars.ProgressbarAware] = None,
        signature: typing.Optional[abc_signatures.ProgressbarSignatureProtocol] = None,
        calculation_service: typing.Optional[abc_math_operations.CalculationServiceAware] = None,
    ) -> None:
        self._signature = utils.none_or(signatures.Signature(), signature)
        self._sector_cls = utils.none_or(sectors.Sector, sector_cls)
        self._progressbar_cls = utils.none_or(progressbars.Progressbar, progressbar_cls)
        self._calculation_service = utils.none_or(
            math_operations.ProgressbarCalculationService, calculation_service
        )

    @classmethod
    def from_signature(
        cls, signature: abc_signatures.ProgressbarSignatureProtocol, /
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
    ) -> typing.Optional[progressbars.Progressbar[abc_sectors.SectorAware]]:
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
        self, signature: abc_signatures.ProgressbarSignatureProtocol, /
    ) -> ProgressbarWriter[sectors.Sector]:
        self._signature = signature
        return self

    @property
    def signature(self) -> abc_signatures.ProgressbarSignatureProtocol:
        return self._signature

    @property
    def sector_cls(self) -> typing.Type[abc_sectors.SectorAware]:
        return self._sector_cls

    @property
    def progressbar_cls(self) -> typing.Type[abc_progressbars.ProgressbarAware]:
        return self._progressbar_cls

    @property
    def calculation_cls(self) -> typing.Type[abc_math_operations.CalculationServiceAware]:
        return self._calculation_service
