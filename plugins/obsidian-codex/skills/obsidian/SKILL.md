---
name: obsidian
description: Use when Codex needs to search, read, edit, organize, summarize, beautify, link, tag, lint, or otherwise operate an Obsidian vault through the official Obsidian CLI, local vault files, or optional REST/MCP bridges.
---

# Obsidian Codex

Use this skill whenever the user asks Codex to work with Obsidian notes or an Obsidian vault.

## Operating Model

Prefer this order:

1. Use an installed MCP or app connector if the current session exposes one for the user's Obsidian vault.
2. Use the official `obsidian` CLI for live Obsidian actions, command execution, active app behavior, search, daily notes, and command palette workflows.
3. Use `scripts/obsidian_vault.py` for deterministic local markdown operations when the vault path is known.
4. Use the Obsidian Local REST API only when the user has enabled it and supplied the API key through environment variables.

Never guess a vault path when writing. For reads, search likely local vault paths only when the user explicitly asks to discover vaults. Treat the vault as user data: preserve unrelated edits, avoid broad rewrites, and make the smallest change that completes the task.

## Setup Checks

Before write operations, verify:

- The vault path is known through `OBSIDIAN_VAULT`, user input, or project configuration.
- The target file path resolves inside the vault.
- The note is markdown unless the user asked to handle attachments or canvas files.
- Obsidian CLI availability when a live app action is required.

Run:

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py doctor --vault /path/to/vault
```

## Core Workflows

### Query Notes

Use search first, then read the most relevant notes. Cite note paths in the response.

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py search "topic" --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py read "Folder/Note.md" --vault /path/to/vault
```

For richer Obsidian-native search, use:

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py cli search query="topic"
```

### Edit Notes

Read the note first. Preserve frontmatter, existing links, task state, callouts, and embeds. Use patch-style edits for local repository files when the vault is inside the current workspace. For external vault writes, ask before making broad changes.

Use the helper for simple appends or exact file replacement:

```bash
python3 plugins/obsidian-codex/scripts/obsidian_vault.py append "Folder/Note.md" "Text to add" --vault /path/to/vault
python3 plugins/obsidian-codex/scripts/obsidian_vault.py write "Folder/Note.md" --stdin --vault /path/to/vault
```

### Organize and Link

For organization tasks:

- Normalize title, aliases, tags, status, source, created, and updated frontmatter.
- Add wikilinks to existing notes when names match real files.
- Build or update topic index/MOC pages.
- Keep source notes, concept notes, entity notes, project notes, and logs distinct.
- Add backlinks intentionally; do not create link spam.

### Beautify Notes

Improve scanability without changing meaning:

- Stable title and summary.
- Clear headings.
- Short intro.
- Tables for comparable data.
- Callouts for decisions, warnings, contradictions, and open questions.
- Tags and aliases in frontmatter.
- Related links at the end.

### Lint and Maintain

Check:

- Orphan notes with no incoming links.
- Dead wikilinks.
- Duplicate titles or aliases.
- Missing or inconsistent tags.
- Stale TODOs.
- Empty notes.
- Notes missing frontmatter.
- Attachments not referenced by any note.

### Source Ingestion

When ingesting a source, create durable notes rather than a one-off summary:

- Source note with citation metadata.
- Concept notes for reusable ideas.
- Entity notes for people, projects, organizations, tools, or papers.
- Index updates.
- Cross-links and tags.
- Open questions and follow-up research queue.

## Inspired Feature Set

This plugin adapts the strongest ideas from Claude Obsidian:

- `/wiki` equivalent: bootstrap or continue a structured vault.
- `/save` equivalent: save a conversation into a durable note.
- Ingest: convert files, links, or pasted content into connected notes.
- Query: answer from vault notes with cited note paths.
- Lint: detect orphans, dead links, stale claims, weak tags, and missing cross-references.
- Hot cache: maintain a short recent-context note such as `wiki/hot.md`.
- Auto research: create a research plan, collect sources, synthesize notes, and file gaps.
- Canvas-ready graph planning for visual maps and Obsidian canvas files.

## Safety Rules

- Do not delete notes unless the user explicitly asks.
- Do not bulk rename or move notes without showing the intended mapping first.
- Keep generated tags lowercase kebab-case unless the vault already uses a different convention.
- Preserve user prose where cleanup can be done with additive structure.
- When facts come from web research, include source links in the note.

