"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import typing

from multibar.discord import errors


__all__: typing.Sequence[str] = (
    "BAR",
    "PERCENTS",
    "IS_LEFT",
    "Manipulator",
)


class _ManipulatorParamBase:
    """``|class|``

    Base class with `format` method.

    Parameters:
    -----------
    prefix: :class:`typing.Optional[str]` = '['
        Base prefix for customizing progress output.

    suffix: :class:`typing.Optional[str]` = ']'
        Base suffix for customizing progress output.
    """

    prefix: typing.Optional[str] = "["
    suffix: typing.Optional[str] = "]"

    def format(
        self, prefix: typing.Optional[str] = "[", suffix: typing.Optional[str] = "]"
    ) -> _ManipulatorParamBase:
        """``|method|``

        Method for formatting the output of a specific parameter.

        Parameters:
        -----------
        prefix: :class:`typing.Optional[str]` = '['
            The string that will be displayed up to a certain element.

        suffix: :class:`typing.Optional[str]` = ']'
            The string to be displayed after a certain element.

        Returns:
        --------
        self: :class:`_ManipulatorParamBase`
            Class instance to allow for fluent-style chaining.
        """
        for k, v in locals().items():
            setattr(self, k, v)
        return self


class _Bar(_ManipulatorParamBase):
    """``|class|``

    Progress element responsible for the progress bar.

    Example of usage:
    -----------------
    ```py

    import bar
    from bar.discord.ext import BAR

    embed = bar.discord.ProgressEmbed().add_manipulator(
        BAR.format('{{', '}}')
    ).add_field(
        name='field',
        value='field value',
        progress=bar.ProgressBar(10, 100).write_progress(**bar.ProgressTemplates.ADVANCED)
    )
    ```
    """

    def format(self, prefix: typing.Optional[str] = "", suffix: typing.Optional[str] = "") -> _Bar:
        """``|method|``

        !!! note
            Changed the default value of `prefix` and `suffix`.

        Method for formatting the output of the progress bar parameter.

        Parameters:
        -----------
        prefix: :class:`typing.Optional[str]` = '['
            The string that will be displayed up to a certain element.

        suffix: :class:`typing.Optional[str]` = ']'
            The string to be displayed after a certain element.

        Returns:
        --------
        self: :class:`_Bar`
            Class instance to allow for fluent-style chaining.
        """
        super().format(prefix=prefix, suffix=suffix)
        return self

    def reverse(self) -> _Bar:
        """``|method|``

        If True, then it will swap the `name` and `value` in the field.

        Returns:
        --------
        self: :class:`_Bar`
            Class instance to allow for fluent-style chaining.
        """
        setattr(self, "_reverse", True)
        return self


class _Percents(_ManipulatorParamBase):
    """The class that is responsible for output of `percents` parameter."""


class _IsLeft(_ManipulatorParamBase):
    """The class that is responsible for output of `is_left` parameter."""


class Manipulator:
    """``|class|``

    Main manipulator class.

    Parameters:
    -----------
    setup: :class:`typing.Iterable`
        An iterable object that contains parameters: (
            Optional[BAR],
            Optional[PERCENTS],
            Optional[IS_LEFT],
        )

    Raises:
    -------
    :class:`errors.MissingRequiredArgument`
        If all three parameters are not specified.
    """

    def __init__(self, setup: typing.Iterable[typing.Any]) -> None:
        if not any(i is not None for i in setup):
            raise errors.MissingRequiredArgument("<BAR | PERCENTS | IS_LEFT> for manipulator")

        for idx, parameter in enumerate(setup):
            if parameter is not None:
                parameter.position = idx
                setattr(self, parameter.__class__.__name__.lower(), parameter)


BAR = _Bar()
PERCENTS = _Percents()
IS_LEFT = _IsLeft()
