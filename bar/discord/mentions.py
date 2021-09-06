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


__all__: typing.Sequence[str] = ("AllowedMentions",)


@dataclasses.dataclass()
class AllowedMentions:
    """``|dataclass|``

    The class that defines allowed mentions in message.

    Parameters:
    -----------
    users: :class:`bool` = False
        If True, it will allow to mention users.

    roles: :class:`bool` = False
        If True, it will allow to mention roles.

    everyone: :class:`bool` = False
        If True, it will allow to mention everyone.
    """

    users: bool = False
    roles: bool = False
    everyone: bool = False

    @staticmethod
    def as_dict(cls: AllowedMentions, /) -> typing.Dict[str, typing.Any]:
        """``|staticmethod|``

        Returns the AllowedMentions object as dictionary.

        Parameters:
        -----------
        cls: :class:`AllowedMentions` [Positional only]
            Class for packing into a dictionary.

        Returns:
        --------
        data: :class:`typing.Dict[str, typing.Any]`
            AllowedMentions object as dict.
        """
        data: typing.Dict[str, typing.Any] = {"parse": []}
        for k, v in cls.__dict__.items():
            if v:
                data["parse"].append(k)
        return data

    @classmethod
    def none(cls) -> AllowedMentions:
        """``|classmethod|``

        Template for AllowedMentions, which prohibits all mentions.

        Returns:
        --------
        :class:`AllowedMentions`
        """
        return cls()

    @classmethod
    def all(cls) -> AllowedMentions:
        """``|classmethod|``

        Template for AllowedMentions, which allows all mentions.

        Returns:
        --------
        :class:`AllowedMentions`
        """
        return cls(users=True, roles=True, everyone=True)
