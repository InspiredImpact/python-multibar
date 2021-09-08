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
import asyncio

from multibar.discord import errors, AllowedMentions
from multibar.discord.ext.context import Context
from multibar.discord.embed import ProgressEmbed
from multibar.discord.HTTP import DiscordHTTP, Route


__all__: typing.Sequence[str] = ("send",)


async def send(
    content: typing.Optional[str] = None,
    *,
    token: str,
    tts: bool = False,
    reply: bool = False,
    return_response: bool = False,
    channel_id: typing.Optional[int] = None,
    context: typing.Optional[Context] = None,
    loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    allowed_mentions: AllowedMentions = AllowedMentions.all(),
    embeds: typing.Optional[typing.List[ProgressEmbed]] = None,
) -> typing.Any:
    """``|coro|``

    Main method for sending messages in discord.

    # Quite a lot of parameters available in the API are missing,
    # if necessary, they will be added in the next versions of the library.

    Parameters:
    -----------
    content: :class:`typing.Optional[str]` = None
        Message content.

    tts: :class:`bool` = False [Keyword only]
        TTS message parameter.

    allowed_mentions: :class:`AllowedMentions` = AllowedMentions.all() [Keyword only]
        Message allowed mentions.

    channel_id: :class:`typing.Optional[int]` = None [Keyword only]
        The `channel` to send the message to. If None will search `context.channel_id`.

    context: :class:`typing.Optional[Context]` = None [Keyword only]
        Context for sending messages and `message_reference` (reply parameter).

    embeds: :class:`typing.List[ProgressEmbed]` = None [Keyword only]
        List of embeds to be send.

    token: :class:`str` [Keyword only]
        Bot token.

    loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` = None [Keyword only]
        Asyncio loop.

    return_response: :class:`bool` = False [Keyword only]
        If True, will return response of request.

    reply: :class:`bool` = False [Keyword only]
        If True, will take parameters for `message_reference` from the passed context .

    Returns:
    --------
    :class:`typing.Optional[ClientResponse]:`
        If return_response else None.

    Raises:
    -------
    :class:`errors.DiscordError`
        If len(content) > 2000.

    :class:`errors.MissingRequiredArgument`
        If `channel_id` is None and `context.channel_id` is None.
    """
    data: typing.Dict[str, typing.Any] = {"embeds": []}
    if embeds:
        for embed in embeds:
            data["embeds"].append(await embed._source_())

    data["tts"] = tts
    if content:
        if len(content) > 2000:
            raise errors.DiscordError("Length of content cannot be more than 2000 characters.")
        else:
            data["content"] = content

    data["allowed_mentions"] = AllowedMentions.as_dict(allowed_mentions)
    if reply and context is not None:
        data["message_reference"] = {
            "guild_id": context.guild_id,
            "channel_id": context.channel_id,
            "message_id": context.message_id,
        }

    loop = asyncio.get_event_loop() if loop is None else loop

    route = Route(
        "POST",
        "/channels/{channel_id}/messages",
        json=data,
        channel_id=(ch_id := context.channel_id if context else channel_id),
    )
    if ch_id is None:
        raise errors.MissingRequiredArgument("channel_id :class:`int`")

    async with DiscordHTTP(route, token, loop=loop) as resp:
        if return_response:
            return resp
