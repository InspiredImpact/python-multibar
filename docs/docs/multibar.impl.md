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
    *args: Any,
    fill: str,
    line: str,
    start: Optional[str] = None,
    unfilled_start: Optional[str] = None,
    end: Optional[str] = None,
    unfilled_end: Optional[str] = None,
    **kwargs: Any,
) -> ProgressbarContainer[AbstractSectorMixin]:
```
#### `def` write_progress
!!! info
    Function that writes progressbar from certain characters.

- ** *args ** (Any) - Args that will be passed in custom Sector implementation.
- **fill** (str) - Fill character that uses for non empty sectors.
- **line** (str) - Line character for empty sectors.
- **start** (Optional[str]) - First progressbar character, default: None.
- **unfilled_start** (Optional[str]) - Unfilled first progressbar character, default: None.
- **end** (Optional[str]) - Last progressbar character, default: None
- **unfilled_end** (Optional[str]) - Unfilled last progressbar character, default: None.
- ** `**kwargs` ** (Any) - Kwargs that will be passed in custom Container implementation.

```py
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
```
#### `async` async_write_progress
!!! info
    Function that asynchronously writes progressbar from certain characters.

- ** *args ** (Any) - Args that will be passed in custom Sector implementation.
- **fill** (str) - Fill character that uses for non empty sectors.
- **line** (str) - Line character for empty sectors.
- **start** (Optional[str]) - First progressbar character, default: None.
- **unfilled_start** (Optional[str]) - Unfilled first progressbar character, default: None.
- **end** (Optional[str]) - Last progressbar character, default: None
- **unfilled_end** (Optional[str]) - Unfilled last progressbar character, default: None.
- **loop** (Optional[asyncio.AbstractEventLoop]) - Event loop for making awaitable future from sync.
- ** `**kwargs` ** (Any) - Kwargs that will be passed in custom Container implementation.

```py
def write_from_customer(
    self,
    *args: Any,
    customer: Type[AbstractCustomerMixin],
    **kwargs: Any,
) -> ProgressbarContainer[_SectorT_co]:
```
#### `def` write_from_customer
!!! info
    Function that writes progressbar from customer class.

- ** *args ** (Any) - Args that will be passed in custom Sector implementation.
- **customer** (Type[AbstractCustomerMixin]) - Subclass of AbstractCustomerMixin.
- ** `**kwargs` ** (Any) - Kwargs that will be passed in custom Container implementation.

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
    *args: Any,
    customer: Type[AbstractCustomerMixin],
    loop: Optional[asyncio.AbstractEventLoop] = None,
    **kwargs: Any,
) -> Coroutine[ProgressbarContainer[AbstractSectorMixin], None, None]:
```
#### `async` async_write_from_customer
!!! info
    Function that asynchronously writes progressbar from customer class.

- ** *args ** (Any) - Args that will be passed in custom Sector implementation.
- **customer** (Type[AbstractCustomerMixin]) - Subclass of AbstractCustomerMixin.
- **loop** (Optional[asyncio.AbstractEventLoop]) - Event loop for making awaitable future from sync.
- ** `**kwargs` ** (Any) - Kwargs that will be passed in custom Container implementation.
