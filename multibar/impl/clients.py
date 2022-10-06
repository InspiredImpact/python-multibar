# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Implementations of Python-Multibar clients."""
from __future__ import annotations

__all__ = ("ProgressbarClient",)

import typing

from multibar import types as progress_types
from multibar import utils
from multibar.api import clients as abc_clients
from multibar.impl import contracts
from multibar.impl import hooks as hooks_
from multibar.impl import writers

if typing.TYPE_CHECKING:
    from multibar.api import contracts as abc_contracts
    from multibar.api import hooks as abc_hooks
    from multibar.api import progressbars as abc_progressbars
    from multibar.api import sectors as abc_sectors
    from multibar.api import writers as abc_writers


class ProgressbarClient(abc_clients.ProgressbarClientAware):
    """Implementation of abc_clients.ProgressbarClientAware.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    __slots__ = ("_hooks", "_writer", "_contract_manager")

    def __init__(
        self,
        *,
        hooks: typing.Optional[abc_hooks.HooksAware] = None,
        progress_writer: typing.Optional[abc_writers.ProgressbarWriterAware] = None,
        contract_manager: typing.Optional[abc_contracts.ContractManagerAware] = None,
    ) -> None:
        """
        Parameters
        ----------
        hooks : typing.Optional[HooksAware] = None
            Progressbar client hooks.
        progress_writer : typing.Optional[ProgressbarWriterAware[AbstractSector]] = None
            Writer for progressbar generation.
        contract_manager : typing.Optional[ContractManagerAware] = None
            Contract manager for any progress checks.
        """
        self._hooks = utils.none_or(hooks_.Hooks(), hooks)
        self._writer = utils.none_or(writers.ProgressbarWriter(), progress_writer)

        if contract_manager is None:
            contract_manager = contracts.ContractManager()
            contract_manager.subscribe(contracts.WRITE_PROGRESS_CONTRACT)

        self._contract_manager: abc_contracts.ContractManagerAware = contract_manager

    def _validate_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers on-error hooks if broken contract raise error.

        !!! warning
            It will not handle broken contract, if contract.raise_errors equals to False.

        Parameters
        ----------
        *args: typing.Any
            Arguments to contract check.

        **kwargs: typing.Any
            Keyword arguments to contract check.
        """
        try:
            self._contract_manager.check_contracts(*args, **kwargs)
        except Exception as exc:
            self._hooks.trigger_on_error(*args, exc, **kwargs)

    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> abc_progressbars.ProgressbarAware[abc_sectors.AbstractSector]:
        """Generates a progressbar, can be a wrapper for ProgressWriterAware.write()
        to implement hooks and various kinds of checks.

        Parameters
        ----------
        start_value : int, /
            Start value (current progress) for progressbar math operations.
        end_value : int, /
            End value (needed progress) for progressbar math operations.
        length : int = 20, *
            Length of progressbar for progressbar math operations.

        Raises
        ------
        errors.TerminatedContractError
            This contract is signed by default. Checks if the Start value is greater
            than the End value, if so, an error will be raised.

            !!! info
                You can unsubscribe from this contract as follows:
                ```py hl_lines="4"
                import multibar

                client = multibar.ProgressbarClient()
                client.contract_manager.terminate(multibar.INPUT_VALUES_CONTRACT)
                ```

        Returns
        -------
        progressbars.ProgressbarAware[sectors.AbstractSector]
            Progressbar instance.
        """
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

    def set_hooks(self, hooks: abc_hooks.HooksAware, /) -> ProgressbarClient:
        """Sets hooks to the client.

        Parameters
        ----------
        hooks : hooks_.HooksAware
            Any hooks to set.

        Returns
        -------
        Self
            ProgressbarClient object to allow fluent-style.
        """
        self._hooks = hooks
        return self

    def update_hooks(self, hooks: abc_hooks.HooksAware, /) -> ProgressbarClient:
        """Updates hooks for the client.

        Parameters
        ----------
        hooks : hooks_.HooksAware
            Any hooks to update.

        Returns
        -------
        Self
            ProgressbarClient object to allow fluent-style.
        """
        self._hooks.update(hooks)
        return self

    @property
    def hooks(self) -> abc_hooks.HooksAware:
        """
        Returns
        -------
        hooks_.HooksAware
            Client hooks.
        """
        return self._hooks

    @property
    def contract_manager(self) -> abc_contracts.ContractManagerAware:
        """
        Returns
        -------
        contracts.ContractManagerAware
            Client contract manager for checks.
        """
        return self._contract_manager

    @property
    def writer(self) -> abc_writers.ProgressbarWriterAware:
        """
        Returns
        -------
        writers.ProgressbarWriterAware[sectors.AbstractSector]
            Progressbar writer for progress generating.
        """
        return self._writer
