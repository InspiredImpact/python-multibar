from hamcrest import assert_that, not_, is_in, equal_to

from multibar.utils import cached_property, none_or


class MockClass:
    def __init__(self) -> None:
        self.state_attr: int = 2

    @cached_property
    def mock_property(self) -> int:
        return self.state_attr ** 1_000


class TestCachedProperty:
    def test_assert_property_in_cache(self) -> None:
        fake_instance = MockClass()
        assert_that("mock_property", not_(is_in(fake_instance.__dict__)))

        # Getting attr for prop caching
        getattr(fake_instance, "mock_property")

        assert_that("mock_property", is_in(fake_instance.__dict__))

    def test_cachedproperty_update_cache(self) -> None:
        fake_instance = MockClass()
        assert_that("mock_property", not_(is_in(fake_instance.__dict__)))

        # Getting attr for prop caching
        raw_value = fake_instance.mock_property

        assert_that("mock_property", is_in(fake_instance.__dict__))

        fake_instance.state_attr = 3
        value_from_cache = fake_instance.mock_property
        assert_that(value_from_cache, equal_to(raw_value))

        cached_property.update_cache_for(fake_instance, "mock_property")
        # Getting attr for updating prop cache
        new_raw_value = fake_instance.mock_property
        new_value_from_cache = fake_instance.mock_property

        assert_that(new_raw_value, equal_to(new_value_from_cache))
        assert_that(new_raw_value, not_(equal_to(value_from_cache)))


class TestNoneOr:
    def test_actual_is_none(self) -> None:
        cls = None
        result = none_or(int, cls)

        assert_that(result, equal_to(int))

    def test_actual_is_not_none(self) -> None:
        cls = float
        result = none_or(int, cls)

        assert_that(result, equal_to(float))
