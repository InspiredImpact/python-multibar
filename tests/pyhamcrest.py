from __future__ import annotations

__all__ = ("subclass_of",)

import typing

from hamcrest.core.base_matcher import BaseMatcher

if typing.TYPE_CHECKING:
    from hamcrest.core.description import Description


class IsSubclassOf(BaseMatcher):
    def __init__(
        self,
        cls_or_tuple: typing.Union[typing.Type[typing.Any], tuple[typing.Type[typing.Any], ...]], /
    ) -> None:
        self._cls_or_tuple = cls_or_tuple
        self.failed: typing.Optional[str] = None

    def _matches(self, cls: typing.Type[typing.Any]) -> bool:
        result = issubclass(cls, self._cls_or_tuple)
        if not result:
            self.failed = cls
        return result

    def describe_to(self, description: Description) -> None:
        (
            description.append_text("failing on ").append_text(
                f"<{self.failed}> attribute"
            )
        )


def subclass_of(
    cls_or_tuple: typing.Union[typing.Type[typing.Any], tuple[typing.Type[typing.Any], ...]], /
) -> IsSubclassOf:
    return IsSubclassOf(cls_or_tuple)

