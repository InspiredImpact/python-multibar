from __future__ import annotations

__all__ = ("ProgressbarClient",)

import typing

from multibar import utils
from multibar import types as progress_types
from multibar.api import clients
from multibar.impl import hooks as hooks_
from multibar.impl import writers
from multibar.impl import contracts

if typing.TYPE_CHECKING:
    from multibar.api import hooks as abc_hooks
    from multibar.api import writers as abc_writers
    from multibar.api import contracts as abc_contracts
    from multibar.api import progressbars as abc_progressbars
    from multibar.api import sectors as abc_sectors


class ProgressbarClient(clients.ProgressbarClientAware):
    def __init__(
        self,
        *,
        hooks: typing.Optional[abc_hooks.HooksAware] = None,
        progress_writer: typing.Optional[abc_writers.ProgressbarWriterAware] = None,
        contract_manager: typing.Optional[abc_contracts.ContractManagerAware] = None,
    ) -> None:
        self._hooks = utils.none_or(hooks_.Hooks(), hooks)
        self._writer = utils.none_or(writers.ProgressbarWriter(), progress_writer)

        if contract_manager is None:
            contract_manager = contracts.ContractManager()
            contract_manager.subscribe(contracts.WriteProgressContract())

        self._contract_manager: abc_contracts.ContractManagerAware = contract_manager

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
    ) -> typing.Optional[abc_progressbars.ProgressbarAware[abc_sectors.SectorAware]]:
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

    def set_hooks(self, hooks: abc_hooks.HooksAware) -> ProgressbarClient:
        self._hooks = hooks
        return self

    def update_hooks(self, hooks: abc_hooks.HooksAware) -> ProgressbarClient:
        self._hooks = self._hooks | hooks
        return self

    @property
    def hooks(self) -> abc_hooks.HooksAware:
        return self._hooks

    @property
    def contract_manager(self) -> abc_contracts.ContractManagerAware:
        return self._contract_manager
