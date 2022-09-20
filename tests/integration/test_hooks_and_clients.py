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
from hamcrest import assert_that, equal_to

from multibar.impl.clients import ProgressbarClient
from multibar.impl.hooks import WRITER_HOOKS
from multibar.impl.signatures import SimpleSignature

SIG = SimpleSignature()  # Default signature


def test_progress_writer_hook() -> None:
    client = ProgressbarClient()
    client.set_hooks(WRITER_HOOKS)

    progressbar = client.get_progress(50, 100, length=6)

    # Filled progressbar part
    assert_that(progressbar[0].name, equal_to(SIG.start.on_filled))
    assert_that(progressbar[1].name, equal_to(SIG.middle.on_filled))
    assert_that(progressbar[2].name, equal_to(SIG.middle.on_filled))

    # Unfilled progressbar part
    assert_that(progressbar[3].name, equal_to(SIG.middle.on_unfilled))
    assert_that(progressbar[4].name, equal_to(SIG.middle.on_unfilled))
    assert_that(progressbar[5].name, equal_to(SIG.end.on_unfilled))
