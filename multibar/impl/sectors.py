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
"""Implementation of progressbar sector interfaces."""
from __future__ import annotations

__all__ = ("Sector",)

import typing

from multibar.api import sectors

if typing.TYPE_CHECKING:
    from multibar.api import progressbars


class Sector(sectors.AbstractSector):
    """Implementation of sectors.AbstractSector.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    def add_to_progressbar(self: Sector, progressbar: progressbars.ProgressbarAware[Sector], /) -> Sector:
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
        progressbar.add_sector(self)
        return self

    def change_name(self, new_display_name: str, /) -> Sector:
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
        self._name = new_display_name
        return self

    @property
    def name(self) -> str:
        """
        Returns
        -------
        str
            Sector display name.
        """
        return self._name

    @property
    def is_filled(self) -> bool:
        """
        Returns
        -------
        str
            Sector filled value.
        """
        return self._is_filled

    @property
    def position(self) -> int:
        """
        Returns
        -------
        str
            Sector position in the progressbar.
        """
        return self._position
