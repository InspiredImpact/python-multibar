from __future__ import annotations

__all__ = ("ProgressbarClientAware",)

import abc
import typing

from . import contracts
from . import hooks as hooks_

if typing.TYPE_CHECKING:
    from multibar.api import progressbars, sectors


class ProgressbarClientAware(abc.ABC):
    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]:
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
    ) -> typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]:
        ...

    @abc.abstractmethod
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]:
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
