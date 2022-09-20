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
"""Interfaces for progressbar sectors."""
from __future__ import annotations

__all__ = ("AbstractSector",)

import abc
import typing

if typing.TYPE_CHECKING:
    from . import progressbars

SelfT = typing.TypeVar("SelfT", bound="AbstractSector")


class AbstractSector(abc.ABC):
    """Abstraction for sector implementations."""

    __slots__ = ("_name", "_is_filled", "_position")

    def __init__(self, name: str, is_filled: bool, position: int) -> None:
        """
        Parameters
        ----------
        name : str
            Sector display name.
        is_filled : bool
            Sector filled value.
        position : int
            Sector position in the progressbar.
        """
        self._name = name
        self._is_filled = is_filled
        self._position = position

    @abc.abstractmethod
    def add_to_progressbar(self: SelfT, progressbar: progressbars.ProgressbarAware[SelfT], /) -> SelfT:
        """Adds sector self to progressbar.

        Parameters
        ----------
        progressbar : progressbars.ProgressbarAware[SelfT], /
            Progressbar to add self for.

        Returns
        -------
        Self
            The sector object to allow fluent-style.
        """
        ...

    @abc.abstractmethod
    def change_name(self, new_display_name: str, /) -> AbstractSector:
        """Changes sector display name.

        Parameters
        ----------
        new_display_name : str, /
            New display name to set.

        Returns
        -------
        Self
            The sector object to allow fluent-style.
        """
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Returns
        -------
        str
            Sector display name.
        """
        ...

    @property
    @abc.abstractmethod
    def is_filled(self) -> bool:
        """
        Returns
        -------
        str
            Sector filled value.
        """
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        """
        Returns
        -------
        str
            Sector position in the progressbar.
        """
        ...
