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
import typing

from behave import use_fixture


def use_fixture_by_tag(
    tag: str,
    context: typing.Any,
    fixture_registry: typing.MutableMapping[typing.Hashable, typing.Callable[..., typing.Any]],
) -> typing.Any:
    fixture_data = fixture_registry.get(tag, None)
    if fixture_data is None:
        raise LookupError(f"Unknown fixture-tag: {tag}")

    fixture_func = fixture_data
    return use_fixture(fixture_func, context)
