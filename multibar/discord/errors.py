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

from multibar.core.errors import ProgressError

if typing.TYPE_CHECKING:
    from aiohttp import ClientResponse


__all__: typing.Sequence[str] = (
    "DiscordError",
    "HTTPError",
    "DiscordServerError",
    "ForbiddenError",
    "NotFoundError",
    "MissingRequiredArgument",
    "ManipulatorIsAlreadyExistsError",
    "UnexpectedArgumentError",
)


""" ``|Exception hierarchy|``

ProgressError:
    DiscordError:
        MissingRequiredArgument
        ManipulatorIsAlreadyExistsError
        UnexpectedArgumentError

        HTTPError:
            DiscordServerError
            NotFoundError
            ForbiddenError
"""


class DiscordError(ProgressError):
    """``|exception|``

    Base exception for discord section.
    """


class MissingRequiredArgument(DiscordError):
    """``|exception|``

    Raised when a required argument of something is not specified.

    Parameters:
    -----------
    argument: :class:`typing.Any`
        Argument that missing.
    """

    def __init__(self, argument: typing.Any) -> None:
        super().__init__(f"Missing required argument: {argument}")


class ManipulatorIsAlreadyExistsError(DiscordError):
    """``|exception|``

    Raised when trying to add an embed manipulator a second time.
    """

    def __init__(self) -> None:
        super().__init__("The manipulator is already installed on this embed.")


class UnexpectedArgumentError(DiscordError):
    """``|exception|``

    Raised when an unexpected argument is received.

    Parameters:
    -----------
    argument: :class:`typing.Any`
        Unexpected argument.

    expected: :class:`typing.Optional[str]` = None
        Argument that was expected.
    """

    def __init__(self, argument: typing.Any, expected: typing.Optional[str] = None) -> None:
        msg = f"Argument {argument} was never expected. "
        if isinstance(expected, str):
            msg += f"Expected {expected}"
        super().__init__(msg)


class HTTPError(DiscordError):
    """``|exception|``

    Basic error for all API related exceptions.

    Parameters:
    -----------
    response: :class:`ClientResponse`
        Received response.

    message: :class:`typing.Union[str, dict]`
        Received message.
    """

    def __init__(
        self,
        response: ClientResponse,
        message: typing.Union[str, typing.Dict[str, typing.Any]],
    ) -> None:
        super().__init__(f"Status: {response.status}.\nResponse: {response}\nMessage: {message}")


class DiscordServerError(HTTPError):
    """``|exception|``

    Raised when a 500 range status code occurs.
    """


class NotFoundError(HTTPError):
    """``|exception|``

    Raised for when status code 404 occurs.
    """


class ForbiddenError(HTTPError):
    """``|exception|``

    Raised for when status code 403 occurs.
    """
