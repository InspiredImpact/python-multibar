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
        self, check: contracts.ContractCheck, /, *, raise_errors: bool,
    ) -> IO[None]:
        if raise_errors:
            raise errors.TerminatedContractError(check)

        self_module = self.__module__ + "." + self.__class__.__name__
        output.print_heading(f"{self_module} was broken.", level=1)

        output.print("Print smth errors...")

        return IO(None)


FAKE_RESTRICTED_PROGRESSBAR_CONTRACT = FakeRestrictedProgressbarContract()
