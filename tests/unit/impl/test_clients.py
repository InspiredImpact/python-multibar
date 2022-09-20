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
from functools import partial

import pytest
from hamcrest import (
    assert_that,
    calling,
    greater_than,
    has_length,
    has_properties,
    instance_of,
    not_,
    raises,
)

from multibar.api.clients import ProgressbarClientAware
from multibar.api.contracts import ContractManagerAware
from multibar.api.hooks import HooksAware
from multibar.api.writers import ProgressbarWriterAware
from multibar.errors import TerminatedContractError
from multibar.impl.clients import ProgressbarClient
from tests.utils import ConsoleOutputInterceptor


class TestProgressbarClient:
    def test_base(self) -> None:
        client = ProgressbarClient()
        assert_that(client, instance_of(ProgressbarClientAware))
        assert_that(
            client,
            has_properties(
                {
                    "hooks": instance_of(HooksAware),
                    "writer": instance_of(ProgressbarWriterAware),
                    "contract_manager": instance_of(ContractManagerAware),
                }
            ),
        )

    def test_base_contracts(self) -> None:
        client = ProgressbarClient()

        with pytest.raises(TerminatedContractError):
            client.get_progress(100, 50)

        client.contract_manager.set_raise_errors(False)
        with ConsoleOutputInterceptor() as output_warnings:
            assert_that(calling(partial(client.get_progress, 100, 50)), not_(raises(TerminatedContractError)))

        assert_that(output_warnings, has_length(greater_than(0)))
