from __future__ import annotations

__all__ = ("ProgressbarWriterAware",)

import abc
import typing

from . import calculation_service as math_operations
from . import progressbars, sectors, signatures


class ProgressbarWriterAware(abc.ABC):
    """Interface for progressbar writer implementations."""

    __slots__ = ()

    @classmethod
    @abc.abstractmethod
    def from_signature(cls, signature: signatures.ProgressbarSignatureProtocol, /) -> ProgressbarWriterAware:
        """Alternative constructor from signature.

        Parameters
        ----------
        signature : signatures.ProgressbarSignatureProtocol, /
            Signature to init.

        Returns
        -------
        ProgressbarWriterAware[sectors.AbstractSector]
            Instance of progressbar writer.
        """
        ...

    @typing.overload
    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
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
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    def write(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        """Writes progress without any hooks or checks.

        Parameters
        ----------
        start_value : int, /
            Start value (current progress).

        end_value : int, /
            End value (needed progress).

        length : int, *
            Length of progressbar.
        """
        ...

    @abc.abstractmethod
    def bind_signature(self, signature: signatures.ProgressbarSignatureProtocol, /) -> ProgressbarWriterAware:
        """Sets new progressbar signature.

        Parameters
        ----------
        signature : signatures.ProgressbarSignatureProtocol, /
            New signature to set.

        Returns
        -------
        Self
            Progressbar writer object to allow fluent-style.
        """
        ...

    @property
    @abc.abstractmethod
    def signature(self) -> signatures.ProgressbarSignatureProtocol:
        """
        Returns
        -------
        signatures.ProgressbarSignatureProtocol
            Progressbar signature.
        """
        ...

    @property
    @abc.abstractmethod
    def sector_cls(self) -> typing.Type[sectors.AbstractSector]:
        """
        Returns
        -------
        typing.Type[sectors.AbstractSector]
            Progressbar sector cls.
        """
        ...

    @property
    @abc.abstractmethod
    def progressbar_cls(self) -> typing.Type[progressbars.ProgressbarAware[sectors.AbstractSector]]:
        """
        Returns
        -------
        typing.Type[progressbars.ProgressbarAware[sectors.AbstractSector]]
            Progressbar cls.
        """
        ...

    @property
    @abc.abstractmethod
    def calculation_cls(self) -> typing.Type[math_operations.AbstractCalculationService]:
        """
        Returns
        -------
        typing.Type[math_operations.AbstractCalculationService]
            Calculation cls.
        """
        ...
