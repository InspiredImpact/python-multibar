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
    """``|function|``

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
    sphinx_parser = argparse.ArgumentParser(
        prog="ProgressBar",
        usage="Available flags:\n--mypy\n--flake8",
        description="Small cli parser for source code checks",
        epilog="Source code: https://github.com/Animatea/python-multibar",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sphinx_parser.add_argument(
        "--mypy",
        required=False,
        help="Checking source code with mypy --strict",
        action="store_true",
    )
    sphinx_parser.add_argument(
        "--flake8",
        required=False,
        help="Checking source code for PEP8 with flake8",
        action="store_true",
    )
    namespace = sphinx_parser.parse_args()
    if namespace.mypy:
        if not exists("mypy"):
            warnings.warn("Mypy is not installed!")
        else:
            os.system("mypy --config-file pyproject.toml multibar")
    elif namespace.flake8:
        if not exists("flake8"):
            warnings.warn("Flake8 is not installed!")
        else:
            os.system("flake8 --config=tox.ini multibar")
            print("Flake8 check completed.")
