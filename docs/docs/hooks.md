```py
class AbstractCustomerMixin()
```
??? abstract "Expand source code"
    ```py
    class AbstractCustomerMixin(abc.ABC):
        def __init__(self, ctx: ProgressContainer) -> None:
            self.ctx = ctx

        @abc.abstractmethod
        def fill(self, ctx: ProgressContainer) -> Any:
            ...

        @abc.abstractmethod
        def line(self, ctx: ProgressContainer) -> Any:
            ...

        @abc.abstractmethod
        def start(self, ctx: ProgressContainer) -> Any:
            ...

        @abc.abstractmethod
        def end(self, ctx: ProgressContainer) -> Any:
            ...

        @abc.abstractmethod
        def unfilled_start(self, ctx: ProgressContainer) -> Any:
            ...

        @abc.abstractmethod
        def unfilled_end(self, ctx: ProgressContainer) -> Any:
            ...
    ```

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

!!! info
    Hook that defines certain character for progressbar.
    All methods in this class takes context by second argument.

#### `class` AbstractCustomerMixin abc methods
- **fill** - Fill character that uses for non empty sectors.
- **line** - Line character for empty sectors.
- **start** - First progressbar character.
- **unfilled_start** - Unfilled first progressbar character.
- **end** - Last progressbar character.
- **unfilled_end** - Unfilled last progressbar character.
