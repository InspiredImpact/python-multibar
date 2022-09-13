from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from multibar.api import contracts


class MultibarError(Exception):
    pass


class ContractError(MultibarError):
    pass


class ContractResponseError(ContractError):
    __slots__ = ("contract_check",)

    def __init__(self, check: contracts.ContractCheck, /) -> None:
        self.contract_check = check
        super().__init__(self._process_check())

    def _process_check(self) -> str:
        messages = self.contract_check.errors + self.contract_check.warnings
        return " & ".join(messages)


class UnsignedContractError(ContractError):
    pass


class TerminatedContractError(ContractResponseError):
    pass
