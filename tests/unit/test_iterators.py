import collections.abc

import pytest
from hamcrest import assert_that, instance_of, is_in, equal_to

from multibar import iterators
from tests.pyhamcrest import subclass_of


def test_iterator() -> None:
    iterator = iterators.Iterator(iter(()))

    assert_that(iterators.Iterator, subclass_of(collections.abc.Iterator))
    assert_that(iterator, instance_of(collections.abc.Iterator))

    assert_that("_iterator", is_in(iterator.__slots__))

    with pytest.raises(StopIteration):
        next(iterator)


def test_convertable_index_iterator() -> None:
    iterator1 = iterators.Iterator(iter((24, 235, 34)))
    assert_that(list(iterator1.indexes()), equal_to([0, 1, 2]))

    iterator2 = iterators.Iterator(iter((34, 6546, 32)))
    assert_that(list(iterator2.indexes(conversion=lambda i: i + 1)), equal_to([1, 2, 3]))
