#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a neutral Vibe Lens snapshot and optional HTML review sandbox."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any


DEFAULT_RECORD = Path("docs") / "iteration-record.md"
DEFAULT_REPORT = Path("docs") / "vibe-lens-report.html"
LEGACY_RECORDS = [Path("docs") / "迭代记录.md"]

DONE_STATUSES = {
    "done",
    "closed",
    "resolved",
    "complete",
    "completed",
    "verified",
    "已解决",
    "完成",
    "已验证",
}

SECTION_ALIASES = {
    "issue_pool": ["Issue Pool", "问题池"],
    "active_work": ["Active Work", "当前工作", "进行中工作"],
    "follow_up": ["Follow-up Flow Notes", "追问流程专项记录"],
    "iteration_log": ["Iteration Log", "迭代记录"],
    "direction": ["Current Product Direction", "当前产品方向", "产品方向"],
}

FIELD_ALIASES = {
    "id": ["ID", "编号"],
    "issue": ["Issue", "Question", "问题"],
    "impact": ["Impact", "影响"],
    "priority": ["Priority", "Signal", "优先级"],
    "status": ["Status", "状态"],
    "next_step": ["Next Step", "Next View", "下一步"],
    "files": ["Files Or Areas", "Related Files", "关联文件", "涉及文件"],
    "source": ["Source", "来源"],
    "evidence": ["Evidence", "证据"],
}


def section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def section_any(text: str, headings: list[str]) -> str:
    for heading in headings:
        block = section(text, heading)
        if block:
            return block
    return ""


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


def value(row: dict[str, str], field: str, default: str = "") -> str:
    for name in FIELD_ALIASES[field]:
        if name in row:
            return row[name]
    return default


def is_open_issue(issue: dict[str, str]) -> bool:
    return value(issue, "status").strip().lower() not in DONE_STATUSES


def resolve_record(project_root: Path, record_path: Path | None = None) -> Path:
    if record_path:
        return record_path

    candidates = [project_root / DEFAULT_RECORD]
    candidates.extend(project_root / legacy for legacy in LEGACY_RECORDS)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return project_root / DEFAULT_RECORD


def run_git(project_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )


def has_git_head(project_root: Path) -> bool:
    return run_git(project_root, ["rev-parse", "--verify", "HEAD"]).returncode == 0


def collect_git_diff(project_root: Path, diff_ref: str | None = None) -> dict[str, Any]:
    inside = run_git(project_root, ["rev-parse", "--is-inside-work-tree"])
    if inside.returncode != 0:
        return {
            "available": False,
            "range": "none",
            "total_added": 0,
            "total_deleted": 0,
            "changed_file_count": 0,
            "files": [],
            "untracked_files": [],
            "status": [],
        }

    base_args = [diff_ref] if diff_ref else (["HEAD"] if has_git_head(project_root) else [])
    numstat = run_git(project_root, ["diff", "--numstat", *base_args])
    name_status = run_git(project_root, ["diff", "--name-status", *base_args])
    status = run_git(project_root, ["status", "--short", "--untracked-files=all"])

    files = []
    total_added = 0
    total_deleted = 0
    if numstat.returncode == 0:
        for line in numstat.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            added_raw, deleted_raw, path = parts[0], parts[1], parts[2]
            added = int(added_raw) if added_raw.isdigit() else None
            deleted = int(deleted_raw) if deleted_raw.isdigit() else None
            if added is not None:
                total_added += added
            if deleted is not None:
                total_deleted += deleted
            files.append(
                {
                    "path": path,
                    "added": added,
                    "deleted": deleted,
                    "binary": added is None or deleted is None,
                }
            )

    file_status = []
    if name_status.returncode == 0:
        for line in name_status.stdout.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                file_status.append({"status": parts[0], "path": parts[-1]})

    untracked = []
    status_rows = []
    if status.returncode == 0:
        for line in status.stdout.splitlines():
            if not line:
                continue
            code = line[:2]
            path = line[3:].strip()
            status_rows.append({"status": code.strip(), "path": path})
            if code == "??":
                untracked.append(path)

    return {
        "available": True,
        "range": diff_ref or ("HEAD" if base_args else "working tree"),
        "total_added": total_added,
        "total_deleted": total_deleted,
        "changed_file_count": len(files),
        "files": files,
        "file_status": file_status,
        "untracked_files": sorted(untracked),
        "status": status_rows,
    }


def build_snapshot(
    project_root: Path,
    record_path: Path | None = None,
    diff_ref: str | None = None,
) -> dict[str, Any]:
    record = resolve_record(project_root, record_path)
    text = record.read_text(encoding="utf-8")

    issues = parse_markdown_table(section_any(text, SECTION_ALIASES["issue_pool"]))
    open_questions = [issue for issue in issues if is_open_issue(issue)]
    issue_counts = Counter(value(issue, "status", "unknown") for issue in issues)

    active_work_rows = parse_markdown_table(section_any(text, SECTION_ALIASES["active_work"]))
    follow_up_rows = parse_markdown_table(section_any(text, SECTION_ALIASES["follow_up"]))
    iterations = parse_iterations(section_any(text, SECTION_ALIASES["iteration_log"]))
    direction_text = section_any(text, SECTION_ALIASES["direction"])

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(project_root),
        "record": str(record),
        "record_exists": record.exists(),
        "issue_count": len(issues),
        "open_question_count": len(open_questions),
        "question_counts": dict(sorted(issue_counts.items())),
        "issues": issues,
        "open_questions": open_questions[:20],
        "active_work_count": len(active_work_rows),
        "active_work": active_work_rows,
        "follow_up_case_count": len(follow_up_rows),
        "follow_up_cases": follow_up_rows,
        "latest_iteration": iterations[0] if iterations else None,
        "iteration_direction": {
            "headings": iterations[:10],
            "current_direction": direction_text,
        },
        "git_diff": collect_git_diff(project_root, diff_ref),
        "conflict_signals": build_conflict_signals(active_work_rows),
    }


def build_conflict_signals(active_work_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: dict[str, list[str]] = {}
    for row in active_work_rows:
        session = row.get("Session") or row.get("会话") or "unknown"
        files = value(row, "files")
        for part in re.split(r"[,，]", files):
            key = part.strip()
            if not key:
                continue
            seen.setdefault(key, []).append(session)
    return [
        {
            "area": area,
            "sessions": ", ".join(sessions),
            "signal": "multiple active sessions mention this area",
        }
        for area, sessions in sorted(seen.items())
        if len(set(sessions)) > 1
    ]


def record_template(today: date | None = None) -> str:
    current_date = (today or date.today()).isoformat()
    return f"""# Vibe Lens Record

This file is the lightweight source record for Vibe Lens.
Vibe Lens turns this record plus Git diff data into a visual review sandbox.

## Guardrails

- Do not rename these headings: `## Issue Pool`, `## Active Work`, `## Follow-up Flow Notes`, `## Iteration Log`.
- Do not rename these legacy Issue Pool columns when they exist: `ID`, `Issue`, `Impact`, `Priority`, `Status`, `Next Step`.
- Do not rank issues or tell the operator what must be done first from this file alone.
- Treat `Priority` as legacy descriptive metadata only; the lens displays it but does not use it as a decision rule.
- You can freely edit row content, add new rows, and add extra sections.

## Current Product Direction

- Positioning: a review sandbox for messy vibe-coding projects.
- Main user: builders and beginner AI product managers who need to see questions, code changes, direction, and evidence in one place.
- Current focus: show information clearly; do not arrange work or impose weights.

## Issue Pool

| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | First review question | operator | open | Replace this starter row with a real question | docs/iteration-record.md |

## Active Work

| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| {current_date} | Bootstrap Vibe Lens record | docs/iteration-record.md | in progress | Replace this row after the first real work item is complete |

## Follow-up Flow Notes

| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Multiple AI chats work on the same project | Each chat may hold a different mental model | Parallel edits can conflict | Show active work and touched areas as neutral signals |

## Iteration Log

### {current_date}: Initialize Vibe Lens record
Goal:
- Create a local source record that can feed a visual review sandbox.

Discovered Issues:
- Manual setup is friction for first-time users.

Decisions:
- Use `docs/iteration-record.md` as the default input record.
- Keep Markdown as the source record, not the final viewing platform.

Completed:
- Initialized the Vibe Lens record.

Verification:
- Run the lens snapshot script and confirm it can read this file.

Unfinished:
- Replace the starter rows with project-specific questions and evidence.
"""


def init_record(project_root: Path, record_path: Path | None = None) -> Path:
    record = record_path or project_root / DEFAULT_RECORD
    record.parent.mkdir(parents=True, exist_ok=True)
    if not record.exists():
        record.write_text(record_template(), encoding="utf-8")
    return record


def template_path() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "report_template.html"


def write_html_report(snapshot: dict[str, Any], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    template = template_path().read_text(encoding="utf-8")
    payload = json.dumps(snapshot, ensure_ascii=False).replace("<", "\\u003c")
    html = template.replace("__LENS_DATA__", payload)
    output.write_text(html, encoding="utf-8")
    return output


def print_text(snapshot: dict[str, Any]) -> None:
    diff = snapshot["git_diff"]
    print(f"Record: {snapshot['record']}")
    print(
        f"Questions: {snapshot['issue_count']} total, "
        f"{snapshot['open_question_count']} open"
    )

    if snapshot["question_counts"]:
        print("Question counts by status:")
        for key, count in snapshot["question_counts"].items():
            print(f"  - {key}: {count}")

    if snapshot["open_questions"]:
        print("Open questions:")
        for issue in snapshot["open_questions"][:5]:
            issue_id = value(issue, "id", "-")
            title = value(issue, "issue", str(issue))
            status = value(issue, "status", "unknown")
            print(f"  - {issue_id} [{status}] {title}")
    else:
        print("Open questions: none")

    if diff["available"]:
        print(
            "Code diff: "
            f"+{diff['total_added']} -{diff['total_deleted']} "
            f"across {diff['changed_file_count']} tracked files"
        )
        if diff["untracked_files"]:
            print(f"Untracked files: {', '.join(diff['untracked_files'][:8])}")
    else:
        print("Code diff: git repository not available")

    latest = snapshot["latest_iteration"] or "none"
    print(f"Latest iteration: {latest}")
    print(f"Active work rows: {snapshot['active_work_count']}")
    print(f"Follow-up flow cases: {snapshot['follow_up_case_count']}")
    if snapshot["conflict_signals"]:
        print("Conflict signals:")
        for signal in snapshot["conflict_signals"]:
            print(f"  - {signal['area']}: {signal['sessions']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root")
    parser.add_argument("--record", "--record-path", dest="record", help="Explicit record path")
    parser.add_argument("--diff-ref", help="Git diff base or range, defaults to HEAD when available")
    parser.add_argument("--init", action="store_true", help="Create docs/iteration-record.md when it is missing")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    parser.add_argument("--html", action="store_true", help="Generate a static HTML Vibe Lens report")
    parser.add_argument("--output", help="HTML output path, defaults to docs/vibe-lens-report.html")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    record_path = Path(args.record).resolve() if args.record else None

    if args.init:
        record_path = init_record(project_root, record_path)

    try:
        snapshot = build_snapshot(project_root, record_path, args.diff_ref)
    except FileNotFoundError as exc:
        missing = resolve_record(project_root, record_path)
        raise SystemExit(
            f"Vibe Lens record not found: {missing}\n"
            "Run this command once to create it:\n"
            f"  python {Path(__file__).name} --project-root {project_root} --init"
        ) from exc

    if args.html:
        output = Path(args.output).resolve() if args.output else project_root / DEFAULT_REPORT
        write_html_report(snapshot, output)
        print(f"HTML report: {output}")
    elif args.json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    else:
        print_text(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
