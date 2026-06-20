# Contributing to Gestione Bocciofila

## Before you start

- Read `README.md`.
- Treat operational club data as sensitive.
- Do not commit activation files, debug logs, or exported player datasets.

## Development rules

- Keep changes scoped and reviewable.
- Prefer removing obsolete artifacts over preserving historical noise.
- If you change the deployed bundle references, update `index.html` and `sw.js` together.
- If you improve deployment behavior, keep FTP configuration environment-based.

## Pull requests

Each PR should include:
- a short problem statement;
- the chosen approach;
- validation performed;
- notes on any operational or deployment impact.

## Validation

Minimum expected checks:
- verify referenced JS/CSS bundle paths remain consistent
- verify PWA/service-worker paths if touched
- verify no secrets or club-specific data were introduced
