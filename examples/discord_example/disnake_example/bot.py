__all__ = ("DISNAKE_BOT",)

import disnake
from disnake.ext import commands
from returns.unsafe import unsafe_perform_io

import multibar
from examples.discord_example.disnake_example import events
from examples.discord_example.leveling import users
from examples.discord_example.leveling.impl.level_manager import UserLevelingManager
from examples.discord_example.leveling.impl.math_operations import MathOperations
from examples.discord_example.leveling.impl.repository import CachedJSONUserRepository
from examples.discord_example.leveling.impl.unit_of_work import JSONUserUnitOfWork

DISNAKE_BOT = commands.InteractionBot(
    test_guilds=[Your_Guild_ID],
    prefix="//",
)
progressbar_writer = multibar.ProgressbarWriter.from_signature(multibar.SquareEmojiSignature())
leveling_manager = UserLevelingManager(
    uow=JSONUserUnitOfWork(  # U can switch repo param value to JSONUserRepository, and it will work fine.
        json_fp="data.json", repo=CachedJSONUserRepository(json_fp="data.json")
    ),
    math=MathOperations(),
)


@DISNAKE_BOT.listen("on_message")
async def on_message_event(message: disnake.Message) -> None:
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
            DISNAKE_BOT.dispatch(
                "user_level_up_event",
                events.UserLevelUpdateEvent(user),
            )


@DISNAKE_BOT.event
async def on_user_level_up_event(event: events.UserLevelUpdateEvent) -> None:
    """Event that dispatches when user level needs to be incremented."""
    event.user.lvlup()  # For cache
    with leveling_manager.uow as uow:
        await uow.handle_lvlup_for(event.user.id)


@DISNAKE_BOT.slash_command(name="profile", description="Displays user profile.")
async def profile_command(inter: disnake.ApplicationCommandInteraction) -> None:
    field_fmt = lambda value: "```" + str(value) + "```"

    with leveling_manager.uow as uow:
        user = await uow.products.get_user_by_id(inter.author.id)

        if user is None:
            await uow.products.add_user(users.User.from_identifier(inter.author.id))
            await inter.send("Your data successfully registered. Run command again.")
            return

        needed_xp = leveling_manager.math.get_needed_experience_for(user.level)

        embed = disnake.Embed(title=f"{inter.author.display_name} profile")
        embed.add_field("Your level", field_fmt(user.level), inline=True)
        embed.add_field("Your experience", field_fmt(f"{user.xp}/{needed_xp}"), inline=True)
        embed.add_field("Progress", progressbar_writer.write(user.xp, needed_xp), inline=False)

        await inter.send(embed=embed)
