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

from .templates import *
from .core import *
from .inheritance import *
from ._about import *
from .tools import *
from .enums import *


__all__: typing.Sequence[str] = (
    "ProgressBar",
    "ProgressObject",
    "ProgressTemplates",
    "DiscordTemplates",
    "MusicBar",
    "version_info",
    "__version__",
    "LibraryInfo",
    "Progress",
    "ProgressTools",
    "CallbackAs",
)


def version_info() -> str:
    return ".".join((str(getattr(__version__.value, i)) for i in Version._fields))
