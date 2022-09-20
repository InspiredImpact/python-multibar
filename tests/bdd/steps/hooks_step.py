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
from __future__ import annotations

import collections.abc
import typing

from behave import given, then, when
from hamcrest import (
    assert_that,
    equal_to,
    has_length,
    has_properties,
    has_property,
    instance_of,
)

from multibar.api.hooks import HooksAware
from multibar.impl.hooks import Hooks
from tests.pyhamcrest import subclass_of

if typing.TYPE_CHECKING:

    class _HasHooks(typing.Protocol):
        hooks: HooksAware


@given("we have a created instance of the Hooks class")
def creating_hooks_instance_step(context: typing.Any) -> None:
    # hooks = Hooks()
    # context.hooks = hooks
    assert_that(
        context,
        has_properties(
            {
                "hooks": instance_of(HooksAware),
            },
        ),
    )


@then("we are testing its basic behavior")
def base_behavior_testing_step(context: _HasHooks) -> None:
    assert_that(context.hooks, instance_of(HooksAware))
    assert_that(Hooks, subclass_of(collections.abc.Sized))  # has __len__ method

    assert_that(
        context.hooks,
        has_properties(
            {
                "pre_execution_hooks": equal_to([]),
                "post_execution_hooks": equal_to([]),
                "on_error_hooks": equal_to([]),
            },
        ),
    )


@when("we add new callbacks using the HooksAware interface")
def adding_callbacks_step(context: _HasHooks) -> None:
    context.hooks.add_post_execution(lambda *args, **kwargs: True)
    context.hooks.add_pre_execution(lambda *args, **kwargs: True)
    context.hooks.add_on_error(lambda *args, **kwargs: True)


@then("these callbacks are stored in special attributes that represent lists")
def checking_hook_callbacks_step(context: _HasHooks) -> None:
    assert_that(
        context.hooks,
        has_properties(
            {
                "pre_execution_hooks": has_length(1),
                "post_execution_hooks": has_length(1),
                "on_error_hooks": has_length(1),
            },
        ),
    )


@then("we run all the {hook} hook callbacks and compare it with scenario examples {callback:Boolean}")
def trigger_all_hook_callbacks_and_compare_results_step(context: _HasHooks, hook: str, callback: bool) -> None:
    assert_that(
        context.hooks,
        has_property(
            hook,
            instance_of(list),
        ),
    )

    for hook_callback in getattr(context.hooks, hook):
        assert_that(hook_callback(), equal_to(callback))
