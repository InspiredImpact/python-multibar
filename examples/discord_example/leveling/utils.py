__all__ = ("dump_json_async",)

import typing

import ujson
from aiofiles.threadpool.text import AsyncTextIOWrapper


async def dump_json_async(
    aio: AsyncTextIOWrapper,
    /,
    mapping: typing.MutableMapping[str, typing.Any],
    *,
    indent: int = 4,
) -> None:
    """Function for reduce the number of lines of code and improve readability.

    Parameters
    ----------
    aio: AsyncTextIOWrapper, /
        Async text io state.

    mapping: typing.MutableMapping[str, typing.Any]
        Mapping to dumps.

    indent: int = 4, *
        JSON indentation.
    """

    await aio.seek(0)
    await aio.write(ujson.dumps(mapping, indent=indent))
    await aio.truncate()
