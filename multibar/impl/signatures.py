__all__ = (
    "SimpleSignature",
    "SignatureSegment",
)

import dataclasses


@dataclasses.dataclass
class SignatureSegment:
    on_filled: str
    on_unfilled: str


@dataclasses.dataclass
class SimpleSignature:
    start: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="<", on_unfilled="-"))
    end: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled=">", on_unfilled="-"))
    middle: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="+", on_unfilled="-"))
