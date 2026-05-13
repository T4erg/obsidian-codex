#!/usr/bin/env python3
"""Small local helper for Codex-driven Obsidian vault operations."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]#|]+)(?:[#|][^\]]*)?\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9][A-Za-z0-9_/-]*)")


def vault_root(args: argparse.Namespace) -> Path:
    raw = args.vault or os.environ.get("OBSIDIAN_VAULT")
    if not raw:
        raise SystemExit("Set OBSIDIAN_VAULT or pass --vault /path/to/vault.")
    root = Path(raw).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Vault does not exist or is not a directory: {root}")
    return root


def note_path(root: Path, rel_path: str) -> Path:
    rel = rel_path.strip().lstrip("/")
    path = (root / rel).resolve()
    if root != path and root not in path.parents:
        raise SystemExit(f"Path escapes vault: {rel_path}")
    return path


def markdown_files(root: Path) -> list[Path]:
    ignored = {".obsidian", ".trash", ".git", "node_modules"}
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in ignored for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def cmd_doctor(args: argparse.Namespace) -> None:
    root = vault_root(args)
    payload = {
        "vault": str(root),
        "markdown_files": len(markdown_files(root)),
        "obsidian_cli": shutil.which("obsidian"),
        "obsidian_config": (root / ".obsidian").exists(),
    }
    print(json.dumps(payload, indent=2))


def cmd_list(args: argparse.Namespace) -> None:
    root = vault_root(args)
    for path in markdown_files(root):
        print(rel(root, path))


def cmd_read(args: argparse.Namespace) -> None:
    root = vault_root(args)
    path = note_path(root, args.path)
    if not path.exists():
        raise SystemExit(f"Note not found: {args.path}")
    print(read_text(path), end="")


def cmd_write(args: argparse.Namespace) -> None:
    root = vault_root(args)
    path = note_path(root, args.path)
    text = sys.stdin.read() if args.stdin else args.content
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(rel(root, path))


def cmd_append(args: argparse.Namespace) -> None:
    root = vault_root(args)
    path = note_path(root, args.path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = ""
    if path.exists() and read_text(path) and not read_text(path).endswith("\n"):
        prefix = "\n"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(prefix + args.content)
        if not args.content.endswith("\n"):
            handle.write("\n")
    print(rel(root, path))


def cmd_search(args: argparse.Namespace) -> None:
    root = vault_root(args)
    query = args.query.lower()
    results = []
    for path in markdown_files(root):
        text = read_text(path)
        haystack = f"{rel(root, path)}\n{text}".lower()
        count = haystack.count(query)
        if count:
            first_line = next((line.strip() for line in text.splitlines() if query in line.lower()), "")
            results.append({"path": rel(root, path), "matches": count, "preview": first_line[:240]})
    results.sort(key=lambda item: (-item["matches"], item["path"]))
    print(json.dumps(results[: args.limit], indent=2, ensure_ascii=False))


def cmd_tags(args: argparse.Namespace) -> None:
    root = vault_root(args)
    counts: Counter[str] = Counter()
    for path in markdown_files(root):
        counts.update(TAG_RE.findall(read_text(path)))
    print(json.dumps(dict(sorted(counts.items())), indent=2, ensure_ascii=False))


def cmd_backlinks(args: argparse.Namespace) -> None:
    root = vault_root(args)
    target = Path(args.path).with_suffix("").name
    hits = []
    for path in markdown_files(root):
        text = read_text(path)
        links = [Path(match).with_suffix("").name for match in WIKILINK_RE.findall(text)]
        if target in links:
            hits.append(rel(root, path))
    print(json.dumps(hits, indent=2, ensure_ascii=False))


def cmd_lint(args: argparse.Namespace) -> None:
    root = vault_root(args)
    files = markdown_files(root)
    names = {path.with_suffix("").name: path for path in files}
    incoming: Counter[str] = Counter()
    dead_links: dict[str, list[str]] = {}
    missing_frontmatter = []
    empty = []

    for path in files:
        text = read_text(path)
        if not text.strip():
            empty.append(rel(root, path))
        if not text.startswith("---\n"):
            missing_frontmatter.append(rel(root, path))
        for raw_link in WIKILINK_RE.findall(text):
            name = Path(raw_link).with_suffix("").name
            if name in names:
                incoming[name] += 1
            else:
                dead_links.setdefault(rel(root, path), []).append(raw_link)

    orphans = [rel(root, path) for name, path in names.items() if incoming[name] == 0]
    payload = {
        "empty": empty,
        "missing_frontmatter": missing_frontmatter,
        "orphans": sorted(orphans),
        "dead_links": dead_links,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_cli(args: argparse.Namespace) -> None:
    executable = shutil.which("obsidian")
    if not executable:
        raise SystemExit("Obsidian CLI not found. Enable it in Obsidian Settings -> General.")
    completed = subprocess.run([executable, *args.obsidian_args], check=False)
    raise SystemExit(completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate an Obsidian vault for Codex workflows.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_vault_arg(command: argparse.ArgumentParser) -> argparse.ArgumentParser:
        command.add_argument("--vault", help="Path to the Obsidian vault. Defaults to OBSIDIAN_VAULT.")
        return command

    add_vault_arg(sub.add_parser("doctor")).set_defaults(func=cmd_doctor)
    add_vault_arg(sub.add_parser("list")).set_defaults(func=cmd_list)

    read = add_vault_arg(sub.add_parser("read"))
    read.add_argument("path")
    read.set_defaults(func=cmd_read)

    write = add_vault_arg(sub.add_parser("write"))
    write.add_argument("path")
    write.add_argument("content", nargs="?", default="")
    write.add_argument("--stdin", action="store_true")
    write.set_defaults(func=cmd_write)

    append = add_vault_arg(sub.add_parser("append"))
    append.add_argument("path")
    append.add_argument("content")
    append.set_defaults(func=cmd_append)

    search = add_vault_arg(sub.add_parser("search"))
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_search)

    add_vault_arg(sub.add_parser("tags")).set_defaults(func=cmd_tags)

    backlinks = add_vault_arg(sub.add_parser("backlinks"))
    backlinks.add_argument("path")
    backlinks.set_defaults(func=cmd_backlinks)

    add_vault_arg(sub.add_parser("lint")).set_defaults(func=cmd_lint)

    cli = sub.add_parser("cli")
    cli.add_argument("obsidian_args", nargs=argparse.REMAINDER)
    cli.set_defaults(func=cmd_cli)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
