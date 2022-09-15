__all__ = ("HIKARI_LIGHTBULB_BOT",)

import hikari
import lightbulb
import multibar
from returns.unsafe import unsafe_perform_io

from examples.discord_example.hikari_lightbulb_example import events
from examples.discord_example.leveling import users
from examples.discord_example.leveling.impl.level_manager import UserLevelingManager
from examples.discord_example.leveling.impl.math_operations import MathOperations
from examples.discord_example.leveling.impl.repository import CachedJSONUserRepository
from examples.discord_example.leveling.impl.unit_of_work import JSONUserUnitOfWork

HIKARI_LIGHTBULB_BOT = lightbulb.BotApp(
    token="Your Token Here",
    prefix="//",
    banner=None,
    default_enabled_guilds=Your_Guild_ID,
)
progressbar_writer = multibar.ProgressbarWriter.from_signature(multibar.SquareEmojiSignature())
leveling_manager = UserLevelingManager(
    uow=JSONUserUnitOfWork(  # U can switch repo param value to JSONUserRepository, and it will work fine.
        json_fp="data.json", repo=CachedJSONUserRepository(json_fp="data.json")
    ),
    math=MathOperations(),
)


@HIKARI_LIGHTBULB_BOT.listen()
async def on_message_event(event: hikari.MessageCreateEvent) -> None:
    """The on-message event where we add user experience and dispatch new leveling events."""
    if event.is_bot:
        return

    with leveling_manager.uow as uow:
        user = await uow.products.get_user_by_id(event.author_id)

        if user is None:
            user = users.User.from_identifier(event.author_id)
            await uow.products.add_user(user)

        await uow.products.increase_xp_for(
            user.id,
            unsafe_perform_io(leveling_manager.random_xp()),
        )

        if leveling_manager.user_reached_next_level(user):
            await HIKARI_LIGHTBULB_BOT.dispatch(events.UserLevelUpdateEvent(app=event.app, user=user))


@HIKARI_LIGHTBULB_BOT.listen()
async def on_user_level_up_event(event: events.UserLevelUpdateEvent) -> None:
    """Event that dispatches when user level needs to be incremented."""
    event.user.lvlup()
    with leveling_manager.uow as uow:
        await uow.handle_lvlup_for(event.user.id)


@HIKARI_LIGHTBULB_BOT.command
@lightbulb.command("profile", "Displays user profile.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def profile_command(ctx: lightbulb.Context) -> None:
    field_fmt = lambda value: "```" + str(value) + "```"

    with leveling_manager.uow as uow:
        user = await uow.products.get_user_by_id(ctx.author.id)

        if user is None:
            await uow.products.add_user(users.User.from_identifier(ctx.author.id))
            await ctx.respond("Your data successfully registered. Run command again.")
            return

        needed_xp = leveling_manager.math.get_needed_experience_for(user.level)

        embed = hikari.Embed(title=f"{ctx.author.username} profile")
        embed.add_field("Your level", field_fmt(user.level), inline=True)
        embed.add_field("Your experience", field_fmt(f"{user.xp}/{needed_xp}"), inline=True)
        embed.add_field("Progress", progressbar_writer.write(user.xp, needed_xp), inline=False)

        await ctx.respond(embed=embed)
