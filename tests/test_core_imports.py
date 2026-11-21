"""The pure core imports only the standard library (Story 1.2; AD-1, NFR-2).

forecasting/ and explanation/ may import the Python standard library and their
own modules, and explanation/ may also import forecasting/. Any other import,
such as Django, a database driver, the web app or forecasting/ importing
explanation/, fails the test. The test reads the source with ast, so it imports
nothing from the core.
"""

import ast
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
# What each core package may import besides the standard library (AD-1).
ALLOWED = {
    "forecasting": {"forecasting"},
    "explanation": {"explanation", "forecasting"},
}
CORE_FILES = sorted(
    path for package in ALLOWED for path in (SRC / package).rglob("*.py")
)


def forbidden_imports(source, package):
    """The top-level modules that source, a module in package, may not import (AD-1)."""
    imported = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.update(alias.name.partition(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            # src/ is no package, so a relative import cannot leave its package.
            imported.add(package if node.level else node.module.partition(".")[0])
    return sorted(
        name
        for name in imported
        if name not in sys.stdlib_module_names and name not in ALLOWED[package]
    )


@pytest.mark.parametrize(
    "path", CORE_FILES, ids=lambda path: path.relative_to(SRC).as_posix()
)
def test_core_imports_only_the_standard_library(path):
    """AD-1, NFR-2: no module in forecasting/ or explanation/ imports anything
    outside the standard library, except explanation/ importing forecasting/."""
    package = path.relative_to(SRC).parts[0]

    assert forbidden_imports(path.read_text(encoding="utf-8"), package) == []


def test_the_import_test_reads_both_core_packages():
    """AD-1: the test finds the modules of both core packages, so a moved or
    renamed package cannot make it pass without checking anything."""
    assert {path.relative_to(SRC).parts[0] for path in CORE_FILES} == set(ALLOWED)


@pytest.mark.parametrize(
    ("package", "source", "expected"),
    [
        ("forecasting", "import django", ["django"]),
        ("forecasting", "import explanation", ["explanation"]),
        ("forecasting", "from explanation.text import sentence", ["explanation"]),
        ("explanation", "from web.models import Company", ["web"]),
        (
            "explanation",
            "import psycopg\nimport requests.adapters",
            ["psycopg", "requests"],
        ),
        ("forecasting", "def week():\n    import openpyxl\n", ["openpyxl"]),
        ("forecasting", "from __future__ import annotations\nimport datetime", []),
        ("forecasting", "from . import display\nfrom .display import week_label", []),
        (
            "explanation",
            "from forecasting import forecast_product\nimport forecasting.display",
            [],
        ),
    ],
)
def test_the_import_check_on_example_modules(package, source, expected):
    """AD-1: the check finds every import outside the standard library and the
    allowed core package, also one inside a function, and allows relative imports."""
    assert forbidden_imports(source, package) == expected
