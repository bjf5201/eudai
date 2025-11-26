#!/bin/sh -e

# Use the Python executable provided from the `-p` option, or a default.
[ "$1" = "-p" ] && PYTHON=$2 || PYTHON="python3"

REQUIREMENTS="/server/pyproject.toml"
VENV="/server/.venv/"

set -x

# Check if 'uv' is available. If not, fail gracefully with a helpful message.
if ! command -v uv >/dev/null 2>&1; then
    echo "Error: 'uv' is not installed or not found in your PATH."
    echo "Please install 'uv' from https://github.com/astral-sh/uv and ensure it is available on your PATH."
    exit 1
fi

# Use uv to create the virtual environment unless running in GitHub Actions
if [ -z "$GITHUB_ACTIONS" ]; then
    uv venv "$VENV" --python "$PYTHON"
    ADD="$VENV/bin/uv add"
else
    ADD="uv add"
fi

# Install dependencies with uv
$ADD "$REQUIREMENTS"