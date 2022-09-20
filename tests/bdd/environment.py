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

import parse
from behave import register_type
from behave.fixture import fixture, use_fixture_by_tag

from multibar.impl.hooks import Hooks


@parse.with_pattern(r"(?i)true|false")
def parse_boolean(text: str) -> bool:
    return text.lower() == "true"


@fixture()
def config_emulation_fixture(context: typing.Any) -> typing.Iterator[str]:
    context.hooks = hooks = Hooks()
    yield hooks


fixture_registry: typing.MutableMapping[str, typing.Callable[[typing.Any], typing.Any]] = {
    "fixture.multibar.impl.hooks": config_emulation_fixture,
}


def before_tag(context: typing.Any, tag: str) -> typing.Any:
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)


register_type(Boolean=parse_boolean)
