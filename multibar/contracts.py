from __future__ import annotations
import abc
import typing
import dataclasses

from returns.io import impure

from . import utils
from . import output
from . import types as progress_types


class ContractError(Exception):
    pass


class UnsignedContractError(ContractError):
    pass


class TerminatedContractError(ContractError):
    __slots__ = ("contract_check",)

    def __init__(self, *, check: ContractCheck) -> None:
        self.contract_check = check
        super().__init__(self._process_check())

    def _process_check(self) -> str:
        messages = self.contract_check.errors + self.contract_check.warnings
        return " & ".join(messages)


@dataclasses.dataclass
class ContractCheck:
    kept: bool
    metadata: dict[str, typing.Any] = dataclasses.field(default_factory=dict)
    warnings: list[str] = dataclasses.field(default_factory=list)
    errors: list[str] = dataclasses.field(default_factory=list)

    @classmethod
    def done(
        cls,
        metadata: typing.Optional[dict[str, typing.Any]] = None,
    ) -> ContractCheck:
        return cls(kept=True, metadata=utils.none_or({}, metadata))

    @classmethod
    def terminated(
        cls,
        metadata: typing.Optional[dict[str, typing.Any]] = None,
        warnings: typing.Optional[list[str]] = None,
        errors: typing.Optional[list[str]] = None,
    ) -> ContractCheck:
        return cls(
            kept=False,
            metadata=utils.none_or({}, metadata),
            warnings=utils.none_or([], warnings),
            errors=utils.none_or([], errors),
        )


class ContractAware(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> ContractCheck:
        ...

    @abc.abstractmethod
    def render_terminated_contract(self, check: ContractCheck, /, *, raise_errors: bool) -> None:
        ...


class ContractManagerAware(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def trigger_contract(
        self, contract: ContractAware, *args: typing.Any, **kwargs: typing.Any,
    ) -> None:
        ...

    @abc.abstractmethod
    def trigger_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @abc.abstractmethod
    def subscribe(self, contract: ContractAware, /) -> None:
        ...

    @abc.abstractmethod
    def terminate(self, contract: ContractAware, /) -> None:
        ...

    @abc.abstractmethod
    def set_raise_errors(self, value: bool, /) -> None:
        ...

    @property
    @abc.abstractmethod
    def contracts(self) -> list[ContractAware]:
        ...


class ContractManager(ContractManagerAware):
    def __init__(self, *, raise_errors: bool = False) -> None:
        self._contracts: list[ContractAware] = []
        self._raise_errors = raise_errors

    def _agreed_with_manager(self, contract: ContractAware, /) -> bool:
        return contract in self._contracts

    def set_raise_errors(self, value: bool, /) -> None:
        self._raise_errors = value

    def trigger_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for contract in self._contracts:
            self.trigger_contract(contract, *args, **kwargs)

    def trigger_contract(
        self, contract: ContractAware, *args: typing.Any, **kwargs: typing.Any,
    ) -> None:
        if not self._agreed_with_manager(contract):
            raise UnsignedContractError(f"Contract {type(contract).__name__} is unsigned.")

        contract_check = contract.check(*args, **kwargs)
        if not contract_check.kept:
            contract.render_terminated_contract(
                contract_check, raise_errors=self._raise_errors,
            )

    def subscribe(self, contract: ContractAware, /) -> None:
        self._contracts.append(contract)

    def terminate(self, contract: ContractAware, /) -> None:
        self._contracts.remove(contract)

    @property
    def contracts(self) -> list[ContractAware]:
        return self._contracts

####################
# WRITER CONTRACTS #
####################

class WriteProgressContract(ContractAware):
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> ContractCheck:
        call_metadata = meta = typing.cast(progress_types.ProgressMetadataType, kwargs.pop("metadata", {}))
        if not call_metadata:
            return ContractCheck.terminated(
                errors=["Needs metadata argument."],
                metadata=call_metadata,
            )

        start, end, length = meta["start_value"], meta["end_value"], meta["length"]
        if start > end:
            return ContractCheck.terminated(
                errors=["Start value cannot be more than end value."],
                metadata=call_metadata,
            )

        if length <= 0:
            return ContractCheck.terminated(
                errors=["Length of progress bar must be more than 0."],
                metadata=call_metadata,
            )

        return ContractCheck.done(
            metadata=call_metadata,
        )

    @impure
    def render_terminated_contract(self, check: ContractCheck, /, *, raise_errors: bool) -> None:
        if raise_errors:
            raise TerminatedContractError(check=check)

        self_module = self.__module__ + "." + "WriteProgressContract"
        output.print_heading(f"{self_module} was broken", level=1, indent=False)
        output.print(f"Warnings: {len(check.warnings)}", bold=True)

        for warning in check.warnings:
            output.print_warning(warning)

        output.print(f"Errors: {len(check.errors)}", bold=True)

        for error in check.errors:
            output.print_error(error)
