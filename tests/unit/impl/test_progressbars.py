import collections.abc
import typing
from unittest.mock import Mock

from hamcrest import assert_that, has_length, has_properties, instance_of

from multibar.api.progressbars import ProgressbarAware
from multibar.impl.progressbars import Progressbar
from tests.pyhamcrest import subclass_of


@typing.runtime_checkable
class SupportsGetitem(typing.Protocol):
    def __getitem__(self, item: typing.Any) -> typing.Any:
        raise NotImplementedError


@typing.runtime_checkable
class SupportsIter(typing.Protocol):
    def __iter__(self) -> typing.Iterator[typing.Any]:
        raise NotImplementedError


class TestProgressbars:
    def test_base(self) -> None:
        progressbar_state = Progressbar()

        assert_that(Progressbar, subclass_of(ProgressbarAware))
        assert_that(Progressbar, subclass_of(collections.abc.Iterable))
        assert_that(progressbar_state, instance_of(SupportsGetitem))

        assert_that(
            progressbar_state,
            has_properties(
                {
                    "storage": instance_of(SupportsIter),
                    "length": instance_of(int),
                },
            ),
        )
        assert_that(type(progressbar_state.storage), subclass_of(collections.abc.Sequence))

    def test_add_sector(self) -> None:
        progressbar = Progressbar()
        assert_that(progressbar.storage, has_length(0))

        progressbar.add_sector(Mock())
        assert_that(progressbar.storage, has_length(1))
