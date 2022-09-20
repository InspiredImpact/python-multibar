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
""" """
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
