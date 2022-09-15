__all__ = (
    "SimpleSignature",
    "SignatureSegment",
    "SquareEmojiSignature",
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


@dataclasses.dataclass
class SquareEmojiSignature:
    start: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":small_orange_diamond:", on_unfilled=":black_large_square:")
    )
    end: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":small_orange_diamond:", on_unfilled=":black_large_square:")
    )
    middle: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":orange_square:", on_unfilled=":black_large_square:")
    )
