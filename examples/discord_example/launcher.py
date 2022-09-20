__all__ = (
    "AbstractLauncher",
    "HikariTanjunLauncher",
    "HikariLightbulbLauncher",
    "DiscordpyLauncher",
    "DisnakeLauncher",
    "main",
)

import abc
import logging

from examples.discord_example import (
    discord_py_example,
    disnake_example,
    hikari_lightbulb_example,
    hikari_tanjun_example,
)

_LOGGER = logging.getLogger(__name__)


class AbstractLauncher(abc.ABC):
    """Interface for any discord-api-wrapper-library client launch."""

    @abc.abstractmethod
    def run_app(self) -> None:
        """Runs client."""
        ...


class HikariTanjunLauncher(AbstractLauncher):
    # << inherited docstring from AbstractLauncher >>

    def run_app(self) -> None:
        # << inherited docstring from AbstractLauncher >>

        # !!! note
        #     Before using this launcher, you must specify your
        #     token in hikari_tanjun_example/bot.py
        #     (instead of "Your Token Here")

        hikari_tanjun_example.HIKARI_TANJUN_BOT.run()

        _LOGGER.info(
            "BOT %s SUCCESSFULLY LAUNCHED.",
            self.__class__.__name__,
        )


class HikariLightbulbLauncher(AbstractLauncher):
    # << inherited docstring from AbstractLauncher >>

    def run_app(self) -> None:
        # << inherited docstring from AbstractLauncher >>

        # !!! note
        #     Before using this launcher, you must specify your
        #     token in hikari_lightbulb_example/bot.py
        #     (instead of "Your Token Here")

        hikari_lightbulb_example.HIKARI_LIGHTBULB_BOT.run()

        _LOGGER.info(
            "BOT %s SUCCESSFULLY LAUNCHED.",
            self.__class__.__name__,
        )


class DisnakeLauncher(AbstractLauncher):
    # << inherited docstring from AbstractLauncher >>

    def run_app(self) -> None:
        # << inherited docstring from AbstractLauncher >>
        disnake_example.DISNAKE_BOT.run(
            token="Your Token Here",  # <------ TOKEN
        )

        _LOGGER.info(
            "BOT %s SUCCESSFULLY LAUNCHED.",
            self.__class__.__name__,
        )


class DiscordpyLauncher(AbstractLauncher):
    # << inherited docstring from AbstractLauncher >>

    def run_app(self) -> None:
        # << inherited docstring from AbstractLauncher >>
        discord_py_example.DISCORDPY_BOT.run(
            token="Your Token Here",  # <------ TOKEN
        )

        _LOGGER.info(
            "BOT %s SUCCESSFULLY LAUNCHED.",
            self.__class__.__name__,
        )


def main(launcher: AbstractLauncher, /) -> None:
    launcher.run_app()


if __name__ == "__main__":
    """You can use any implementation of AbstractLauncher.

    Examples
    --------
    >>> main(HikariTanjunLauncher())
    >>> main(HikariLightbulbLauncher())
    >>> main(DisnakeLauncher())
    >>> main(DiscordpyLauncher())
    """

    main(HikariTanjunLauncher())
