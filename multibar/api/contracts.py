from __future__ import annotations

__all__ = (
    "ContractAware",
    "ContractCheck",
    "ContractManagerAware",
)

import abc
import dataclasses
import typing

from returns.io import IO

from multibar import utils


@dataclasses.dataclass
class ContractCheck:
    kept: bool
    metadata: typing.MutableMapping[typing.Any, typing.Any] = dataclasses.field(default_factory=dict)
    warnings: list[str] = dataclasses.field(default_factory=list)
    errors: list[str] = dataclasses.field(default_factory=list)

    @classmethod
    def done(
        cls,
        metadata: typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None,
    ) -> ContractCheck:
        return cls(kept=True, metadata=utils.none_or({}, metadata))

    @classmethod
    @typing.no_type_check
    def terminated(
        cls,
        metadata: typing.Optional[typing.MutableMapping[typing.Any, typing.Any]] = None,
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
    def render_terminated_contract(self, check: ContractCheck, /, *, raise_errors: bool) -> IO[None]:
        ...


class ContractManagerAware(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def check_contract(
        self,
        contract: ContractAware,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        ...

    @abc.abstractmethod
    def check_contracts(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @abc.abstractmethod
    def subscribe(self, contract: ContractAware, /) -> None:
        ...

    @abc.abstractmethod
    def terminate(self, contract: ContractAware, /) -> None:
        ...

    @abc.abstractmethod
    def terminate_all(self) -> None:
        ...

    @abc.abstractmethod
    def set_raise_errors(self, value: bool, /) -> None:
        ...

    @property
    @abc.abstractmethod
    def contracts(self) -> list[ContractAware]:
        ...

    @property
    @abc.abstractmethod
    def raise_errors(self) -> bool:
        ...
