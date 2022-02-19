from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

import pytest
from hamcrest import assert_that, equal_to

from multibar import ProgressBar
from multibar.internal import Sector
from tests_basics._tools import (
    has_args,
    has_implemented,
    is_dataclass,
    sequence_of,
    testlogger,
)

if TYPE_CHECKING:
    from multibar.internal import ProgressbarContainer


@pytest.fixture(name="progresstemplate")
def progress_template_object() -> Generator[ProgressbarContainer[Sector], Any, Any]:
    yield ProgressBar(50, 100, length=30).write_progress(fill="+", line="-")


@pytest.mark.usefixtures("testlogger")
@pytest.mark.parametrize("current,total,length", [pytest.param(20, 100, 10)])
def test_progressbar_object(current: int, total: int, length: int) -> None:
    assert_that(ProgressBar, is_dataclass())

    progress = ProgressBar(current, total, length=length).write_progress(fill="+", line="-")

    assert_that(progress.length, equal_to(10))


@pytest.mark.usefixtures("testlogger")
def test_progressbar_sector_container(progresstemplate: ProgressbarContainer[Sector]) -> None:
    assert_that(progresstemplate.bar, sequence_of(Sector))
    assert_that(len(progresstemplate.bar), equal_to(30))
    assert_that(progresstemplate.bar, is_dataclass())
    assert_that(type(progresstemplate.bar), has_implemented("__len__", "__getitem__", "__repr__"))


@pytest.mark.usefixtures("testlogger")
def test_progressbar_state(progresstemplate: ProgressbarContainer[Sector]) -> None:
    assert_that(progresstemplate.state, has_args("current", "total"))
    assert_that(progresstemplate.state.percents(allow_float=False), equal_to(50))
