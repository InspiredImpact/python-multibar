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
__all__ = (
    "FakeRestrictedProgressbarContract",
    "FAKE_RESTRICTED_PROGRESSBAR_CONTRACT",
)

import typing

from returns.io import IO

from multibar import errors, output
from multibar.api import contracts


class FakeRestrictedProgressbarContract(contracts.ContractAware):
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> contracts.ContractCheck:
        call_metadata = typing.cast(typing.MutableMapping[typing.Any, typing.Any], kwargs.pop("metadata", {}))
        if not call_metadata:
            return contracts.ContractCheck.terminated(
                errors=["Needs metadata argument."],
                metadata=call_metadata,
            )

        if call_metadata["length"] > 20:
            return contracts.ContractCheck.terminated(
                errors=["Progressbar length cannot be more than 20."],
                metadata=call_metadata,
            )

        return contracts.ContractCheck.done(
            metadata=call_metadata,
        )

    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: bool,
    ) -> IO[None]:
        if raise_errors:
            raise errors.TerminatedContractError(check)

        self_module = self.__module__ + "." + self.__class__.__name__
        output.print_heading(f"{self_module} was broken.", level=1)

        output.print("Print smth errors...")

        return IO(None)


FAKE_RESTRICTED_PROGRESSBAR_CONTRACT = FakeRestrictedProgressbarContract()
