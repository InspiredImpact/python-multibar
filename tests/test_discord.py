import unittest

from multibar import discord, ProgressBar, ProgressBlanks
from multibar.discord.ext import Context, BAR, PERCENTS, IS_LEFT


class DiscordTests(unittest.TestCase):
    def test_embed(self) -> None:
        embed = discord.ProgressEmbed(
            title="title",
            description="description",
            type="rich",
            url="https://www.google.com",
            color=0x2F3136,
        )
        self.assertTrue(embed.title)
        self.assertTrue(embed.description)
        self.assertTrue(embed.type)
        self.assertTrue(embed.url)
        self.assertTrue(embed.color)

    def test_embed_with_progress_field(self) -> None:
        embed = discord.ProgressEmbed(title="hello")
        bar = ProgressBar(10, 100)
        embed.add_field(
            name="name",
            value="value",
            progress=bar.write_progress(**ProgressBlanks.ADVANCED),
        )
        self.assertTrue(embed.fields)

    def test_embed_with_manipulator(self) -> None:
        embed = discord.ProgressEmbed(title="title")
        embed.add_manipulator(BAR.reverse(), PERCENTS.format("{", "}"), IS_LEFT.format("{{", "}}"))
        self.assertTrue(hasattr(embed, "_has_manipulator"))
        manipulator = getattr(embed, "_has_manipulator")
        self.assertTrue(hasattr(manipulator._bar, "_reverse"))
        self.assertTrue(hasattr(manipulator._percents, "prefix"))
        self.assertTrue(hasattr(manipulator._percents, "suffix"))
        self.assertTrue(hasattr(manipulator._isleft, "prefix"))
        self.assertTrue(hasattr(manipulator._isleft, "suffix"))

    def test_context(self) -> None:
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
