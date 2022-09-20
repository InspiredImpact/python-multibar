# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
