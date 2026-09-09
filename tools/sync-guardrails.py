#!/usr/bin/env python3
"""
Keeps the guardrails resource page in sync with the real, downloadable
files in docs/resources/claude-code-guardrails/.

The script and settings are shown on the page, shipped as downloads, and
re-implemented in JS for the live tester. Hand-copying them between those
places is how they drift apart (and how the audit-log claim ended up
wrong), so the page's code blocks are generated from the files instead.

Usage: python3 tools/sync-guardrails.py
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs/resources/claude-code-guardrails"
PAGE = ROOT / "en/resources/claude-code-guardrails.html"

BLOCKS = {"settings.json": SRC / "settings.json", "guard.sh": SRC / "guard.sh"}


def main() -> int:
    page = PAGE.read_text(encoding="utf-8")
    changed = []

    for name, path in BLOCKS.items():
        code = html.escape(path.read_text(encoding="utf-8").rstrip("\n"), quote=False)
        pattern = re.compile(
            r"(<!-- sync:" + re.escape(name) + r" --><pre><code>).*?(</code></pre><!-- /sync -->)",
            re.DOTALL,
        )
        if not pattern.search(page):
            print(f"ERROR: no sync markers for {name} in {PAGE.name}", file=sys.stderr)
            return 1
        new_page = pattern.sub(lambda m: m.group(1) + code + m.group(2), page)
        if new_page != page:
            changed.append(name)
        page = new_page

    PAGE.write_text(page, encoding="utf-8")
    print("synced:", ", ".join(changed) if changed else "already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
