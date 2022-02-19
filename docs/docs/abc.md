```py
class AbstractSectorMixin(
    name: str, position: int, empty: bool
)
```
??? abstract "Expand source code"
    ```py
    class AbstractSectorMixin(Comparable, Representable, abc.ABC):
        __slots__ = ("name", "position", "empty")

        def __init__(self, *, name: str, position: int, empty: bool) -> None:
            self.name = name
            self.position = position
            self.empty = empty
    ```

!!! info
    That abc mixin used in inheritance for creating your custom Sector objects.

??? example "Expand example"
    ```py
    from typing import Any

    from multibar import ProgressBar
    from multibar.interfaces import AbstractSectorMixin


    class CustomSector(AbstractSectorMixin):
        def __init__(
            self,
            name: str,
            position: int,
            some_custom_var: int = 20,
            empty: bool = False,
        ) -> None:
            super().__init__(
                name=name,
                position=position,
                empty=empty,
            )
            self.custom_var = some_custom_var

        def __repr__(self) -> str:
            return self.name

        def __hash__(self) -> int:
            return hash(self.custom_var)

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, CustomSector):
                return other.custom_var == self.custom_var
            return NotImplemented

        def double_var(self) -> int:
            return self.custom_var * 2


    bar = ProgressBar(10, 20, sector_cls=CustomSector)
    progress = bar.write_progress(fill="+", line="-", some_custom_var=10)

    assert isinstance(progress.bar[0], CustomSector)
    assert progress.bar[0].double_var() == 20
    ```
#### `class` AbstractSectorMixin params
- **name** (str) - Sector character.
- **position** (int) - Sector position in container.
- **empty** (bool) - True if sector is empty (line character), default: False.

```py
class AbstractSeqBasedContainerMixin()
```

??? abstract "Expand source code"
    ```py
    class AbstractSeqBasedContainerMixin(Representable, Sized, abc.ABC, Generic[T]):
        """``abc mixin``
        Class that is abstract mixin for subclassing
        (creating custom Container implementations).
        """

        @overload
        def __getitem__(self, item: int) -> T:
            ...

        @overload
        def __getitem__(self, item: slice) -> Iterable[T]:
            ...

        @abc.abstractmethod
        def __getitem__(
            self,
            item: Union[int, slice],
        ) -> Union[Iterable[T], T]:
            ...

        def __enter__(self) -> AbstractSeqBasedContainerMixin[T]:
            return self

        @overload
        def __exit__(self, exc_type: None, exc_val: None, exc_tb: None) -> None:
            ...

        @overload
        def __exit__(
            self,
            exc_type: Type[BaseException],
            exc_val: BaseException,
            exc_tb: TracebackType,
        ) -> None:
            ...

        def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
        ) -> None:
            self.finalize()

        def finalize(self) -> None:
            """``sync method``
            Called in `__exit__` method.
            """

        @abc.abstractmethod
        def put(self, item: T) -> None:
            """``abc method``
            Puts item to storage.

            Parameters:
            -----------
            item: :class:`~T`
                Any item to storage.
            """

        @property
        @abc.abstractmethod
        def view(self) -> Iterable[T]:
            """``abc method``
            Returns iterator over :class:`~T`
            """
    ```

!!! info
    That abc mixin used in inheritance for creating your custom Container objects, that stores Sectors.

??? example "Expand example"
    ```py
    from __future__ import annotations

    import logging
    from typing import Iterable, List, Union, overload

    from multibar import ProgressBar
    from multibar.interfaces import AbstractBaseContainerMixin
    from multibar.internal import Sector

    logger = logging.getLogger(__name__)


    class CustomContainer(AbstractSeqBasedContainerMixin[Sector]):
        def __init__(self) -> None:
            self._storage: List[Sector] = []

        def __repr__(self) -> str:
            return "".join(i.name for i in self._storage)

        def __len__(self) -> int:
            return len(self._storage)

        @overload
        def __getitem__(self, item: int) -> Sector:
            ...

        @overload
        def __getitem__(self, item: slice) -> Iterable[Sector]:
            ...

        def __getitem__(
            self,
            item: Union[int, slice],
        ) -> Union[Sector, Iterable[Sector]]:
            return self._storage[item]

        def finalize(self) -> None:
            logger.debug("Bar container was succesfullly created.")

        def view(self) -> Iterable[Sector]:
            for sector in self._storage:
                yield sector

        def put(self, item: Sector) -> None:
            self._storage.append(item)

        def some_custom_method(self) -> None:
            while False:
                _ = (yield)


    bar = ProgressBar(10, 20, container_cls=CustomContainer)
    progress = bar.write_progress(fill="+", line="-")

    assert isinstance(progress.bar, CustomContainer)
    assert hasattr(progress.bar, "some_custom_method")
    ```
