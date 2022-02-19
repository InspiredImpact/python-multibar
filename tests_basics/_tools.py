from __future__ import annotations

__all__ = ["testlogger", "is_dataclass", "sequence_of", "has_implemented", "has_args"]

import logging
from dataclasses import is_dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Generator,
    Generic,
    Iterable,
    Optional,
    Type,
    TypeVar,
    Union,
)

import pytest
from hamcrest.core.base_matcher import BaseMatcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description

T = TypeVar("T")


@pytest.fixture()
def testlogger() -> Generator[logging.Logger, Any, None]:
    logger = logging.getLogger()
    logger.info("Running function object test...")
    yield logger
    logger.info("Testing complete.")


class IsDataclass(BaseMatcher, Generic[T]):
    def __init__(self) -> None:
        self.failed: Optional[str] = None

    def _matches(self, item: Type[T]) -> bool:
        if not is_dataclass(item):
            self.failed = item.__name__
            return False
        return True

    def describe_to(self, description: Description) -> None:
        (description.append_text("failing on ").append_text(f"<{self.failed}> attribute"))


class SequenceOf(BaseMatcher, Generic[T]):
    def __init__(self, *, type: Type[T]) -> None:
        self.type = type
        self.failed_on: Optional[str] = None

    def _matches(self, iterable: Iterable[Union[Type[T], Any]]) -> bool:
        for element in iterable:
            if not isinstance(element, self.type):
                self.failed_on = type(element)
                return False
        return True

    def describe_to(self, description: Description) -> None:
        (description.append_text("failing on ").append_text(f"{self.failed_on} element"))


InstanceT = TypeVar("InstanceT", bound=object)


class HasImplemented(BaseMatcher, Generic[InstanceT]):
    def __init__(self, *methods: str) -> None:
        self.methods = methods
        self.failed_on: Optional[str] = None

    def _matches(self, item: InstanceT) -> bool:
        for method in self.methods:
            if method not in item.__dict__ or item.__dict__[method] is None:
                self.failed_on = method
                return False
        return True

    def describe_to(self, description: Description) -> None:
        (description.append_text("failing on ").append_text(f"{self.failed_on} method"))


class HasAttributes(BaseMatcher, Generic[T]):
    def __init__(self, *attrs: str) -> None:
        self.attrs = attrs
        self.failed: Optional[str] = None

    def _matches(self, item: T) -> bool:
        for attr in self.attrs:
            if not hasattr(item, attr):
                self.failed = attr
                return False
        return True

    def describe_to(self, description: Description) -> None:
        (description.append_text("failing on ").append_text(f"<{self.failed}> attribute"))


def is_dataclass() -> Type[IsDataclass[T]]:
    return IsDataclass


def sequence_of(type: Type[T]) -> SequenceOf[T]:
    return SequenceOf(type=type)


def has_implemented(*methods: str) -> HasImplemented[InstanceT]:
    return HasImplemented(*methods)


def has_args(*attributes: str) -> HasAttributes[T]:
    return HasAttributes(*attributes)
