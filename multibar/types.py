from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from multibar.api import calculation_service, progressbars, sectors, signatures


class ProgressMetadataType(typing.TypedDict, total=False):
    start_value: int
    end_value: int
    length: int
    sig: signatures.ProgressbarSignatureProtocol
    progressbar: typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]
    calculation_service_cls: typing.Type[calculation_service.AbstractCalculationService]