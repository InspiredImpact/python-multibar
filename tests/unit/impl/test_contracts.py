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
from unittest.mock import Mock

import pytest
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    greater_than,
    has_length,
    has_properties,
    instance_of,
    not_,
    raises,
)

from multibar.api.contracts import ContractAware, ContractManagerAware
from multibar.errors import TerminatedContractError, UnsignedContractError
from multibar.impl.contracts import ContractManager
from tests.impl.contracts import FAKE_RESTRICTED_PROGRESSBAR_CONTRACT
from tests.utils import ConsoleOutputInterceptor


def test_fake_restricted_progressbar_contract() -> None:
    assert_that(FAKE_RESTRICTED_PROGRESSBAR_CONTRACT, instance_of(ContractAware))


class TestContractManager:
    def test_contracts_subscribe_and_unsubscribe(self) -> None:
        contract_manager = ContractManager()
        assert_that(contract_manager, instance_of(ContractManagerAware))

        contract_mock = Mock()

        assert_that(contract_manager.contracts, has_length(0))

        contract_manager.subscribe(contract_mock)
        assert_that(contract_manager.contracts, has_length(1))

        contract_manager.terminate(contract_mock)
        assert_that(contract_manager.contracts, has_length(0))

        contract_manager.subscribe(contract_mock)
        contract_manager.terminate_all()
        assert_that(contract_manager.contracts, has_length(0))

    def test_new_contracts(self) -> None:
        contract_manager = ContractManager()
        restricted_metadata_with_error = {
            "length": 20 + 1,
        }
        contract_manager.subscribe(FAKE_RESTRICTED_PROGRESSBAR_CONTRACT)

        assert_that(
            contract_manager,
            has_properties(
                {
                    "raise_errors": equal_to(True),  # By default
                    "contracts": instance_of(list),
                }
            ),
        )

        with pytest.raises(UnsignedContractError):
            contract_manager.check_contract(Mock())

        with pytest.raises(TerminatedContractError):
            contract_manager.check_contract(
                FAKE_RESTRICTED_PROGRESSBAR_CONTRACT,
                metadata=restricted_metadata_with_error,
            )

        with pytest.raises(TerminatedContractError):
            contract_manager.check_contracts(metadata=restricted_metadata_with_error)

        contract_manager.set_raise_errors(False)
        assert_that(contract_manager.raise_errors, equal_to(False))

        with ConsoleOutputInterceptor() as output_warnings:
            assert_that(
                calling(
                    partial(
                        contract_manager.check_contract,
                        FAKE_RESTRICTED_PROGRESSBAR_CONTRACT,
                        metadata=restricted_metadata_with_error,
                    )
                ),
                not_(raises(TerminatedContractError)),
            )

        assert_that(output_warnings, has_length(greater_than(0)))
