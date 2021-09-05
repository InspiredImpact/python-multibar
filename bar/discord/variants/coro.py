import typing


__all__: typing.Sequence[str] = (
    'Coro',
    'CoroFunc',
)


T = typing.TypeVar('T')
Coro = typing.Coroutine[typing.Any, typing.Any, T]
CoroFunc = typing.Callable[..., Coro[typing.Any]]
