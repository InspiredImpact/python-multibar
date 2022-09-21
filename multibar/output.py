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
"""This module implements the prebound method pattern to create a simple api output to the console."""
from __future__ import annotations

__all__ = (
    "PrinterAware",
    "TermcolorPrinter",
    "print",
    "new_line",
    "print_success",
    "print_warning",
    "print_heading",
    "print_error",
)

import abc
import typing

import termcolor
import typing_extensions
from returns.io import IO

from . import settings, utils

if typing.TYPE_CHECKING:
    ErrorType: typing_extensions.TypeAlias = typing.Literal["error"]
    WarningType: typing_extensions.TypeAlias = typing.Literal["warning"]
    SuccessType: typing_extensions.TypeAlias = typing.Literal["success"]

    HeadingLevelOneType: typing_extensions.TypeAlias = typing.Literal[1]
    HeadingLevelTwoType: typing_extensions.TypeAlias = typing.Literal[2]
    HeadingLevelThreeType: typing_extensions.TypeAlias = typing.Literal[3]

    OutputTypes: typing_extensions.TypeAlias = typing.Union[
        ErrorType,
        WarningType,
        SuccessType,
    ]
    ColorsType: typing_extensions.TypeAlias = typing.Literal["red", "green", "yellow"]

    HeadingLevelsType: typing_extensions.TypeAlias = typing.Union[
        HeadingLevelOneType,
        HeadingLevelTwoType,
        HeadingLevelThreeType,
    ]

_PRINTER_KEY: typing.Literal["PRINTER"] = "PRINTER"

ERROR: ErrorType = "error"
"""Error literal identifier."""

SUCCESS: SuccessType = "success"
"""Success literal identifier."""

WARNING: WarningType = "warning"
"""Warning literal identifier."""

COLORS: typing.Final[dict[OutputTypes, ColorsType]] = {ERROR: "red", SUCCESS: "green", WARNING: "yellow"}
"""Constant that stores dict, in which key is print status and value is print color."""

HEADING_LEVEL_ONE: HeadingLevelOneType = 1
"""First level heading identifier."""

HEADING_LEVEL_TWO: HeadingLevelTwoType = 2
"""Second level heading identifier."""

HEADING_LEVEL_THREE: HeadingLevelThreeType = 3
"""Third level heading identifier."""

HEADING_MAP: typing.Final[dict[HeadingLevelsType, tuple[str, bool]]] = {
    HEADING_LEVEL_ONE: ("=", True),
    HEADING_LEVEL_TWO: ("-", True),
    HEADING_LEVEL_THREE: ("-", False),
}
"""Constant that stores dict, in which key is heading level and value is header metadata."""


class PrinterAware(abc.ABC):
    """Interface for printer implementations."""

    @typing.overload
    @abc.abstractmethod
    def print(self) -> IO[None]:
        ...

    @typing.overload
    @abc.abstractmethod
    def print(self, text: str) -> IO[None]:
        ...

    @typing.overload
    @abc.abstractmethod
    def print(
        self,
        text: str,
        *,
        bold: bool,
        color: typing.Optional[str],
        newline: bool,
    ) -> IO[None]:
        ...

    @abc.abstractmethod
    def print(
        self,
        text: str = "",
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> IO[None]:
        """Prints text in console.

        Parameters
        ----------
        text : str = ""
            Text to print.
        bold : bool = False
            If true, will make text bold.
        color : typing.Optional[str] = None
            Changes text output color.
        newline : bool = True
            If true, will print new line after `text`.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        ...


class TermcolorPrinter(PrinterAware):
    """Implementation of printer interface."""

    def print(
        self,
        text: str = "",
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> IO[None]:
        """Prints text in console.

        !!! note
            Documentation duplicated for mkdocs auto-reference
            plugin.

        Parameters
        ----------
        text : str = ""
            Text to print.
        bold : bool = False
            If true, will make text bold.
        color : typing.Optional[str] = None
            Changes text output color.
        newline : bool = True
            If true, will print new line after `text`.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        termcolor_attrs: list[str] = []
        if bold:
            termcolor_attrs.append("bold")
        if newline:
            text += "\n"
        termcolor.cprint(text, color, attrs=termcolor_attrs)
        return IO(None)


_PRINTER_STATE: typing.Final[PrinterAware] = TermcolorPrinter()


class Output:
    """Class that represents console printer.

    !!! note
        `#!py @returns.io.impure` decorator shadows the underlying
        signature of a function, which makes it difficult to
        work with the IDE because it's easy to miss out on
        required arguments when calling a function.

        Therefore, we use an explicit `#!py return IO(None)` to
        maintain the logic of the project.
    """

    def print(
        self,
        text: str = "",
        /,
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> IO[None]:
        """Prints text in console.

        Parameters
        ----------
        text : str = ""
            Text to print.
        bold : bool = False
            If true, will make text bold.
        color : typing.Optional[str] = None
            Changes text output color.
        newline : bool = True
            If true, will print new line after `text`.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        self.printer.print(
            text,
            bold=bold,
            color=color,
            newline=newline,
        )
        return IO(None)

    def new_line(self) -> IO[None]:
        """Prints new line in console.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        self.printer.print()
        return IO(None)

    def print_heading(
        self,
        text: str,
        /,
        *,
        level: HeadingLevelsType,
        style: typing.Optional[OutputTypes] = None,
        indent: bool = True,
    ) -> IO[None]:
        """Prints headings in console.

        Parameters
        ----------
        text : str
            Text to header.
        level : HeadingLevelsType
            Header level.
        style : typing.Optional[OutputTypes] = None
            If is not None, will change header style.
        indent : bool = True
            If True, will print new line after text.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        color = COLORS[style] if style else None
        line_char, show_line_above = HEADING_MAP[level]
        heading_line = line_char * len(text)

        if show_line_above:
            self.printer.print(heading_line, bold=True, color=color)

        self.printer.print(text, bold=True, color=color)
        self.printer.print(heading_line, bold=True, color=color)

        if indent:
            self.printer.print()

        return IO(None)

    def print_success(self, text: str, /, *, bold: bool = True) -> IO[None]:
        """Prints text as success.

        Parameters
        ----------
        text: str
            Text to print.
        bold: bool = True
            If True, will print text as bold.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        self.printer.print(text, color=COLORS[SUCCESS], bold=bold)
        return IO(None)

    def print_error(self, text: str, /, *, bold: bool = True) -> IO[None]:
        """Prints text as error.

        Parameters
        ----------
        text: str
            Text to print.
        bold: bool = True
            If True, will print text as bold.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        self.printer.print(text, color=COLORS[ERROR], bold=bold)
        return IO(None)

    def print_warning(self, text: str, /) -> IO[None]:
        """Prints text as warning.

        Parameters
        ----------
        text: str
            Text to print.

        Returns
        -------
        IO[None]
            Displays text in console.
        """
        self.printer.print(text, color=COLORS[WARNING])
        return IO(None)

    def update_printer(self) -> None:
        """Updates cache for printer cached_property.

        !!! info
            For example of usage see `cached_property` class.

        Returns
        -------
        None
        """
        utils.cached_property.update_cache_for(self, "printer")

    @utils.cached_property
    def printer(self) -> PrinterAware:
        """Cached property that returns printer implementation.

        Returns
        -------
        PrinterAware
            Printer implementation.
        """
        if _PRINTER_KEY in settings.settings:
            return settings.settings[_PRINTER_KEY]
        return _PRINTER_STATE


# Implementation of prebound method pattern
_output = Output()

print = _output.print
"""Prints text in console.

??? example "Expand example of prebound pattern usage"
    ```pycon hl_lines="3 4"
    >>> from multibar import output

    >>> output.print_heading("Testing complete", level=1, indent=False)
    >>> output.print_success("Checks passed: N.")

    {== ========================= ==}
    {==                           ==}
    {==     Testing complete      ==}
    {==                           ==}
    {== ========================= ==}

    {++ Checks passed: N. ++}
    ```
"""

new_line = _output.new_line
"""Prints new line in console."""

print_success = _output.print_success
"""Prints text as success."""

print_heading = _output.print_heading
"""Prints headings in console."""

print_error = _output.print_error
"""Prints text as error."""

print_warning = _output.print_warning
"""Prints text as warning."""
