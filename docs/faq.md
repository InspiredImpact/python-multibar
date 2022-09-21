# FAQ

## :question: What is the difference between [`Writer`](impl/writers.md) and [`Client`](impl/clients.md)
[Writer](impl/writers.md) `aggregates` certain attributes in the same way as [Client](impl/clients.md), that can be accessed via properties.
See the documentation for a list of all properties.

!!! note
    [Client](impl/clients.md) aggregates [Writer](impl/writers.md) with other customization logic.

!!! Information
    [Writer](impl/writers.md) is slightly faster than [Client](impl/clients.md) because [Client](impl/clients.md)
    has [Contract Manager](#what-is-a-contract-manager) that checks all contracts and [Hooks](#how-hooks-work),
    which are also triggers when progress generates.

    The difference in speed is not big, but it is.

The [Client](impl/clients.md) works on an abstraction higher than the [Writer](impl/writers.md).
!!! tldr "TL;DR"
    [Client](impl/clients.md) can enable validation when generating progress and trigger pre/post/on-error hooks.
    <br>
    [Writer](impl/writers.md) can only interact with progressbar logic (like signature, sectors, math operations).

## :question: How [`hooks`](impl/hooks.md) work
In [Client](impl/clients.md) implementation hooks called thrice:

!!! quote
    ```py
    def get_progress(...) -> abc_progressbars.ProgressbarAware[abc_sectors.AbstractSector]:
        call_metadata: progress_types.ProgressMetadataType = {...}

        # <-- Validation call #1 -->
        self._validate_contracts(self._writer, metadata=call_metadata)
        # <-- Pre-execution call with metadata #2 -->
        self._hooks.trigger_pre_execution(self, metadata=call_metadata)

        # Generates progressbar
        progressbar = self._writer.write(start_value, end_value, length=length)
        # Sets progressbar to metadata
        call_metadata["progressbar"] = progressbar

        # <-- Triggers Post-execution with progressbar in metadata #3 -->
        self._hooks.trigger_post_execution(self, metadata=call_metadata)
        ...
    ```
> Post-execution is called with metadata, that stores progressbar object, where it can transform *(in post-execution)*.
> For example, this is how [hooks.WRITER_HOOKS](impl/hooks.md) works.

## :question: What is a [`contract manager`](impl/contracts.md)
The contract manager is a class that is responsible for various checks related to the progress bar.
For more details see:
- [Contracts](impl/contracts.md) in documentation.
- [Examples on github](https://github.com/Animatea/python-multibar/blob/main/examples/custom_contracts.py)

## :question: How the [`progressbar`](impl/progressbars.md) works
[Progressbar](impl/progressbars.md) - a collection that consists of sectors (objects that represent 1 character of the progress bar,
but have an additional methods).

!!! example
    ```py
    import multibar

    progressbar = multibar.ProgressbarWriter().write(100, 100)
    assert type(progressbar) is multibar.Progressbar  # Writer returns progressbar

    first_sector = progressbar[0]  # Supports __getitem__
    assert type(first_sector) is multibar.Sector  # Progressbar consists of sectors
    ```

## :question: How the Python-Multibar [`global settings`](settings.md) work
!!! note
    Python-Multibar settings is [`Singleton`](https://python-patterns.guide/gang-of-four/singleton/).

> For more details see in documentation: [click](settings.md)
