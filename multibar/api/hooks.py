from __future__ import annotations

__all__ = (
    "HookSignatureType",
    "HooksAware",
)

import abc
import collections.abc
import typing

import typing_extensions

if typing.TYPE_CHECKING:
    from . import clients

HookSignatureType: typing_extensions.TypeAlias = typing.Callable[..., typing.Optional[bool]]


class HooksAware(abc.ABC):
    """Interface to progress hooks implementation."""

    __slots__ = ()

    @abc.abstractmethod
    def __len__(self) -> int:
        """Returns length of all hooks. Used for bool() and len() operations."""
        ...

    @abc.abstractmethod
    def add_to_client(self, client: clients.ProgressbarClientAware, /) -> HooksAware:
        """Adds hooks to the client.

        Parameters
        ----------
        client : clients.ProgressbarClientAware, /
            Client to add.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def update(self, other: HooksAware, /) -> HooksAware:
        """Updates self hooks from other hooks object.

        Parameters
        ----------
        other : HooksAware, /
            Other hooks object to update.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def add_pre_execution(self, callback: HookSignatureType, /) -> HooksAware:
        """Adds pre-execution callback.

        Parameters
        ----------
        callback : HookSignatureType, /
            Pre-execution callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def add_post_execution(self, callback: HookSignatureType, /) -> HooksAware:
        """Adds post-execution callback.

        Parameters
        ----------
        callback : HookSignatureType, /
            Post-execution callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def add_on_error(self, callback: HookSignatureType, /) -> HooksAware:
        """Adds on-error callback.

        Parameters
        ----------
        callback : HookSignatureType, /
            On-error callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def trigger_post_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all post-execution callbacks.

        *args : typing.Any
            Arguments to trigger.

        **kwargs : typing.Any
            Keyword arguments to trigger.
        """
        ...

    @abc.abstractmethod
    def trigger_pre_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all pre-execution callbacks.

        *args : typing.Any
            Arguments to trigger.

        **kwargs : typing.Any
            Keyword arguments to trigger.
        """
        ...

    @abc.abstractmethod
    def trigger_on_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all on-error callbacks.

        *args : typing.Any
            Arguments to trigger.

        **kwargs : typing.Any
            Keyword arguments to trigger.
        """
        ...

    @property
    @abc.abstractmethod
    def pre_execution_hooks(self) -> collections.abc.Sequence[HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of pre-execution hooks.
        """
        ...

    @property
    @abc.abstractmethod
    def post_execution_hooks(self) -> collections.abc.Sequence[HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of post-execution hooks.
        """
        ...

    @property
    @abc.abstractmethod
    def on_error_hooks(self) -> collections.abc.Sequence[HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of on-error hooks.
        """
        ...
