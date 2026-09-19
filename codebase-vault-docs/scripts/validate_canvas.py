#!/usr/bin/env python3
"""Validate every .canvas file under a vault: JSON parses, edges point at real nodes,
edges only join adjacent rows, and same-row nodes do not overlap horizontally.

Usage: validate_canvas.py VAULT_ROOT
Exit status 1 on parse errors or dangling edges; layout issues are reported as warnings.
"""
import json
import sys
from pathlib import Path

ROW_TOLERANCE = 20  # px; nodes whose y differs by less than this share a row


def check(path: Path) -> tuple[int, int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path}: invalid JSON: {e}")
        return 1, 0
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    errors = warnings = 0
    rows = sorted({n["y"] for n in nodes.values()})
    row_of = {}
    for nid, n in nodes.items():
        row_of[nid] = next(i for i, y in enumerate(rows) if abs(n["y"] - y) < ROW_TOLERANCE)
    for e in data.get("edges", []):
        a, b = e.get("fromNode"), e.get("toNode")
        if a not in nodes or b not in nodes:
            print(f"{path}: edge {e.get('id')} references a missing node ({a} -> {b})")
            errors += 1
            continue
        if abs(row_of[a] - row_of[b]) > 1:
            print(f"{path}: edge {a} -> {b} skips {abs(row_of[a] - row_of[b]) - 1} row(s); mention it in prose instead")
            warnings += 1
    by_row = {}
    for nid, r in row_of.items():
        by_row.setdefault(r, []).append(nodes[nid])
    for r, ns in by_row.items():
        ns.sort(key=lambda n: n["x"])
        for left, right in zip(ns, ns[1:]):
            if left["x"] + left["width"] > right["x"]:
                print(f"{path}: nodes {left['id']} and {right['id']} overlap in row {r}")
                warnings += 1
    return errors, warnings


def main(root: Path) -> int:
    files = list(root.rglob("*.canvas"))
    errors = warnings = 0
    for f in files:
        e, w = check(f)
        errors += e
        warnings += w
    print(f"{len(files)} canvas file(s), {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
