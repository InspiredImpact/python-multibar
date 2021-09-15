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
    """``typed dict``

    line: :class:`str`
        Line emoji of music bar.

    current: :class:`str`
        Emoji that will be set to the current progress position.
    """

    line: str
    current: str


class CharsDefault(typing.TypedDict):
    """``typed dict``

    fill :class:`str`
        Fill emoji of progress bar.

    line: :class:`str`
        Line emoji of progress bar.
    """

    fill: str
    line: str


class CharsAdvanced(CharsDefault, total=False):
    """``typed dict``

    start: :class:`str`
        Start emoji of progress bar.

    unfilled_start: :class:`str`
        Unfilled_start emoji of progress bar.

    end: :class:`str`
        End emoji of progress bar.

    unfilled_end: :class:`str`
        Unfilled_end emoji of progress bar.
    """

    start: str
    unfilled_start: str
    end: str
    unfilled_end: str


CharsSnowflake = typing.Union[CharsDefault, CharsAdvanced]
