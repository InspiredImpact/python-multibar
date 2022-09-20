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

__all__ = ("FakeSector",)

import typing

from multibar.api import sectors

if typing.TYPE_CHECKING:
    from multibar.api import progressbars


class FakeSector(sectors.AbstractSector):
    def add_to_progressbar(self, progressbar: progressbars.ProgressbarAware[FakeSector], /) -> FakeSector:
        return self

    def change_name(self, value: str, /) -> FakeSector:
        return self

    @property
    def name(self) -> str:
        return ""

    @property
    def is_filled(self) -> bool:
        return False

    @property
    def position(self) -> int:
        return -1
