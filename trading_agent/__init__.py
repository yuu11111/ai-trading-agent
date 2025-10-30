"""Compatibility shim package.

This empty package exists only so editable-build tooling (hatch/poetry) that
derives a package name from the project metadata finds a matching directory.
The repository's real source modules live under the `src` package and imports
in the project use `src.*` (so adding this shim is a no-op at runtime).

Remove this file if you restructure the project to a conventional package
layout (e.g. move package modules under `trading_agent/` and update imports).
"""

# Intentionally empty
