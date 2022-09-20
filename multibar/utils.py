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
"""Python-Multibar project utilities."""
from __future__ import annotations

__all__ = ("Singleton", "cached_property", "none_or")

import threading
import typing

_InstanceT = typing.TypeVar("_InstanceT")
"""Any instance object."""

_ActualT = typing.TypeVar("_ActualT")
"""Actual value that will be None."""

_AlternativeT = typing.TypeVar("_AlternativeT")
"""Alternative value that will be returned if `_ActualT` is None."""

_SINGLETON_LOCK: typing.Final[threading.Lock] = threading.Lock()
"""Lock for accessing to singleton instances."""


@typing.overload
def none_or(alternative: _AlternativeT, actual: typing.Literal[None], /) -> _AlternativeT:
    ...


@typing.overload
def none_or(alternative: _AlternativeT, actual: _ActualT, /) -> _ActualT:
    ...


def none_or(
    alternative: _AlternativeT, actual: typing.Union[_ActualT, typing.Literal[None]], /
) -> typing.Union[_AlternativeT, _ActualT]:
    """Returns alternative value, if actual is None.

    Parameters
    ----------
    alternative : _AlternativeT
        Alternative value that will be returned if `_ActualT` is None.
    actual : typing.Union[_ActualT, typing.Literal[None]]
        Actual value that will be None.

    Returns
    -------
    typing.Union[_AlternativeT, _ActualT]
        `Alternative` value, if `actual` is None, otherwise `actual`.
    """
    return alternative if actual is None else actual


class cached_property:
    """Simple cached property implementation that sets in `self.__dict__`
    function callback by `function.__name__` key.

    !!! warning
        This implementation of `cached_property` will not work with slotted
        classes.

    ??? example "Expand example of usage"
        ``` py hl_lines="15 16 17 18 19 20 21 22"
            class Owner:
                '''Owner class.'''

                def __init__(self) -> None:
                    self._hard_attribute = 1

                def set_new_attribute(self, new: typing.Any, /) -> None:
                    self._hard_attribute = new

                @utils.cached_property
                def some_owner_hard_attribute(self) -> typing.Any:
                    return self._hard_attribute

            >>> own = Owner()
            >>> own.some_owner_hard_attribute
            1
            >>> own.set_new_attribute(2)
            >>> own.some_owner_hard_attribute
            1
            >>> cached_property.update_cache_for(own, "some_owner_hard_attribute")
            >>> own.some_owner_hard_attribute
            2
        ```
    """

    def __init__(self, func: typing.Callable[[_InstanceT], typing.Any], /) -> None:
        """
        Parameters
        ----------
        func : typing.Callable[[_InstanceT], typing.Any]
            Function to cache.
        """
        self.func = func

    def __get__(
        self,
        instance: _InstanceT,
        owner: typing.Optional[typing.Type[typing.Any]] = None,
    ) -> typing.Any:
        """Returns cached function callback.

        Parameters
        ----------
        instance : _InstanceT
            Property instance.
        owner : typing.Optional[typing.Type[typing.Any]] = None
            Property owner.
        """
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result

    @staticmethod
    def update_cache_for(state: _InstanceT, prop_name: str, /) -> None:
        """Updates cached_property on instance by property name.

        Parameters
        ----------
        state : _InstanceT
            Instance to update cached_property for
        prop_name : str
            Property name to update cache for.
        """
        del state.__dict__[prop_name]


class Singleton(type):
    """Metaclass that implements Singleton pattern.

    ??? example "Expand example of usage"
        ```py hl_lines="7 8 9 10 11"
        class Class(metaclass=Singleton):
            def __init__(self) -> None:
                self.attribute = 1

        >>> self = Class()
        >>> self2 = Class()
        >>> self2.attribute
        1
        >>> self.attribute = 2
        >>> self2.attribute
        2
        ```

    Attributes
    ----------
    _instances : dict[typing.Type[typing.Any], typing.Any] = {}
        Dict of instances, where key is Type[instance].
    """

    _instances: dict[typing.Type[typing.Any], typing.Any] = {}

    def __call__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        """Returns thread-safe class instance if exists.

        Parameters
        ----------
        *args : typing.Any
            Argument to type call.
        **kwargs : typing.Any
            Keyword arguments to type call.

        Returns
        -------
        typing.Any
            Class instance.
        """

        if cls not in cls._instances:
            with _SINGLETON_LOCK:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
