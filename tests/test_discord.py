import unittest
import datetime

from multibar import discord, ProgressBar, ProgressTemplates
from multibar.discord.ext import Context, BAR, PERCENTS, IS_LEFT


class DiscordTests(unittest.TestCase):
    """``|test case|``

    All tests related to the discord in our module.
    """

    def test_embed(self) -> None:
        """ProgressEmbed testing"""

        embed = discord.ProgressEmbed(
            title="title",
            description="description",
            type="rich",
            url="https://www.google.com",
            color=0x2F3136,
            timestamp=datetime.datetime.utcnow() + datetime.timedelta(days=1),
        )
        # embed attributes
        self.assertTrue(embed.title)
        self.assertTrue(embed.description)
        self.assertTrue(embed.type)
        self.assertTrue(embed.url)
        self.assertTrue(embed.color)
        self.assertTrue(embed.timestamp)

        # Setting and removing author (this example also applies to video, provider, image).
        embed.set_author(name="Author")
        self.assertTrue(hasattr(embed, "_author"))
        embed.remove_author()
        self.assertTrue(not hasattr(embed, "_author"))

        # embed fields
        embed.add_field(name="name", value="value", inline=False)
        self.assertTrue(embed.fields)
        embed.remove_field(0)
        self.assertTrue(len(embed.fields.origin) == 0)  # (Proxy object that have `origin` attribute).

    def test_embed_with_progress_field(self) -> None:
        """ProgressField testing"""
        embed = discord.ProgressEmbed(title="hello")
        bar = ProgressBar(10, 100)
        embed.add_field(
            name="name",
            value="value",
            progress=bar.write_progress(**ProgressTemplates.ADVANCED),
        )
        self.assertTrue(embed.fields)

    def test_embed_with_manipulator(self) -> None:
        """Embed manipulator testing"""
        embed = discord.ProgressEmbed(title="title")
        embed.add_manipulator(BAR.reverse(), PERCENTS.format("{", "}"), IS_LEFT.format("{{", "}}"))
        self.assertTrue(embed.has_manipulator)

        # Manipulator attributes.
        manipulator = getattr(embed, "_has_manipulator")
        self.assertTrue(hasattr(manipulator._bar, "_reverse"))
        self.assertTrue(hasattr(manipulator._percents, "prefix"))
        self.assertTrue(hasattr(manipulator._percents, "suffix"))
        self.assertTrue(hasattr(manipulator._isleft, "prefix"))
        self.assertTrue(hasattr(manipulator._isleft, "suffix"))

    def test_context(self) -> None:
        """Context testing"""
        context = Context(
            channel_id=777077743035744226,
            author_id=337954786190295020,
            guild_id=744099317836677121,
            message_id=884105687146299542,
        )
        self.assertIsInstance(context.channel_id, int)
        self.assertIsInstance(context.author_id, int)
        self.assertIsInstance(context.guild_id, int)
        self.assertIsInstance(context.message_id, int)


if __name__ == "__main__":
    unittest.main()
