import dataclasses

import multibar


@dataclasses.dataclass
class MyOwnSignature(multibar.ProgressbarSignatureProtocol):
    start: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled="<", on_unfilled="^")
    )
    middle: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled="*", on_unfilled="^")
    )
    end: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled=">", on_unfilled="^")
    )


writer = multibar.ProgressbarWriter.from_signature(MyOwnSignature())
