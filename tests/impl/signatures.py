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
