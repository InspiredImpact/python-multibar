from __future__ import annotations

__all__ = ("ProgressbarWriter",)

import typing

from multibar import utils
from multibar.api import sectors as abc_sectors
from multibar.api import writers as abc_writers

from . import calculation_service as math_operations
from . import progressbars, sectors, signatures

if typing.TYPE_CHECKING:
    from multibar.api import calculation_service as abc_math_operations
    from multibar.api import progressbars as abc_progressbars
    from multibar.api import signatures as abc_signatures


class ProgressbarWriter(abc_writers.ProgressbarWriterAware):
    __slots__ = ("_signature", "_sector_cls", "_progressbar_cls", "_calculation_service")

    def __init__(
        self,
        *,
        sector_cls: typing.Optional[typing.Type[abc_sectors.AbstractSector]] = None,
        progressbar_cls: typing.Optional[
            typing.Type[abc_progressbars.ProgressbarAware[abc_sectors.AbstractSector]]
        ] = None,
        signature: typing.Optional[abc_signatures.ProgressbarSignatureProtocol] = None,
        calculation_service: typing.Optional[
            typing.Type[abc_math_operations.AbstractCalculationService]
        ] = None,
    ) -> None:
        """
            Parameters
            ----------
            sector_cls: typing.Optional[typing.Type[abc_sectors.AbstractSector]] = None, *
                Progressbar sector cls for writer.

            progressbar_cls: typing.Optional[typing.Type[ProgressbarT_co]] = None, *
                Progressbar cls for writer.

            signature: typing.Optional[abc_signatures.ProgressbarSignatureProtocol] = None, *
                Progressbar signature for writer.

            calculation_service: typing.Optional[
                typing.Type[abc_math_operations.AbstractCalculationService]
            ] = None, *
                Math operations for writer.
        ) -> None:
        """
        self._signature = utils.none_or(signatures.SimpleSignature(), signature)
        self._sector_cls = utils.none_or(sectors.Sector, sector_cls)
        self._progressbar_cls = utils.none_or(
            progressbars.Progressbar[abc_sectors.AbstractSector], progressbar_cls
        )
        self._calculation_service = utils.none_or(
            math_operations.ProgressbarCalculationService, calculation_service
        )

    @classmethod
    def from_signature(
        cls,
        signature: abc_signatures.ProgressbarSignatureProtocol,
        /,
    ) -> ProgressbarWriter:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        return cls(
            sector_cls=None,
            progressbar_cls=None,
            signature=signature,
            calculation_service=None,
        )

    @typing.final
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> abc_progressbars.ProgressbarAware[abc_sectors.AbstractSector]:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        sig = self._signature
        sector_cls = self._sector_cls
        progressbar = self._progressbar_cls()
        calculation_service = self._calculation_service(start_value, end_value, length)

        for sector_index in calculation_service.calculate_filled_indexes():
            progressbar.add_sector(sector_cls(sig.middle.on_filled, True, sector_index))

        for sector_index in calculation_service.calculate_unfilled_indexes():
            progressbar.add_sector(sector_cls(sig.middle.on_unfilled, False, sector_index))

        return progressbar

    def bind_signature(
        self,
        signature: abc_signatures.ProgressbarSignatureProtocol,
        /,
    ) -> ProgressbarWriter:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        self._signature = signature
        return self

    @property
    def signature(self) -> abc_signatures.ProgressbarSignatureProtocol:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        return self._signature

    @property
    def sector_cls(self) -> typing.Type[abc_sectors.AbstractSector]:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        return self._sector_cls

    @property
    def progressbar_cls(self) -> typing.Type[abc_progressbars.ProgressbarAware[abc_sectors.AbstractSector]]:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        return self._progressbar_cls

    @property
    def calculation_cls(self) -> typing.Type[abc_math_operations.AbstractCalculationService]:
        # << inherited docstring for multibar.api.writers.ProgressbarWriterAware >>
        return self._calculation_service
