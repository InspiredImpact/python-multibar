from __future__ import annotations

__all__ = ["ProgressBar"]

import asyncio
from dataclasses import dataclass
from functools import partial
from typing import (
    Any,
    Coroutine,
    Generic,
    Optional,
    Type,
    TypeVar,
    cast,
    overload,
)

from multibar.flags import FillFlag
from multibar.pytypes import NoneType, NotImplementedType
from multibar.internal.crate import (
    ProgressbarContainer,
    ProgressContainer,
    SectorContainer,
)
from multibar.internal.customer import AbstractCustomerMixin
from multibar.internal.factories import SphinxSectorFactory
from multibar.internal.product import Sector
from multibar.interfaces.containers import AbstractSeqBasedContainerMixin
from multibar.interfaces.product import AbstractSectorMixin

_ContainerT_co = TypeVar(
    "_ContainerT_co", bound=AbstractSeqBasedContainerMixin[AbstractSectorMixin], covariant=True
)
_SectorT_co = TypeVar("_SectorT_co", bound=AbstractSectorMixin, covariant=True)


@dataclass
class ProgressBar(Generic[_SectorT_co, _ContainerT_co]):
    current: int
    total: int
    length: int = 20
    sector_cls: Optional[Type[_SectorT_co]] = None
    container_cls: Optional[Type[_ContainerT_co]] = None

    def __post_init__(self) -> None:
        if self.container_cls is None:
            self.container_cls = cast(
                Type[_ContainerT_co],
                SectorContainer,
            )

        self.factory: SphinxSectorFactory[_SectorT_co] = SphinxSectorFactory.from_bind(
            sector_type=cast(Type[_SectorT_co], Sector if self.sector_cls is None else self.sector_cls)
        )

    @overload
    def write_progress(
        self,
        fill: str,
        line: str,
    ) -> ProgressbarContainer[_SectorT_co]:
        ...

    @overload
    def write_progress(
        self,
        *args: Any,
        fill: str,
        line: str,
        **kwargs: Any,
    ) -> ProgressbarContainer[_SectorT_co]:
        ...

    @overload
    def write_progress(
        self,
        fill: str,
        line: str,
        start: str,
        unfilled_start: str,
        end: str,
        unfilled_end: str,
    ) -> ProgressbarContainer[_SectorT_co]:
        ...

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
    ) -> ProgressbarContainer[AbstractSectorMixin]:
        progress = ProgressContainer(self.current, self.total)
        percents = progress.percents(allow_float=False)
        assert self.container_cls is not None

        with self.container_cls() as container:
            for i in range(rest := (round(percents / (100 / self.length)))):
                container.put(
                    self.factory.create_product(
                        *args, name=fill, position=i, empty=False, **kwargs,
                    )
                )

            for i in range(self.length - rest):
                container.put(
                    self.factory.create_product(
                        *args, name=line, position=i + rest, empty=True, **kwargs,
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
                progress=progress,
            )

    @overload
    async def async_write_progress(
        self,
        fill: str,
        line: str,
    ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
        ...

    @overload
    async def async_write_progress(
        self,
        fill: str,
        line: str,
        loop: asyncio.AbstractEventLoop,
    ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
        ...

    @overload
    async def async_write_progress(
        self,
        *args: Any,
        fill: str,
        line: str,
        **kwargs: Any,
    ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
        ...

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
    ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
        if loop is None:
            loop = asyncio.get_event_loop()

        return cast(
            Coroutine[ProgressbarContainer[_SectorT_co], None, None],
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
    ) -> ProgressbarContainer[_SectorT_co]:
        ctx = ProgressContainer(self.current, self.total)
        kwargs_new = {}
        for as_str in AbstractCustomerMixin.__abstractmethods__:
            progress_char = getattr(customer, as_str)(customer, ctx)
            if not isinstance(progress_char, (NotImplementedType, NoneType)):
                kwargs_new[as_str] = progress_char

        kwargs.update(kwargs_new)
        return self.write_progress(*args, **kwargs)

    @overload
    async def async_write_from_customer(
        self,
        customer: Type[AbstractCustomerMixin],
    ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
        ...

    @overload
    async def async_write_from_customer(
        self,
        *args: Any,
        customer: Type[AbstractCustomerMixin],
        **kwargs: Any,
    ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
        ...

    @overload
    async def async_write_from_customer(
        self,
        customer: Type[AbstractCustomerMixin],
        loop: asyncio.AbstractEventLoop,
    ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
        ...

    async def async_write_from_customer(
        self,
        *args: Any,
        customer: Type[AbstractCustomerMixin],
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs: Any,
    ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
        if loop is None:
            loop = asyncio.get_event_loop()

        return cast(
            Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None],
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
