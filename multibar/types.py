from __future__ import annotations

__all__ = ("ProgressMetadataType",)

import typing

if typing.TYPE_CHECKING:
    from multibar.api import calculation_service, progressbars, sectors, signatures


class ProgressMetadataType(typing.TypedDict, total=False):
    start_value: int
    """Start value (current progress)."""

    end_value: int
    """End value (needed progress)."""

    length: int
    """Length of progressbar."""

    sig: signatures.ProgressbarSignatureProtocol
    """Progressbar signature."""

    progressbar: typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]
    """Progressbar instance."""

    calculation_service_cls: typing.Type[calculation_service.AbstractCalculationService]
    """Math operations cls."""
