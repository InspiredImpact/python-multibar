__all__ = ["none_or"]

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
        if not hasattr(instance, "__dict__"):
            # For correct execution of cls.update_cache_for
            return self.func
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result

    @classmethod
    def update_cache_for(cls, state: object, prop_name: str) -> None:
        state_type = type(state)
        origin = getattr(state_type, prop_name)
        delattr(state, prop_name)
        setattr(state_type, prop_name, cls(origin))
