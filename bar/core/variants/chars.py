"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typing


__all__: typing.Sequence[str] = (
    "CharsDefault",
    "CharsAdvanced",
    "CharsSnowflake",
    "MusicChars",
)


class MusicChars(typing.TypedDict):
    line: str
    current: str


class CharsDefault(typing.TypedDict):
    fill: str
    line: str


class CharsAdvanced(CharsDefault, total=False):
    start: str
    unfilled_start: str
    end: str
    unfilled_end: str


CharsSnowflake = typing.Union[CharsDefault, CharsAdvanced]
