from __future__ import annotations

__all__ = (
    "HookSignatureType",
    "HooksAware",
)

import abc
import typing

import typing_extensions

if typing.TYPE_CHECKING:
    from . import clients

HookSignatureType: typing_extensions.TypeAlias = typing.Callable[..., typing.Optional[bool]]


class HooksAware(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def __len__(self) -> int:
        ...

    @abc.abstractmethod
    def add_to_client(self, writer: clients.ProgressbarClientAware, /) -> HooksAware:
        ...

    @abc.abstractmethod
    def update(self, other: HooksAware, /) -> HooksAware:
        ...

    @abc.abstractmethod
    def add_pre_execution(self, callback: HookSignatureType, /) -> HooksAware:
        ...

    @abc.abstractmethod
    def add_post_execution(self, callback: HookSignatureType, /) -> HooksAware:
        ...

    @abc.abstractmethod
    def add_on_error(self, callback: HookSignatureType, /) -> HooksAware:
        ...

    @abc.abstractmethod
    def trigger_post_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @abc.abstractmethod
    def trigger_pre_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @abc.abstractmethod
    def trigger_on_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @property
    @abc.abstractmethod
    def pre_execution_hooks(self) -> list[HookSignatureType]:
        ...

    @property
    @abc.abstractmethod
    def post_execution_hooks(self) -> list[HookSignatureType]:
        ...

    @property
    @abc.abstractmethod
    def on_error_hooks(self) -> list[HookSignatureType]:
        ...
