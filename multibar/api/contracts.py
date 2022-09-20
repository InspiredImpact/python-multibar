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
"""Interfaces for progressbar contracts."""
from __future__ import annotations

__all__ = (
    "ContractAware",
    "ContractCheck",
    "ContractManagerAware",
)

import abc
import collections.abc
import dataclasses
import typing

from returns.io import impure

from multibar import utils


@dataclasses.dataclass
class ContractCheck:
    """Response for contracts."""

    kept: bool
    """True if the contract is not broken (contains no errors or warnings)."""

    metadata: typing.MutableMapping[typing.Any, typing.Any] = dataclasses.field(default_factory=dict)
    """Contract metadata to check."""

    warnings: list[str] = dataclasses.field(default_factory=list)
    """Contract warnings."""

    errors: list[str] = dataclasses.field(default_factory=list)
    """Contract errors."""

    @classmethod
    def done(
        cls,
        metadata: typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None,
    ) -> ContractCheck:
        """Alternative constructor that used if contract is kept.

        Parameters
        ----------
        metadata : typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None
            Contract metadata to return.

        Returns
        -------
        ContractCheck
            Contract response.
        """
        return cls(kept=True, metadata=utils.none_or({}, metadata))

    @classmethod
    @typing.no_type_check
    def terminated(
        cls,
        metadata: typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None,
        warnings: typing.Optional[list[str]] = None,
        errors: typing.Optional[list[str]] = None,
    ) -> ContractCheck:
        """Alternative constructor that used if contract is broken.

        Parameters
        ----------
        metadata : typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None
            Contract metadata to return.
        warnings : typing.Optional[list[str]] = None
            Warnings to return.
        errors : typing.Optional[list[str]] = None
            Errors to return.

        Returns
        -------
        ContractCheck
            Contract response.
        """
        return cls(
            kept=False,
            metadata=utils.none_or({}, metadata),
            warnings=utils.none_or([], warnings),
            errors=utils.none_or([], errors),
        )


class ContractAware(abc.ABC):
    """Interface for contract implementations."""

    __slots__ = ()

    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> ContractCheck:
        """Checks contract for errors and warnings.

        Parameters
        ----------
        *args : typing.Any
            Arguments to check.
        **kwargs : typing.Any
            Keyword arguments to check.

        Returns
        -------
        ContractCheck
            Contract response.
        """
        ...

    @impure
    @abc.abstractmethod
    def render_terminated_contract(
        self,
        check: ContractCheck,
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

        Returns
        -------
        typing.Any
            Any value depending on context and implementation.
        """
        ...


class ContractManagerAware(abc.ABC):
    """Interface for contract manager implementations."""

    __slots__ = ()

    @abc.abstractmethod
    def check_contract(
        self,
        contract: ContractAware,
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

        Returns
        -------
        None
        """
        ...

    @abc.abstractmethod
    def check_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Checks all contracts.

        *args: typing.Any
            Arguments to contracts check.
        **kwargs: typing.Any
            Keyword arguments to contracts check.

        Returns
        -------
        None
        """
        ...

    @abc.abstractmethod
    def subscribe(self, contract: ContractAware, /) -> None:
        """Subscribes for contract.

        Parameters
        ----------
        contract : ContractAware
            Contract to subscribe.

        Returns
        -------
        None
        """
        ...

    @abc.abstractmethod
    def terminate(self, contract: ContractAware, /) -> None:
        """Terminates any contract.

        Parameters
        ----------
        contract : ContractAware
            Contract to terminate.

        Returns
        -------
        None
        """
        ...

    @abc.abstractmethod
    def terminate_all(self) -> None:
        """Terminates all contracts.

        Returns
        -------
        None
        """
        ...

    @abc.abstractmethod
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
        ...

    @property
    @abc.abstractmethod
    def contracts(self) -> collections.abc.Sequence[ContractAware]:
        """
        Returns
        -------
        collections.abc.Sequence[ContractAware]
            Sequence of the contracts.
        """
        ...

    @property
    @abc.abstractmethod
    def raise_errors(self) -> bool:
        """
        Returns
        -------
        bool
            Raise errors boolean value.
        """
        ...
