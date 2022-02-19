from __future__ import annotations

__all__ = ["AbstractCustomerMixin"]

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from multibar.internal.crate import ProgressContainer


class AbstractCustomerMixin(abc.ABC):
    """Hook for flexible emoji defining.

    !!! Note:
        In further versions this hook will be deprecated.

    Parameters:
    -----------
    ctx: :class:`ProgressContainer`
        Current progress state.
    """

    def __init__(self, ctx: ProgressContainer) -> None:
        self.ctx = ctx

    @abc.abstractmethod
    def fill(self, ctx: ProgressContainer) -> Any:
        """Defines :fill: character for progress bar."""

    @abc.abstractmethod
    def line(self, ctx: ProgressContainer) -> Any:
        """Defines :line: character for progress bar."""

    @abc.abstractmethod
    def start(self, ctx: ProgressContainer) -> Any:
        """Defines :start: character for progress bar."""

    @abc.abstractmethod
    def end(self, ctx: ProgressContainer) -> Any:
        """Defines :end: character for progress bar."""

    @abc.abstractmethod
    def unfilled_start(self, ctx: ProgressContainer) -> Any:
        """Defines :unfilled_start: character for progress bar."""

    @abc.abstractmethod
    def unfilled_end(self, ctx: ProgressContainer) -> Any:
        """Defines :unfilled_end: character for progress bar."""
