"""This module implements the prebound method pattern to create a simple api output to the console."""
from __future__ import annotations

__all__ = [
    "PrinterAware",
    "TermcolorPrinter",
    "print",
    "new_line",
    "print_success",
    "print_warning",
    "print_heading",
    "print_error",
]

import abc
import typing

import termcolor
from returns.io import IO, impure

from . import utils
from . import settings

if typing.TYPE_CHECKING:
    ErrorType: typing.TypeAlias = typing.Literal["error"]
    WarningType: typing.TypeAlias = typing.Literal["warning"]
    SuccessType: typing.TypeAlias = typing.Literal["success"]

    HeadingLevelOneType: typing.TypeAlias = typing.Literal[1]
    HeadingLevelTwoType: typing.TypeAlias = typing.Literal[2]
    HeadingLevelThreeType: typing.TypeAlias = typing.Literal[3]

    OutputTypes: typing.TypeAlias = typing.Union[
        ErrorType, WarningType, SuccessType,
    ]
    ColorsType: typing.TypeAlias = typing.Literal["red", "green", "yellow"]

    HeadingLevelsType: typing.TypeAlias = typing.Union[
        HeadingLevelOneType, HeadingLevelTwoType, HeadingLevelThreeType,
    ]

_PRINTER_KEY: typing.Final[typing.Literal["PRINTER"]] = "PRINTER"

ERROR: typing.Final[ErrorType] = "error"
SUCCESS: typing.Final[SuccessType] = "success"
WARNING: typing.Final[WarningType] = "warning"
COLORS: typing.Final[dict[OutputTypes, ColorsType]] = {ERROR: "red", SUCCESS: "green", WARNING: "yellow"}

HEADING_LEVEL_ONE: typing.Final[typing.Literal[1]] = 1
HEADING_LEVEL_TWO: typing.Final[typing.Literal[2]] = 2
HEADING_LEVEL_THREE: typing.Final[typing.Literal[3]] = 3

HEADING_MAP: typing.Final[dict[HeadingLevelsType, tuple[str, bool]]] = {
    HEADING_LEVEL_ONE: ("=", True),
    HEADING_LEVEL_TWO: ("-", True),
    HEADING_LEVEL_THREE: ("-", False),
}


class PrinterAware(abc.ABC):
    @abc.abstractmethod
    def print(
        self,
        text: str = "",
        /,
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> IO[None]:
        ...


class TermcolorPrinter(PrinterAware):
    def print(
        self,
        text: str = "",
        /,
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> IO[None]:
        termcolor_attrs: list[str] = []
        if bold:
            termcolor_attrs.append("bold")
        if newline:
            text += "\n"
        termcolor.cprint(text, color, attrs=termcolor_attrs)
        return IO(None)


_PRINTER_STATE: typing.Final[PrinterAware] = TermcolorPrinter()


class Output:
    @impure
    @typing.overload
    def print(self) -> None:
        ...

    @impure
    @typing.overload
    def print(
        self,
        text: str,
        /,
        *,
        bold: bool,
        color: typing.Optional[str],
        newline: bool,
    ) -> None:
        ...

    @impure
    def print(
        self,
        text: str = "",
        /,
        *,
        bold: bool = False,
        color: typing.Optional[str] = None,
        newline: bool = True,
    ) -> None:
        self.printer.print(
            text, bold=bold, color=color, newline=newline,
        )

    @impure
    def new_line(self) -> None:
        self.printer.print()

    @impure
    def print_heading(
        self,
        text: str,
        /,
        *,
        level: HeadingLevelsType,
        style: typing.Optional[OutputTypes] = None,
        indent: bool = True,
    ) -> None:
        color = COLORS[style] if style else None
        line_char, show_line_above = HEADING_MAP[level]
        heading_line = line_char * len(text)

        if show_line_above:
            self.printer.print(heading_line, bold=True, color=color)

        self.printer.print(text, bold=True, color=color)
        self.printer.print(heading_line, bold=True, color=color)

        if indent:
            self.printer.print()

    @impure
    def print_success(self, text: str, /, *, bold: bool = True) -> None:
        self.printer.print(text, color=COLORS[SUCCESS], bold=bold)

    @impure
    def print_error(self, text: str, /, *, bold: bool = True) -> None:
        self.printer.print(text, color=COLORS[ERROR], bold=bold)

    @impure
    def print_warning(self, text: str, /) -> None:
        self.printer.print(text, color=COLORS[WARNING])

    def update_printer(self) -> None:
        utils.cached_property.update_cache_for(self, "printer")

    @utils.cached_property
    def printer(self) -> PrinterAware:
        if _PRINTER_KEY in settings.settings:
            return settings.settings[_PRINTER_KEY]
        return _PRINTER_STATE


_output = Output()
print = _output.print
new_line = _output.new_line
print_success = _output.print_success
print_heading = _output.print_heading
print_error = _output.print_error
print_warning = _output.print_warning
