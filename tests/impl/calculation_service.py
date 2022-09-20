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
import collections.abc
import typing

__all__ = ("FakeCalculationService",)

from multibar.api import calculation_service


class FakeCalculationService(calculation_service.AbstractCalculationService):
    def calculate_filled_indexes(self) -> collections.abc.Iterator[int]:
        return iter(())

    def calculate_unfilled_indexes(self) -> collections.abc.Iterator[int]:
        return iter(())

    @property
    def progressbar_length(self) -> int:
        return -1

    @property
    def progress_percents(self) -> float:
        return float("NaN")

    @staticmethod
    def get_progress_percentage(start: typing.Union[int, float], end: typing.Union[int, float], /) -> float:
        return float("NaN")
