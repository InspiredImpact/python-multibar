__all__ = (
    "SignatureSegmentProtocol",
    "ProgressbarSignatureProtocol",
)

import typing


@typing.runtime_checkable
class SignatureSegmentProtocol(typing.Protocol):
    @property
    def on_filled(self) -> typing.Union[str, bytes]:
        # TODO: mypy has some problems with typing.AnyStr
        raise NotImplementedError

    @property
    def on_unfilled(self) -> typing.Union[str, bytes]:
        raise NotImplementedError


@typing.runtime_checkable
class ProgressbarSignatureProtocol(typing.Protocol):
    @property
    def start(self) -> SignatureSegmentProtocol:
        raise NotImplementedError

    @property
    def end(self) -> SignatureSegmentProtocol:
        raise NotImplementedError

    @property
    def middle(self) -> SignatureSegmentProtocol:
        raise NotImplementedError
