#!/usr/bin/env python3
"""Check that every [[wikilink]] and ![[embed]] in a vault resolves unambiguously,
and that no table cell holds a pipe-aliased link.

Usage: check_wikilinks.py VAULT_ROOT
Exit status 1 if anything is broken.
"""
import re
import sys
from pathlib import Path

LINK = re.compile(r"\[\[([^\]]+?)\]\]")
INLINE_CODE = re.compile(r"`[^`]*`")


def main(root: Path) -> int:
    all_files = [p for p in root.rglob("*") if p.is_file() and ".obsidian" not in p.parts]
    md_files = [p for p in all_files if p.suffix == ".md"]
    by_stem, by_name = {}, {}
    for p in all_files:
        by_name.setdefault(p.name, []).append(p)
        if p.suffix == ".md":
            by_stem.setdefault(p.stem, []).append(p)
    problems = 0
    for p in md_files:
        in_fence = False
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            if in_fence:
                continue
            stripped = INLINE_CODE.sub("", line)  # Obsidian does not link inside backticks
            for raw in LINK.findall(stripped):
                raw = raw.replace("\\|", "|")
                target = raw.split("|")[0].split("#")[0].split("^")[0].strip()
                if stripped.lstrip().startswith("|") and "|" in raw:
                    print(f"{p}:{n}: pipe-aliased link inside a table cell: [[{raw}]]")
                    problems += 1
                if not target:
                    continue  # heading-only link within the same file
                if "/" in target:
                    ok = (root / (target + ".md")).exists() or (root / target).exists()
                    if not ok:
                        print(f"{p}:{n}: unresolved link [[{raw}]]")
                        problems += 1
                    continue
                matches = by_name.get(target) if "." in target else by_stem.get(target)
                if not matches:
                    print(f"{p}:{n}: unresolved link [[{raw}]]")
                    problems += 1
                elif len(matches) > 1:
                    where = ", ".join(str(m.relative_to(root)) for m in matches)
                    print(f"{p}:{n}: ambiguous link [[{raw}]] matches {len(matches)} files ({where}); use the full vault path")
                    problems += 1
    print(f"{len(md_files)} files, {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
