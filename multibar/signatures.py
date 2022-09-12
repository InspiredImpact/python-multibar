import dataclasses
import typing


@typing.runtime_checkable
class SignatureSegmentProtocol(typing.Protocol):
    @property
    def on_filled(self) -> typing.AnyStr:
        raise NotImplementedError

    @property
    def on_unfilled(self) -> typing.AnyStr:
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


@dataclasses.dataclass
class SignatureSegment:
    on_filled: typing.AnyStr
    on_unfilled: typing.AnyStr


@dataclasses.dataclass
class Signature:
    start: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="<", on_unfilled="o"))
    end: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled=">", on_unfilled="o"))
    middle: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="+", on_unfilled="o"))
