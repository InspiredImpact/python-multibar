"""
Copyright [2021] [DenyS]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import typing


__all__: typing.Sequence[str] = (
    'is_empty_field',
)


def is_empty_field(obj: str, /) -> bool:
    """ ``|inspection|``

    Checks if an object is empty.

    Parameters:
    -----------
    obj: :class:`str` [Positional only]
        Object to be checked.

    Returns:
    --------
    :class:`bool`
    """
    return any((len(obj) == 0, obj is None))
