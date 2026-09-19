#!/usr/bin/env python3
"""Validate every .canvas file under a vault: JSON parses, edges point at real nodes,
edges only join adjacent rows, and same-row nodes keep the minimum horizontal gap.

Usage: validate_canvas.py VAULT_ROOT
Exit status 1 on parse errors or dangling edges; layout issues are reported as warnings.
"""
import json
import sys
from pathlib import Path

ROW_TOLERANCE = 20  # px; nodes whose y differ by less than this share a row
MIN_GAP = 60  # px between neighbors in a row, per the layout rules


def check(path: Path) -> tuple[int, int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{path}: invalid JSON: {e}")
        return 1, 0
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    boxes = {nid: n for nid, n in nodes.items() if n.get("type") != "group"}  # groups span rows
    errors = warnings = 0
    tops: list[float] = []
    for y in sorted(n["y"] for n in boxes.values()):
        if not tops or y - tops[-1] >= ROW_TOLERANCE:
            tops.append(y)
    row_of = {nid: max(i for i, t in enumerate(tops) if n["y"] >= t - ROW_TOLERANCE) for nid, n in boxes.items()}
    for e in data.get("edges", []):
        a, b = e.get("fromNode"), e.get("toNode")
        if a not in nodes or b not in nodes:
            print(f"{path}: edge {e.get('id')} references a missing node ({a} -> {b})")
            errors += 1
            continue
        if a in row_of and b in row_of and abs(row_of[a] - row_of[b]) > 1:
            print(f"{path}: edge {a} -> {b} skips {abs(row_of[a] - row_of[b]) - 1} row(s); mention it in prose instead")
            warnings += 1
    by_row: dict[int, list] = {}
    for nid, r in row_of.items():
        by_row.setdefault(r, []).append(boxes[nid])
    for r, ns in by_row.items():
        ns.sort(key=lambda n: n["x"])
        for left, right in zip(ns, ns[1:]):
            gap = right["x"] - (left["x"] + left["width"])
            if gap < 0:
                print(f"{path}: nodes {left['id']} and {right['id']} overlap in row {r}")
                warnings += 1
            elif gap < MIN_GAP:
                print(f"{path}: nodes {left['id']} and {right['id']} are {gap:.0f}px apart in row {r}; keep {MIN_GAP}px")
                warnings += 1
    return errors, warnings


def main(root: Path) -> int:
    files = sorted(root.rglob("*.canvas"))
    errors = warnings = 0
    for f in files:
        e, w = check(f)
        errors += e
        warnings += w
    print(f"{len(files)} canvas file(s), {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
