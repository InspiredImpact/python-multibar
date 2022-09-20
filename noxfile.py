import typing

import nox

MAIN_PKG: typing.Final[str] = "multibar"
TESTS_PKG: typing.Final[str] = "tests"
EXAMPLES_PKG: typing.Final[str] = "examples"

NOX_PKGS: typing.Final[tuple[str, ...]] = (MAIN_PKG, TESTS_PKG, EXAMPLES_PKG)
RUN_BLACK_ON_PKGS: typing.Final[tuple[str, ...]] = (MAIN_PKG, EXAMPLES_PKG)

BASE_REQUIREMENTS: typing.Final[tuple[str, ...]] = ("-r", "requirements.txt")
DEV_REQUIREMENTS: typing.Final[tuple[str, ...]] = ("-r", "dev-requirements.txt")


@nox.session(python=["3.9", "3.10"])
def pytest(session: nox.Session) -> None:
    """Runs all tests in `tests` package."""

    session.install(*DEV_REQUIREMENTS)
    session.install(*BASE_REQUIREMENTS)

    session.run("pytest")


@nox.session
def reformat_code(session: nox.Session) -> None:
    """Formats code according to `black` and `isort` standards."""

    session.install(*DEV_REQUIREMENTS)
    session.install(*BASE_REQUIREMENTS)

    session.run("black", "--config=pyproject.toml", *RUN_BLACK_ON_PKGS)
    session.run("isort", "--profile=black", *NOX_PKGS)


@nox.session(reuse_venv=True)
def mypy(session: nox.Session) -> None:
    """Checks `multibar` package for type-hint errors."""

    session.install(*DEV_REQUIREMENTS)
    session.install(*BASE_REQUIREMENTS)

    session.run("mypy", "-p", "multibar", "--config", "pyproject.toml")
