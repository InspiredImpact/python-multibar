`@dataclass`
```py
class ProgressContainer(
    current: int, total: int
)
```
??? abstract "Expand source code"
    ```py
    @dataclass(frozen=True)
    class ProgressContainer:
        current: int
        total: int

        @overload
        def percents(self, *, allow_float: Literal[False]) -> int:
            ...

        @overload
        def percents(self, *, allow_float: Literal[True]) -> float:
            ...

        def percents(self, *, allow_float: bool = False) -> Union[int, float]:
            initial = (self.current / self.total) * 100
            if allow_float:
                return initial

            return int(initial)
    ```
#### `class` ProgressContainer
- **current** (int) - Current progress value.
- **total** (int) - Needed progress value.

```py
def percents(
    self, *, allow_float: bool = False,
) -> Union[int, float]:
```
#### `def` percents
Returns percentage of current progress ((current/total) * 100).

- **allow_float** (bool) - If True, will return float, otherwise - int. Default: False.

`@dataclass`
```py
class ProgressbarContainer(
    length: int
    progress: ProgressContainer
    bar: AbstractBaseContainerMixin[_AbcSectorT_co] = field(repr=False)
)
```
??? abstract "Expand source code"
    ```py
    _AbcSectorT_co = TypeVar("_AbcSectorT_co", bound=AbstractSectorMixin, covariant=True)


    @dataclass(frozen=True, order=True)
    class ProgressbarContainer(Sized, Generic[_AbcSectorT_co]):
        length: int
        progress: ProgressContainer
        bar: AbstractBaseContainerMixin[_AbcSectorT_co] = field(repr=False)

        def __eq__(self, other: Any) -> bool:
            if isinstance(other, ProgressbarContainer):
                return (
                    self.progress.current == other.progress.current
                    and self.progress.total == other.progress.total
                )

            return NotImplemented

        def __len__(self) -> int:
            return len(self.bar)

        @overload
        def __getitem__(
            self,
            item: int,
        ) -> _AbcSectorT_co:
            ...

        @overload
        def __getitem__(
            self,
            item: slice,
        ) -> Iterable[_AbcSectorT_co]:
            ...

        def __getitem__(
            self,
            item: Union[int, slice],
        ) -> Union[_AbcSectorT_co, Iterable[_AbcSectorT_co]]:
            return self.bar[item]
    ```
#### `class` ProgressbarContainer
- **length** (int) - Length of progress bar.
- **progress** (ProgressContainer) - Progress container object.
- **bar** (AbstractBaseContainerMixin[_AbcSectorT_co]) - Container that stores progressbar sectors. Default: dataclass.field(repr=False).

```py
class SectorContainer()
```
??? abstract "Expand source code"
    ```py
    @dataclass
    class SectorContainer(AbstractSeqBasedContainerMixin[_AbcSectorT_co]):
        def __post_init__(self) -> None:
            self._storage: List[_AbcSectorT_co] = []

        def __repr__(self) -> str:
            return "".join(s.name for s in self._storage)

        def __len__(self) -> int:
            return len(self._storage)

        @overload
        def __getitem__(
            self,
            item: int,
        ) -> _AbcSectorT_co:
            ...

        @overload
        def __getitem__(
            self,
            item: slice,
        ) -> Iterable[_AbcSectorT_co]:
            ...

        def __getitem__(
            self,
            item: Union[int, slice],
        ) -> Union[Iterable[_AbcSectorT_co], _AbcSectorT_co]:
            return self._storage[item]

        def put(self, item: AbstractSectorMixin) -> None:
            self._storage.append(cast(_AbcSectorT_co, item))

        def finalize(self) -> None:
            pass

        @property
        def view(self) -> List[_AbcSectorT_co]:
            return self._storage
    ```

```py
def put(self, item: AbstractSectorMixin) -> None:
```
#### `def` put
Puts item to storage.

- **item** (AbstractSectorMixin) - Any Sector object.

```py
def finalize(self) -> None:
```
#### `def` finalize
Method that used in `__exit__`.

```py
@property
def view(self) -> List[_AbcSectorT_co]:
```
#### `@property` view
Returns iterator over sectors.
