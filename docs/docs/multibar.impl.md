`@dataclass`
```py
class ProgressBar(
    current: int,
    total: int,
    length: int = 20,
    sector_cls: Optional[Type[_SectorT_co]] = None,
    container: Optional[Type[_ContainerT_co]] = None,
)
```
??? abstract "Expand source code"
    ```py
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
            *,
            fill: str,
            line: str,
        ) -> ProgressbarContainer[_SectorT_co]:
            ...

        @overload
        def write_progress(
            self,
            *,
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
            *,
            fill: str,
            line: str,
            start: Optional[str] = None,
            unfilled_start: Optional[str] = None,
            end: Optional[str] = None,
            unfilled_end: Optional[str] = None,
        ) -> ProgressbarContainer[AbstractSectorMixin]:
            progress = ProgressContainer(self.current, self.total)
            percents = progress.percents(allow_float=False)
            assert self.container_cls is not None

            with self.container_cls() as container:
                for i in range(rest := (round(percents / (100 / self.length)))):
                    container.put(self.factory.create_product(fill, i, empty=False))

                for i in range(self.length - rest):
                    container.put(self.factory.create_product(line, i + rest, empty=True))

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
            *,
            fill: str,
            line: str,
        ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
            ...

        @overload
        async def async_write_progress(
            self,
            *,
            fill: str,
            line: str,
            loop: asyncio.AbstractEventLoop,
        ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
            ...

        async def async_write_progress(
            self,
            *,
            fill: str,
            line: str,
            start: Optional[str] = None,
            unfilled_start: Optional[str] = None,
            end: Optional[str] = None,
            unfilled_end: Optional[str] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None,
        ) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
            if loop is None:
                loop = asyncio.get_event_loop()

            return cast(
                Coroutine[ProgressbarContainer[_SectorT_co], None, None],
                await loop.run_in_executor(
                    None,
                    partial(
                        self.write_progress,
                        fill=fill,
                        line=line,
                        end=end,
                        start=start,
                        unfilled_start=unfilled_start,
                        unfilled_end=unfilled_end,
                    ),
                ),
            )

    def write_from_customer(
        self,
        *,
        customer: Type[AbstractCustomerMixin],
    ) -> ProgressbarContainer[_SectorT_co]:
        ctx = ProgressContainer(self.current, self.total)
        kwargs = {}
        for as_str in AbstractCustomerMixin.__abstractmethods__:
            progress_char = getattr(customer, as_str)(customer, ctx)
            if not isinstance(progress_char, (NotImplementedType, NoneType)):
                kwargs[as_str] = progress_char

        return self.write_progress(**kwargs)

        @overload
        async def async_write_from_customer(
            self,
            *,
            customer: Type[AbstractCustomerMixin],
        ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
            ...

        @overload
        async def async_write_from_customer(
            self,
            *,
            customer: Type[AbstractCustomerMixin],
            loop: asyncio.AbstractEventLoop,
        ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
            ...

        async def async_write_from_customer(
            self,
            *,
            customer: Type[AbstractCustomerMixin],
            loop: Optional[asyncio.AbstractEventLoop] = None,
        ) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
            if loop is None:
                loop = asyncio.get_event_loop()

            return cast(
                Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None],
                await loop.run_in_executor(
                    None,
                    partial(
                        self.write_from_customer,
                        customer=customer,
                    ),
                ),
            )
    ```
??? note "Expand SectorFactory trick"
    ```py
    from typing import Any

    from multibar import ProgressBar
    from multibar.interfaces import AbstractSectorMixin
    from multibar.internal import Sector

    bar = ProgressBar(10, 20)
    progress = bar.write_progress(fill="+", line="-")
    assert isinstance(progress.bar[0], Sector)


    class CustomSector(AbstractSectorMixin):
        def __init__(
            self,
            name: str,
            position: int,
            some_custom_var: int,
            empty: bool = False,
        ) -> None:
            super().__init__(name=name, position=position, empty=empty)
            self.some_custom_var = some_custom_var

        def __repr__(self) -> str:
            return self.name

        def __hash__(self) -> int:
            return hash(self.some_custom_var)

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, CustomSector):
                return other.some_custom_var == self.some_custom_var
            return NotImplemented

        def some_stuff(self) -> str:
            return "yes" if self.some_custom_var > 10 else "no"


    # Rebinding factory sector cls.
    bar.factory.rebind(sector_type=CustomSector)

    # Getting first sector of progressbar.
    other_progress = bar.write_progress(fill="+", line="-", some_custom_var=10)
    first_sector = other_progress.bar[0]

    # Asserting results.
    assert isinstance(first_sector, CustomSector)
    assert first_sector.some_stuff() == "no"
    ```

#### `class` ProgressBar
!!! info
    The main class with which you can create progressbars and customize their containers.

- **current** (int) - Current progress value.
- **total** (int) - Needed progress value.
- **length** (int) - ProgressBar length, default: 20.
- **sector_cls** (Optional[Type[_SectorT_co]]) - Subclass of AbstractSectorMixin, default: None.
- **container_cls** (Optional[Type[_ContainerT_co]]) - Subclass of AbstractBaseContainerMixin, default: None.

```py
def write_progress(
    self,
    *,
    fill: str,
    line: str,
    start: Optional[str] = None,
    unfilled_start: Optional[str] = None,
    end: Optional[str] = None,
    unfilled_end: Optional[str] = None,
) -> ProgressbarContainer[AbstractSectorMixin]:
```
#### `def` write_progress
!!! info
    Function that writes progressbar from certain characters.

- **fill** (str) - Fill character that uses for non empty sectors.
- **line** (str) - Line character for empty sectors.
- **start** (Optional[str]) - First progressbar character, default: None.
- **unfilled_start** (Optional[str]) - Unfilled first progressbar character, default: None.
- **end** (Optional[str]) - Last progressbar character, default: None
- **unfilled_end** (Optional[str]) - Unfilled last progressbar character, default: None.


```py
async def async_write_progress(
    self,
    *,
    fill: str,
    line: str,
    start: Optional[str] = None,
    unfilled_start: Optional[str] = None,
    end: Optional[str] = None,
    unfilled_end: Optional[str] = None,
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> Coroutine[ProgressbarContainer[_SectorT_co], None, None]:
```
#### `async` async_write_progress
!!! info
    Function that asynchronously writes progressbar from certain characters.

- **fill** (str) - Fill character that uses for non empty sectors.
- **line** (str) - Line character for empty sectors.
- **start** (Optional[str]) - First progressbar character, default: None.
- **unfilled_start** (Optional[str]) - Unfilled first progressbar character, default: None.
- **end** (Optional[str]) - Last progressbar character, default: None
- **unfilled_end** (Optional[str]) - Unfilled last progressbar character, default: None.
- **loop** (Optional[asyncio.AbstractEventLoop]) - Event loop for making awaitable future from sync.

```py
def write_from_customer(
    self,
    *,
    customer: Type[AbstractCustomerMixin],
) -> ProgressbarContainer[_SectorT_co]:
```
#### `def` write_from_customer
!!! info
    Function that writes progressbar from customer class.

- **customer** (Type[AbstractCustomerMixin]) - Subclass of AbstractCustomerMixin.

??? example "Expand example"
    ```py
    from __future__ import annotations

    from typing import TYPE_CHECKING, Any

    from multibar import ProgressBar
    from multibar.internal import AbstractCustomerMixin

    if TYPE_CHECKING:
        from multibar.internal import ProgressContainer

    bar = ProgressBar(8, 20)


    class Customer(AbstractCustomerMixin):
        def fill(self, ctx: ProgressContainer) -> Any:
            if ctx.percents(allow_float=False) < 50:
                return "1"
            return "2"

        def line(self, ctx: ProgressContainer) -> Any:
            if ctx.percents(allow_float=False) > 50:
                return "3"
            return "4"

        def start(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def end(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def unfilled_start(self, ctx: ProgressContainer) -> Any:
            return NotImplemented

        def unfilled_end(self, ctx: ProgressContainer) -> Any:
            return NotImplemented


    progress = bar.write_from_customer(customer=Customer)
    assert str(progress.bar) == "11111111444444444444"  # percents < 50

    other_bar = ProgressBar(15, 20)
    other_progress = other_bar.write_from_customer(customer=Customer)
    assert str(other_progress.bar) == "22222222222222233333"  # line value changed (percents > 50)
    ```

```py
async def async_write_from_customer(
    self,
    *,
    customer: Type[AbstractCustomerMixin],
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
```
#### `async` async_write_from_customer
!!! info
    Function that asynchronously writes progressbar from customer class.

- **customer** (Type[AbstractCustomerMixin]) - Subclass of AbstractCustomerMixin.
- **loop** (Optional[asyncio.AbstractEventLoop]) - Event loop for making awaitable future from sync.
