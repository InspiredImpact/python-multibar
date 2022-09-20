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
from hamcrest import assert_that, has_length

from multibar.impl.hooks import Hooks
from tests.utils import ConsoleOutputInterceptor


class TestHooks:
    def test_trigger_all_hook_callbacks(self) -> None:
        hooks = Hooks()

        # Hooks-add part tested on tests/bdd/steps/hooks_step.py
        hooks.add_on_error(lambda *args, **kwargs: print("Hello World!"))
        hooks.add_post_execution(lambda *args, **kwargs: print("Hello World!"))
        hooks.add_pre_execution(lambda *args, **kwargs: print("Hello World!"))

        # Console output interceptor used because hooks does not return anything
        with ConsoleOutputInterceptor() as on_error_output:
            hooks.trigger_on_error()

        assert_that(on_error_output, has_length(1))

        with ConsoleOutputInterceptor() as on_pre_execution:
            hooks.trigger_pre_execution()

        assert_that(on_pre_execution, has_length(1))

        with ConsoleOutputInterceptor() as on_post_execution:
            hooks.trigger_post_execution()

        assert_that(on_post_execution, has_length(1))
