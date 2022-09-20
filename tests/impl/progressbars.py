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

__all__ = ("FakeProgressbar",)

import typing

from multibar.api import progressbars, sectors


class FakeProgressbar(progressbars.ProgressbarAware[sectors.AbstractSector]):
    def __getitem__(self, item: typing.Any) -> typing.Any:
        return None

    def add_sector(self, sector: sectors.AbstractSector, /) -> FakeProgressbar[sectors.AbstractSector]:
        return self

    def replace_visual(self, sector_pos: int, new_visual: str, /) -> FakeProgressbar[sectors.AbstractSector]:
        return self

    @property
    def length(self) -> int:
        return -1

    @property
    def storage(self) -> typing.Sequence[sectors.AbstractSector]:
        return ()
