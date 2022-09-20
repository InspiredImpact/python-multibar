import dataclasses

import multibar


@dataclasses.dataclass
class MyOwnSignature:
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
assert str(writer.write(50, 100, length=6)) == "***^^^"  # ProgressbarWriter works only with `middle` value

client = multibar.ProgressbarClient(progress_writer=writer)
client.set_hooks(multibar.WRITER_HOOKS)  # This hook replaces `start` and `end` values
assert str(client.get_progress(100, 100, length=6)) == "<****>"
