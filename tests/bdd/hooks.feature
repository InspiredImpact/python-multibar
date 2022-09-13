@fixture.multibar.impl.hooks
Feature: Hooks step by step testing
    """Behavior-driven development Hook Tests

    In this case, it is very convenient to use the BDD methodology
    with python "behave" tool.

    "behave" allows you to give one context to all Features,
    which is very handy in out case:
        1)  We create hooks, test their behavior and implement them in context.
        2)  We get hooks from the context, test the mechanics of adding hooks,
            then update the context.
        3)  We getting updated hooks from the context, run all callbacks
            hooks according to the provided "hooks" template.

    This allows you to make the code cleaner, because you no need to
    create new class instances.
    """

    Scenario: Testing base behave
        Given we have a created instance of the Hooks class
        Then we are testing its basic behavior

    Scenario: Test adding hook callbacks
        When we add new callbacks using the HooksAware interface
        Then these callbacks are stored in special attributes that represent lists

    Scenario Template: Test triggering any hook callbacks
        """Scenario template for all hook callbacks

        This template provides all implemented types of callbacks for an instance of
        the Hooks class.
        """
        Then we run all the <hook> hook callbacks and compare it with scenario examples <callback>

        Examples: Hook trigger function names
            | hook                 | callback |
            | on_error_hooks       | True     |
            | pre_execution_hooks  | True     |
            | post_execution_hooks | True     |
