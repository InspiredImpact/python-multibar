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
from unittest.mock import Mock

from hamcrest import assert_that, has_properties, instance_of, is_, is_not

from multibar.api.writers import ProgressbarWriterAware
from multibar.impl.writers import ProgressbarWriter
from tests.pyhamcrest import subclass_of


class TestProgressbarWriter:
    def test_base(self) -> None:
        writer_state = ProgressbarWriter()

        assert_that(ProgressbarWriter, subclass_of(ProgressbarWriterAware))
        assert_that(
            writer_state,
            has_properties(
                {
                    "signature": is_not(None),
                    "sector_cls": is_not(None),
                    "progressbar_cls": is_not(None),
                    "calculation_cls": is_not(None),
                },
            ),
        )

    def test_alternative_constructors(self) -> None:
        writer_state = ProgressbarWriter.from_signature(Mock())
        assert_that(writer_state, instance_of(ProgressbarWriter))

    def test_bind_signature(self) -> ProgressbarWriter:
        writer_state = ProgressbarWriter()
        mock_signature = Mock()

        assert_that(writer_state.signature, is_not(mock_signature))

        writer_state.bind_signature(mock_signature)
        assert_that(writer_state.signature, is_(mock_signature))
