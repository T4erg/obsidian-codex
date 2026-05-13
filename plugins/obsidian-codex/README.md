# Obsidian Codex

Obsidian Codex is a local Codex plugin for operating an Obsidian vault. It is inspired by the Claude Obsidian compounding wiki workflow: sources become durable notes, notes are indexed and linked, sessions can be saved, and the vault is kept healthy with linting and cleanup passes.

The plugin is designed around three integration layers:

- Official Obsidian CLI for live Obsidian actions, command execution, search, daily notes, and app-aware workflows.
- Local vault file operations for reliable markdown reads, writes, search, tags, backlinks, and frontmatter edits.
- Optional REST or MCP bridge for users who enable Obsidian Local REST API or an Obsidian CLI REST/MCP server.

## Setup

1. Install Obsidian 1.12+ and enable **Settings -> General -> Command line interface**.
2. Register the `obsidian` command from Obsidian's setup prompt.
3. Keep Obsidian running when using CLI-backed commands.
4. Set `OBSIDIAN_VAULT` to your vault path, or pass `--vault /path/to/vault` to the helper script.

Optional deeper integration:

- Enable the Obsidian Local REST API plugin for authenticated REST access.
- Use an MCP bridge such as a filesystem vault server or Obsidian CLI REST server when you want tool-native access.

## Helper Script

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py doctor --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py search "project roadmap" --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py read "Projects/Roadmap.md" --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py tags --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py backlinks "Projects/Roadmap.md" --vault /path/to/vault
```

For live Obsidian CLI commands:

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py cli search query="meeting notes"
python3 plugins/obsidian-codex/scripts/obsidian_vault.py cli daily:append content="- [ ] Review notes"
```

## Capability Map

- Query: full-text search, file lookup, tag inventory, backlink lookup, index traversal.
- Edit: create, overwrite, append, frontmatter-aware cleanup guidance, section-safe edits through local files or REST when configured.
- Organize: tag suggestions, folder placement, index pages, MOC pages, backlink creation, orphan detection.
- Summarize: source ingestion, session saving, rolling `wiki/hot.md`, topic briefs, executive summaries.
- Maintain: dead wikilink checks, orphan pages, missing frontmatter, duplicate title detection, stale TODO sweeps.
- Beautify: note template normalization, headings, callouts, tables, metadata, embeds, and concise summaries.
- Research: source-first notes with citations, gap lists, follow-up research plans, and review queues.

