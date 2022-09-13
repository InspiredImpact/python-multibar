import typing

from behave import use_fixture


def use_fixture_by_tag(
    tag: str,
    context: typing.Any,
    fixture_registry: typing.MutableMapping[typing.Hashable, typing.Callable[..., typing.Any]],
) -> typing.Any:
    fixture_data = fixture_registry.get(tag, None)
    if fixture_data is None:
        raise LookupError(f"Unknown fixture-tag: {tag}")

    fixture_func = fixture_data
    return use_fixture(fixture_func, context)
