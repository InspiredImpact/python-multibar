from __future__ import annotations

__all__ = ("ProgressbarClientAware",)

import abc
import typing

from . import contracts
from . import hooks as hooks_

if typing.TYPE_CHECKING:
    from multibar.api import progressbars, sectors, writers


class ProgressbarClientAware(abc.ABC):
    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    def set_hooks(self, hooks: hooks_.HooksAware) -> ProgressbarClientAware:
        ...

    @abc.abstractmethod
    def update_hooks(self, hooks: hooks_.HooksAware) -> ProgressbarClientAware:
        ...

    @property
    @abc.abstractmethod
    def hooks(self) -> hooks_.HooksAware:
        ...

    @property
    @abc.abstractmethod
    def contract_manager(self) -> contracts.ContractManagerAware:
        ...

    @property
    @abc.abstractmethod
    def writer(self) -> writers.ProgressbarWriterAware[sectors.AbstractSector]:
        ...
