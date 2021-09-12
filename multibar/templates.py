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

import typing
import contextlib

if typing.TYPE_CHECKING:
    from multibar.core.variants import CharsDefault, CharsAdvanced


__all__: typing.Sequence[str] = (
    "ProgressTemplates",
    "DiscordTemplates",
)


# There were too many errors with paths when opening the json file, I decided not to risk it.
_templates: typing.Dict[str, typing.Any] = {
    "ProgressTemplates": {
        "ADVANCED": {
            "fill": "█",
            "line": "●",
            "start": "◄",
            "end": "►",
            "unfilled_start": "◁",
            "unfilled_end": "▷",
        },
        "DEFAULT": {"fill": "█", "line": "●"},
    },
    "DiscordTemplates": {
        "ADVANCED": {
            "fill": ":orange_circle:",
            "line": ":white_large_square:",
            "start": ":small_orange_diamond:",
            "end": ":small_orange_diamond:",
            "unfilled_start": ":white_medium_small_square:",
            "unfilled_end": ":white_medium_small_square:",
        },
        "DEFAULT": {
            "fill": ":red_square:",
            "line": ":black_large_square:",
        }
    }
}


class TemplatesMeta(type):
    """``|metaclass|``

    The metaclass with which templates are set.
    """

    def __new__(
        mcs: typing.Type[TemplatesMeta],
        name: str,
        bases: typing.Tuple[type, ...],
        attrs: typing.Dict[str, typing.Any],
    ) -> TemplatesMeta:
        with contextlib.suppress(KeyError):
            for attr in attrs["__annotations__"]:
                attrs[attr] = _templates[name][attr]
        return super().__new__(mcs, name, bases, attrs)


class ProgressTemplates(metaclass=TemplatesMeta):
    ADVANCED: CharsAdvanced
    DEFAULT: CharsDefault


class DiscordTemplates(metaclass=TemplatesMeta):
    ADVANCED: CharsAdvanced
    DEFAULT: CharsDefault
