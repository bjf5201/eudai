from pathlib import Path

import nox

# Default sessions when running plain `nox`
nox.options.sessions = ["lint", "mypy", "tests", "docs-build"]

# Paths for project layout
PROJECT_DIR = Path("server") / "eudai"
SRC_DIR = PROJECT_DIR / "src"
TESTS_DIR = PROJECT_DIR / "tests"
DOCS_DIR = Path("docs")


@nox.session
def lint(session: nox.Session) -> None:
    """
    Lint and format the backend with ruff.
    """
    if not PROJECT_DIR.exists():
        session.error(f"{PROJECT_DIR} does not exist. Adjust PROJECT_DIR in noxfile.py.")

    session.chdir(str(PROJECT_DIR))
    session.install("ruff")

    # Format first, then lint
    session.run("ruff", "format", "src", "tests", external=true)
    session.run("ruff", "check", "src", "tests", external=true)


@nox.session
def mypy(session: nox.Session) -> None:
    """
    Type-check the backend with mypy.
    """
    if not PROJECT_DIR.exists():
        session.error(f"{PROJECT_DIR} does not exist. Adjust PROJECT_DIR in noxfile.py.")

    session.chdir(str(PROJECT_DIR))
    # Install your package + mypy
    session.run("pip", "install", "-e", ".", external=True)
    session.install("mypy")

    # Start with main.py; include tests/ once it exists.
    targets = ["src"]
    if TESTS_DIR.exists():
        targets.append("tests")

    session.run("mypy", *targets)


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the test suite with coverage.

    If tests/ doesn't exist yet, this session will *skip* instead of failing.
    """
    if not PROJECT_DIR.exists():
        session.error(f"{PROJECT_DIR} does not exist. Adjust PROJECT_DIR in noxfile.py.")

    session.chdir(str(PROJECT_DIR))
    session.run("pip", "install", "-e", ".", external=True)
    session.install("pytest", "coverage[toml]")

    if not TESTS_DIR.exists():
        session.log("No tests/ directory found; skipping tests session.")
        return

    # Single coverage file for now
    session.env["COVERAGE_FILE"] = ".coverage"
    session.run("coverage", "run", "-m", "pytest", "tests")


@nox.session(name="docs-build")
def docs_build(session: nox.Session) -> None:
    """
    Build the documentation from the top-level docs/ directory.
    """
    if not DOCS_DIR.exists():
        session.error("docs/ directory not found at repo root.")

    session.install("sphinx", "sphinx-rtd-theme")
    session.chdir(str(PROJECT_DIR))
    session.run("pip", "install", "-e", ".", external=True)

    session.chdir(str(DOCS_DIR.project))
    build_dir = DOCS_DIR / "_build"
    build_dir.mkdir(parents=True, exist_ok=True)

    session.run("sphinx-build", "-W", "docs", str(build_dir))


@nox.session
def coverage(session: nox.Session) -> None:
    """
    Combine coverage from multiple test runs and optionally generate XML.

    - `nox -s coverage`        → combine & show text report
    - `nox -s coverage -- xml` → combine & write coverage.xml
    """
    if not PROJECT_DIR.exists():
        session.error(f"{PROJECT_DIR} does not exist. Adjust PROJECT_DIR in noxfile.py.")

    session.chdir(str(PROJECT_DIR))
    session.install("coverage[toml]")

    session.run("coverage", "combine")

    if session.posargs and session.posargs[0] == "xml":
        session.run("coverage", "xml")
    else:
        session.run("coverage", "report")
