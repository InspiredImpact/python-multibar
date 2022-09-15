__all__ = ("DISCORDPY_BOT",)

import typing

import discord
from discord.ext import commands
import multibar
from returns.unsafe import unsafe_perform_io

from examples.discord_example.disnake_example import events
from examples.discord_example.leveling import users
from examples.discord_example.leveling.impl.level_manager import UserLevelingManager
from examples.discord_example.leveling.impl.math_operations import MathOperations
from examples.discord_example.leveling.impl.repository import CachedJSONUserRepository
from examples.discord_example.leveling.impl.unit_of_work import JSONUserUnitOfWork

progressbar_writer = multibar.ProgressbarWriter.from_signature(multibar.SquareEmojiSignature())
leveling_manager = UserLevelingManager(
    uow=JSONUserUnitOfWork(  # U can switch repo param value to JSONUserRepository, and it will work fine.
        json_fp="data.json", repo=CachedJSONUserRepository(json_fp="data.json")
    ),
    math=MathOperations(),
)


class DiscordpyBot(commands.Bot):
    def __init__(
        self,
        *args: typing.Any,
        testing_guild_id: typing.Optional[int] = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id

    async def setup_hook(self) -> None:
        if self.testing_guild_id is not None:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)


DISCORDPY_BOT = DiscordpyBot(
    intents=discord.Intents.default(),
    command_prefix="//",
    testing_guild_id=Your_Guild_ID,
)


@DISCORDPY_BOT.listen("on_message")
async def on_message_event(message: discord.Message) -> None:
    """The on-message event where we add user experience and dispatch new leveling events."""
    if message.author.bot:
        return

    with leveling_manager.uow as uow:
        user = await uow.products.get_user_by_id(message.author.id)

        if user is None:
            user = users.User.from_identifier(message.author.id)
            await uow.products.add_user(user)

        await uow.products.increase_xp_for(
            user.id,
            unsafe_perform_io(leveling_manager.random_xp()),
        )

        if leveling_manager.user_reached_next_level(user):
            DISCORDPY_BOT.dispatch(
                "user_level_up_event",
                events.UserLevelUpdateEvent(user),
            )


@DISCORDPY_BOT.event
async def on_user_level_up_event(event: events.UserLevelUpdateEvent) -> None:
    """Event that dispatches when user level needs to be incremented."""
    event.user.lvlup()
    with leveling_manager.uow as uow:
        await uow.handle_lvlup_for(event.user.id)


@DISCORDPY_BOT.tree.command(name="profile", description="Displays user profile.")
async def profile_command(inter: discord.Interaction) -> None:
    field_fmt = lambda value: "```" + str(value) + "```"

    with leveling_manager.uow as uow:
        user = await uow.products.get_user_by_id(inter.user.id)

        if user is None:
            await uow.products.add_user(users.User.from_identifier(inter.user.id))
            await inter.response.send_message("Your data successfully registered. Run command again.")
            return

        needed_xp = leveling_manager.math.get_needed_experience_for(user.level)

        embed = discord.Embed(title=f"{inter.user.display_name} profile")
        embed.add_field(name="Your level", value=field_fmt(user.level), inline=True)
        embed.add_field(name="Your experience", value=field_fmt(f"{user.xp}/{needed_xp}"), inline=True)
        embed.add_field(name="Progress", value=progressbar_writer.write(user.xp, needed_xp), inline=False)

        await inter.response.send_message(embed=embed)
