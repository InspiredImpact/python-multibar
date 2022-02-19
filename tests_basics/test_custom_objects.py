from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Iterable, List, Union, overload

import pytest
from hamcrest import assert_that, equal_to, instance_of

from multibar import ProgressBar
from multibar.interfaces import (
    AbstractCustomerMixin,
    AbstractSectorMixin,
    AbstractSeqBasedContainerMixin,
)
from multibar.internal import Sector
from tests_basics._tools import has_args, testlogger

if TYPE_CHECKING:
    from multibar.internal import ProgressContainer

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("testlogger")
def test_custom_sector() -> None:
    class CustomSector(AbstractSectorMixin):
        def __init__(
            self,
            name: str,
            position: int,
            some_custom_var: int = 20,
            empty: bool = False,
        ) -> None:
            super().__init__(
                name=name,
                position=position,
                empty=empty,
            )
            self.custom_var = some_custom_var

        def __repr__(self) -> str:
            return self.name

        def __hash__(self) -> int:
            return hash(self.custom_var)

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, CustomSector):
                return other.custom_var == self.custom_var
            return NotImplemented

        def double_var(self) -> int:
            return self.custom_var * 2

    progress = ProgressBar(10, 20, sector_cls=CustomSector).write_progress(
        fill="+", line="-", some_custom_var=10
    )

    assert_that(progress.bar[0], instance_of(CustomSector))
    assert_that(progress.bar[0].double_var(), equal_to(20))


@pytest.mark.usefixtures("testlogger")
def test_custom_container() -> None:
    class CustomContainer(AbstractSeqBasedContainerMixin[Sector]):
        def __init__(self) -> None:
            self._storage: List[Sector] = []

        def __repr__(self) -> str:
            return "".join(i.name for i in self._storage)

        def __len__(self) -> int:
            return len(self._storage)

        @overload
        def __getitem__(self, item: int) -> Sector:
            ...

        @overload
        def __getitem__(self, item: slice) -> Iterable[Sector]:
            ...

        def __getitem__(
            self,
            item: Union[int, slice],
        ) -> Union[Sector, Iterable[Sector]]:
            return self._storage[item]

        def finalize(self) -> None:
            logger.debug("Bar container was succesfullly created.")

        def view(self) -> Iterable[Sector]:
            for sector in self._storage:
                yield sector

        def put(self, item: Sector) -> None:
            self._storage.append(item)

        def some_custom_method(self) -> str:
            return "yes" if self._storage else "no"

    bar = ProgressBar(10, 20, container_cls=CustomContainer)
    progress = bar.write_progress(fill="+", line="-")

    assert_that(progress.bar, instance_of(CustomContainer))
    assert_that(progress.bar, has_args("some_custom_method"))


@pytest.mark.usefixtures("testlogger")
def test_customer() -> None:
    bar = ProgressBar(8, 20)

    class Customer(AbstractCustomerMixin):
        def fill(self, ctx: ProgressContainer) -> Any:
            if ctx.percents(allow_float=False) < 50:
                return "1"
            return "2"

        def line(self, ctx: ProgressContainer) -> Any:
            if ctx.percents(allow_float=False) > 50:
                return "3"
            return "4"

        def start(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def end(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def unfilled_start(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def unfilled_end(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

    progress = bar.write_from_customer(customer=Customer)
    assert_that(str(progress.bar), equal_to("11111111444444444444"))  # percents < 50

    other_bar = ProgressBar(15, 20)
    other_progress = other_bar.write_from_customer(customer=Customer)
    assert_that(
        str(other_progress.bar), equal_to("22222222222222233333")
    )  # line value changed (percents > 50)
