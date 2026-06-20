# Security Policy

## Scope

Gestione Bocciofila may be used with operational club data and player information.

## Do not publish

- activation files
- FTP credentials
- debug logs
- exported player CSV files
- club-specific operational datasets

## Reporting

Please do not open public issues for live security problems that expose credentials or real user data.

Report privately to the maintainer with:
- affected file or flow
- impact
- reproduction steps
- suggested mitigation

## Contributor rules

- Never commit secrets.
- Never commit real club datasets.
- Prefer environment variables and example configurations over embedded credentials.
