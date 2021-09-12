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
import warnings
import functools


__all__: typing.Sequence[str] = (
    "find",
    "to_async",
    "PackArgs",
    "ignored",
    "AsCallable",
    "deprecated",
)


T = typing.TypeVar("T")
FT = typing.TypeVar("FT", bound=typing.Callable[..., bool])  # Function type


def ignored(method: typing.Callable[..., typing.Any], /) -> typing.Callable[..., typing.Any]:
    """``|decorator|``

    Used primarily to ignore and not call a specific method.
    Used both from the user side and in the source code
    (in places where you do not need to call the main methods,
    and the rest require this for modernization).

    Parameters:
    -----------
    method: :class:`Callable[..., Any]` [Positional only]
        Callable object.

    Returns:
    --------
    method: :class:`Callable[..., Any]`
        Callable object.
    """
    setattr(method, "__progress_ignored__", True)
    return method


def deprecated(
    replacement: str, /, *, with_invoke: bool = False
) -> typing.Callable[..., typing.Callable[..., typing.Any]]:
    """``|decorator|``

    Warning for deprecated methods from old version of
    library or currently outdated classes/functions.

    Parameters:
    -----------
    callable_: :class:`Callable[..., Any]` [Positional only]
        Callable object.

    replacement: :class:`str` [Positional only]
        Method to use instead of deprecated.

    with_invoke: :class:`bool` = False [Keyword only]
        If True, it will return the result of calling the object.

    Raises:
    -------
    ProgressInvokeError:
        If `with_invoke = True` and there was an error calling the object.

    Returns:
    --------
    Wrapped function: :class:`Callable[..., [Callable[..., Any]]]`
        Callback if with_invoke = True or callable object.
    """

    def inner(callable_: typing.Callable[..., typing.Any], /) -> typing.Callable[..., typing.Any]:
        @functools.wraps(callable_)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            setattr(callable_, "__progress_deprecated__", True)
            warnings.warn(
                f"Method {callable_.__qualname__} is deprecated, just use {replacement}",
                category=DeprecationWarning,
            )
            if with_invoke:
                if inspect.iscoroutinefunction(callable_):
                    callback = asyncio.run(callable_(*args, **kwargs))
                else:
                    callback = callable_(*args, **kwargs)
                return callback
            else:
                return callable_

        return wrapper

    return inner


def find(
    predicate: FT, iterator: typing.Iterable[T], /, *, get_all: bool = False
) -> typing.Optional[typing.Union[T, typing.List[T]]]:
    """``|function|``

    A function with which you can find the first or all matches in an iterable object.

    Parameters:
    -----------
    predicate: :class:`Callable[..., bool]`
        Check (callable) to find element(s).

    iterator: :class:`Iterable[Any]`
        The object (iterable) in which the object(s) will be searched.

    get_all: :class:`bool` = False
        If True, it will return all matches, otherwise - the first match.

    Returns:
    --------
    All matches in the list if get_all = True or
    the first match if False, otherwise, if nothing
    is found, it will return None.
    """
    if get_all:
        return [i for i in iterator if predicate(i)]
    else:
        for element in iterator:
            if predicate(element):
                return element


def to_async(
    loop: typing.Optional[asyncio.AbstractEventLoop] = None,
) -> typing.Callable[..., typing.Callable[..., asyncio.Future[T]]]:
    """``|decorator|``

    A decorator that turns the callable object into Awaitalbe asyncio.Future.

    Parameters:
    -----------
    func: :class:`Callable[..., asyncio.Future[T]]`
        Callable object.

    loop: :class:`Optional[asyncio.AbstractEventLoop]` = None
        Loop, with which we will create an asyncio.Future object.

    Returns:
    --------
    Wrapped function: :class:`Callable[..., Callable[..., Future[T]]]`
    """

    def inner(func: typing.Callable[..., asyncio.Future[T]]) -> typing.Callable[..., asyncio.Future[T]]:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> asyncio.Future[T]:
            if loop is None:
                loop_ = asyncio.new_event_loop()
                asyncio.set_event_loop(loop_)
            else:
                loop_ = loop
            future = loop_.create_future()
            future.set_result(func(*args, **kwargs))
            return asyncio.wrap_future(future, loop=loop_)

        return wrapper

    return inner


class PackArgs:
    """``|class|``

    A class for wrapping arguments to make it easier to access attributes in the future.

    Features:
    ---------
    __call__: PackArgs()
        Returns the values of all attributes.

    __setitem__: PackArgs()['foo'] = bar
        Adds an element to the current instance of the class.

    __iter__: for i in PackArgs(): ...
        Iterate over the attributes of the class instance.

    __repr__: repr(PackArgs())
        Development information.

    Properties:
    -----------
    args: :class:`List[Any]`
        **positional** arguments that an instance of the class stores.

    kwargs: :class:`Dict[str, Any]`
        **keyword** arguments that an instance of the class stores.
    """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        for idx, arg in enumerate(args, 1):
            self[f"positional_{idx}"] = arg

        for k, v in kwargs.items():
            self[str(k)] = v

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.List[typing.Any]:
        return [getattr(self, i) for i in self]

    def __setitem__(self, key: str, value: typing.Any) -> None:
        setattr(self, key, value)

    def __iter__(self) -> typing.Iterator[str]:
        items = dict(self.__dict__)  # Removing "ItemsView" restrictions
        return iter(items)

    def __repr__(self) -> str:
        argsv = (f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({', '.join(argsv)})"

    @property
    def args(self) -> typing.List[typing.Any]:
        return [getattr(self, arg) for arg in dir(self) if arg.startswith("positional_")]

    @property
    def kwargs(self) -> typing.Dict[str, typing.Any]:
        return {k: getattr(self, k) for k, _ in self.__dict__.items() if not k.startswith("positional_")}


class AsCallable:
    """``|class|``

    The class that makes of :non callable: object - :callable: object.

    Parameters:
    -----------
    result: :class:`Any`
        The value to be made callable.

    Features:
    ---------
    __call__: :class:`Any`
        Returns the value that should have been made callable.

    __repr__: :class:`str`
        Development information.
    """

    def __init__(self, result: typing.Any) -> None:
        self.result = result

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        return self.result

    def __repr__(self) -> str:
        return f"<ProgressObject(callback={self.result})>"
