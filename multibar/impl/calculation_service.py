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
"""Implementations of Python-Multibar math operations."""
from __future__ import annotations

__all__ = ("ProgressbarCalculationService",)

import collections.abc
import typing

from multibar.api import calculation_service


class ProgressbarCalculationService(calculation_service.AbstractCalculationService):
    """Implementation of calculation_service.AbstractCalculationService.

    !!! note
        Documentation duplicated for mkdocs auto-reference
        plugin.
    """

    def calculate_filled_indexes(self) -> collections.abc.Iterator[int]:
        """Returns iterator over progressbar filled sector indexes.
        This method is implemented for a more comfortable calculation
        of the position of the sector in the progress bar.

        Returns
        -------
        collections.abc.Iterator[int]
            Iterator over progressbar filled sector indexes.
        """
        filled_range = range(round(self.progress_percents / (100 / self._length)))
        return iter(filled_range)

    def calculate_unfilled_indexes(self) -> collections.abc.Iterator[int]:
        """Returns iterator over progressbar unfilled sector indexes.
        This method is implemented for a more comfortable calculation
        of the position of the sector in the progress bar.

        Returns
        -------
        collections.abc.Iterator[int]
            Iterator over progressbar unfilled sector indexes.
        """
        filled_range_len = len(tuple(self.calculate_filled_indexes()))
        unfilled_range = range(self._length - filled_range_len)
        return map(lambda i: i + filled_range_len, unfilled_range)

    @staticmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        """Alternative staticmethod to get progress percentage.

        Parameters
        -----------
        start : typing.Union[int, float]
            Start value (current progress) for progressbar math operations.
        end : typing.Union[int, float]
            End value (needed progress) for progressbar math operations.
        """
        return (start / end) * 100

    @property
    def progress_percents(self) -> float:
        """Returns current progress percentage.

        Returns
        -------
        float
            Float progress percentage.
        """
        return self.get_progress_percentage(self._start_value, self._end_value)
