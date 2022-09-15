from __future__ import annotations

__all__ = ("Settings", "settings")

import collections.abc
import typing

SelfT = typing.TypeVar("SelfT", bound="Settings")


def _config_get_function(self: SelfT, key: str) -> typing.Any:
    if key[:2] != "__":
        return self._config[key]
    return self.__dict__[key]


class Settings:
    """Multibar global settings."""

    __getattr__ = __getitem__ = _config_get_function

    def __init__(self) -> None:
        self._config: dict[str, typing.Any] = {}

    def __contains__(self, item: typing.Any) -> bool:
        if not isinstance(item, collections.abc.Hashable):
            return item in self._config.values()
        return item in self._config

    def __copy__(self) -> Settings:
        return self.copy()

    def copy(self) -> Settings:
        new_instance = self.__class__()
        new_instance.configure(**self._config)
        return new_instance

    def configure(self, **kwargs: typing.Any) -> None:
        self._config.update(kwargs)


settings = Settings()
