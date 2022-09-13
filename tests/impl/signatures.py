from __future__ import annotations

__all__ = ("FakeSignature",)

import dataclasses
import typing
from unittest.mock import Mock

if typing.TYPE_CHECKING:
    from multibar.api.signatures import SignatureSegmentProtocol


@dataclasses.dataclass
class FakeSignature:
    start: SignatureSegmentProtocol = dataclasses.field(default=Mock())
    middle: SignatureSegmentProtocol = dataclasses.field(default=Mock())
    end: SignatureSegmentProtocol = dataclasses.field(default=Mock())
