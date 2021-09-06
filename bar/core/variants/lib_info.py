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


__all__: typing.Sequence[str] = ("Info",)


T = typing.TypeVar("T")


class Info(typing.Generic[T]):
    """Annotation for filtering global variables.

    Parameters:
    -----------
    value: :class:`TypeVar`
        A parameter that stores the value of a certain variable.

    Features:
    ---------
    * `__repr__`: repr(Info())
        Development Information.

    * `__str__`: str(Info()) | Info()
        Will output the value that stores value.
    """

    def __init__(self, value: T) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Info(value={self.value})"

    def __str__(self) -> str:
        return str(self.value)
