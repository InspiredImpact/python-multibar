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

import abc
import typing


__all__: typing.Sequence[str] = ("EmbedABC",)


class EmbedABC(abc.ABC):
    """``|abc class|``

    The main abstract class for embed and its parameters.

    Abstract methods:
    -----------------
    _source_: :class:`typing.Dict[str, typing.Any]`
        Method that returns the source code of the embed or
        its parameter in json format for API request.
    """

    @abc.abstractmethod
    def _source_(self) -> typing.Any:
        ...
