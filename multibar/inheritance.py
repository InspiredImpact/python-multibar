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
import inspect
import asyncio
import itertools

from multibar import templates
from multibar.enums import CallbackAs
from multibar.core.variants import CharsSnowflake
from multibar.utils import ignored, to_async, AsCallable
from multibar.core import ProgressBar, errors, ProgressObject

if typing.TYPE_CHECKING:
    T_co = typing.TypeVar("T_co", covariant=True)

    class _HasIadd(typing.Protocol[T_co]):
        def __iadd__(self, other: typing.Any) -> typing.Any:
            ...

    from multibar.core.variants import ReturnAs


__all__: typing.Sequence[str] = ("Progress",)


T = typing.TypeVar("T")


class _ParametersInterface:
    """``|class|``

    The class was created in order to increase the readability of the code and ease of access
    to various attributes for further generation of the progress bar.

    # Instances of the classes are labeled TypeVar because I still haven't figured out
    # the best way to type-hint them :D.

    Parameters:
    -----------
    current_instance: :class:`TypeVar` [Positional only]
        The current instance of the class from which we will receive parameters.

    other_instance: :class:`TypeVar` [Positional only]
        Another instance of the class is required for the unique parameter.

    method: :class:`str` [Positional only]
        The name of the current method to create unique parameters.

    Properties:
    -----------
    now_param: :class:`Optional[int]`
        The parameter of the current progress (required, if None - will cause an error).

    needed_param: :class:`Optional[int]`
        The total progress parameter (required, if None - will cause an error).

    length_param: :class:`int` = 20
        Progress bar length parameter.

    deque_param: :class:`bool` = False
        The deque parameter, if True - then instead of a list with sectors,
        it will return a deque object with sectors.

    chars_param: :class:`CharsSnowflake` = ProgressTemplates.ADVANCED
        Parameter that affects the progress bar emoji.

    unique: :class:`str`
        Unique pattern of parameter names.
    """

    def __init__(self, current_instance: typing.Any, other_instance: typing.Any, method: str, /) -> None:
        self.__method_name = method
        self.__c_instance = current_instance

        self.__unique: str = f"{other_instance.__class__.__name__}_{method}"

    @property
    def now_param(self) -> typing.Optional[int]:
        return typing.cast(typing.Optional[int], self.__c_instance[f"__now_param__{self.__unique}"])

    @property
    def needed_param(self) -> typing.Optional[int]:
        return typing.cast(typing.Optional[int], self.__c_instance[f"__needed_param__{self.__unique}"])

    @property
    def length_param(self) -> int:
        return typing.cast(int, getattr(self.__c_instance, f"__length_param__{self.__unique}", 20))

    @property
    def deque_param(self) -> bool:
        return typing.cast(bool, getattr(self.__c_instance, f"__deque_param__{self.__unique}", False))

    @property
    def chars_param(self) -> CharsSnowflake:
        return typing.cast(
            CharsSnowflake,
            getattr(self.__c_instance, f"__chars_param__{self.__unique}", templates.ProgressTemplates.ADVANCED),
        )

    @property
    def unique(self) -> str:
        return self.__unique


class Progress:
    """``|class|``

    A class inherited from which we can create progress bars.
    Additional functions for this implementation: :class:`ProgressMixin`

    In __init_subclass__, we call all the methods, thereby saving their
    callback, so that we can wrap them in the class initializer later.

    Parameters:
    -----------
    save_callback: :class:`bool` = False
        If True, then the function callback will be saved.

    returns_as: :class:`int` = 1
        This specifies the type of how the result will be returned
        (default / callable / awaitable), more details: :class:`bar.enums.CallbackAs`.

    loop: :class:`asyncio.AbstractEventLoop`
        Used if return_as = CallbackAs.awaitable (3) to create an asyncio.Future object.

    **kwargs: :class:`Any`
        Not used (shadow).

    Example of usage:
    -----------------
    ```py
    from multibar.utils import ignored

    class TestCase(Progress, save_callback=True):

        # Values can be set in any order. #
        async def foo(self):  # OK.
            self.chars({'fill': '++', 'line': '--'})
            self.length(10)
            self.now(40)
            self.needed(100)
            return 'Python'

        # Synchronous functions are supported in the same way as asynchronous. #
        def bar(self):  # OK.
            self.chars({'fill': '+', 'line': '-'})
            self.now(80)
            self.needed(100)
            self.length(10)
            return True

        # You can also copy the function #
        def baz(self):  # OK.
            self.copy('bar')

        # !But arguments in functions are not supported! #
        def egg(self, a: int, b: int) -> int:  # Error.
            self.copy('baz')
            return a + b

        # This function will be ignored. #
        @ignored
        def spam(self, a: int, b: int) -> int:  # OK.
            return a + b

    test = TestCase()

    print(test.foo)
    PackArgs(progress=++++++++------------, callback=Python)

    print(test.bar)
    PackArgs(progress=++++++++--, callback=True)

    print(test.baz)
    <ProgressObject(callback=PackArgs(progress=++++++++--, callback=None))>

    print(test.egg)
    TypeError: egg() missing 2 required positional arguments: 'a' and 'b'

    print(test.spam(1, 2))
    3
    ```
    """

    def __init_subclass__(
        cls: typing.Type[Progress],
        save_callback: bool = False,
        return_as: ReturnAs = 1,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        **kwargs: typing.Any,
    ) -> None:
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg] # Mypy doesn't understand __init_subclass__.
        for new_attr in (
            "_save_callback",
            "_return_as",
            "_loop",
        ):  # For mypy "attr-defined".
            setattr(cls, new_attr, locals().get(new_attr[1:]))

        for method_name in itertools.filterfalse(lambda m: m.startswith("_"), dir(cls)):
            if not hasattr((method := getattr(cls, method_name)), "__progress_ignored__"):
                # Save the callback of each method in each subclass.
                try:
                    if inspect.iscoroutinefunction(method):
                        callback = asyncio.run(method(cls))
                    else:
                        callback = method(cls)
                except Exception as exc:
                    raise errors.ProgressInvokeError(exc)

                setattr(cls, f"__{cls.__name__}_{method.__name__}_callback__", callback)

    def __init__(self) -> None:
        for cls in Progress.__subclasses__():
            methods: typing.List[str] = [
                m
                for m in filter(
                    lambda m: all(
                        (
                            not m.startswith("_"),  # Removing unnecessary methods and default dunders.
                            inspect.isfunction(getattr(cls, m)),  # Removing non callable objects.
                            hasattr(
                                cls, f"__{cls.__name__}_{m}_callback__"
                            ),  # Checking if the method uses @ignored.
                        )
                    ),
                    dir(cls),
                )
            ]
            # We wrap methods by changing them.
            for method in methods:
                setattr(
                    self,
                    method,
                    self.__wrap_method(
                        self,
                        method,
                        loop=getattr(self, "_loop"),
                        ret_type=getattr(self, "_return_as"),
                    ),
                )

    def __getitem__(self, item: str) -> typing.Any:
        return getattr(self, item, None)

    @ignored
    def __wrap_method(
        self,
        instance: typing.Any,
        method: str,
        *,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        ret_type: ReturnAs = 1,
    ) -> typing.Any:
        """``|function|``

        The method by which the function is wrapped and the progress bar is generated.

        Parameters:
        -----------
        instance: :class:`Any` [Positional only]
            The current instance of the class.

        method: :class:`str` [Positional only]
            Method to be wrapped.

        loop: :class:`asyncio.AbstractEventLoop` [Keyword only]
            Used to create a progress bar, if None, then by default it will be asyncio.get_event_loop().

        ret_type: :class:`int` = 1 [Keyword only]
            This specifies the type of how the result will be returned
            (default / callable / awaitable), more details: :class:`bar.enums.CallbackAs`.

        Returns:
        --------
        Callable object (progress bar result).

        Raises:
        -------
        :class:`errors.BadCallbackTypeSpecified`:
            If the wrong callback type is specified.
        """
        exists = getattr(instance, method, None)
        if exists is None:
            return
        elif hasattr(exists, "__progress_ignored__"):
            return exists
        else:
            interface = _ParametersInterface(self, instance, method)
            bar: ProgressBar = ProgressBar(
                interface.now_param,
                interface.needed_param,
                length=interface.length_param,
                deque=interface.deque_param,
            )
            progress: _HasIadd[ProgressObject] = asyncio.run(
                bar.async_write_progress(interface.chars_param, loop=loop)
            )
            if getattr(instance, "_save_callback", False):
                # With __iadd__ we have parsed this into PackArgs with progress and callback attrs.
                progress += getattr(instance, f"__{interface.unique}_callback__")

            if ret_type == CallbackAs.default:
                return progress
            elif ret_type == CallbackAs.callable:
                return AsCallable(progress)
            elif ret_type == CallbackAs.awaitable:
                return to_async(loop=loop)(progress)
            else:
                raise errors.BadCallbackTypeSpecified(ret_type, "Literal[1, 2, 3]")

    @classmethod
    @ignored
    def now(cls: typing.Type[Progress], num: int, /) -> None:
        """``|classmethod|``

        The parameter of the current progress.

        Parameters:
        -----------
        num: :class:`int`
            Current progress number.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)
            def foo(self):  # Asynchronous functions are also supported.
                self.now(10)
        ```
        """
        setattr(cls, "__now_param__" + cls.__name__ + "_" + inspect.stack()[1][3], num)

    @classmethod
    @ignored
    def needed(cls: typing.Type[Progress], num: int, /) -> None:
        """``|classmethod|``

        The parameter of the needed progress.

        Parameters:
        -----------
        num: :class:`int`
            Needed progress number.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)
            def foo(self):  # Asynchronous functions are also supported.
                self.needed(100)
        ```
        """
        setattr(cls, "__needed_param__" + cls.__name__ + "_" + inspect.stack()[1][3], num)

    @classmethod
    @ignored
    def length(cls: typing.Type[Progress], num: int, /) -> None:
        """``|classmethod|``

        The parameter of the length of the progress bar.

        Parameters:
        -----------
        num: :class:`int`
            Length number.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)
            def foo(self):  # Asynchronous functions are also supported.
                self.length(10)  # Default: 20
        ```
        """
        setattr(cls, "__length_param__" + cls.__name__ + "_" + inspect.stack()[1][3], num)

    @classmethod
    @ignored
    def deque(cls: typing.Type[Progress], value: bool, /) -> None:
        """``|classmethod|``

        The deque parameter, if True, will return the collections.deque
        object instead of the usual list. (Each progress bar symbol is a
        separate list item or deque with a specific set of attributes).

        Parameters:
        -----------
        value: :class:`bool`
            Deque value.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)
            def foo(self):  # Asynchronous functions are also supported.
                self.deque(True)  # Default: False
        ```
        """
        setattr(cls, "__deque_param__" + cls.__name__ + "_" + inspect.stack()[1][3], value)

    @classmethod
    @ignored
    def chars(cls: typing.Type[Progress], chars: CharsSnowflake) -> None:
        """``|classmethod|``

        A parameter that accepts a dictionary from {specific value: symbol},
        from which the progress bar will already be made.

        Parameters:
        -----------
        chars: :class:`CharsSnowflake`
            Progress bar characters.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)
            def foo(self):  # Asynchronous functions are also supported.
                self.chars({'fill': '+', 'line': '-'})  # Default: bar.ADVANCED
        ```
        """
        setattr(cls, "__chars_param__" + cls.__name__ + "_" + inspect.stack()[1][3], chars)

    @classmethod
    @ignored
    def copy(cls: typing.Type[Progress], reference: str) -> None:
        """``|classmethod|``

        Method that copies all parameters of another method in the same class.

        Parameters:
        -----------
        reference: :class:`str`
            The name of the method whose parameters need to be copied.

        Returns:
        --------
        :class:`NoneType`

        Example of usage:
        -----------------
        ```py

        class TestCase(Progress)

            def bar(self):
                self.now(10)
                self.needed(100)
                self.deque(True)
                self.chars({'fill': '+', 'line': '-'})

            def foo(self):  # Asynchronous functions are also supported.
                self.copy('bar')
        ```
        """
        if reference not in dir(cls):
            # Bad method name specified.
            raise errors.CannotFindReference(reference)

        stack = inspect.stack()  # Get the current stack.
        # Unique parameter for each function progress bar to
        # avoid further mistakes with duplicate class and function names.
        unique = f"{cls.__name__}_{stack[1][3]}"
        # Get all unique attributes from the specified reference.
        for dunder in filter(lambda m: m.endswith(f"{cls.__name__}_{reference}"), dir(cls)):
            # And we set them in the same class for further generation of the progress bar.
            setattr(
                cls,
                f'{dunder[:dunder.find("__", 1) + 2]}{unique}',
                getattr(cls, dunder),
            )
