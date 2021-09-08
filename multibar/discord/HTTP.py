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

import sys
import types
import typing
import asyncio
import aiohttp
import warnings
import dataclasses

from multibar import version_info
from multibar.discord import errors

if typing.TYPE_CHECKING:
    from multibar.discord.variants import SnowFlake


T = typing.TypeVar("T")


__all__: typing.Sequence[str] = (
    "Route",
    "DiscordHTTP",
    "DiscordWebSocketResponse",
)


if sys.platform.startswith("win"):
    """Fixing an error with an unclosed session on windows."""
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class DiscordWebSocketResponse(aiohttp.ClientWebSocketResponse):
    """``|class|``

    WebSocket response class for ClientSession.
    """

    async def close(self, *, code: int = 1000, message: bytes = b"") -> bool:
        return await super().close(code=code, message=message)


@dataclasses.dataclass()
class Route:
    """``|dataclass|``

    Router class for the basis of the request.

    Parameters:
    -----------
    method: :class:`str`
        Request method.

    endpoint: :class:`str`
        API endpoint.

    json: :class:`typing.Dict[str, typing.Any]`
        Json for API request.

    guild_id: :class:`typing.Optional[SnowFlake]`
        Guild id for API request.

    message_id: :class:`typing.Optional[SnowFlake]`
        Message id for API request.

    channel_id: :class:`typing.Optional[SnowFlake]`
        Channel id for API request.

    BASE: :class:`typing.Final[str]`
        Base API url.

    Properties:
    -----------
    url: :class:`str`
        Final url for API request.
    """

    method: str
    endpoint: str
    json: typing.Dict[str, typing.Any]
    guild_id: typing.Optional[SnowFlake] = None
    message_id: typing.Optional[SnowFlake] = None
    channel_id: typing.Optional[SnowFlake] = None
    BASE: typing.Final[str] = "https://discord.com/api/v8"

    @property
    def url(self) -> str:
        return (Route.BASE + self.endpoint).format(
            channel_id=self.channel_id,
            guild_id=self.guild_id,
            message_id=self.message_id,
        )


class DiscordHTTP:
    """``|class|``

    The main class for calling the API.

    Parameters:
    -----------
    route: :class:`Route` [Positional only]
        Basic params from route.

    token: :class:`str`
        Bot token.

    session: :class:`typing.Optional[aiohttp.ClientSession]` [Keyword only]
        Aiohttp client session.

    loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` [Keyword only]
        Asyncio loop.

    connector: :class:`typing.Optional[aiohttp.BaseConnector]` [Keyword only]
        Aiohttp connector.

    ws_response_class: :class:`typing.Type[aiohttp.ClientWebSocketResponse]` = DiscordWebSocketResponse
        [Keyword only]
        Aiohttp WebSocket response class.
    """

    def __init__(
        self,
        route: Route,
        /,
        token: str,
        *,
        session: typing.Optional[aiohttp.ClientSession] = None,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        connector: typing.Optional[aiohttp.BaseConnector] = None,
        ws_response_class: typing.Type[aiohttp.ClientWebSocketResponse] = DiscordWebSocketResponse,
    ) -> None:
        self._route = route
        self._token = token
        self._loop = loop or asyncio.get_event_loop()
        self.__session = (
            session
            if session is not None
            else (aiohttp.ClientSession(connector=connector, ws_response_class=ws_response_class))
        )

        _user_agent = (
            "DiscordBot (https://github.com/Animatea/python-multibar {0}) Python/{1[1]}.{1[0]} aiohttp/{2}"
        )
        self.headers = {
            "User-Agent": _user_agent.format(version_info(), sys.version_info, aiohttp.__version__)
        }

    async def __aenter__(self) -> typing.Any:
        return await self.make_request()

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        await self.close()

    async def make_request(self) -> typing.Any:
        self.headers.update({"Content-Type": "application/json", "Authorization": f"Bot {self._token}"})
        async with self.__session.request(
            method=self._route.method,
            url=self._route.url,
            headers=self.headers,
            json=self._route.json,
        ) as response:
            data = await response.json()
            if 300 > response.status >= 200:
                return data

            elif response.status == 429:
                warnings.warn("We are being rate limited.")

            elif response.status == 403:
                raise errors.ForbiddenError(response, data)

            elif response.status == 404:
                raise errors.NotFoundError(response, data)

            elif response.status == 500:
                raise errors.DiscordServerError(response, data)

            else:
                raise errors.HTTPError(response, data)

    async def close(self) -> typing.NoReturn:
        await self.__session.close()
