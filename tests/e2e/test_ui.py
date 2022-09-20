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
import dataclasses
import typing

import pytest
from hamcrest import assert_that, equal_to, instance_of
from returns.io import IO

from multibar import (
    WRITER_HOOKS,
    ContractAware,
    ContractCheck,
    Hooks,
    Progressbar,
    ProgressbarClient,
    SignatureSegment,
    errors,
    output,
)


def test_basic_ui() -> None:
    client = ProgressbarClient()

    assert_that(client.get_progress(50, 100), instance_of(Progressbar))


class TestAdvancedUI:
    def test_extended_progressbar(self) -> None:
        @dataclasses.dataclass
        class CustomSignature:
            """Signature value-object."""

            start: SignatureSegment = dataclasses.field(
                default=SignatureSegment(on_filled="<!", on_unfilled="-"),
            )
            middle: SignatureSegment = dataclasses.field(
                default=SignatureSegment(on_filled="#", on_unfilled="-"),
            )
            end: SignatureSegment = dataclasses.field(
                default=SignatureSegment(on_filled="!>", on_unfilled="-"),
            )

        client = ProgressbarClient()
        client.writer.bind_signature(CustomSignature())
        client.set_hooks(WRITER_HOOKS)

        progressbar = client.get_progress(50, 100, length=6)
        assert_that(
            str(progressbar),
            equal_to("<!##---"),
        )

    def test_custom_hooks(self) -> None:
        def _reverse_bar_hook(*_: typing.Any, **kwargs: typing.Any) -> None:
            metadata = kwargs["metadata"]
            reversed(metadata["progressbar"])

        client = ProgressbarClient()
        progress_without_hooks = client.get_progress(50, 100, length=6)

        assert_that(str(progress_without_hooks), equal_to("+++---"))

        hooks = Hooks()
        hooks.add_post_execution(_reverse_bar_hook)  # Progressbar will be added to kwargs metadata after execution
        client.set_hooks(hooks)  # We use .set_hooks() because now client hooks is empty.
        # If your state have hooks, use .update_hooks() method
        progress_with_hooks = client.get_progress(50, 100, length=6)

        assert_that(str(progress_with_hooks), equal_to("---+++"))

    def test_custom_contracts(self) -> None:
        class CustomProgressContract(ContractAware):
            """A contract that limits the length of the progressbar to 6 elements."""

            def check(self, *args: typing.Any, **kwargs: typing.Any) -> ContractCheck:
                call_metadata = typing.cast(typing.MutableMapping[typing.Any, typing.Any], kwargs.pop("metadata", {}))
                if not call_metadata:
                    return ContractCheck.terminated(
                        errors=["Needs metadata argument."],
                        metadata=call_metadata,
                    )

                if call_metadata["length"] > 6:
                    return ContractCheck.terminated(
                        errors=["Progressbar length cannot be more than 6."],
                        metadata=call_metadata,
                    )

                return ContractCheck.done(
                    metadata=call_metadata,
                )

            def render_terminated_contract(
                self,
                check: ContractCheck,
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

        # We need store contracts as constants, because .terminate() and .terminate_all()
        # methods removes object from contracts storage by object id.
        CUSTOM_PROGRESSBAR_CONTRACT_STATE = CustomProgressContract()

        client = ProgressbarClient()
        client.contract_manager.subscribe(CUSTOM_PROGRESSBAR_CONTRACT_STATE)

        with pytest.raises(errors.TerminatedContractError):
            client.get_progress(50, 100, length=6 + 1)
