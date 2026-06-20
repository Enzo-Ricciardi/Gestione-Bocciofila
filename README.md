# Gestione Bocciofila

Gestione Bocciofila is a browser-based web application for bocce clubs, focused on player management, random draws, match organization, printable boards, and local-first operational workflows.

This repository contains the standalone public-ready extraction of the application from the broader website monorepo.

## Current scope

- Player list management
- Presence tracking
- Automatic draw generation
- Court assignment
- Match result entry
- Printable summaries
- CSV import/export for player lists
- Backup-oriented local workflow

## Architecture

The current public repository is build-oriented:
- `index.html` loads the current production bundle from `assets/`
- service worker support is provided through `sw.js`
- a small set of PHP utilities remains for free-access and deployment diagnostics

## Repository structure

- `index.html` — application entry page
- `assets/` — current production JS/CSS bundle
- `sw.js` — service worker
- `license_manager.php` — free-access API response
- `admin_generator.php` — free-access informational page
- `test_server.php` — optional server write test
- `deploy_bocciofila.py` — FTP deployment script

## Local development

This repository currently exposes the production-ready web app bundle rather than the original front-end source tree.

You can still:
- inspect and review the deployed application structure
- improve deployment, documentation, and surrounding PHP/PWA behavior
- help define a cleaner source-level build workflow for future collaboration

To preview locally, serve the repository root with a static or PHP-capable local server.

## Configuration

Deployment credentials must be provided through environment variables:
- `BOCCE_FTP_HOST`
- `BOCCE_FTP_USER`
- `BOCCE_FTP_PASS`
- optional: `BOCCE_FTP_TLS`

Do not commit:
- activation records
- debug logs
- player CSV exports
- real operational datasets

## Project status

Gestione Bocciofila is being prepared for open collaboration.

Current priorities:
- repository hygiene
- contributor onboarding
- clearer source/build workflow
- reduction of operational-only artifacts in version control

## Contributing

See `CONTRIBUTING.md`.

## Security

See `SECURITY.md`.

## License

MIT License. See `LICENSE`.
