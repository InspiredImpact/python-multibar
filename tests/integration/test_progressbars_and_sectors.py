import typing

from hamcrest import assert_that, equal_to, has_length, has_properties, not_

from multibar.api.sectors import AbstractSector
from multibar.impl.progressbars import Progressbar
from multibar.impl.sectors import Sector

_T = typing.TypeVar("_T")


def test_progressbar_and_sectors() -> None:
    progressbar = Progressbar()

    sector_name: typing.Literal["name"] = "name"
    sector_pos: typing.Literal[0] = 0

    # Progressbar tested in tests/unit/impl/test_progressbars
    assert_that(progressbar.sectors, has_length(0))

    progressbar.add_sector(Sector(sector_name, True, sector_pos))
    assert_that(progressbar.sectors, has_length(1))

    # Sector properties tested in tests/unit/impl/test_sectors
    assert_that(progressbar.sectors[0].name, equal_to(sector_name))

    new_sector_name: typing.Literal["new_name"] = "new_name"

    progressbar.replace_display_name_for(sector_pos, new_sector_name)
    assert_that(progressbar.sectors[0].name, not_(equal_to(sector_name)))
    assert_that(progressbar.sectors[0].name, equal_to(new_sector_name))


def test_for_each() -> None:
    progressbar_state = Progressbar()
    progressbar_state.add_sector(Sector("hello", True, 0)).add_sector(Sector("world", True, 0))
    progressbar_state.for_each(lambda s: s.change_name("hello world"))

    assert_that(
        progressbar_state[0],
        has_properties(
            {
                "name": "hello world",
            },
        ),
    )
    assert_that(
        progressbar_state[1],
        has_properties(
            {
                "name": "hello world",
            },
        ),
    )


def test_set_sectors() -> None:
    progressbar_state = Progressbar()
    progressbar_state.add_sector(Sector("hello", True, 0))
    sectors = [Sector("hello world", True, 0)]
    progressbar_state = progressbar_state.set_new_sectors(sectors)

    assert_that(
        progressbar_state[0],
        has_properties(
            {
                "name": "hello world",
            },
        ),
    )


def test_map() -> None:
    class SectorImpl(AbstractSector):
        add_to_progressbar = change_name = name = is_filled = position = lambda *_, **__: None

        def extended_method(self) -> int:
            return len(self._name)

    progressbar_state = Progressbar()
    progressbar_state.add_sector(SectorImpl("hello", True, 0))

    def _map_function(sector: _T, /) -> _T:
        sector.name_length = len(sector._name)
        return sector

    new_progressbar_state = progressbar_state.map(_map_function)
    first_sector = new_progressbar_state[0]
    assert_that(
        first_sector,
        has_properties(
            {
                "name_length": len(first_sector._name),
            },
        ),
    )
    assert_that(first_sector.extended_method(), equal_to(len(first_sector._name)))
