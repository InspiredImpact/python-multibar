import re

import pytest
from hamcrest import assert_that, instance_of

from multibar.regex import DISCORD_EMOJI_REGEX
from tests_basics._tools import testlogger


@pytest.mark.usefixtures("testlogger")
def test_discord_emoji_regex() -> None:
    some_discord_emoji = "Hello <a:hi:780370639497724913>!"

    assert_that(DISCORD_EMOJI_REGEX, instance_of(re.Pattern))
    assert_that(DISCORD_EMOJI_REGEX.match(some_discord_emoji) is not None)
