## Base signature example

<!-- termynal -->

```
$ import multibar
$ writer = multibar.ProgressbarWriter()
$ progressbar = writer.write(50, 100, length=6)
+++---
$ type(progressbar)
[<class 'multibar.impl.progressbars.Progressbar'>](impl/progressbars.md)
$ type(progressbar[0])
[<class 'multibar.impl.sectors.Sector'>](impl/sectors.md)
```

## Square Emoji signature example

<!-- termynal -->

```
$ from multibar import ProgressbarWriter, SquareEmojiSignature
$ writer = ProgressbarWriter.from_signature(SquareEmojiSignature())
$ progressbar = writer.write(50, 100, length=6)
🟧🟧🟧⬛️⬛️⬛️  # If the environment supports emoji
```

## Square Emoji signature that supports `start` & `end` values

<!-- termynal -->

```
$ from multibar import ProgressbarClient, SquareEmojiSignature, WRITER_HOOKS
# Client configuration
$ client = ProgressbarClient()
$ client.writer.bind_signature(SquareEmojiSignature())
$ client.set_hooks(WRITER_HOOKS)
# Product
$ progressbar = client.get_progress(100, 100, length=6)
🔸🟧🟧🟧🟧🔸  # If the environment supports emoji
```
