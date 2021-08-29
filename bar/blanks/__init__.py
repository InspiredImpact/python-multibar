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

from __future__ import annotations

import os
import json
import typing
import contextlib

if typing.TYPE_CHECKING:
    from bar.core.variants import CharsDefault, CharsAdvanced


__all__: typing.Sequence[str] = (
    'ProgressBlanks',
    'DiscordBlanks',
)


with open(os.getcwd() + '/bar/blanks/blanks.json', 'r', encoding='utf-8') as file:
    all_templates = json.load(file)


class BlanksMeta(type):
    """

    soon.

    """

    def __new__(
        mcs: typing.Type[BlanksMeta],
        name: str,
        bases: typing.Tuple[type, ...],
        attrs: typing.Dict[str, typing.Any],
    ) -> type:
        with contextlib.suppress(KeyError):
            for attr in attrs['__annotations__']:
                attrs[attr] = all_templates[name][attr]
        return super().__new__(mcs, name, bases, attrs)


class ProgressBlanks(metaclass=BlanksMeta):
    ADVANCED: CharsAdvanced
    DEFAULT: CharsDefault


class DiscordBlanks(metaclass=BlanksMeta):
    ...
