"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typing


__all__: typing.Sequence[str] = (
    "ProgressError",
    "MissingRequiredArguments",
    "ProgressInvokeError",
    "CannotFindReference",
    "BadValue",
    "BadValueSpecified",
    "BadCallbackTypeSpecified",
)


""" Exception hierarchy

ProgressError:
    MissingRequiredArguments
    ProgressInvokeError
    CannotFindReference

    BadValue:
        BadCallbackTypeSpecified
        BadValueSpecified
"""


class ProgressError(Exception):
    """``|exception|``

    Base exception from which all others in this library inherit.
    """


class MissingRequiredArguments(ProgressError):
    """``|exception|``

    Raised when no required arguments are specified.

    Parameters:
    -----------
    *args: :class:`Any`
        Missing arguments.
    """

    def __init__(self, *args: typing.Any) -> None:
        super().__init__(f"Missing required args: {args}")


class ProgressInvokeError(ProgressError):
    """``|exception|``

    Used at some point to reraise an error.

    Parameters:
    -----------
    original_exc: :class:`BaseException`
        The error that was originally caused.
    """

    def __init__(self, exc: BaseException) -> None:
        self.original_exc = exc
        super().__init__(f"Function raised an exception: {exc.__class__.__name__}: {exc}")


class CannotFindReference(ProgressError):
    """``|exception|``

    Raised when a reference to a specific object is not found.

    Parameters:
    -----------
    reference: :class:`str`
        Object reference that was not found.
    """

    def __init__(self, reference: str) -> None:
        super().__init__(reference)


class BadValue(ProgressError):
    """``|exception|``

    Basic error for the category of exceptions that are
    thrown when an invalid value is specified.
    """


class BadCallbackTypeSpecified(BadValue):
    """``|exception|``

    Raised when an invalid value is specified for the callback setting.

    Parameters:
    -----------
    received: :class:`Any`
        The parameter that is received.

    expected: :class:`str`
        Parameter that was expected.
    """

    def __init__(self, received: typing.Any, expected: str) -> None:
        super().__init__(f"Got {received}, expected {expected}:")


class BadValueSpecified(BadValue):
    """``|exception|``

    Raised when an invalid value has been specified.
    """
