__all__ = ["DISCORD_EMOJI_REGEX"]

import re

DISCORD_EMOJI_REGEX = re.compile(r"\w|\W[a-zA-Z]+:\d+")
