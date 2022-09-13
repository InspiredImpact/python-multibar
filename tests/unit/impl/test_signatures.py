from unittest.mock import Mock

from hamcrest import assert_that, instance_of

from multibar.api.signatures import (
    ProgressbarSignatureProtocol,
    SignatureSegmentProtocol,
)
from multibar.impl.signatures import SignatureSegment, SimpleSignature


class TestSignatures:
    def test_signature_segment_base(self) -> None:
        assert_that(SignatureSegment(Mock(), Mock()), instance_of(SignatureSegmentProtocol))

    def test_simple_signature_base(self) -> None:
        assert_that(SimpleSignature(Mock(), Mock(), Mock()), instance_of(ProgressbarSignatureProtocol))
