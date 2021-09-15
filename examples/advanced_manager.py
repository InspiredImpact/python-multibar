from __future__ import annotations

import abc
import copy
import types
import typing
import dataclasses
import collections

from multibar import ProgressBar, ProgressObject, ProgressTemplates

if typing.TYPE_CHECKING:
    from multibar.core.variants import CharsSnowflake

    T = typing.TypeVar("T")
    MaybeString = typing.Union[T, str]
    CT = typing.TypeVar("CT", bound=typing.Callable[..., typing.Any])  # Callable type
    _KT = typing.TypeVar("_KT")
    _VT = typing.TypeVar("_VT")

    LogT = typing.TypeVar("LogT", bound=typing.Mapping[typing.Any, typing.Any])
    _ActionType = typing.Literal["left", "right"]
    _ActionPattern = typing.Tuple[str, typing.Dict[str, typing.Any]]


def find_idx_by(predicate: CT, sequence: typing.Sequence[T], /) -> typing.Optional[int]:
    """Find the index of a specific element of the sequence."""
    for index, element in enumerate(sequence):
        if predicate(element):
            return index


class CacheManager(collections.UserDict):
    """Cash, which stores the last actions with the progress bar."""

    def __init__(self, **kwargs: typing.Any) -> None:
        self.maxsize: int = kwargs.pop("maxsize", 8)
        super().__init__(**kwargs)

    def __missing__(self, key: MaybeString[int]) -> typing.Any:
        """Handle both string and integer keys."""
        if isinstance(key, str):
            # Without this check, __missing__ would work for any key, resulting in recursion.
            raise KeyError(key)
        else:
            return self[str(key)]

    def __contains__(self, item: object) -> bool:
        return str(item) in self.data

    def __setitem__(self, key: _KT, value: _VT) -> None:
        self.data[str(key)] = value


@dataclasses.dataclass(frozen=True)
class Action:
    """Object of a certain action with a progress bar."""
    type: _ActionType
    idx: str
    result: typing.Any


class ActionManager:
    """Small interface for working with actions."""

    def __init__(self, action_log: LogT) -> None:
        self.__action_log = action_log

    @property
    def logs(self) -> types.MappingProxyType[_KT, _VT]:
        return types.MappingProxyType(self.__action_log)

    @property
    def last_action(self) -> Action:
        items_list = list(self.__action_log.items())
        return self._from_pattern(items_list[-1])

    @staticmethod
    def _from_pattern(value: _ActionPattern) -> Action:
        dict_: typing.Dict[str, typing.Any] = value[1]
        return Action(dict_["type"], value[0], dict_["result"])

    def last_actions(self) -> typing.List[Action]:
        actions: typing.List[Action] = []
        for item in list(self.__action_log.items()):
            actions.append(self._from_pattern(item))
        return actions


class ManagerABC(metaclass=abc.ABCMeta):
    """Base abstract class to control the methods implementation."""

    def __init__(self, obj: ProgressObject) -> None:
        self.bar = obj.bar
        self._cached_bar = copy.deepcopy(self.bar)
        self._cache = CacheManager()

    def __str__(self) -> str:
        return "".join(i.emoji_name for i in self.bar)

    def __len__(self) -> int:
        return len(self.bar)

    def __getitem__(self, item: typing.Any) -> typing.Any:
        return self.bar[item]

    def cache_action(self, name: _ActionType, result: typing.Any) -> None:
        """Put a certain action in the cache."""
        if len(self._cache) >= self._cache.maxsize:
            self._cache.popitem()

        cls_name = self.__class__.__name__
        idx = find_idx_by(lambda i: result.position == i.position, self._cached_bar)
        if cls_name in self._cache:
            _path = self._cache[cls_name]
        else:
            _path = self._cache

        _path.update({idx: {"type": name, "result": result}})

    @property
    def cache(self) -> types.MappingProxyType[_KT, _VT]:
        """Returning cache as proxy."""
        return types.MappingProxyType(self._cache)

    @abc.abstractmethod
    def popleft(self) -> None:
        """Removing first sector of progressbar."""

    @abc.abstractmethod
    def popright(self) -> None:
        """Removing last sector of progressbar."""

    @abc.abstractmethod
    def to_dict(self) -> typing.Dict[str, _VT]:
        """Converting current state to dict."""


class DequeManager(ManagerABC):
    """A class for working with progress bars of the :class:`collections.deque`."""

    def popleft(self) -> None:
        _ = self.bar.popleft()
        self.cache_action("left", _)

    def popright(self) -> None:
        _ = self.bar.pop()
        self.cache_action("right", _)

    def to_dict(self) -> typing.Dict[str, _VT]:
        attrs = dict(self.__dict__)
        return attrs


class ListManager(ManagerABC):
    """A class for working with progress bars of the :class:`builtins.list`."""

    def popleft(self) -> None:
        # From the point of view of speed,
        # I do not recommend using this method,
        # because the lists for this are not
        # so well optimized and shifting the
        # entire queue can take O(n) time.
        _ = self.bar.pop(0)
        self.cache_action("left", _)

    def popright(self) -> None:
        _ = self.bar.pop()
        self.cache_action("right", _)

    def to_dict(self) -> typing.Dict[str, _VT]:
        attrs = dict(self.__dict__)
        return attrs


class ProgressInitiator:
    """
    The main initializer class that accepts parameters
    on which further work will depend.
    """

    def __init__(self, progressbar: ProgressBar) -> None:
        self.progressbar = progressbar

    def init_progress(self, chars: CharsSnowflake) -> ManagerABC:
        """
        Depending on the context, it determines what type of
        progress bar needs to be created and returns it.
        """
        if isinstance(self.progressbar, ProgressBar):
            progressbar = self.progressbar.write_progress(**chars)
            if self.progressbar.deque:
                return DequeManager(progressbar)
            else:
                return ListManager(progressbar)
        else:
            raise TypeError("Progressbar is already initialized")


if __name__ == "__main__":
    initiator = ProgressInitiator(ProgressBar(40, 100))
    progress_manager = initiator.init_progress(ProgressTemplates.DEFAULT)
    action_manager = ActionManager(progress_manager._cache)

    print("Progress manager:", progress_manager)
    progress_manager.popleft()
    print("Length after popleft():", len(progress_manager))
    progress_manager.popright()
    print("Length after popright():", len(progress_manager))
    print("Progress manager cached actions:", progress_manager.cache)

    print("Last actioN:", action_manager.last_action)
    print("Last actionS:", action_manager.last_actions())

    # __missing__ and __contains__
    print(0 in progress_manager.cache)
    print('0' in progress_manager.cache)
