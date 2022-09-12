from __future__ import annotations
import abc
import typing

from . import utils
from . import writers
from . import contracts
from . import hooks as hooks_
from . import types as progress_types

if typing.TYPE_CHECKING:
    from . import progressbars
    from . import sectors


class ProgressbarClientAware(abc.ABC):
    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> typing.Optional[progressbars.Progressbar[sectors.AbstractSector]]:
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
    ) -> typing.Optional[progressbars.Progressbar[sectors.AbstractSector]]:
        ...

    @abc.abstractmethod
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> typing.Optional[progressbars.Progressbar[sectors.AbstractSector]]:
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


class ProgressbarClient(ProgressbarClientAware):
    def __init__(
        self,
        *,
        hooks: typing.Optional[hooks_.HooksAware] = None,
        progress_writer: typing.Optional[writers.ProgressbarWriterAware] = None,
        contract_manager: typing.Optional[contracts.ContractManagerAware] = None,
    ) -> None:
        self._hooks = utils.none_or(hooks_.Hooks(), hooks)
        self._writer = utils.none_or(writers.ProgressbarWriter(), progress_writer)

        if contract_manager is None:
            contract_manager = contracts.ContractManager()
            contract_manager.subscribe(contracts.WriteProgressContract())

        self._contract_manager: contracts.ContractManagerAware = contract_manager

    def _validate_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        try:
            self._contract_manager.trigger_contracts(*args, **kwargs)
        except Exception as exc:
            self._hooks.trigger_on_error(*args, exc, **kwargs)

    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> typing.Optional[progressbars.Progressbar[sectors.AbstractSector]]:
        writer = self._writer
        call_metadata: progress_types.ProgressMetadataType = {
            "calculation_service_cls": writer.calculation_cls,
            "progressbar": None,
            "start_value": start_value,
            "end_value": end_value,
            "length": length,
            "sig": writer.signature,
        }

        self._validate_contracts(self._writer, metadata=call_metadata)
        self._hooks.trigger_pre_execution(self, metadata=call_metadata)

        progressbar = self._writer.write(start_value, end_value, length=length)
        call_metadata["progressbar"] = progressbar

        self._hooks.trigger_post_execution(self, metadata=call_metadata)
        return progressbar

    def set_hooks(self, hooks: hooks_.HooksAware) -> ProgressbarClient:
        self._hooks = hooks
        return self

    def update_hooks(self, hooks: hooks_.HooksAware) -> ProgressbarClient:
        self._hooks = self._hooks | hooks
        return self

    @property
    def hooks(self) -> hooks_.HooksAware:
        return self._hooks

    @property
    def contract_manager(self) -> contracts.ContractManagerAware:
        return self._contract_manager
