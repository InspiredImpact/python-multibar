import typing

from bar.enums import CallbackAs


__all__: typing.Sequence[str] = (
    'ReturnAs',
)


ReturnAs = typing.Union[
    typing.Literal[CallbackAs.default, CallbackAs.callable, CallbackAs.awaitable],
    typing.Literal[1, 2, 3]
]
