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
import functools

from multibar.core import errors
from multibar.enums import CallbackAs
from multibar.templates import ProgressTemplates
from multibar.core import ProgressBar, ProgressObject
from multibar.utils import to_async, PackArgs, AsCallable

if typing.TYPE_CHECKING:
    from multibar.core.variants import CharsSnowflake, FromClassInstance, ReturnAs


__all__: typing.Sequence[str] = (
    "from_class",
    "ParamBase",
)


T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)  # covariant


class ParamBase(typing.Generic[T_co]):
    """``|class|``

    The main class for all parameters used to further customize the progress bar.

    Parameters:
    -----------
    instance: :class:`ParamBase`
        An instance of the parameter class for the decorator.

    value: :class:`typing.TypeVar`
        Parameter class instance attribute.
    """

    def __init__(self, instance: ParamBase[T_co], value: T) -> None:
        self.value = value
        setattr(instance, self.__class__.__name__.lower() + "_param", self)


class Chars(ParamBase[T]):
    """``|class-parameter|``

    A class-parameter for the main decorator.

    Parameters:
    -----------
    instance: :class:`ParamBase`
        An instance of the parameter class for the decorator.

    fill: :class:`str` [Keyword only]
        Emoji, which will fill the progress bar.

    line: :class:`str` [Keyword only]
        Unfilled progress bar emoji.

    unfilled_start: :class:`typing.Optional[str]` [Keyword only]
        Unfilled start emoji of progress bar.

    start: :class:`typing.Optional[str]` [Keyword only]
        Start emoji of progress bar.

    unfilled_end: :class:`typing.Optional[str]` [Keyword only]
        Unfilled end emoji of progress bar.

    end: :class:`typing.Optional[str]` [Keyword only]
        End emoji of progress bar.

    Properties:
    -----------
    as_dict: :class:`typing.Dict[str, str]`
        Returns a dictionary with the passed characters.
    """

    def __init__(
        self,
        instance: ParamBase[T],
        /,
        *,
        fill: typing.Optional[str] = None,
        line: typing.Optional[str] = None,
        start: typing.Optional[str] = None,
        end: typing.Optional[str] = None,
        unfilled_start: typing.Optional[str] = None,
        unfilled_end: typing.Optional[str] = None,
    ) -> None:
        self.instance = instance
        self.fill = fill
        self.line = line
        if fill is None or line is None:
            raise errors.MissingRequiredArguments("<fill:str:> or <line:str:>")
        self.start = start
        self.end = end
        self.unfilled_start = unfilled_start
        self.unfilled_end = unfilled_end
        super().__init__(
            self.instance,
            {k: v for k, v in locals().items() if isinstance(v, str) or v is None},
        )

    @property
    def as_dict(self) -> typing.Dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if v}

    @classmethod
    def from_dict(
        cls: typing.Type[Chars[T]],
        instance: typing.Any,
        chars: CharsSnowflake,
    ) -> Chars[T]:
        """``|classmethod|``

        The second way is to pass characters to create a progress bar.

        Example of usage:
        -----------------
        ```py

        [Optional] from bar.core.variants import FromClassBase

        @from_class()
        class Example(FromClassBase):
            ("
            Example of usage `from_class` deco.
            It is not necessary to inherit from FromClassBase,
            it is only necessary for the convenience of working
            with methods inside the class and to avoid various
            warnings from mypy.
            ")

            async def foo(self):
                self.now(self, 10)
                self.needed(self, 100)
                self.chars.from_dict(
                    self,
                    {'fill': '+', 'line': '-'}
                )

            example = Example()
            print(example.foo)
            ++------------------
        """
        return cls(instance, **chars)


class FromClassSetup:
    """``|class|``

    The class with the help of which the basis for further work is created.

    Parameters:
    -----------
    __allowed_params__: :class:`typing.Sequence[typing.Any]`
        Allowed parameters that will later be used as classes.
    """

    __allowed_params__: typing.Sequence[typing.Any] = (
        "Now",
        "Needed",
        "Length",
        "Deque",
        Chars,
    )

    def __init__(self) -> None:
        # In the class initializer, other class parameters are created depending on the context.
        for maybe_cls in FromClassSetup.__allowed_params__:
            if not inspect.isclass(maybe_cls):
                setattr(
                    self,
                    maybe_cls.lower(),
                    type(maybe_cls, (ParamBase,), {"__progress_object__": True}),
                )
            else:
                setattr(self, maybe_cls.__name__.lower(), maybe_cls)


class FromClass:
    """``|class|``

    The class containing the main methods for working with the decorator.

    Parameters:
    -----------
    cls: :class:`FromClassInstance` [Keyword only]
        Instance of the class to be decorated.

    save_callback: :class:`bool` = False [Keyword only]
        If True, will keep the function callback.

    return_as: :class:`ReturnAs` = 1 [Keyword only]
        Returns an object depending on the selected type.

    loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` = None [Keyword only]
        Asyncio loop.
    """

    def __init__(
        self,
        *,
        cls: FromClassInstance,
        save_callback: bool = False,
        return_as: ReturnAs = 1,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self.__cls = cls
        self.__save_callback = save_callback
        self.__return_as = return_as
        if loop is None:
            self.__loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.__loop)
        else:
            self.__loop = loop

    def invoke_and_hook_all(self, *args: typing.Any, **kwargs: typing.Any) -> FromClassInstance:
        """``|method|``

        The main method where all methods are called and their values are set.
        """
        for c in itertools.filterfalse(lambda i: i.startswith("_"), dir((base := FromClassSetup()))):
            setattr(self.__cls, c, getattr(base, c))
        for method_name in dir(self.__cls):
            if all(
                (
                    not method_name.startswith("_"),
                    not hasattr(
                        (method := getattr(self.__cls, method_name)),
                        "__progress_object__",
                    ),
                    not hasattr(method, "__progress_ignored__"),
                    inspect.ismethod(method),
                )
            ):
                try:
                    if inspect.iscoroutinefunction(method):
                        callback = asyncio.run(method(*args, **kwargs))
                    else:
                        callback = method(*args, **kwargs)
                except Exception as exc:
                    raise errors.ProgressInvokeError(exc) from exc

                wrapped_callback = asyncio.run(self.wrap_callback(self.__cls, callback))

                if self.__return_as == CallbackAs.default:
                    setattr(self.__cls, method.__name__, wrapped_callback)
                elif self.__return_as == CallbackAs.callable:
                    setattr(self.__cls, method.__name__, AsCallable(wrapped_callback))
                elif self.__return_as == CallbackAs.awaitable:
                    setattr(
                        self.__cls,
                        method.__name__,
                        to_async(loop=self.__loop)(lambda: wrapped_callback),
                    )
                else:
                    raise errors.BadCallbackTypeSpecified(self.__return_as, "Literal[1, 2, 3]")
        return self.__cls

    async def wrap_callback(
        self,
        instance: FromClassInstance,
        callback: typing.Union[PackArgs, ProgressObject],
        /,
    ) -> typing.Union[PackArgs, ProgressObject]:
        """``|coro|``

        The method in which we wrap the callback by setting a new value to it.

        Parameters:
        -----------
        instance: :class:`FromClassInstance` [Positional only]
            The state of the class from which the parameters will be taken.

        callback: :class:`typing.Union[PackArgs, ProgressObject]` [Positional only]
            Initial function callback.
        """
        deque = getattr(instance, "deque_param", None)
        length = getattr(instance, "length_param", None)
        chars = getattr(instance, "chars_param", None)

        bar: ProgressBar = ProgressBar(
            instance.now_param.value,
            instance.needed_param.value,
            length=20 if not hasattr(length, "value") else length.value,
            deque=False if not hasattr(length, "value") else deque.value,
        )
        progress = await bar.async_write_progress(
            ProgressTemplates.ADVANCED if not hasattr(chars, "value") else chars.value
        )
        if self.__save_callback:
            return PackArgs(callback=callback, progress=progress)
        else:
            return progress


def from_class(
    *,
    save_callback: bool = False,
    return_as: ReturnAs = 1,
    loop: typing.Optional[asyncio.AbstractEventLoop] = None,
) -> typing.Callable[..., typing.Callable[..., typing.Any]]:
    """``|decorator|``

    Parameters:
    -----------
    save_callback: :class:`bool` = False [Keyword only]
        If True, will keep the function callback.

    return_as: :class:`ReturnAs` = 1 [Keyword only]
        Returns an object depending on the selected type.

    loop: :class:`typing.Optional[asyncio.AbstractEventLoop]` = None [Keyword only]
        Asyncio loop.
    """

    def inner(cls: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
        @functools.wraps(cls)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> FromClassInstance:
            cfg = {
                "cls": cls(*args, **kwargs),
                "save_callback": save_callback,
                "return_as": return_as,
                "loop": loop,
            }
            return FromClass(**cfg).invoke_and_hook_all(*args, **kwargs)

        return wrapper

    return inner
