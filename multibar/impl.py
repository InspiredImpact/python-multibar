from __future__ import annotations

__all__ = ["ProgressBar"]

import asyncio
from dataclasses import dataclass
from functools import partial
from typing import Any, Coroutine, Generic, Optional, Type, TypeVar, cast

from multibar.flags import FillFlag
from multibar.interfaces.containers import AbstractSeqBasedContainerMixin
from multibar.interfaces.customer import AbstractCustomerMixin
from multibar.interfaces.product import AbstractSectorMixin
from multibar.internal.crate import (
    ProgressbarContainer,
    ProgressContainer,
    SectorContainer,
)
from multibar.internal.factories import SphinxSectorFactory
from multibar.internal.product import Sector
from multibar.pytypes import NoneType, NotImplementedType

_AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)
_AbcContainerT_co = TypeVar("_AbcContainerT_co", bound=AbstractSeqBasedContainerMixin[Any], covariant=True)


@dataclass
class ProgressBar(Generic[_AbcSectorT_co, _AbcContainerT_co]):
    """``dataclass``
    Class that creates progress bars.

    Raises:
    -------
    :class:`AssertionError`:
        1) If :current: parameter more that :total:.
        2) If :current: parameter less than 0.

    Parameters:
    -----------
    current: :class:`int`
        Current progress value.

        !!! Note:
            Current progress value cannot be less than 0,
            otherwise AssertionError will be raised.

    total: :class:`int`
        Needed progress value.

        !!! Note:
            Current progress value cannot be less than :current:,
            otherwise AssertionError will be raised.

    length: :class:`int` = 20
        Length of progress bar.

    sector_cls: :class:`Optional[Type[AbstractSectorMixin]]` = None
        Custom Sector implementation.

        For more information and examples see:
            https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

    container_cls: :class:`Optional[
        Type[AbstractSeqBasedContainerMixin[AbstractSectorMixin]]
    ] = None`
        Custom container implementation.

        For more information and examples see:
            https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
    """

    current: int
    total: int
    length: int = 20
    sector_cls: Optional[Type[_AbcSectorT_co]] = None
    container_cls: Optional[Type[_AbcContainerT_co]] = None

    def __post_init__(self) -> None:
        assert self.current >= 0, "Current progress cannot be less than 0."
        assert self.current <= self.total, "Current progress cannot be more than total progress."

        if self.container_cls is None:
            self.container_cls = SectorContainer  # type: ignore[assignment]

        self.factory: SphinxSectorFactory[AbstractSectorMixin] = SphinxSectorFactory.from_bind(
            sector_type=cast(
                Type[AbstractSectorMixin], Sector if self.sector_cls is None else self.sector_cls
            )
        )

    def write_progress(
        self,
        *args: Any,
        fill: str,
        line: str,
        start: Optional[str] = None,
        unfilled_start: Optional[str] = None,
        end: Optional[str] = None,
        unfilled_end: Optional[str] = None,
        **kwargs: Any,
    ) -> ProgressbarContainer[_AbcSectorT_co]:
        # TODO: Maybe adapter?
        #  Somehow the method signature with *args and **kwargs does not look very good...
        """``sync method``
        Method that generates synchronously progress bar.

        *args: :class:`Any`
            Args that will be passed in custom Sector implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

        fill: :class:`str`
            Fill character of progress bar.

            !!! Abstract:
                This symbol is used on first fill (depending on progress).

        line: :class:`str`
            Fill character of progress bar.

            !!! Abstract:
                This symbol is used on last (second) fill (depending on progress).

        start: :class:`Optional[str]` = None
            If passed, will replace first FILLED emoji of progress bar (depending on progress).

        unfilled_start: :class:`Optional[str]` = None
            If passed, will replace first EMPTY emoji of progress bar (depending on progress).

        end: :class:`Optional[str]` = None
            If passed, will replace last FILLED emoji of progress bar (depending on progress).

        unfilled_end: :class:`Optional[str]` = None
            If passed, will replace last EMPTY emoji of progress bar (depending on progress).

        **kwargs: :class:`Any`
            Kwargs that will be passed in custom Container implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
        """
        progress = ProgressContainer(self.current, self.total)
        percents = progress.percents(allow_float=False)
        assert self.container_cls is not None

        with self.container_cls() as container:
            for i in range(rest := (round(percents / (100 / self.length)))):
                container.put(
                    self.factory.create_product(
                        *args,
                        name=fill,
                        position=i,
                        empty=False,
                        **kwargs,
                    )
                )

            for i in range(self.length - rest):
                container.put(
                    self.factory.create_product(
                        *args,
                        name=line,
                        position=i + rest,
                        empty=True,
                        **kwargs,
                    )
                )

            # Add `unfilled_start` if it is specified and none of the sectors is yet filled.
            if unfilled_start is not None and percents < FillFlag.FIRST:
                container[0].name = unfilled_start

            # Otherwise, if `start` is specified, it will be added to the beginning.
            elif percents >= FillFlag.FIRST and start is not None:
                container[0].name = start

            # If `unfilled_end` is specified and the last sector is not filled, then the
            # corresponding character will be added to the end of the progress bar.
            if unfilled_end is not None and percents < FillFlag.LAST:
                container[-1].name = unfilled_end

            # Otherwise, if end is specified, the character corresponding to the
            # given argument will be appended to the end of the progressbar.
            elif percents >= FillFlag.LAST and end is not None:
                container[-1].name = end

            return ProgressbarContainer(
                bar=container,
                length=self.length,
                state=progress,
            )

    async def async_write_progress(
        self,
        *args: Any,
        fill: str,
        line: str,
        start: Optional[str] = None,
        unfilled_start: Optional[str] = None,
        end: Optional[str] = None,
        unfilled_end: Optional[str] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs: Any,
    ) -> Coroutine[ProgressbarContainer[_AbcSectorT_co], None, None]:
        """``sync method``
        Method that generates synchronously progress bar.

        *args: :class:`Any`
            Args that will be passed in custom Sector implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

        fill: :class:`str`
            Fill character of progress bar.

            !!! Abstract:
                This symbol is used on first fill (depending on progress).

        line: :class:`str`
            Fill character of progress bar.

            !!! Abstract:
                This symbol is used on last (second) fill (depending on progress).

        start: :class:`Optional[str]` = None
            If passed, will replace first FILLED emoji of progress bar (depending on progress).

        unfilled_start: :class:`Optional[str]` = None
            If passed, will replace first EMPTY emoji of progress bar (depending on progress).

        end: :class:`Optional[str]` = None
            If passed, will replace last FILLED emoji of progress bar (depending on progress).

        unfilled_end: :class:`Optional[str]` = None
            If passed, will replace last EMPTY emoji of progress bar (depending on progress).

        loop: :class:`Optional[asyncio.AbstractEventLoop]` = None
            Event loop that used for creating awaitable object and further run in executor.

        **kwargs: :class:`Any`
            Kwargs that will be passed in custom Container implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
        """
        if loop is None:
            loop = asyncio.get_event_loop()

        return cast(
            Coroutine[ProgressbarContainer[_AbcSectorT_co], None, None],
            await loop.run_in_executor(
                None,
                partial(
                    self.write_progress,
                    *args,
                    fill=fill,
                    line=line,
                    end=end,
                    start=start,
                    unfilled_start=unfilled_start,
                    unfilled_end=unfilled_end,
                    **kwargs,
                ),
            ),
        )

    def write_from_customer(
        self,
        *args: Any,
        customer: Type[AbstractCustomerMixin],
        **kwargs: Any,
    ) -> ProgressbarContainer[_AbcSectorT_co]:
        """``sync method``
        Method that generates synchronously progress bar from Customer classes.

        Parameters:
        -----------
        *args: :class:`Any`
            Args that will be passed in custom Sector implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

        customer: :class:`Type[AbstractCustomerMixin]`
            Customer implementation class.

        **kwargs: :class:`Any`
            Kwargs that will be passed in custom Container implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
        """
        ctx = ProgressContainer(self.current, self.total)
        kwargs_new = {}
        for as_str in AbstractCustomerMixin.__abstractmethods__:
            progress_char = getattr(customer, as_str)(customer, ctx)
            if not isinstance(progress_char, (NotImplementedType, NoneType)):
                kwargs_new[as_str] = progress_char

        kwargs.update(kwargs_new)
        return self.write_progress(*args, **kwargs)

    async def async_write_from_customer(
        self,
        *args: Any,
        customer: Type[AbstractCustomerMixin],
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs: Any,
    ) -> Coroutine[ProgressbarContainer[_AbcSectorT_co], None, None]:
        """``sync method``
        Method that generates synchronously progress bar from Customer classes.

        Parameters:
        -----------
        *args: :class:`Any`
            Args that will be passed in custom Sector implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractsectormixin

        customer: :class:`Type[AbstractCustomerMixin]`
            Customer implementation class.

        loop: :class:`Optional[asyncio.AbstractEventLoop]` = None
            Event loop that used for creating awaitable object and further run in executor.

        **kwargs: :class:`Any`
            Kwargs that will be passed in custom Container implementation.

            For more information and examples see:
                https://animatea.github.io/python-multibar/abc/?h=abstractseqbasedcontainermixin
        """
        if loop is None:
            loop = asyncio.get_event_loop()

        return cast(
            Coroutine[ProgressbarContainer[_AbcSectorT_co], None, None],
            await loop.run_in_executor(
                None,
                partial(
                    self.write_from_customer,
                    *args,
                    customer=customer,
                    **kwargs,
                ),
            ),
        )
