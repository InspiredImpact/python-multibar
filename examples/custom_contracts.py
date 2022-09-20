import typing

from hamcrest import assert_that, calling, raises  # pip3 install PyHamcrest
from returns.io import impure

from multibar import WRITE_PROGRESS_CONTRACT, ProgressbarClient, errors, output
from multibar.api import contracts


class RestrictedEndValueContract(contracts.ContractAware):
    """Checks if end value (needed progress) is not bigger than 200."""

    END_VALUE_BOUND: typing.Literal[200] = 200

    def check(self, *args: typing.Any, **kwargs: typing.Any) -> contracts.ContractCheck:
        call_metadata = typing.cast(typing.MutableMapping[typing.Any, typing.Any], kwargs.pop("metadata", {}))
        if not call_metadata:
            return contracts.ContractCheck.terminated(
                errors=["Needs metadata argument."],
                metadata=call_metadata,
            )

        # For call metadata members you can check types.ProgressMetadataType or find it in docs.
        if call_metadata["end_value"] > self.END_VALUE_BOUND:
            return contracts.ContractCheck.terminated(
                errors=["Progressbar end value cannot be more than 200."],
                metadata=call_metadata,
            )

        return contracts.ContractCheck.done(
            metadata=call_metadata,
        )

    @impure
    def render_terminated_contract(
        self,
        check: contracts.ContractCheck,
        /,
        *,
        raise_errors: bool,
    ) -> typing.Any:
        if raise_errors:
            raise errors.TerminatedContractError(check)

        self_module = self.__module__ + "." + self.__class__.__name__
        output.print_heading(f"{self_module} was broken.", level=1)

        output.print_error("Progressbar end value cannot be more than 200.")


RESTRICTED_END_VALUE_CONTRACT = RestrictedEndValueContract()


client = ProgressbarClient()
client.contract_manager.terminate(WRITE_PROGRESS_CONTRACT)  # You can terminate exiting contracts.
client.contract_manager.subscribe(RESTRICTED_END_VALUE_CONTRACT)

# Raises errors.TerminatedContractError because end value (needed progress) more than 200.
assert_that(calling(client.get_progress).with_args(50, 201), raises(errors.TerminatedContractError))
