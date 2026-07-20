"""Shared pytest fixtures for the Flask application."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Iterator

import pytest
from flask.testing import FlaskClient

PROJECT_MODULES = ("app", "analysis", "db")


@pytest.fixture
def app_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[tuple[FlaskClient, object, Path]]:
    """Create an isolated Flask client backed by a temporary SQLite database."""
    database_path = tmp_path / "fingerprints-test.s3db"
    monkeypatch.setenv("BROWSER_FP_DB", str(database_path))

    # app.py initializes the database during import. Remove previously imported
    # project modules so every test receives the temporary database path.
    for module_name in PROJECT_MODULES:
        sys.modules.pop(module_name, None)

    app_module = importlib.import_module("app")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        yield client, app_module, database_path

    for module_name in PROJECT_MODULES:
        sys.modules.pop(module_name, None)
