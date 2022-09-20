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
from unittest.mock import Mock

from hamcrest import assert_that, has_length, has_properties, instance_of

from multibar.api.progressbars import ProgressbarAware
from multibar.impl.progressbars import Progressbar
from tests.pyhamcrest import subclass_of


@typing.runtime_checkable
class SupportsGetitem(typing.Protocol):
    def __getitem__(self, item: typing.Any) -> typing.Any:
        raise NotImplementedError


@typing.runtime_checkable
class SupportsIter(typing.Protocol):
    def __iter__(self) -> typing.Iterator[typing.Any]:
        raise NotImplementedError


class TestProgressbars:
    def test_base(self) -> None:
        progressbar_state = Progressbar()

        assert_that(Progressbar, subclass_of(ProgressbarAware))
        assert_that(progressbar_state, instance_of(SupportsGetitem))

        assert_that(
            progressbar_state,
            has_properties(
                {
                    "sectors": instance_of(SupportsIter),
                    "length": instance_of(int),
                },
            ),
        )
        assert_that(type(progressbar_state.sectors), subclass_of(collections.abc.Sequence))

    def test_add_sector(self) -> None:
        progressbar = Progressbar()
        assert_that(progressbar.sectors, has_length(0))

        progressbar.add_sector(Mock())
        assert_that(progressbar.sectors, has_length(1))
