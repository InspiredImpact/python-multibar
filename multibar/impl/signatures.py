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
"""Python-Multibar signature implementations."""
from __future__ import annotations

__all__ = (
    "SimpleSignature",
    "SignatureSegment",
    "SquareEmojiSignature",
)

import dataclasses


@dataclasses.dataclass
class SignatureSegment:
    """Dataclass that stores segment data."""

    on_filled: str
    """On filled state."""

    on_unfilled: str
    """On unfilled state."""


@dataclasses.dataclass
class SimpleSignature:
    """Dataclass that stores simple signature data."""

    start: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="<", on_unfilled="-"))
    """Progressbar start char."""

    end: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled=">", on_unfilled="-"))
    """Progressbar end char."""

    middle: SignatureSegment = dataclasses.field(default=SignatureSegment(on_filled="+", on_unfilled="-"))
    """Progressbar middle char (between start and and)."""


@dataclasses.dataclass
class SquareEmojiSignature:
    """Dataclass that stores square emoji signature data."""

    start: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":small_orange_diamond:", on_unfilled=":black_large_square:")
    )
    """Progressbar start char."""

    end: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":small_orange_diamond:", on_unfilled=":black_large_square:")
    )
    """Progressbar end char.""" """"""

    middle: SignatureSegment = dataclasses.field(
        default=SignatureSegment(on_filled=":orange_square:", on_unfilled=":black_large_square:")
    )
    """Progressbar middle char (between start and and)."""
