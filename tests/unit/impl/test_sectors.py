import typing

from hamcrest import assert_that, equal_to, has_properties, instance_of, not_

from multibar.api.sectors import AbstractSector
from multibar.impl.sectors import Sector
from tests.pyhamcrest import subclass_of


class TestSectors:
    def test_base(self) -> None:
        sector_state = Sector("name", True, 0)
        assert_that(Sector, subclass_of(AbstractSector))

        assert_that(
            sector_state,
            has_properties(
                {
                    "name": instance_of(str),
                    "is_filled": instance_of(bool),
                    "position": instance_of(int),
                },
            ),
        )

    def test_change_name(self) -> None:
        sector_name: typing.Literal["name"] = "name"
        sector_state = Sector("name", True, 0)

        assert_that(sector_state.name, equal_to(sector_name))

        new_name: typing.Literal["new_name"] = "new_name"

        sector_state.change_name(new_name)
        assert_that(sector_state.name, not_(equal_to(sector_name)))
        assert_that(sector_state.name, equal_to(new_name))
