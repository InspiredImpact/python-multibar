import typing

import parse
from behave import register_type
from behave.fixture import fixture, use_fixture_by_tag

from multibar.impl.hooks import Hooks


@parse.with_pattern(r"(?i)true|false")
def parse_boolean(text: str) -> bool:
    return text.lower() == "true"


@fixture()
def config_emulation_fixture(context: typing.Any) -> typing.Iterator[str]:
    context.hooks = hooks = Hooks()
    yield hooks


fixture_registry: typing.MutableMapping[str, typing.Callable[[typing.Any], typing.Any]] = {
    "fixture.multibar.impl.hooks": config_emulation_fixture,
}


def before_tag(context: typing.Any, tag: str) -> typing.Any:
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)


register_type(Boolean=parse_boolean)
