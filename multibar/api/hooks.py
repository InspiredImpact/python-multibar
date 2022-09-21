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
"""Interfaces for progressbar hooks."""
from __future__ import annotations

__all__ = ("HooksAware",)

import abc
import collections.abc
import typing

if typing.TYPE_CHECKING:
    from multibar import types

    from . import clients


class HooksAware(abc.ABC):
    """Interface to progress hooks implementation."""

    __slots__ = ()

    @abc.abstractmethod
    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Length of all hooks.
        """
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
    def add_pre_execution(self, callback: types.HookSignatureType, /) -> HooksAware:
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
    def add_post_execution(self, callback: types.HookSignatureType, /) -> HooksAware:
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
    def add_on_error(self, callback: types.HookSignatureType, /) -> HooksAware:
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
        ...

    @abc.abstractmethod
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
        ...

    @abc.abstractmethod
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
        ...

    @property
    @abc.abstractmethod
    def pre_execution_hooks(self) -> collections.abc.Sequence[types.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of pre-execution hooks.
        """
        ...

    @property
    @abc.abstractmethod
    def post_execution_hooks(self) -> collections.abc.Sequence[types.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of post-execution hooks.
        """
        ...

    @property
    @abc.abstractmethod
    def on_error_hooks(self) -> collections.abc.Sequence[types.HookSignatureType]:
        """
        Returns
        -------
        collections.abc.Sequence[HookSignatureType]
            Sequence of on-error hooks.
        """
        ...
