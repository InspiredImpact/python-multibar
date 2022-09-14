import typing

from hamcrest import assert_that, equal_to, has_length, not_

from multibar.impl.progressbars import Progressbar
from multibar.impl.sectors import Sector


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
