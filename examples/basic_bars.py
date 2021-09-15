import asyncio

from multibar import ProgressBar, MusicBar, ProgressTemplates, ProgressObject, MusicTemplates


def get_progress(now: int, needed: int, /) -> ProgressObject:
    """Writing sync progress."""
    bar = ProgressBar(now, needed, length=30)
    return bar.write_progress(**ProgressTemplates.DEFAULT)


def get_music_progress(current: int, total: int, /) -> ProgressObject:
    """Writing sync music progress."""
    musicbar = MusicBar(current, total, length=15)
    return musicbar.write_progress(**MusicTemplates.CHARS)


async def async_get_progress(
    now: int, needed: int, /, *, loop: asyncio.AbstractEventLoop
) -> ProgressObject:
    """Writing async progress."""
    bar = ProgressBar(now, needed)
    return await bar.async_write_progress(ProgressTemplates.DEFAULT, loop=loop)


async def async_get_music_progress(
    current: int, total: int, /, *, loop: asyncio.AbstractEventLoop
) -> ProgressObject:
    """Writing async music progress."""
    musicbar = MusicBar(current, total)
    return await musicbar.async_write_progress(MusicTemplates.CHARS, loop=loop)


if __name__ == "__main__":
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
    for progress in (
        get_progress(10, 100),
        get_music_progress(50, 100),
        loop.run_until_complete(async_get_progress(30, 100, loop=loop)),
        loop.run_until_complete(async_get_music_progress(60, 100, loop=loop))
    ):
        print(str(progress), f"{progress.percents}%", f"{progress.now}/{progress.needed}")
