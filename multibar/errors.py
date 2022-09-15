from __future__ import annotations

__all__ = (
    "MultibarError",
    "ContractError",
    "ContractResponseError",
    "UnsignedContractError",
    "TerminatedContractError",
)

import typing

if typing.TYPE_CHECKING:
    from multibar.api import contracts


class MultibarError(Exception):
    """Base multibar error."""

    pass


class ContractError(MultibarError):
    """Base contracts error."""

    pass


class ContractResponseError(ContractError):
    """Error that parses contract response."""

    __slots__ = ("contract_check",)

    def __init__(self, check: contracts.ContractCheck, /) -> None:
        self.contract_check = check
        super().__init__(self._process_check())

    def _process_check(self) -> str:
        messages = self.contract_check.errors + self.contract_check.warnings
        return " & ".join(messages)


class UnsignedContractError(ContractError):
    """Raises if contract manager is not subscribed for specify contract."""

    pass


class TerminatedContractError(ContractResponseError):
    """Raises if contract is broken."""

    pass
