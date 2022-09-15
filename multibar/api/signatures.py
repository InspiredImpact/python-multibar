__all__ = (
    "SignatureSegmentProtocol",
    "ProgressbarSignatureProtocol",
)

import typing


@typing.runtime_checkable
class SignatureSegmentProtocol(typing.Protocol):
    """Signature segment protocol (protocol for one char, that has two states).

    Examples
    --------
    >>> import dataclasses
    ...
    >>> @dataclasses.dataclass
    ... class SignatureSegment:
    ...     on_filled: str = dataclasses.field(default="+")
    ...     on_unfilled: str = dataclasses.field(default="-")
    ...
    >>> isinstance(SignatureSegment(), SignatureSegmentProtocol)
    True

    >>> def function_that_accepts_signature_segment(
    ...     segment: SignatureSegmentProtocol, /
    ... ) -> tuple[str, str]:
    ...     return segment.on_filled, segment.on_unfilled
    ...
    >>> function_that_accepts_signature_segment(SignatureSegment())  # Mypy happy :)
    ('+', '-')
    """

    @property
    def on_filled(self) -> str:
        """
        Returns
        -------
        str
            On filled state.
        """
        raise NotImplementedError

    @property
    def on_unfilled(self) -> str:
        """
        Returns
        -------
        str
            On unfilled state.
        """
        raise NotImplementedError


@typing.runtime_checkable
class ProgressbarSignatureProtocol(typing.Protocol):
    """Signature protocol.

    Examples
    --------
    >>> import dataclasses
    >>> from unittest.mock import Mock  # mock for signature segment
    ...
    >>> @dataclasses.dataclass
    ... class Signature:
    ...     start: SignatureSegmentProtocol = dataclasses.field(default=Mock())
    ...     middle: SignatureSegmentProtocol = dataclasses.field(default=Mock())
    ...     end: SignatureSegmentProtocol = dataclasses.field(default=Mock())
    ...
    >>> def function_that_checks_signature(
    ...     signature: ProgressbarSignatureProtocol, /
    ... ) -> bool:
    ...     return isinstance(signature, ProgressbarSignatureProtocol)
    ...
    >>> function_that_checks_signature(Signature())  # Mypy happy :)
    True
    """

    @property
    def start(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar start char.
        """
        raise NotImplementedError

    @property
    def end(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar end char.
        """
        raise NotImplementedError

    @property
    def middle(self) -> SignatureSegmentProtocol:
        """
        Returns
        -------
        SignatureSegmentProtocol
            Progressbar middle char (between start and and).
        """
        raise NotImplementedError
