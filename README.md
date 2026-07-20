# Browser Fingerprint Lab

A cleaned public version of a bachelor-thesis prototype for collecting browser
fingerprint attributes and exploring their categorical entropy.

The repository contains **no collected dataset**. Each installation creates its
own local SQLite database under `data/`, and that directory is excluded from Git.

## What it collects

After the user explicitly presses the collection button, the local demo records:

- User-Agent, platform and language;
- screen resolution and colour depth;
- a deterministic canvas hash;
- WebGL vendor and renderer when the browser exposes them;
- a small font-availability sample and plugin names;
- selected HTTP request headers;
- storage, cookie, Do Not Track and ad-blocking signals.

## Architecture

```text
Browser UI
   │  explicit collection
   ▼
Flask JSON API
   │
   ├── SQLite: local samples only
   └── standard-library entropy analysis
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:8080`.

The database is created automatically at `data/fingerprints.s3db`.

## Run with Docker

```bash
docker compose up --build
```

The `./data` directory is mounted into the container, so local samples survive a
container restart but are not committed to Git.

## Privacy and ethical use

This project is an educational research prototype, not a production tracking,
anti-fraud or identification system. Run it only on systems you control or with
informed consent. Do not publish collected datasets without an appropriate legal
and ethical basis.

See [docs/PRIVACY.md](docs/PRIVACY.md).

## Limitations

- Browser APIs and privacy protections change over time.
- Several values may be masked, unavailable or deliberately standardised.
- The entropy numbers describe only the local collected sample.
- “Information gain” is a retained legacy pairwise heuristic and should not be
  interpreted as causal importance or a rigorous uniqueness score.
- The built-in development server is for local demonstration only.

## Historical note

The original project was created as a bachelor-thesis prototype. This public
edition removes the historical database and runtime artefacts, replaces log-file
parsing with a JSON API, removes obsolete front-end dependencies, and requires an
explicit user action before collection.

## License

MIT — see [LICENSE](LICENSE).
