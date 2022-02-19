## Flags
| Flag          |   Description |
| ------------- | ------------- |
| `simple`      | Writing simple bar with only :fill: and :line: chars.  |
| `--length`  | ProgressBar length.  |
| `--current` | Current progress value. |
| `--total`   | Needed progress value. |
| `--chars`   |         ProgressBar chars|


!!! info "Chars order"
    Argument passing order (yes, not very convenient, will be changed soon).
    ```py
    1. fill
    2. line
    3. start
    4. end
    5. unfilled_start
    6. unfilled_end
    ```
