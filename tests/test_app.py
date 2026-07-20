"""HTTP and persistence tests for the Flask application."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flask.testing import FlaskClient


def unpack_bundle(
    app_bundle: tuple[FlaskClient, object, Path],
) -> tuple[FlaskClient, Any, Path]:
    return app_bundle


def test_index_page_is_available(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, _, _ = unpack_bundle(app_bundle)

    response = client.get("/")

    assert response.status_code == 200
    assert b"Browser Fingerprint Lab" in response.data
    assert b"Open the local demo" in response.data


def test_collection_page_is_available(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, _, _ = unpack_bundle(app_bundle)

    response = client.get("/browser-fingerprint/")

    assert response.status_code == 200
    assert b"Collect and store one sample" in response.data
    assert b"Run this project only in your own environment" in response.data


def test_headers_endpoint_returns_only_allowlisted_headers(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, _, _ = unpack_bundle(app_bundle)

    response = client.get(
        "/api/headers",
        headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en-US",
            "Authorization": "Bearer must-not-leak",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "accept": "application/json",
        "accept_encoding": "gzip",
        "accept_language": "en-US",
    }


def test_fingerprint_endpoint_rejects_non_object_json(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, _, _ = unpack_bundle(app_bundle)

    response = client.post(
        "/api/fingerprints",
        json=["this", "is", "not", "an", "object"],
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Expected a JSON object."}


def test_fingerprint_endpoint_rejects_invalid_json(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, _, _ = unpack_bundle(app_bundle)

    response = client.post(
        "/api/fingerprints",
        data="{broken-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Expected a JSON object."}


def test_fingerprints_are_stored_in_isolated_database(
    app_bundle: tuple[FlaskClient, object, Path],
) -> None:
    client, app_module, database_path = unpack_bundle(app_bundle)

    first_payload = {
        "useragent": "pytest-browser-one",
        "list_of_plugins": ["Synthetic PDF Viewer"],
        "language": "en-US",
        "canvas": "canvas-test-one",
        "local_storage": True,
        "session_storage": True,
        "cookie": False,
        "unexpected_field": "must be ignored",
    }
    second_payload = {
        "useragent": "pytest-browser-two",
        "list_of_plugins": [],
        "language": "ru-RU",
        "canvas": "canvas-test-two",
        "local_storage": False,
        "session_storage": True,
        "cookie": True,
    }

    first_response = client.post("/api/fingerprints", json=first_payload)
    second_response = client.post("/api/fingerprints", json=second_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_result = first_response.get_json()
    second_result = second_response.get_json()

    assert first_result["id"] == 1
    assert first_result["sample_count"] == 1
    assert second_result["id"] == 2
    assert second_result["sample_count"] == 2

    assert set(second_result) == {
        "id",
        "sample_count",
        "order",
        "entropy",
        "information_gain",
    }
    assert len(second_result["order"]) == 19

    rows = app_module.read_fingerprints()

    assert database_path.is_file()
    assert len(rows) == 2
    assert rows[0]["useragent"] == "pytest-browser-one"
    assert rows[0]["list_of_plugins"] == '["Synthetic PDF Viewer"]'
    assert rows[0]["local_storage"] == "true"
    assert rows[0]["cookie"] == "false"
    assert rows[1]["useragent"] == "pytest-browser-two"
    assert rows[1]["list_of_plugins"] == "[]"
    assert rows[1]["local_storage"] == "false"
    assert rows[1]["cookie"] == "true"
    assert "unexpected_field" not in rows[0]
