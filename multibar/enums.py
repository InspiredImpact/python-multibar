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


__all__: typing.Sequence[str] = ("CallbackAs",)


@typing.final
class CallbackAs(enum.IntEnum):
    """``|int enumeration|``

    Enumeration for callback type.

    default: :class:`int` = 1
        Mean the default ProgressObject or PackArgs[callback, ProgressObject].

    callable: :class:`int` = 2
        Callable object.

    awaitable: :class:`int` = 3
        Awaitable object (asyncio.Future).
    """

    default = 1
    callable = 2
    awaitable = 3
