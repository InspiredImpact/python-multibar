from __future__ import annotations

import io
import sys
import typing


class ConsoleOutputInterceptor(list[str]):
    def __enter__(self) -> ConsoleOutputInterceptor:
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args: typing.Any) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
