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
"""Python-Multibar project types."""
from __future__ import annotations

__all__ = ("ProgressMetadataType",)

import typing

import typing_extensions

if typing.TYPE_CHECKING:
    from multibar.api import calculation_service, progressbars, sectors, signatures


HookSignatureType: typing_extensions.TypeAlias = typing.Callable[..., typing.Optional[bool]]
"""Type for hook callable signature.

!!! info
    By default hook callable accepts `*args` and `**kwargs` parameters.
"""


class ProgressMetadataType(typing.TypedDict, total=False):
    """Progress metadata type for hooks triggering."""

    start_value: int
    """Start value (current progress)."""

    end_value: int
    """End value (needed progress)."""

    length: int
    """Length of progressbar."""

    sig: signatures.ProgressbarSignatureProtocol
    """Progressbar signature."""

    progressbar: typing.Optional[progressbars.ProgressbarAware[sectors.AbstractSector]]
    """Progressbar instance."""

    calculation_service_cls: typing.Type[calculation_service.AbstractCalculationService]
    """Math operations cls."""
