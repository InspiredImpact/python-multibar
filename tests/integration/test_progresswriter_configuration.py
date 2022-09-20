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
from hamcrest import assert_that, instance_of

from multibar.impl.calculation_service import ProgressbarCalculationService
from multibar.impl.progressbars import Progressbar
from multibar.impl.sectors import Sector
from multibar.impl.signatures import SimpleSignature
from multibar.impl.writers import ProgressbarWriter
from tests.impl.calculation_service import FakeCalculationService
from tests.impl.progressbars import FakeProgressbar
from tests.impl.sectors import FakeSector
from tests.impl.signatures import FakeSignature
from tests.pyhamcrest import subclass_of


class TestProgressWriterConfiguration:
    def test_base(self) -> None:
        default_writer_state = ProgressbarWriter()

        # ProgressWriter base tested on tests/unit/impl/progressbars.py
        assert_that(default_writer_state.sector_cls, subclass_of(Sector))
        assert_that(default_writer_state.calculation_cls, subclass_of(ProgressbarCalculationService))
        assert_that(default_writer_state.signature, instance_of(SimpleSignature))

        # Setting new configuration
        custom_writer_state = ProgressbarWriter(
            sector_cls=FakeSector,
            progressbar_cls=FakeProgressbar,
            signature=FakeSignature(),
            calculation_service=FakeCalculationService,
        )

        assert_that(custom_writer_state.progressbar_cls, subclass_of(FakeProgressbar))
        assert_that(custom_writer_state.sector_cls, subclass_of(FakeSector))
        assert_that(custom_writer_state.calculation_cls, subclass_of(FakeCalculationService))
        assert_that(custom_writer_state.signature, instance_of(FakeSignature))

    def test_write_progress(self) -> None:
        writer_state = ProgressbarWriter()
        progressbar = writer_state.write(50, 100)

        assert_that(progressbar, instance_of(Progressbar))
