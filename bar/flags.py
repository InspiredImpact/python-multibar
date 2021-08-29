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

import enum
import typing


__all__: typing.Sequence[str] = (
    'FillFlag',
    'MusicBarFlag',
)


@typing.final
class FillFlag(enum.IntFlag):
    """ ``|int flag|``

    The flag that is used to generate the progress bar.

    ClassVars:
    ----------
    # (According to the formula)

    FIRST: :class:`int` = 3
        At `three percent`, the first sector of the progress bar is filled.

    LAST: :class:`int` = 97
        At `ninety-seven percent`, the last sector of the progress bar is filled.
    """
    FIRST = 3
    LAST = 97


@typing.final
class MusicBarFlag(enum.IntFlag):
    """ ``|int flag|``

    ClassVars:
    ----------
    # (According to the formula)

    CORRECT_START: :class:`int` = 1
        Flag for correct calculation of progress.
    """
    CORRECT_START = 1
