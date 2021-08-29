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

import os
import warnings
import argparse
import importlib.util


def exists(pkg_name: str) -> bool:
    """ ``|function|``

    Function to check if a package is explicit.

    Parameters:
    -----------
    pkg_name: :class:`str`
        The name of the package to check.

    Returns:
    --------
    :class:`bool`
    """
    return importlib.util.find_spec(pkg_name) is not None


if __name__ == "__main__":
    """ ``|cli parser|``

    Available flags:
    ----------------
    --mypy:
        If specified, the entire project will be checked
        in accordance with the mypy.ini config file.

    Example of usage:
    -----------------
    # ../progress

    * python -m bar --mypy
    """
    sphinx_parser = argparse.ArgumentParser(
        prog="ProgressBar",
        usage="Available flags:\n" "--mypy",
        description="Some description",
        epilog="Source code: https://github.com/Animatea/Discord-Progressbar",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sphinx_parser.add_argument(
        "--mypy",
        required=False,
        help="Some help for this arg",
        action='store_true',
    )
    namespace = sphinx_parser.parse_args()
    if namespace.mypy is not None:
        if not exists("mypy"):
            warnings.warn("Mypy is not installed!")
        else:
            os.system(
                "mypy --config-file mypy.ini bar"
            )
