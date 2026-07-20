# Privacy and data handling

- The repository ships without a fingerprint database.
- The application creates `data/fingerprints.s3db` locally.
- `data/` and common SQLite extensions are excluded through `.gitignore`.
- Collection starts only after an explicit button press.
- The application does not transmit samples to a third-party service.
- Operators are responsible for consent, retention, access control and deletion.

To reset the local dataset, stop the application and delete:

```bash
rm -f data/fingerprints.s3db
```

A fresh empty database will be created on the next start.
