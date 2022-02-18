from __future__ import annotations

__all__ = ["AbstractCustomerMixin"]

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from multibar.internal.crate import ProgressContainer


class AbstractCustomerMixin(abc.ABC):
    def __init__(self, ctx: ProgressContainer) -> None:
        self.ctx = ctx

    @abc.abstractmethod
    def fill(self, ctx: ProgressContainer) -> Any:
        ...

    @abc.abstractmethod
    def line(self, ctx: ProgressContainer) -> Any:
        ...

    @abc.abstractmethod
    def start(self, ctx: ProgressContainer) -> Any:
        ...

    @abc.abstractmethod
    def end(self, ctx: ProgressContainer) -> Any:
        ...

    @abc.abstractmethod
    def unfilled_start(self, ctx: ProgressContainer) -> Any:
        ...

    @abc.abstractmethod
    def unfilled_end(self, ctx: ProgressContainer) -> Any:
        ...
