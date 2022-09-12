__all__ = ("Signature", "SignatureSegment",)

import dataclasses
import typing


@dataclasses.dataclass
class SignatureSegment:
    on_filled: typing.AnyStr
    on_unfilled: typing.AnyStr


@dataclasses.dataclass
class Signature:
    start: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="<", on_unfilled="o"))
    end: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled=">", on_unfilled="o"))
    middle: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="+", on_unfilled="o"))
