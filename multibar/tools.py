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
import asyncio
import collections.abc

from multibar.utils import ignored
from multibar.core import errors
from multibar.core.variants import CharsSnowflake


__all__: typing.Sequence[str] = ("ProgressTools",)


class ProgressTools:
    """``|class|``

    Additional methods for working with inheritance in our library.
    """

    @staticmethod
    @ignored
    def to_dict(
        *,
        fill: typing.Optional[str] = None,
        line: typing.Optional[str] = None,
        start: typing.Optional[str] = None,
        end: typing.Optional[str] = None,
        unfilled_start: typing.Optional[str] = None,
        unfilled_end: typing.Optional[str] = None,
    ) -> CharsSnowflake:
        """``|staticmethod|``

        Initially, the chars parameter takes a dictionary,
        this method allows you to pass chars as parameters and
        returns a dictionary from them.

        Example of usage:
        -----------------
        ```py
        from multibar.tools import ProgressTools

        class Bars(Progress, ProgressTools, return_as=2):

            async def foo(self):
                self.now(10)
                self.needed(100)
                self.chars(
                    self.to_dict(  # Progress tools
                        fill='+',
                        line='-',
                    )
                )

        bars = Bars()
        print(bars.foo)  # <ProgressObject(callback=++------------------)>
        ```
        """
        if fill is None or line is None:
            raise errors.MissingRequiredArguments("<fill> or <line>")

        return typing.cast(CharsSnowflake, locals())

    @ignored
    def can_run(
        self,
        func: str,
        /,
        *,
        reraise: bool = False,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> bool:
        """``|function|``

        We can say that this method is practically useless,
        because most of the errors will be detected during the
        initialization of the class, but it can reveal some errors
        during the second call of the method.

        Parameters:
        -----------
        func: :class:`str` [Positional only]
            Method name from a class that inherits from Progress.

        reraise: :class:`bool` = False [Keyword only]
            If True, it will display an error, otherwise it will return bool.

        Example of usage:
        -----------------
        ```py
        from multibar.tools import ProgressTools

        class Bars(Progress, ProgressTools, return_as=2):

            async def foo(self):
                self.now(10)
                self.needed(100)
                self.chars(
                    self.to_dict(  # Progress tools
                        fill='+',
                        line='-',
                    )
                )

        bars = Bars()
        print(bars.can_run('foo'))  # True
        ```

        Raises:
        -------
        :class:`errors.ProgressInvokeError`
            If reraise = True and an error occurred.

        Returns:
        --------
        :class:`bool`
        """
        try:
            fn = getattr(self, func)
            if isinstance(fn, collections.abc.Awaitable):
                loop = loop if loop is not None else asyncio.get_event_loop()
                loop.run_until_complete(fn)
            else:
                fn()
            return True
        except Exception as exc:
            if reraise:
                raise errors.ProgressInvokeError(exc) from exc
            else:
                return False
