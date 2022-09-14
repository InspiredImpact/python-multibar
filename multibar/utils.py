__all__ = ("none_or", "cached_property")

import typing

_ActualT = typing.TypeVar("_ActualT")
_AlternativeT = typing.TypeVar("_AlternativeT")


@typing.overload
def none_or(alternative: _AlternativeT, actual: typing.Literal[None], /) -> _AlternativeT:
    ...


@typing.overload
def none_or(alternative: _AlternativeT, actual: _ActualT, /) -> _ActualT:
    ...


def none_or(
    alternative: _AlternativeT, actual: typing.Union[_ActualT, typing.Literal[None]], /
) -> typing.Union[_AlternativeT, _ActualT]:
    if actual is None:
        return alternative
    return actual


class cached_property:
    def __init__(self, func: typing.Callable[..., typing.Any], /) -> None:
        self.func = func

    def __get__(
        self,
        instance: object,
        owner: typing.Optional[typing.Type[typing.Any]] = None,
    ) -> typing.Any:
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result

    @staticmethod
    def update_cache_for(state: object, prop_name: str, /) -> None:
        del state.__dict__[prop_name]
