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

import types
import typing

from multibar.core import errors


__all__: typing.Sequence[str] = ("ProgressBase",)


class ProgressBase:
    """``|class|``

    Base progress class. Currently inherited from it:

    * :class:`ProgressBar`
    * :class:`MusicBar`

    Features:
    ---------
    __aenter__: :class:`ProgressBase`
        ``async context manager``.

    __aexit__: :class:`ProgressBase`
        ``async context manager``.

    __enter__: :class:`ProgressBase`
        ``context manager``.

    __exit__: :class:`ProgressBase`
        ``context manager``.
    """

    async def __aenter__(self) -> ProgressBase:
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> ProgressBase:
        return self

    def __enter__(self) -> ProgressBase:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> ProgressBase:
        return self

    @staticmethod
    def _check_locals(**parameters: typing.Any) -> None:
        """Checks for the correct operation of the progress bar."""
        now: typing.Optional[int] = parameters.pop("now", None)
        needed: typing.Optional[int] = parameters.pop("needed", None)

        if now is None or needed is None:
            raise errors.MissingRequiredArguments("<now> or <needed> :class:`int`")

        elif parameters.pop("length") < 1:
            raise errors.BadValueSpecified("[length] parameter must be > 0")

        elif now > needed:
            raise errors.BadValueSpecified("<now> parameter cannot be more then <needed>")
