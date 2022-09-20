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
"""Interfaces for progressbar clients."""
from __future__ import annotations

__all__ = ("ProgressbarClientAware",)

import abc
import typing

from multibar.api import progressbars, sectors, writers

from . import contracts
from . import hooks as hooks_


class ProgressbarClientAware(abc.ABC):
    """Interface for implementing a progress client that adds new features."""

    __slots__ = ()

    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    @typing.overload
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        ...

    @abc.abstractmethod
    def get_progress(
        self,
        start_value: int,
        end_value: int,
        /,
        *,
        length: int = 20,
    ) -> progressbars.ProgressbarAware[sectors.AbstractSector]:
        """Generates a progressbar, can be a wrapper for ProgressWriterAware.write()
        to implement hooks and various kinds of checks.

        Parameters
        ----------
        start_value : int, /
            Start value (current progress) for progressbar math operations.
        end_value : int, /
            End value (needed progress) for progressbar math operations.
        length : int = 20, *
            Length of progressbar for progressbar math operations.

        Returns
        -------
        progressbars.ProgressbarAware[sectors.AbstractSector]
            Progressbar instance.
        """
        ...

    @abc.abstractmethod
    def set_hooks(self, hooks: hooks_.HooksAware, /) -> ProgressbarClientAware:
        """Sets hooks to the client.

        Parameters
        ----------
        hooks : hooks_.HooksAware
            Any hooks to set.

        Returns
        -------
        Self
            ProgressbarClient object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def update_hooks(self, hooks: hooks_.HooksAware, /) -> ProgressbarClientAware:
        """Updates hooks for the client.

        Parameters
        ----------
        hooks : hooks_.HooksAware
            Any hooks to update.

        Returns
        -------
        Self
            ProgressbarClient object to allow fluent-style.
        """
        ...

    @property
    @abc.abstractmethod
    def hooks(self) -> hooks_.HooksAware:
        """
        Returns
        -------
        hooks_.HooksAware
            Client hooks.
        """
        ...

    @property
    @abc.abstractmethod
    def contract_manager(self) -> contracts.ContractManagerAware:
        """
        Returns
        -------
        contracts.ContractManagerAware
            Client contract manager for checks.
        """
        ...

    @property
    @abc.abstractmethod
    def writer(self) -> writers.ProgressbarWriterAware:
        """
        Returns
        -------
        writers.ProgressbarWriterAware[sectors.AbstractSector]
            Progressbar writer for progress generating.
        """
        ...
