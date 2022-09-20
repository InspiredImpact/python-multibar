# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python-Multibar project settings."""
from __future__ import annotations

__all__ = ("Settings", "settings")

import collections.abc
import typing

from multibar import utils

SelfT = typing.TypeVar("SelfT", bound="Settings")
"""Self Type for Settings instance."""


def _config_get_function(self: SelfT, key: str) -> typing.Any:
    if key[:2] != "__":
        return self._config[key]
    return self.__dict__[key]


class Settings(metaclass=utils.Singleton):
    """Multibar global settings singleton.

    !!! tldr "Currently used for"
        | Option      | Type           | Default          |
        | ----------- | ---------------|----------------- |
        | `PRINTER`   | PrinterAware   | TermcolorPrinter |

    ??? example "Expand example of usage"
        ```py hl_lines="12"
        import typing

        from returns.io import IO

        from multibar import output, settings

        class MyOwnPrinter(output.PrinterAware):
            def print(self, *args: typing.Any, **kwargs: typing.Any) -> IO[None]:
                # Implementation of your [colored] printer.
                return IO(None)

        settings.settings.configure(PRINTER=MyOwnPrinter)
        ```
    """

    __getattr__ = __getitem__ = _config_get_function

    def __init__(self) -> None:
        self._config: dict[str, typing.Any] = {}

    def __contains__(self, item: typing.Any) -> bool:
        """If item is not hashable, checks for config.values(),
        otherwise config.keys()."""
        if not isinstance(item, collections.abc.Hashable):
            return item in self._config.values()
        return item in self._config

    def configure(self, **kwargs: typing.Any) -> None:
        """Updates global settings config.

        Parameters
        ----------
        **kwargs : typing.Any
            Keyword arguments to configure.
        """
        self._config.update(kwargs)


settings = Settings()
"""Multibar global settings singleton."""
