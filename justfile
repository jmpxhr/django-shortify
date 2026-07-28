set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
set dotenv-load := false

export UV_NO_SYNC := '1'

# List all available recipes
_default:
    @just --list --unsorted --list-submodules

# Install dependencies
[group('dev')]
install:
    uv sync --all-groups --all-extras

# Format code with ruff
[group('dev')]
format:
    uv run ruff format
    uv run ruff check

# Run all linters
[group('dev')]
lint:
    uv run ruff check --exit-non-zero-on-fix
    uv run ruff format --check --diff

# Run all type checkers
[group('type-check')]
type-check:
    uv run mypy .
    uv run pyrefly check --remove-unused-ignores
