"""
session_tool.py — Claude Code session JSONL Swiss Army knife.

Commands:
  list     List all sessions (most recent first)
  summary  Quick summary of a single session
  parse    Full readable conversation dump
  search   Search inside a session for a keyword
  restore  Recreate Written files from a session
  find     Search across ALL sessions for a keyword
"""
import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Fix Windows console Unicode issues
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

PROJECTS_ROOT = Path(r"C:\Users\yahya\.claude\projects")

# ─── helpers ──────────────────────────────────────────────────────────────────

def iter_entries(jsonl_path):
    """Yield parsed JSON objects from a JSONL file, line by line."""
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    yield obj
            except json.JSONDecodeError:
                pass

def is_real_user_message(entry):
    return (
        entry.get("type") == "user"
        and "sourceToolAssistantUUID" not in entry
        and "promptId" in entry
    )

def get_user_text(entry):
    content = entry.get("message", {}).get("content", [])
    if isinstance(content, str):
        return content.strip()
    parts = []
    for c in content:
        if isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text", ""))
    return " ".join(parts).strip()

def get_tool_calls(entry):
    calls = []
    content = entry.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return calls
    for c in content:
        if isinstance(c, dict) and c.get("type") == "tool_use":
            calls.append((c.get("name", ""), c.get("input", {})))
    return calls

def get_assistant_text(entry):
    content = entry.get("message", {}).get("content", [])
    if not isinstance(content, list):
        return ""
    parts = []
    for c in content:
        if isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text", "").strip())
    return "\n".join(p for p in parts if p)

def find_slug_and_date(jsonl_path):
    slug, date_str = "", ""
    for entry in iter_entries(jsonl_path):
        t = entry.get("type", "")
        if t == "ai-title":
            slug = entry.get("aiTitle", "")
        ts = entry.get("timestamp", "")
        if ts and not date_str:
            date_str = ts[:10]
        if slug and date_str:
            break
    return slug, date_str

def out(text, output_file=None):
    if output_file:
        output_file.write(text + "\n")
    else:
        print(text)

# ─── commands ─────────────────────────────────────────────────────────────────

def cmd_list(args):
    sessions = []
    for jsonl in PROJECTS_ROOT.rglob("*.jsonl"):
        try:
            stat = jsonl.stat()
            slug, date_str = find_slug_and_date(jsonl)
            sessions.append((stat.st_mtime, jsonl, slug, date_str, stat.st_size))
        except Exception:
            pass

    sessions.sort(reverse=True)
    print(f"{'Date':<12} {'Size':>8}  {'Slug':<40} {'File'}")
    print("-" * 110)
    for mtime, path, slug, date_str, size in sessions[:50]:
        size_kb = size // 1024
        print(f"{date_str or '?':<12} {size_kb:>6}KB  {slug[:40]:<40} {path.name}")


def cmd_summary(args):
    path = Path(args.file)
    slug, date_str = find_slug_and_date(path)
    user_messages = []
    written_files = []
    bash_commands = []
    edited_files = []

    for entry in iter_entries(path):
        if is_real_user_message(entry):
            text = get_user_text(entry)
            if text:
                user_messages.append(text[:300])
        elif entry.get("type") == "assistant":
            for name, inp in get_tool_calls(entry):
                if name == "Write":
                    written_files.append(inp.get("file_path", ""))
                elif name == "Edit":
                    edited_files.append(inp.get("file_path", ""))
                elif name == "Bash":
                    bash_commands.append(inp.get("command", "")[:120])

    SEP = "=" * 70
    print(SEP)
    print(f"SESSION SUMMARY")
    print(f"  File:  {path.name}")
    print(f"  Date:  {date_str}")
    print(f"  Slug:  {slug}")
    print(SEP)

    print(f"\n[USER MESSAGES] ({len(user_messages)} total)")
    for i, msg in enumerate(user_messages, 1):
        print(f"  {i}. {msg[:200]}")

    print(f"\n[FILES WRITTEN] ({len(written_files)} total)")
    seen = {}
    for f in written_files:
        seen[f] = seen.get(f, 0) + 1
    for f, count in seen.items():
        suffix = f" (x{count})" if count > 1 else ""
        print(f"  {f}{suffix}")

    if edited_files:
        print(f"\n[FILES EDITED] ({len(set(edited_files))} unique)")
        for f in sorted(set(edited_files)):
            print(f"  {f}")

    if bash_commands:
        print(f"\n[BASH COMMANDS] ({len(bash_commands)} total)")
        for cmd in bash_commands[:20]:
            print(f"  $ {cmd}")
        if len(bash_commands) > 20:
            print(f"  ... and {len(bash_commands) - 20} more")


def cmd_parse(args):
    path = Path(args.file)
    writes_only = args.writes_only
    outf = open(args.output, "w", encoding="utf-8") if args.output else None
    SEP = "=" * 60

    try:
        for entry in iter_entries(path):
            etype = entry.get("type")

            if not writes_only and is_real_user_message(entry):
                text = get_user_text(entry)
                if text:
                    out(f"\n{SEP}\n[USER]\n{text}", outf)

            elif etype == "assistant":
                if not writes_only:
                    text = get_assistant_text(entry)
                    if text:
                        out(f"\n{SEP}\n[ASSISTANT]\n{text}", outf)

                for name, inp in get_tool_calls(entry):
                    if name == "Write":
                        fpath = inp.get("file_path", "")
                        content = inp.get("content", "")
                        out(f"\n{SEP}\n[WRITE] {fpath}\n```\n{content}\n```", outf)
                    elif name == "Edit" and not writes_only:
                        fpath = inp.get("file_path", "")
                        old = inp.get("old_string", "")[:200]
                        new = inp.get("new_string", "")[:200]
                        out(f"\n{SEP}\n[EDIT] {fpath}\n  OLD: {old!r}\n  NEW: {new!r}", outf)
                    elif name == "Bash" and not writes_only:
                        cmd = inp.get("command", "")
                        out(f"\n{SEP}\n[BASH] {cmd}", outf)
                    elif name not in ("Write", "Edit", "Bash", "Read") and not writes_only:
                        out(f"\n{SEP}\n[TOOL:{name}] {json.dumps(inp)[:200]}", outf)
    finally:
        if outf:
            outf.close()
            print(f"Saved to {args.output}")


def cmd_search(args):
    path = Path(args.file)
    keyword = args.keyword.lower()
    SEP = "-" * 60
    found = 0

    for entry in iter_entries(path):
        etype = entry.get("type")
        ts = entry.get("timestamp", "")[:19]

        if is_real_user_message(entry):
            text = get_user_text(entry)
            if keyword in text.lower():
                print(f"\n{SEP}\n[USER @ {ts}]\n{text[:500]}")
                found += 1

        elif etype == "assistant":
            text = get_assistant_text(entry)
            if keyword in text.lower():
                print(f"\n{SEP}\n[ASSISTANT @ {ts}]\n{text[:500]}")
                found += 1

            for name, inp in get_tool_calls(entry):
                inp_str = json.dumps(inp)
                if keyword in inp_str.lower():
                    if name == "Write":
                        print(f"\n{SEP}\n[WRITE @ {ts}] {inp.get('file_path','')}")
                        for line in inp.get("content", "").splitlines():
                            if keyword in line.lower():
                                print(f"  >> {line[:200]}")
                    elif name == "Bash":
                        print(f"\n{SEP}\n[BASH @ {ts}] {inp.get('command','')[:300]}")
                    else:
                        print(f"\n{SEP}\n[TOOL:{name} @ {ts}] {inp_str[:300]}")
                    found += 1

    print(f"\n{'=' * 60}\nFound {found} match(es) for '{args.keyword}'")


def cmd_restore(args):
    path = Path(args.file)
    prefix = args.prefix.rstrip("\\").rstrip("/")
    dry_run = args.dry_run

    file_writes = {}
    for entry in iter_entries(path):
        if entry.get("type") != "assistant":
            continue
        for name, inp in get_tool_calls(entry):
            if name == "Write":
                fpath = inp.get("file_path", "")
                if fpath.startswith(prefix):
                    file_writes[fpath] = inp.get("content", "")

    if not file_writes:
        print(f"No Write calls found with prefix: {prefix}")
        return

    print(f"{'DRY RUN — ' if dry_run else ''}Restoring {len(file_writes)} file(s):\n")
    for fpath, content in file_writes.items():
        print(f"  {fpath} ({len(content)} chars)")
        if not dry_run:
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"    -> Written")

    if dry_run:
        print("\n(dry run — nothing written, remove --dry-run to apply)")
    else:
        print(f"\nDone. {len(file_writes)} file(s) restored.")


def cmd_find(args):
    keyword = args.keyword.lower()
    project_filter = (args.project or "").lower()
    results = []

    for jsonl in PROJECTS_ROOT.rglob("*.jsonl"):
        if project_filter and project_filter not in str(jsonl).lower():
            continue
        try:
            found = False
            slug, date_str = "", ""
            for entry in iter_entries(jsonl):
                if not slug:
                    if entry.get("type") == "ai-title":
                        slug = entry.get("aiTitle", "")
                    ts = entry.get("timestamp", "")
                    if ts and not date_str:
                        date_str = ts[:10]
                if keyword in json.dumps(entry).lower():
                    found = True
                    break
            if found:
                results.append((date_str, jsonl, slug))
        except Exception:
            pass

    results.sort(reverse=True)
    if not results:
        print(f"No sessions found containing '{args.keyword}'")
        return

    print(f"Sessions containing '{args.keyword}':\n")
    for date_str, path, slug in results:
        print(f"  {date_str or '?':<12}  {slug[:40]:<40}  {path.name}")
    print(f"\n{len(results)} session(s) found.")


# ─── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Claude session JSONL tool")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all sessions")

    p = sub.add_parser("summary", help="Summarize a session")
    p.add_argument("file", help="Path to .jsonl file")

    p = sub.add_parser("parse", help="Parse session to readable text")
    p.add_argument("file", help="Path to .jsonl file")
    p.add_argument("--writes-only", action="store_true")
    p.add_argument("--output", "-o", help="Save output to this file")

    p = sub.add_parser("search", help="Search inside a session")
    p.add_argument("file", help="Path to .jsonl file")
    p.add_argument("--keyword", "-k", required=True)

    p = sub.add_parser("restore", help="Restore Written files from a session")
    p.add_argument("file", help="Path to .jsonl file")
    p.add_argument("--prefix", required=True)
    p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("find", help="Search across all sessions for a keyword")
    p.add_argument("--keyword", "-k", required=True)
    p.add_argument("--project", help="Filter by project name substring")

    args = parser.parse_args()
    {
        "list": cmd_list,
        "summary": cmd_summary,
        "parse": cmd_parse,
        "search": cmd_search,
        "restore": cmd_restore,
        "find": cmd_find,
    }[args.command](args)


if __name__ == "__main__":
    main()
