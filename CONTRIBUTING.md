# Contributing

Contributions are welcome.

## Development Checklist

Before opening a pull request:

1. Keep changes scoped to the plugin behavior or documentation.
2. Do not commit vault contents, `.env` files, API keys, or local machine paths.
3. Validate JSON files:

```bash
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/obsidian-codex/.codex-plugin/plugin.json
python3 -m json.tool plugins/obsidian-codex/.mcp.json
```

4. Validate the helper script:

```bash
python3 -B -m py_compile plugins/obsidian-codex/scripts/obsidian_vault.py
```

## Style

- Prefer small, reviewable changes.
- Keep user data local by default.
- Document any new Obsidian CLI, REST, or MCP dependency.

