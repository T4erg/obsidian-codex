# Obsidian Codex

Obsidian Codex is a local Codex plugin that lets Codex operate an Obsidian vault through the official Obsidian CLI, local markdown files, and optional MCP or REST bridges.

The plugin is inspired by compounding-wiki workflows: sources become durable notes, sessions can be saved, indexes are maintained, and the vault can be queried, edited, linked, tagged, linted, and organized over time.

## Features

- Search and read notes from an Obsidian vault.
- Create, append, and update markdown notes.
- Inventory tags and inspect backlinks.
- Detect empty notes, missing frontmatter, orphan notes, and dead wikilinks.
- Use the official `obsidian` CLI for live Obsidian actions when available.
- Provide a Codex skill for note cleanup, summarization, linking, tagging, source ingestion, MOC pages, and research workflows.
- Include an optional MCP filesystem vault bridge template.

## Install

Clone this repository:

```bash
git clone git@github.com:T4erg/obsidian-codex.git
cd obsidian-codex
```

Use this repository as a Codex workspace. The local plugin marketplace entry is already defined in:

```text
.agents/plugins/marketplace.json
```

For user-wide local installation, copy the plugin directory to `~/plugins/obsidian-codex` and add the same marketplace entry to `~/.agents/plugins/marketplace.json`.

## Obsidian Setup

1. Install Obsidian 1.12 or newer.
2. Enable **Settings -> General -> Command line interface**.
3. Register the `obsidian` command from Obsidian's setup prompt.
4. Set your vault path:

```bash
export OBSIDIAN_VAULT="/path/to/your/vault"
```

Do not commit `.env` files or vault-specific local configuration.

## Quick Check

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py doctor --vault "/path/to/your/vault"
python3 plugins/obsidian-codex/scripts/obsidian_vault.py search "agent notes" --vault "/path/to/your/vault"
python3 plugins/obsidian-codex/scripts/obsidian_vault.py lint --vault "/path/to/your/vault"
```

## Usage In Codex

After installing the plugin in Codex, ask for tasks such as:

- Search my Obsidian vault for notes about this topic.
- Clean up this note and add tags, aliases, summary, and related links.
- Find orphan notes and dead links in my vault.
- Save this conversation into my Obsidian daily note.
- Create a topic index/MOC from these related notes.

## Repository Layout

```text
.agents/plugins/marketplace.json
plugins/obsidian-codex/.codex-plugin/plugin.json
plugins/obsidian-codex/skills/obsidian/SKILL.md
plugins/obsidian-codex/scripts/obsidian_vault.py
plugins/obsidian-codex/.mcp.json
```

## Security

This plugin is intended to operate on local user vaults. Treat vault paths, REST API keys, private notes, and `.env` files as sensitive. The repository ignores common local files and environment files by default.

Before publishing changes, run a secret scan such as:

```bash
rg -n "(api[_-]?key|token|secret|password|BEGIN (RSA|OPENSSH|PRIVATE)|sk-|github_pat|ghp_)" .
```

## License

MIT

