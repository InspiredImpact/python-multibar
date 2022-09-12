from __future__ import annotations

__all__ = (
    "ContractManager",
    "WriteProgressContract",
)

import typing

from returns.io import IO

from multibar import errors, output
from multibar import types as progress_types
from multibar.api import contracts


class ContractManager(contracts.ContractManagerAware):
    def __init__(self, *, raise_errors: bool = False) -> None:
        self._contracts: list[contracts.ContractAware] = []
        self._raise_errors = raise_errors

    def _agreed_with_manager(self, contract: contracts.ContractAware, /) -> bool:
        return contract in self._contracts

    def set_raise_errors(self, value: bool, /) -> None:
        self._raise_errors = value

    def check_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for contract in self._contracts:
            self.check_contract(contract, *args, **kwargs)

    def check_contract(
        self,
        contract: contracts.ContractAware,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        if not self._agreed_with_manager(contract):
            raise errors.UnsignedContractError(f"Contract {type(contract).__name__} is unsigned.")

        contract_check = contract.check(*args, **kwargs)
        if not contract_check.kept:
            contract.render_terminated_contract(
                contract_check,
                raise_errors=self._raise_errors,
            )

    def subscribe(self, contract: contracts.ContractAware, /) -> None:
        self._contracts.append(contract)

    def terminate(self, contract: contracts.ContractAware, /) -> None:
        self._contracts.remove(contract)

    @property
    def contracts(self) -> list[contracts.ContractAware]:
        return self._contracts


####################
# WRITER CONTRACTS #
####################


class WriteProgressContract(contracts.ContractAware):
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> contracts.ContractCheck:
        call_metadata = meta = typing.cast(
            typing.MutableMapping[typing.Any, typing.Any], kwargs.pop("metadata", {})
        )
        if not call_metadata:
            return contracts.ContractCheck.terminated(
                errors=["Needs metadata argument."],
                metadata=call_metadata,
            )

        start, end, length = meta["start_value"], meta["end_value"], meta["length"]
        if start > end:
            return contracts.ContractCheck.terminated(
                errors=["Start value cannot be more than end value."],
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

    def render_terminated_contract(
        self, check: contracts.ContractCheck, /, *, raise_errors: bool
    ) -> IO[None]:
        if raise_errors:
            raise errors.TerminatedContractError(check=check)

        self_module = self.__module__ + "." + "WriteProgressContract"
        output.print_heading(f"{self_module} was broken", level=1, indent=False)
        output.print(f"Warnings: {len(check.warnings)}", bold=True)

        for warning in check.warnings:
            output.print_warning(warning)

        output.print(f"Errors: {len(check.errors)}", bold=True)

        for error in check.errors:
            output.print_error(error)

        return IO(None)
