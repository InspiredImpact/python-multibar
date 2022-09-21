# :gear: Quickstart
> If you haven't installed the library yet, then you should start with this section: [`how to install python-multibar`](about.md)

### :gear: Minimal progressbar
#### :small_orange_diamond: Using writer
```py
import multibar

writer = multibar.ProgressbarWriter()
progressbar = writer.write(50, 100, length=10)

assert str(progressbar) == "+++++-----"  # Default signature, that You can change.
assert type(progressbar) is multibar.Progressbar  # Default progressbar collection, that You can change.
```

#### :small_orange_diamond: Using client
```py
client = multibar.ProgressbarClient()
client.set_hooks(multibar.WRITER_HOOKS)  # This hooks allows You to work with `start` and `end` characters of the progress bar.

progressbar = client.get_progress(100, 100, length=10)
assert str(progressbar) == "<++++++++>"  # Default signature, that You can change.
```

!!! error
    The following code will raise [`multibar.errors.TerminatedContractError`](errors.md)!
    ```py
    progressbar = client.get_progress(200, 100)  # Start value more that end value
    ```

    Because by default [`ProgressbarClient()`](impl/clients.md) is subscribed to the [`multibar.WRITE_PROGRESS_CONTRACT`](impl/contracts.md) contract,
    that checks if `start_value` is not more than `end_value` and if `length` is more that zero.

    !!! info "How to terminate [`multibar.WRITE_PROGRESS_CONTRACT`](impl/contracts.md)?"
        You can terminate any contract by the following code:

        !!! warning
            This may allow unexpected behavior, that is described in the comments to the code below.

            If you terminate this contract, it is recommended to write or include in `your` contract
            checks from the [`WriteProgressContract()`](impl/contracts.md) contract.

        **Unexpected behavior #1**
        ```py
        import multibar

        client = multibar.ProgressbarClient()
        client.contract_manager.terminate(multibar.WRITE_PROGRESS_CONTRACT)

        progressbar = client.get_progress(200, 100, length=10)
        assert str(progressbar) == "++++++++++++++++++++"
        assert progressbar.length == len(progressbar) == 20  # But specified length is 10!
        ```

        **Unexpected behavior #2**
        ```py
        client.get_progress(100, 100, length=0)  # This code will raise ZeroDivisionError.
        ```

        **Unexpected behavior #3**
        ```py
        progressbar = client.get_progress(100, 100, length=-1)

        assert str(progressbar) == ""  # Progressbar is empty.
        assert progressbar.length == len(progressbar) == 0
        ```

## :gear: Discord addition & Signature changing
#### :small_orange_diamond: Your custom signature implementation will look like:
```py
import dataclasses

import multibar

@dataclasses.dataclass
class MyOwnSignature:
    start: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled="<", on_unfilled="#"),
    )
    middle: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled="O", on_unfilled="#"),
    )
    end: multibar.SignatureSegmentProtocol = dataclasses.field(
        default=multibar.SignatureSegment(on_filled=">", on_unfilled="#"),
    )
```
#### :small_orange_diamond: Setting signature to writer on creation
```py
multibar.ProgressbarWriter.from_signature(MyOwnSignature())
progressbar = writer.write(50, 100, length=6)

assert str(progressbar) == "OOO###"  # Your custom signature
```

#### :small_orange_diamond: Setting signature to existing writer
```py
existing_writer.bind_signature(MyOwnSignature())
progressbar = writer.write(50, 100, length=6)

assert str(progressbar) == "OOO###"  # Your custom signature
```

#### :small_orange_diamond: Settings signature to ProgressbarClient()
Go to [hooks documentation](impl/hooks.md)
```py
client = multibar.ProgressbarClient()
client.writer.bind_signature(MyOwnSignature())  # Setting signature
# Setting hooks that includes `start` and `end` value into progressbar
client.update_hooks(multibar.WRITER_HOOKS)

progressbar = client.get_progress(100, 100, length=6)

assert str(progressbar) == "<OOOO>"
assert type(progressbar) is multibar.Progressbar
```

#### :small_orange_diamond: Discord pseudocode
```py
import multibar

writer = multibar.ProgressbarWriter.from_signature(
    multibar.SquareEmojiSignature()
)

async def some_command(context: your.library.CommandContext) -> None:
    user = inject(context.author.id)
    await context.create_message(
        writer.write(user.current_xp, user.needed_xp)
    )
```
If `user` progress is, for example, 50%, then in discord it will look like:
[=50%]{: .thin}
