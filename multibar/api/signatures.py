__all__ = (
    "SignatureSegmentProtocol",
    "ProgressbarSignatureProtocol",
)

import typing


@typing.runtime_checkable
class SignatureSegmentProtocol(typing.Protocol):
    @property
    def on_filled(self) -> str:
        raise NotImplementedError

    @property
    def on_unfilled(self) -> str:
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
