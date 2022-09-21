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
"""Implementation of hooks interfaces."""
from __future__ import annotations

__all__ = (
    "Hooks",
    "WRITER_HOOKS",
)

import typing

from multibar import types as ptypes
from multibar.api import hooks

if typing.TYPE_CHECKING:
    from multibar.api import clients


class Hooks(hooks.HooksAware):
    """Implementation of hooks.HooksAware.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    __slots__ = ("_on_error_hooks", "_pre_execution_hooks", "_post_execution_hooks")

    def __init__(self) -> None:
        self._on_error_hooks: list[ptypes.HookSignatureType] = []
        self._pre_execution_hooks: list[ptypes.HookSignatureType] = []
        self._post_execution_hooks: list[ptypes.HookSignatureType] = []

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Length of all hooks.
        """
        return len(self._on_error_hooks + self._pre_execution_hooks + self._post_execution_hooks)

    def add_to_client(self, client: clients.ProgressbarClientAware, /) -> Hooks:
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
        if not client.hooks:
            client.set_hooks(self)
        else:
            client.update_hooks(self)

        return self

    def update(self, other: hooks.HooksAware, /) -> Hooks:
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
        self._on_error_hooks.extend(other.on_error_hooks)
        self._post_execution_hooks.extend(other.post_execution_hooks)
        self._pre_execution_hooks.extend(other.pre_execution_hooks)
        return self

    def add_pre_execution(self, callback: ptypes.HookSignatureType, /) -> Hooks:
        """Adds pre-execution callback.

        Parameters
        ----------
        callback : ptypes.HookSignatureType, /
            Pre-execution callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        self._pre_execution_hooks.append(callback)
        return self

    def add_post_execution(self, callback: ptypes.HookSignatureType, /) -> Hooks:
        """Adds post-execution callback.

        Parameters
        ----------
        callback : ptypes.HookSignatureType, /
            Post-execution callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        self._post_execution_hooks.append(callback)
        return self

    def add_on_error(self, callback: ptypes.HookSignatureType, /) -> Hooks:
        """Adds on-error callback.

        Parameters
        ----------
        callback : ptypes.HookSignatureType, /
            On-error callback.

        Returns
        -------
        Self
            The hook object to allow fluent-style.
        """
        self._on_error_hooks.append(callback)
        return self

    def trigger_post_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all post-execution callbacks.

        Parameters
        ----------
        *args : typing.Any
            Arguments to trigger.
        **kwargs : typing.Any
            Keyword arguments to trigger.

        Returns
        -------
        None
        """
        for hook in self._post_execution_hooks:
            hook(*args, **kwargs)

    def trigger_pre_execution(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all pre-execution callbacks.

        Parameters
        ----------
        *args : typing.Any
            Arguments to trigger.
        **kwargs : typing.Any
            Keyword arguments to trigger.

        Returns
        -------
        None
        """
        for hook in self._pre_execution_hooks:
            hook(*args, **kwargs)

    def trigger_on_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Triggers all on-error callbacks.

        Parameters
        ----------
        *args : typing.Any
            Arguments to trigger.
        **kwargs : typing.Any
            Keyword arguments to trigger.

        Returns
        -------
        None
        """
        if not self._on_error_hooks:
            raise

        else:
            for hook in self._on_error_hooks:
                hook(*args, **kwargs)

    @property
    def pre_execution_hooks(self) -> list[ptypes.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[ptypes.HookSignatureType]
            Sequence of pre-execution hooks.
        """
        return self._pre_execution_hooks

    @property
    def post_execution_hooks(self) -> list[ptypes.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[ptypes.HookSignatureType]
            Sequence of post-execution hooks.
        """
        return self._post_execution_hooks

    @property
    def on_error_hooks(self) -> list[ptypes.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[ptypes.HookSignatureType]
            Sequence of on-error hooks.
        """
        return self._on_error_hooks


def _progress_writer_hook(*_: typing.Any, **kwargs: typing.Any) -> None:
    FIRST_FILL: typing.Literal[3] = 3
    LAST_FILL: typing.Literal[97] = 97

    metadata = typing.cast(ptypes.ProgressMetadataType, kwargs["metadata"])
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
"""Hooks that by default __supports__ in `post-execution` hook
progressbar `start` & `end` chars."""
WRITER_HOOKS.add_post_execution(_progress_writer_hook)
