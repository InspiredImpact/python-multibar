from hamcrest import assert_that, has_length

from multibar.impl.hooks import Hooks
from tests.utils import ConsoleOutputInterceptor


class TestHooks:
    def test_trigger_all_hook_callbacks(self) -> None:
        hooks = Hooks()

        # Hooks-add part tested on tests/bdd/steps/hooks_step.py
        hooks.add_on_error(lambda *args, **kwargs: print("Hello World!"))
        hooks.add_post_execution(lambda *args, **kwargs: print("Hello World!"))
        hooks.add_pre_execution(lambda *args, **kwargs: print("Hello World!"))

        # Console output interceptor used because hooks does not return anything
        with ConsoleOutputInterceptor() as on_error_output:
            hooks.trigger_on_error()

        assert_that(on_error_output, has_length(1))

        with ConsoleOutputInterceptor() as on_pre_execution:
            hooks.trigger_pre_execution()

        assert_that(on_pre_execution, has_length(1))

        with ConsoleOutputInterceptor() as on_post_execution:
            hooks.trigger_post_execution()

        assert_that(on_post_execution, has_length(1))
