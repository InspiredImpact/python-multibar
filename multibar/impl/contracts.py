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
"""Implementation of progressbar contracts."""
from __future__ import annotations

__all__ = (
    "ContractManager",
    "WriteProgressContract",
    "WRITE_PROGRESS_CONTRACT",
    "INPUT_VALUES_CONTRACT",
)

import typing

from returns.io import IO, impure

from multibar import errors, output
from multibar.api import contracts


class ContractManager(contracts.ContractManagerAware):
    """Implementation of contracts.ContractManagerAware.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    __slots__ = ("_contracts", "_raise_errors")

    def __init__(self, *, raise_errors: bool = True) -> None:
        """
        Parameters
        ----------
        raise_errors : bool = True
            If True, will raise errors when contract is broken.
        """
        self._contracts: list[contracts.ContractAware] = []
        self._raise_errors = raise_errors

    def _agreed_with_manager(self, contract: contracts.ContractAware, /) -> bool:
        return contract in self._contracts

    def set_raise_errors(self, value: bool, /) -> None:
        """Render broken contract may contain IO operations
        if raise_errors is False. Otherwise, it returns nothing,
        but throws an error.

        Parameters
        ----------
        value : bool
            Raise errors boolean value.

        Returns
        -------
        None
        """
        self._raise_errors = value

    def check_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Checks all contracts.

        Parameters
        ----------
        *args: typing.Any
            Arguments to contracts check.
        **kwargs: typing.Any
            Keyword arguments to contracts check.

        Returns
        -------
        None
        """
        for contract in self._contracts:
            self.check_contract(contract, *args, **kwargs)

    def check_contract(
        self,
        contract: contracts.ContractAware,
        /,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        """Checks contract for any errors or warnings.

        Parameters
        ----------
        contract : ContractAware
            Contract to check.
        *args: typing.Any
            Arguments to contract check.
        **kwargs: typing.Any
            Keyword arguments to contract check.

        Raises
        ------
        errors.UnsignedContractError
            If manager is not subscribed for specify contract.

        Returns
        -------
        None
        """
        if not self._agreed_with_manager(contract):
            raise errors.UnsignedContractError(f"Contract {type(contract).__name__} is unsigned.")

        contract_check = contract.check(*args, **kwargs)
        if not contract_check.kept:
            contract.render_terminated_contract(
                contract_check,
                raise_errors=self._raise_errors,
            )

    def subscribe(self, contract: contracts.ContractAware, /) -> None:
        """Subscribes for contract.

        Parameters
        ----------
        contract : ContractAware
            Contract to subscribe.

        Returns
        -------
        None
        """
        self._contracts.append(contract)

    def terminate(self, contract: contracts.ContractAware, /) -> None:
        """Terminates any contract.

        Parameters
        ----------
        contract : ContractAware
            Contract to terminate.

        Returns
        -------
        None
        """
        self._contracts.remove(contract)

    def terminate_all(self) -> None:
        """Terminates all contracts.

        Returns
        -------
        None
        """
        self._contracts.clear()

    @property
    def contracts(self) -> list[contracts.ContractAware]:
        """
        Returns
        -------
        collections.abc.Sequence[ContractAware]
            Sequence of the contracts.
        """
        return self._contracts

    @property
    def raise_errors(self) -> bool:
        """
        Returns
        -------
        bool
            Raise errors boolean value.
        """
        return self._raise_errors


####################
# WRITER CONTRACTS #
####################


class WriteProgressContract(contracts.ContractAware):
    """Implementation of contracts.ContractAware.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    def check(self, *args: typing.Any, **kwargs: typing.Any) -> contracts.ContractCheck:
        """Checks contract for errors and warnings.

        Parameters
        ----------
        *args : typing.Any
            Arguments to check.
        **kwargs : typing.Any
            Keyword arguments to check.

        Returns
        -------
        contracts.ContractCheck
            Contract response.
        """
        call_metadata = meta = typing.cast(typing.MutableMapping[typing.Any, typing.Any], kwargs.pop("metadata", {}))
        if not call_metadata:
            return contracts.ContractCheck.terminated(
                errors=["Needs metadata argument."],
                metadata=call_metadata,
            )

        start, end, length = meta["start_value"], meta["end_value"], meta["length"]
        if start > end:
            return contracts.ContractCheck.terminated(
                errors=["`Start` value cannot be more than `End` value."],
                metadata=call_metadata,
            )

        if length <= 0:
            return contracts.ContractCheck.terminated(
                errors=["Length of progress bar must be more than 0."],
                metadata=call_metadata,
            )

        return contracts.ContractCheck.done(
            metadata=call_metadata,
        )

    @typing.overload
    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: typing.Literal[False],
    ) -> typing.NoReturn:
        # Will raise any error.
        ...

    @typing.overload
    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: typing.Literal[True],
    ) -> IO[None]:
        # Will print any errors/warnings in console.
        ...

    @typing.overload
    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: bool,
    ) -> typing.Any:
        ...

    @impure
    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: bool,
    ) -> typing.Any:
        """Renders broken contract.
        May contain IO operations if raise_errors is False.
        Otherwise, it returns nothing, but throws an error.

        Parameters
        ----------
        check : ContractCheck
            Contract response.
        raise_errors : bool
            If True, will raise errors when contract is broken.

        Raises
        ------
        errors.TerminatedContractError
            If `raise_errors` parameter is `True`.

        Returns
        -------
        typing.Any
            Any value depending on context and implementation.
        """
        if raise_errors:
            raise errors.TerminatedContractError(check)

        self_module = self.__module__ + "." + "WriteProgressContract"
        output.print_heading(f"{self_module} was broken", level=1, indent=False)
        output.print(f"Warnings: {len(check.warnings)}", bold=True)

        for warning in check.warnings:
            output.print_warning(warning)

        output.print(f"Errors: {len(check.errors)}", bold=True)

        for error in check.errors:
            output.print_error(error)

        return IO(None)


WRITE_PROGRESS_CONTRACT = WriteProgressContract()
"""Contract that checks if `start_value` is not more than `end_value`
and if `length` is more that zero.

!!! warning
    For subscribing or unsubscribing of `WriteProgressContract` its recommended
    to use this variable, because this methods depends on object `id`.
"""

INPUT_VALUES_CONTRACT = WRITE_PROGRESS_CONTRACT
"""Alias to WRITE_PROGRESS_CONTRACT."""
