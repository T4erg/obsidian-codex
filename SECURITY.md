# Security Policy

## Supported Versions

The `main` branch is the supported development line.

## Reporting A Vulnerability

Please report vulnerabilities through GitHub private vulnerability reporting if it is enabled on the repository. If not, open a minimal public issue that does not include secrets, private vault contents, API keys, or exploit details.

## Data Handling

Obsidian Codex works with local Obsidian vault data. Do not commit:

- Vault contents unless they are intentional examples.
- `.env` files.
- Obsidian Local REST API keys.
- Personal absolute vault paths.
- Private notes, attachments, or exported conversations.

