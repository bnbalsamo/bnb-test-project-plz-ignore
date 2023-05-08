"""Testing environments + steps."""
from pathlib import Path

import nox

nox.options.error_on_external_run = True

SUPPORTED_PYTHONS = ["3.8", "3.9", "3.10", "3.11"]


def get_wheel_path() -> Path:
    """Install the project from the wheel."""
    potential_wheels = list(Path("dist/").glob("*.whl"))
    if len(potential_wheels) != 1:
        err_msg = f"Error finding wheel: {potential_wheels=}"
        raise RuntimeError(err_msg)
    return potential_wheels[0].resolve()


@nox.session(python=SUPPORTED_PYTHONS)  # type: ignore[misc]
def test(session: nox.Session) -> None:
    """Run the unit tests."""
    session.install("-r", "requirements/test_requirements.txt", get_wheel_path())
    session.run("python", "-m", "coverage", "run", "-m", "pytest")
    session.notify("coverage")


@nox.session  # type: ignore[misc]
def introspect(session: nox.Session) -> None:
    """Run code introspection that requires the project be installed."""
    session.install(get_wheel_path(), "mypy", "pylint")
    session.run("python", "-m", "pylint", "src")
    session.run("python", "-m", "mypy", "src")


@nox.session  # type: ignore[misc]
def lint(session: nox.Session) -> None:
    """Run the linters."""
    session.install("pre-commit")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session  # type: ignore[misc]
def docs(session: nox.Session) -> None:
    """Attempt to build the docs."""
    session.install("-r", "requirements/doc_requirements.txt", get_wheel_path())
    session.run("mkdocs", "build")


@nox.session  # type: ignore[misc]
def coverage(session: nox.Session) -> None:
    """Combine the coverage reports."""
    session.install("coverage[toml]")
    session.run("python", "-m", "coverage", "combine")
    session.run("python", "-m", "coverage", "report")
