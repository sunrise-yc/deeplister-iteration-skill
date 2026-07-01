#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print a compact snapshot of a DeepLister iteration record."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
DONE_STATUSES = {"已解决", "完成", "done", "closed", "resolved"}


def section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown_table(block: str) -> list[dict[str, str]]:
    rows = []
    headers: list[str] | None = None
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or "|" not in line[1:]:
            continue
        cells = split_table_row(line)
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if headers is None:
            headers = cells
            continue
        if len(cells) < len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def parse_iterations(block: str) -> list[str]:
    return re.findall(r"^###\s+(.+?)\s*$", block, flags=re.MULTILINE)


def issue_sort_key(issue: dict[str, str]) -> tuple[int, str]:
    priority = issue.get("优先级", "").upper()
    issue_id = issue.get("编号", "")
    return (PRIORITY_ORDER.get(priority, 99), issue_id)


def build_snapshot(project_root: Path, record_path: Path | None = None) -> dict:
    record = record_path or project_root / "docs" / "迭代记录.md"
    text = record.read_text(encoding="utf-8")

    issues = parse_markdown_table(section(text, "问题池"))
    unresolved = [
        issue
        for issue in issues
        if issue.get("状态", "").strip().lower() not in DONE_STATUSES
    ]
    unresolved.sort(key=issue_sort_key)

    issue_counts = Counter(
        f"{issue.get('优先级', '未标优先级')} / {issue.get('状态', '未知状态')}"
        for issue in issues
    )

    follow_up_rows = parse_markdown_table(section(text, "追问流程专项记录"))
    iterations = parse_iterations(section(text, "迭代记录"))

    return {
        "record": str(record),
        "issue_count": len(issues),
        "unresolved_count": len(unresolved),
        "issue_counts": dict(sorted(issue_counts.items())),
        "recommended_next": unresolved[0] if unresolved else None,
        "top_unresolved": unresolved[:5],
        "latest_iteration": iterations[0] if iterations else None,
        "follow_up_case_count": len(follow_up_rows),
    }


def print_text(snapshot: dict) -> None:
    print(f"Record: {snapshot['record']}")
    print(f"Issues: {snapshot['issue_count']} total, {snapshot['unresolved_count']} unresolved")

    if snapshot["issue_counts"]:
        print("Issue counts:")
        for key, count in snapshot["issue_counts"].items():
            print(f"  - {key}: {count}")

    recommended = snapshot["recommended_next"]
    if recommended:
        print("Recommended next task:")
        print(f"  - {recommended.get('编号', '')} [{recommended.get('优先级', '')}] {recommended.get('问题', '')}")
        print(f"    Next: {recommended.get('下一步', '')}")
    else:
        print("Recommended next task: none")

    latest = snapshot["latest_iteration"] or "none"
    print(f"Latest iteration: {latest}")
    print(f"Follow-up flow cases: {snapshot['follow_up_case_count']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="DeepLister project root")
    parser.add_argument("--record", help="Explicit iteration record path")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    record_path = Path(args.record).resolve() if args.record else None
    snapshot = build_snapshot(project_root, record_path)

    if args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        print_text(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
