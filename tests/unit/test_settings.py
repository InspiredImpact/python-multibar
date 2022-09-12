import copy

from hamcrest import assert_that, is_in, instance_of, equal_to, calling, raises, not_

from multibar.settings import settings


class TestSettings:
    def test_settings_copy(self) -> None:
        settings_copy = settings.copy()
        supports_copy = copy.copy(settings)

        settings_copy.configure(key="value")

        assert_that("key", is_in(settings_copy))
        assert_that("key", not_(is_in(settings)))

        supports_copy.configure(key="value")

        assert_that("key", is_in(supports_copy))
        assert_that("key", not_(is_in(settings)))

    def test_settings_state(self) -> None:
        mock_settings = settings.copy()

        assert_that("_config", is_in(mock_settings.__dict__))

    def test_settings_get(self) -> None:
        mock_settings = settings.copy()
        mock_settings.__dict__["__dunder__"] = "I'm dunder."

        assert_that(mock_settings.__dunder__, instance_of(str))
        assert_that(mock_settings["__dunder__"], instance_of(str))

        mock_settings.configure(non_dunder="non_dunder")

        assert_that(mock_settings.non_dunder, equal_to("non_dunder"))
        assert_that(mock_settings["non_dunder"], equal_to("non_dunder"))

        mock_settings.configure(__new_dunder__="new_dunder")

        # Because all dunder-attrs getting from self.__dict__
        assert_that(calling(lambda: mock_settings["__new_dunder__"]), raises(KeyError))
        assert_that(calling(lambda: mock_settings.__new_dunder__), raises(KeyError))

    def test_setting_in(self) -> None:
        mock_settings = settings.copy()

        class NonHashableMock:
            __hash__ = None

        non_hashable_mock = NonHashableMock()
        mock_settings.configure(non_hashable=non_hashable_mock)

        # Hashable keys are searching in dict.keys()
        assert_that("non_hashable", is_in(mock_settings))
        # Non-hashable keys are searching in dict.values()
        assert_that(non_hashable_mock, is_in(mock_settings))
