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
"""Interfaces for progressbar signatures."""
from __future__ import annotations

__all__ = (
    "SignatureSegmentProtocol",
    "ProgressbarSignatureProtocol",
)

import typing


@typing.runtime_checkable
class SignatureSegmentProtocol(typing.Protocol):
    """Signature segment protocol (protocol for one char, that has two states).

    Examples
    --------
    ??? example "Expand example of usage"
        ```py
        >>> import dataclasses
        ...
        >>> @dataclasses.dataclass
        ... class SignatureSegment:
        ...     on_filled: str = dataclasses.field(default="+")
        ...     on_unfilled: str = dataclasses.field(default="-")
        ...
        >>> isinstance(SignatureSegment(), SignatureSegmentProtocol)
        True

        >>> def function_that_accepts_signature_segment(
        ...     segment: SignatureSegmentProtocol, /
        ... ) -> tuple[str, str]:
        ...     return segment.on_filled, segment.on_unfilled
        ...
        >>> function_that_accepts_signature_segment(SignatureSegment())  # Mypy happy :)
        ('+', '-')
        ```
    """

    @property
    def on_filled(self) -> str:
        """
        Returns
        -------
        str
            On filled state.
        """
        raise NotImplementedError

    @property
    def on_unfilled(self) -> str:
        """
        Returns
        -------
        str
            On unfilled state.
        """
        raise NotImplementedError


@typing.runtime_checkable
class ProgressbarSignatureProtocol(typing.Protocol):
    """Signature protocol.

    Examples
    --------
    ??? example "Expand example of usage"
        ```
        >>> import dataclasses
        >>> from unittest.mock import Mock  # mock for signature segment
        ...
        >>> @dataclasses.dataclass
        ... class Signature:
        ...     start: SignatureSegmentProtocol = dataclasses.field(default=Mock())
        ...     middle: SignatureSegmentProtocol = dataclasses.field(default=Mock())
        ...     end: SignatureSegmentProtocol = dataclasses.field(default=Mock())
        ...
        >>> def function_that_checks_signature(
        ...     signature: ProgressbarSignatureProtocol, /
        ... ) -> bool:
        ...     return isinstance(signature, ProgressbarSignatureProtocol)
        ...
        >>> function_that_checks_signature(Signature())  # Mypy happy :)
        True
        ```
    """

    @property
    def start(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar start char.
        """
        raise NotImplementedError

    @property
    def end(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar end char.
        """
        raise NotImplementedError

    @property
    def middle(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar middle char (between start and and).
        """
        raise NotImplementedError
