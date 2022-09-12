from __future__ import annotations

__all__ = ("HookSignatureType", "HooksAware",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import clients

HookSignatureType: typing.TypeAlias = typing.Callable[..., typing.Optional[bool]]


class HooksAware(abc.ABC):
    __slots__ = ()

    def __or__(self, other: typing.Any) -> typing.Any:
        if not isinstance(other, HooksAware):
            return NotImplemented

        self.on_error_hooks.extend(other.on_error_hooks)
        self.post_execution_hooks.extend(other.post_execution_hooks)
        self.pre_execution_hooks.extend(other.pre_execution_hooks)

        return self

    @abc.abstractmethod
    def add_to_client(self, writer: clients.ProgressbarClientAware, /) -> HooksAware:
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
