"""
Rewrite the old version of the library.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
import inspect

from multibar.core.variants import Info


__all__: typing.Sequence[str] = (
    "__version__",
    "Version",
    "LibraryInfo",
)


class Version(typing.NamedTuple):
    """Library version.

    # Also used in the version_info() function in `.__init__.py`

    Parameters:
    -----------
    major: :class:`int`
        Global library update.

    minor: :class:`int`
        Light library update.

    micro: :class:`int`
        Small library update.

    release_stage: :class:`Literal['alpha', 'beta', 'final']`
        Library's current release level.
    """

    major: int
    minor: int
    micro: int
    release_stage: typing.Literal["pre-alpha", "alpha", "beta", "candidate", "final"]


__title__: Info[str] = Info("python-multibar")
__author__: Info[str] = Info("DenyS")
__license__: Info[str] = Info("Apache v2.0")
__copyright__: Info[str] = Info("Copyright [2021] [DenyS]")
__discord__: Info[str] = Info("DenyS#1469")
__discord_server__: Info[str] = Info("discord.gg/KKUFRZCt4f")
__release_date__: Info[str] = Info("")
__version__: Info[Version] = Info(Version(major=2, minor=0, micro=6, release_stage="pre-alpha"))
__information__: Info[str] = Info(
    """
Information:
------------

    * Library code style:
        ``black``

    * Commentaries:
        Are only used when the person writing the code considers it necessary.

    * Docstrings:
        Includes the categories ``Raises``, ``Parameters``, ``Attributes``, ``Features``, ``Returns``
        (of necessity). A generic layout is used that is readable by most code editors.

        Each of the categories is done as a heading, for example:
        '''
        Category:
        ---------
        param: :class:`Any` [Label if arguments are `positional only` or `keyword only`.]
            description
        '''

Useful:
-------
All changes will be displayed in the root directory in the CHANGELOG.md file,
the library also supports the work with console commands, for example: `--mypy`,` --pep8`, etc.


.editorconfig:
--------------
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
"""
)


def _prune_param(param_name: str, /) -> str:
    """``|function|``

    The function with which dunders are trimmed.

    Parameters:
    -----------
    param_name: :class:`str`
        The parameter from which you need to remove the dunders.

    Returns:
    --------
    :class:`str`
    """
    return param_name.split("__")[1]


class LibraryInfo:
    """``|class|``

    Class with information about the library.

    Features:
    ---------
    __str__: :class:`str`
        All attr=value from this class.
    """

    if typing.TYPE_CHECKING:
        author: Info[str]
        title: Info[str]
        copyright: Info[str]
        discord: Info[str]
        discord_server: Info[str]
        release_date: Info[str]
        version: Info[Version]
        information: Info[str]

    def __init__(self) -> None:
        valuesgl = dict(globals())
        for name, value in valuesgl["__annotations__"].items():
            _origin: type = typing.cast(type, typing.get_origin(value))  # for mypy "arg-type"
            if Info in inspect.getmro(_origin):
                setattr(self, _prune_param(name), valuesgl.get(name))

    def __str__(self) -> str:
        return f'Library({", ".join(f"{i}={getattr(self, i).value}" for i in dir(self) if not i.startswith("_"))})'
