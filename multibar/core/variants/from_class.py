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
import dataclasses

if typing.TYPE_CHECKING:
    from .chars import CharsSnowflake


__all__: typing.Sequence[str] = (
    "FromClassInstance",
    "NowParam",
    "NeededParam",
    "LengthParam",
    "DequeParam",
    "CharsParam",
    "FromClassBase",
)


IT = typing.TypeVar("IT")  # Instance type


@dataclasses.dataclass()
class NowParam:
    value: int


@dataclasses.dataclass()
class NeededParam:
    value: int


@dataclasses.dataclass()
class LengthParam:
    value: int


@dataclasses.dataclass()
class DequeParam:
    value: bool


@dataclasses.dataclass()
class CharsParam:
    value: "CharsSnowflake"


@dataclasses.dataclass()
class FromClassInstance:
    now_param: NowParam
    needed_param: NeededParam
    length_param: LengthParam
    deque_param: DequeParam
    chars_param: CharsParam


class _Chars:
    def __init__(*args: typing.Any, **kwargs: typing.Any) -> None:
        ...

    @classmethod
    def from_dict(cls, instance: IT, chars: CharsSnowflake) -> typing.Any:
        ...


@dataclasses.dataclass(init=False)
class FromClassBase:
    """``|dataclass|``

    Hint for comfortable working with the from_class
    decorator and preventing various errors from mypy.
    """

    chars: _Chars

    def now(self, instance: IT, num: int) -> None:
        ...

    def needed(self, instance: IT, num: int) -> None:
        ...

    def length(self, instance: IT, num: int) -> None:
        ...

    def deque(self, instance: IT, value: bool) -> None:
        ...
