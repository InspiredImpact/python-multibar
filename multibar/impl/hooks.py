from __future__ import annotations

__all__ = (
    "Hooks",
    "WRITER_HOOKS",
)

import typing

from multibar import types as progress_types
from multibar.api import hooks

if typing.TYPE_CHECKING:
    from multibar.api import clients
    from multibar.api.hooks import HookSignatureType


class Hooks(hooks.HooksAware):
    __slots__ = ("_on_error_hooks", "_pre_execution_hooks", "_post_execution_hooks")

    def __init__(self) -> None:
        self._on_error_hooks: list[HookSignatureType] = []
        self._pre_execution_hooks: list[HookSignatureType] = []
        self._post_execution_hooks: list[HookSignatureType] = []

    def __len__(self) -> int:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        return len(self._on_error_hooks + self._pre_execution_hooks + self._post_execution_hooks)

    def add_to_client(self, client: clients.ProgressbarClientAware, /) -> Hooks:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        if not client.hooks:
            client.set_hooks(self)
        else:
            client.update_hooks(self)

        return self

    def update(self, other: hooks.HooksAware, /) -> Hooks:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        self._on_error_hooks.extend(other.on_error_hooks)
        self._post_execution_hooks.extend(other.post_execution_hooks)
        self._pre_execution_hooks.extend(other.pre_execution_hooks)
        return self

    def add_pre_execution(self, callback: HookSignatureType, /) -> Hooks:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        self._pre_execution_hooks.append(callback)
        return self

    def add_post_execution(self, callback: HookSignatureType, /) -> Hooks:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        self._post_execution_hooks.append(callback)
        return self

    def add_on_error(self, callback: HookSignatureType, /) -> Hooks:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        self._on_error_hooks.append(callback)
        return self

    def trigger_post_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        for hook in self._post_execution_hooks:
            hook(*args, **kwargs)

    def trigger_pre_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        for hook in self._pre_execution_hooks:
            hook(*args, **kwargs)

    def trigger_on_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        if not self._on_error_hooks:
            raise

        else:
            for hook in self._on_error_hooks:
                hook(*args, **kwargs)

    @property
    def pre_execution_hooks(self) -> list[HookSignatureType]:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        return self._pre_execution_hooks

    @property
    def post_execution_hooks(self) -> list[HookSignatureType]:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
        return self._post_execution_hooks

    @property
    def on_error_hooks(self) -> list[HookSignatureType]:
        # << inherited docstring for multibar.api.hooks.HooksAware >>
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

    assert progressbar is not None
    # Add `unfilled_start` if none of the sectors is yet filled.
    if process_percentage < FIRST_FILL:
        progressbar.replace_display_name_for(0, sig.start.on_unfilled)
    # Otherwise, it will be added to the beginning.
    elif process_percentage >= FIRST_FILL:
        progressbar.replace_display_name_for(0, sig.start.on_filled)
    # If the last sector is not filled, then the
    # corresponding character will be added to the end of the progressbar.
    if process_percentage < LAST_FILL:
        progressbar.replace_display_name_for(-1, sig.end.on_unfilled)
    # Otherwise, the character corresponding to the
    # given argument will be appended to the end of the progressbar.
    elif process_percentage >= LAST_FILL:
        progressbar.replace_display_name_for(-1, sig.end.on_filled)


WRITER_HOOKS = Hooks()
WRITER_HOOKS.add_post_execution(_progress_writer_hook)
