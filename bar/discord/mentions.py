from __future__ import annotations

import typing
import dataclasses


__all__: typing.Sequence[str] = (
    'AllowedMentions',
)


@dataclasses.dataclass()
class AllowedMentions:
    """ ``|dataclass|``

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
        """ ``|staticmethod|``

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
        data: typing.Dict[str, typing.Any] = {'parse': []}
        for k, v in cls.__dict__.items():
            if v:
                data['parse'].append(k)
        return data

    @classmethod
    def none(cls) -> AllowedMentions:
        """ ``|classmethod|``

        Template for AllowedMentions, which prohibits all mentions.

        Returns:
        --------
        :class:`AllowedMentions`
        """
        return cls()

    @classmethod
    def all(cls) -> AllowedMentions:
        """ ``|classmethod|``

        Template for AllowedMentions, which allows all mentions.

        Returns:
        --------
        :class:`AllowedMentions`
        """
        return cls(users=True, roles=True, everyone=True)

