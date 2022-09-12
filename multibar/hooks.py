from __future__ import annotations
import abc
import typing

from . import types as progress_types

if typing.TYPE_CHECKING:
    from . import writers

    HookSignatureType: typing.TypeAlias = typing.Callable[..., typing.Optional[bool]]


class UnboundError(Exception):
    pass


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
    def add_to_writer(self, writer: writers.ProgressbarWriterAware, /) -> HooksAware:
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


class Hooks(HooksAware):
    def __init__(self) -> None:
        self._on_error_hooks: list[HookSignatureType] = []
        self._pre_execution_hooks: list[HookSignatureType] = []
        self._post_execution_hooks: list[HookSignatureType] = []

    def add_to_writer(self, writer: writers.HookedProgressbarWriterAware, /) -> Hooks:
        if writer.hooks is None:
            writer.set_hooks(self)
        else:
            writer.update_hooks(self)

        return self

    def add_pre_execution(self, callback: HookSignatureType, /) -> Hooks:
        self._pre_execution_hooks.append(callback)
        return self

    def add_post_execution(self, callback: HookSignatureType, /) -> Hooks:
        self._post_execution_hooks.append(callback)
        return self

    def add_on_error(self, callback: HookSignatureType, /) -> Hooks:
        self._on_error_hooks.append(callback)
        return self

    def trigger_post_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for hook in self._post_execution_hooks:
            hook(*args, **kwargs)

    def trigger_pre_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for hook in self._pre_execution_hooks:
            hook(*args, **kwargs)

    def trigger_on_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        if not self._on_error_hooks:
            raise

        else:
            for hook in self._on_error_hooks:
                hook(*args, **kwargs)

    @property
    def pre_execution_hooks(self) -> list[HookSignatureType]:
        return self._pre_execution_hooks

    @property
    def post_execution_hooks(self) -> list[HookSignatureType]:
        return self._post_execution_hooks

    @property
    def on_error_hooks(self) -> list[HookSignatureType]:
        return self._on_error_hooks


def _progress_writer_hook(*_: typing.Any, **kwargs: typing.Any) -> None:
    FIRST_FILL: typing.Literal[3] = 3
    LAST_FILL: typing.Literal[97] = 97

    metadata = typing.cast(progress_types.ProgressMetadataType, kwargs["metadata"])
    process_percentage = metadata["calculation_service_cls"].get_progress_percentage(
        metadata["start_value"], metadata["end_value"]
    )
    progressbar = metadata["progressbar"]
    sig = metadata["sig"]

    # Add `unfilled_start` if none of the sectors is yet filled.
    if process_percentage < FIRST_FILL:
        progressbar.replace_visual(0, sig.start.on_unfilled)
    # Otherwise, it will be added to the beginning.
    elif process_percentage >= FIRST_FILL:
        progressbar.replace_visual(0, sig.start.on_filled)
    # If the last sector is not filled, then the
    # corresponding character will be added to the end of the progressbar.
    if process_percentage < LAST_FILL:
        progressbar.replace_visual(-1, sig.end.on_unfilled)
    # Otherwise, the character corresponding to the
    # given argument will be appended to the end of the progressbar.
    elif process_percentage >= LAST_FILL:
        progressbar.replace_visual(-1, sig.end.on_filled)


WRITER_HOOKS = Hooks()
WRITER_HOOKS.add_post_execution(_progress_writer_hook)
