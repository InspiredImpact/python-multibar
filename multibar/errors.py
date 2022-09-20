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
"""Module with Python-Multibar errors."""
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
    """Base multibar error.
    You can use this error to catch any error from Python-Multibar.
    """

    pass


class ContractError(MultibarError):
    """Base contracts error."""

    pass


class ContractResponseError(ContractError):
    """Error that parses contract response."""

    __slots__ = ("contract_check",)

    def __init__(self, check: contracts.ContractCheck, /) -> None:
        """
        Parameters
        ----------
        check : ContractCheck
            Broken contract check response.
        """
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
