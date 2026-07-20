"""Flask application for a local browser-fingerprint research demo."""

from __future__ import annotations

import os
from typing import Any

from flask import Flask, jsonify, render_template, request

from analysis import analyse
from db import init_database, insert_fingerprint, read_fingerprints

app = Flask(__name__)
init_database()


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/browser-fingerprint/")
def browser_fingerprint() -> str:
    return render_template("browser_fingerprint.html")


@app.get("/api/headers")
def request_headers() -> Any:
    """Return only the HTTP request headers used by the local demo."""
    return jsonify(
        {
            "accept": request.headers.get("Accept", ""),
            "accept_encoding": request.headers.get("Accept-Encoding", ""),
            "accept_language": request.headers.get("Accept-Language", ""),
        }
    )


@app.post("/api/fingerprints")
def create_fingerprint() -> Any:
    """Store one explicitly submitted sample and return exploratory metrics."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Expected a JSON object."}), 400

    row_id = insert_fingerprint(payload)
    result = analyse(read_fingerprints())
    result["id"] = row_id
    return jsonify(result), 201


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=8080, debug=debug)
