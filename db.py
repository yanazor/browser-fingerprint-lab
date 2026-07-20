"""SQLite persistence for the browser-fingerprint demo."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Mapping

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(
    os.environ.get("BROWSER_FP_DB", BASE_DIR / "data" / "fingerprints.s3db")
)
SCHEMA_PATH = BASE_DIR / "schema.sql"

FINGERPRINT_COLUMNS = (
    "list_of_plugins",
    "useragent",
    "list_of_fonts",
    "canvas",
    "language",
    "resolution",
    "color_depth",
    "accept_headers",
    "timezone",
    "webgl_renderer",
    "platform",
    "webgl_vendor",
    "content_encoding",
    "accept_lang",
    "adblock",
    "donottrack",
    "local_storage",
    "session_storage",
    "cookie",
)


def connect() -> sqlite3.Connection:
    """Open the local SQLite database and return rows as dictionaries."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    """Create the database schema when it does not exist yet."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect() as connection:
        connection.executescript(schema)


def _normalise_value(value: Any) -> str:
    """Store browser values consistently as text."""
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def insert_fingerprint(payload: Mapping[str, Any]) -> int:
    """Insert one browser fingerprint and return its generated row id."""
    values = [_normalise_value(payload.get(column)) for column in FINGERPRINT_COLUMNS]
    placeholders = ", ".join("?" for _ in FINGERPRINT_COLUMNS)
    columns = ", ".join(FINGERPRINT_COLUMNS)

    with connect() as connection:
        cursor = connection.execute(
            f"INSERT INTO fingerprints ({columns}) VALUES ({placeholders})",
            values,
        )
        return int(cursor.lastrowid)


def read_fingerprints() -> list[dict[str, str]]:
    """Return all collected fingerprints for local exploratory analysis."""
    columns = ", ".join(FINGERPRINT_COLUMNS)
    with connect() as connection:
        rows = connection.execute(
            f"SELECT {columns} FROM fingerprints ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]
