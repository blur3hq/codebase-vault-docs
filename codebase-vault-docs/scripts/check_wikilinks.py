#!/usr/bin/env python3
"""Check that every [[wikilink]] in a vault resolves, and that no table cell holds a pipe-aliased link.

Usage: check_wikilinks.py VAULT_ROOT
Exit status 1 if anything is broken.
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[\[([^\]]+?)\]\]")


def main(root: Path) -> int:
    md_files = [p for p in root.rglob("*.md") if ".obsidian" not in p.parts]
    by_stem = {}
    for p in md_files:
        by_stem.setdefault(p.stem, []).append(p)
    problems = 0
    for p in md_files:
        in_fence = False
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            if in_fence:
                continue
            for raw in LINK.findall(line):
                raw = raw.replace("\\|", "|")
                target = raw.split("|")[0].split("#")[0].split("^")[0].strip()
                if line.lstrip().startswith("|") and "|" in raw:
                    print(f"{p}:{n}: pipe-aliased link inside a table cell: [[{raw}]]")
                    problems += 1
                if not target:
                    continue  # heading-only link within the same file
                if "/" in target:
                    ok = (root / (target + ".md")).exists() or (root / target).exists()
                else:
                    ok = target in by_stem or (root / target).exists()
                if not ok:
                    print(f"{p}:{n}: unresolved link [[{raw}]]")
                    problems += 1
    print(f"{len(md_files)} files, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
