from __future__ import annotations

import collections.abc
import copy
import typing

SelfT = typing.TypeVar("SelfT", bound="Settings")


def _config_get_function(self: SelfT, key: str) -> typing.Any:
    if key[:2] != "__":
        return self._config[key]
    return self.__dict__[key]


class Settings:
    __slots__ = ("_config",)

    __getattr__ = __getitem__ = _config_get_function

    def __init__(self) -> None:
        self._config: dict[str, typing.Any] = {}

    def __contains__(self, item: typing.Any) -> bool:
        if not isinstance(item, collections.abc.Hashable):
            return item in self._config.values()
        return item in self._config

    def __copy__(self) -> Settings:
        return self.copy()

    def __deepcopy__(
        self,
        memodict: typing.Optional[dict[int, typing.Any]] = None,
        /,
    ) -> Settings:
        return self.deepcopy(memodict)

    def copy(self) -> Settings:
        new_instance = self.__class__()
        new_instance.configure(**self._config)
        return new_instance

    def deepcopy(self, memodict: typing.Optional[dict[int, typing.Any]] = None, /) -> Settings:
        if memodict is None:
            memodict = {}

        state = self.__class__()
        memodict[id(self)] = state
        for slot in self.__slots__:
            self_value = getattr(self, slot)
            setattr(state, slot, copy.deepcopy(self_value, memodict))

        return state

    def configure(self, **kwargs: typing.Any) -> None:
        self._config.update(kwargs)


settings = Settings()
