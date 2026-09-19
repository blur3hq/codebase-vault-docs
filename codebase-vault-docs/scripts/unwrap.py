#!/usr/bin/env python3
"""Join hard-wrapped paragraphs and list items into single lines, the way Obsidian expects.

Usage: unwrap.py VAULT_ROOT [--check]
--check only reports files that contain hard-wrapped text (exit 1 if any).
Without it, files are rewritten in place and the word count is verified unchanged.

Rules: blank lines, headings, table rows, list markers and fence toggles reset the
buffer; fenced blocks are copied verbatim; a list item keeps its own indentation.
"""
import re
import sys
from pathlib import Path

BREAK = re.compile(r"^\s*(#|\||---|>)")
LIST = re.compile(r"^\s*([-*+]|\d+\.)\s")
FENCE = re.compile(r"^\s*(```|~~~|\$\$\s*$)")  # code fences and display-math blocks


def unwrap(text: str) -> tuple[str, int]:
    out, buf, joins, in_fence = [], [], 0, False
    for line in text.split("\n"):
        if FENCE.match(line):
            if buf:
                out.append(" ".join(buf)); buf = []
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or not line.strip() or BREAK.match(line):
            if buf:
                out.append(" ".join(buf)); buf = []
            out.append(line)
            continue
        if LIST.match(line) or not buf:
            if buf:
                out.append(" ".join(buf))
            buf = [line]  # keep the first line's own indentation
        else:
            buf.append(line.strip()); joins += 1
    if buf:
        out.append(" ".join(buf))
    return "\n".join(out), joins


def main(argv: list[str]) -> int:
    check = "--check" in argv
    args = [a for a in argv if a != "--check"]
    root = Path(args[0] if args else ".")
    bad = 0
    for p in root.rglob("*.md"):
        if ".obsidian" in p.parts:
            continue
        src = p.read_text(encoding="utf-8")
        new, joins = unwrap(src)
        if not joins:
            continue
        bad += 1
        if check:
            print(f"{p}: {joins} hard-wrapped line(s)")
            continue
        assert len(src.split()) == len(new.split()), f"word count changed in {p}, not writing"
        p.write_text(new, encoding="utf-8")
        print(f"{p}: joined {joins} line(s)")
    return 1 if (check and bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
