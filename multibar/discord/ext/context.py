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
import dataclasses

from multibar.discord.variants import SnowFlake


__all__: typing.Sequence[str] = ("Context",)


@dataclasses.dataclass()
class Context:
    """``|dataclass|``

    Current context.

    Parameters:
    -----------
    channel_id: :class:`typing.Optional[SnowFlake]` = None
        Channel id from context.

    author_id: :class:`typing.Optional[SnowFlake]` = None
        Author id from context.

    message_id: :class:`typing.Optional[SnowFlake]` = None
        Message id from context.

    guild_id: :class:`typing.Optional[SnowFlake]` = None
        Guild id from context.
    """

    channel_id: typing.Optional[SnowFlake] = None
    author_id: typing.Optional[SnowFlake] = None
    message_id: typing.Optional[SnowFlake] = None
    guild_id: typing.Optional[SnowFlake] = None
