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

from hamcrest import assert_that, equal_to, has_length, has_properties, instance_of

from multibar.api.calculation_service import AbstractCalculationService
from multibar.impl.calculation_service import ProgressbarCalculationService


def test_percentage() -> None:
    percentage = ProgressbarCalculationService.get_progress_percentage(50, 100)
    assert_that(percentage, equal_to(50.0))


def test_calculation_service() -> None:
    calc_service = ProgressbarCalculationService(50, 100, 20)
    assert_that(calc_service, instance_of(AbstractCalculationService))

    assert_that(
        calc_service,
        has_properties(
            {
                "start_value": equal_to(50),
                "end_value": equal_to(100),
                "length_value": equal_to(20),
                "progress_percents": equal_to(50.0),
            }
        ),
    )

    first_part = calc_service.calculate_filled_indexes()
    second_part = calc_service.calculate_unfilled_indexes()

    assert_that(first_part, instance_of(collections.abc.Iterator))
    assert_that(second_part, instance_of(collections.abc.Iterator))

    assert_that(list(first_part), has_length(calc_service.length_value // 2))
    assert_that(list(second_part), has_length(calc_service.length_value // 2))
