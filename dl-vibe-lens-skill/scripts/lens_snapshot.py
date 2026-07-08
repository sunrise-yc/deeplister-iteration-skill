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
DEFAULT_SETTINGS = Path("docs") / "vibe-lens-settings.json"
LEGACY_RECORDS = [Path("docs") / "迭代记录.md"]
DEFAULT_SETTINGS_DATA = {
    "reply_entry_mode": "always",
    "record_language": "auto",
}

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
    "verification": ["Verification", "Validation", "验证", "验证记录"],
    "explanation_status": ["Explanation Status", "Explanation", "解释状态", "解释"],
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


EMPTY_VALUES = {"", "-", "none", "None", "NONE", "n/a", "N/A", "无", "暂无", "未记录", "unknown"}
FULL_EXPLANATION_VALUES = {"explained", "full", "complete", "已解释", "完整解释"}
PARTIAL_EXPLANATION_VALUES = {"partial", "部分解释"}
WEAK_EXPLANATION_VALUES = {"insufficient", "missing", "解释不足", "缺解释", "未解释"}


def has_meaningful_text(raw: str) -> bool:
    return raw.strip() not in EMPTY_VALUES


def percent(complete: int, total: int) -> int:
    if total <= 0:
        return 0
    return round((complete / total) * 100)


def issue_signal_breakdown(issue: dict[str, str]) -> dict[str, Any]:
    source_present = has_meaningful_text(value(issue, "source"))
    evidence_present = has_meaningful_text(value(issue, "evidence")) or has_meaningful_text(value(issue, "impact"))
    files_present = has_meaningful_text(value(issue, "files"))
    verification_present = has_meaningful_text(value(issue, "verification"))

    evidence_checks = [
        ("来源", source_present),
        ("证据", evidence_present),
        ("关联文件", files_present),
    ]
    evidence_complete = sum(1 for _name, present in evidence_checks if present)
    evidence_missing = [name for name, present in evidence_checks if not present]

    verification_missing = [] if verification_present else ["验证"]

    explanation_raw = value(issue, "explanation_status").strip()
    explanation_normalized = explanation_raw.lower()
    if explanation_raw in FULL_EXPLANATION_VALUES or explanation_normalized in FULL_EXPLANATION_VALUES:
        explanation_label = "已解释"
        explanation_complete = 1
        explanation_missing: list[str] = []
    elif explanation_raw in PARTIAL_EXPLANATION_VALUES or explanation_normalized in PARTIAL_EXPLANATION_VALUES:
        explanation_label = "部分解释"
        explanation_complete = 0
        explanation_missing = ["完整解释"]
    elif explanation_raw in WEAK_EXPLANATION_VALUES or explanation_normalized in WEAK_EXPLANATION_VALUES:
        explanation_label = "解释不足"
        explanation_complete = 0
        explanation_missing = ["解释"]
    elif has_meaningful_text(explanation_raw):
        explanation_label = explanation_raw
        explanation_complete = 1
        explanation_missing = []
    else:
        explanation_label = "未记录"
        explanation_complete = 0
        explanation_missing = ["解释"]

    total_complete = evidence_complete + (1 if verification_present else 0) + explanation_complete
    total_possible = 5

    return {
        "evidence": {
            "complete": evidence_complete,
            "total": 3,
            "percent": percent(evidence_complete, 3),
            "missing": evidence_missing,
        },
        "verification": {
            "complete": 1 if verification_present else 0,
            "total": 1,
            "percent": 100 if verification_present else 0,
            "missing": verification_missing,
        },
        "explanation": {
            "complete": explanation_complete,
            "total": 1,
            "percent": 100 if explanation_complete else 0,
            "label": explanation_label,
            "missing": explanation_missing,
        },
        "overall_percent": percent(total_complete, total_possible),
    }


def enrich_issue(issue: dict[str, str]) -> dict[str, Any]:
    enriched: dict[str, Any] = dict(issue)
    enriched["__lens"] = issue_signal_breakdown(issue)
    return enriched


def build_cognition_summary(issues: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "issues_with_evidence": sum(1 for issue in issues if issue["__lens"]["evidence"]["percent"] > 0),
        "issues_with_verification": sum(1 for issue in issues if issue["__lens"]["verification"]["percent"] > 0),
        "issues_with_full_explanation": sum(1 for issue in issues if issue["__lens"]["explanation"]["label"] == "已解释"),
        "issues_with_gaps": sum(1 for issue in issues if issue["__lens"]["overall_percent"] < 100),
    }


def resolve_record(project_root: Path, record_path: Path | None = None) -> Path:
    if record_path:
        return record_path

    candidates = [project_root / DEFAULT_RECORD]
    candidates.extend(project_root / legacy for legacy in LEGACY_RECORDS)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return project_root / DEFAULT_RECORD


def ensure_settings(project_root: Path) -> Path:
    settings = project_root / DEFAULT_SETTINGS
    settings.parent.mkdir(parents=True, exist_ok=True)
    if not settings.exists():
        settings.write_text(
            json.dumps(DEFAULT_SETTINGS_DATA, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return settings


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

    raw_issues = parse_markdown_table(section_any(text, SECTION_ALIASES["issue_pool"]))
    issues = [enrich_issue(issue) for issue in raw_issues]
    open_questions = [issue for issue in issues if is_open_issue(issue)]
    issue_counts = Counter(value(issue, "status", "unknown") for issue in raw_issues)

    active_work_rows = parse_markdown_table(section_any(text, SECTION_ALIASES["active_work"]))
    follow_up_rows = parse_markdown_table(section_any(text, SECTION_ALIASES["follow_up"]))
    iterations = parse_iterations(section_any(text, SECTION_ALIASES["iteration_log"]))
    direction_text = section_any(text, SECTION_ALIASES["direction"])
    settings_path = project_root / DEFAULT_SETTINGS
    settings = DEFAULT_SETTINGS_DATA.copy()
    if settings_path.exists():
        settings.update(json.loads(settings_path.read_text(encoding="utf-8")))

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
        "settings": settings,
        "git_diff": collect_git_diff(project_root, diff_ref),
        "conflict_signals": build_conflict_signals(active_work_rows),
        "cognition_summary": build_cognition_summary(issues),
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


def record_template_zh(today: date | None = None) -> str:
    current_date = (today or date.today()).isoformat()
    return f"""# Vibe Lens 记录

这是 Vibe Lens 的数据源文件。
脚本会把这里的记录和 Git diff 数据合在一起，生成一个可视化复盘沙盘。

大白话：这里不是任务裁判，不替你排优先级；它负责把当前问题、历史问题、代码差异、证据和迭代路径展示出来。

## 保护说明

- 不要改名这些标题：`## 问题池`、`## 当前工作`、`## 追问流程专项记录`、`## 迭代记录`。
- 不要把 `## 问题池` 里的表格搬到别的地方。
- 不要只根据这个文件给问题排序，`优先级` 只能当旧字段展示。
- 你可以改表格内容、增加行、增加自己的说明段落。

## 当前产品方向

- 定位：给中后期开始变乱的 vibe-coding 项目做复盘沙盘。
- 使用者：独立开发者、代码新手、正在学习 AI 产品经理的人，以及使用 AI coding agent 的人。
- 当前重点：展示信息，不安排任务，不施加权重。

## 问题池

| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-001 | 第一个需要复盘的问题 | operator | open | 把这一行替换成真实问题 | docs/iteration-record.md |

## 当前工作

| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| {current_date} | 初始化 Vibe Lens 记录 | docs/iteration-record.md | in progress | 第一次真实工作完成后，可以替换这一行 |

## 追问流程专项记录

| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 多个 AI 对话同时改一个项目 | 每个对话可能持有不同上下文 | 并行修改容易冲突 | 把活跃工作和涉及区域作为中性线索展示 |

## 迭代记录

### {current_date}: 初始化 Vibe Lens 记录
目标：
- 创建能喂给可视化复盘沙盘的数据源文件。

发现的问题：
- 手动建文件对第一次使用的人来说太麻烦。

决策：
- 使用 `docs/iteration-record.md` 作为默认输入记录。
- Markdown 只作为数据源，最终展示面是 HTML 报告。

完成：
- 初始化 Vibe Lens 记录。

验证：
- 运行 lens snapshot 脚本，确认它能读这个文件。

未完成：
- 把示例行替换成当前项目真实的问题和证据。
"""


def record_template_en(today: date | None = None) -> str:
    current_date = (today or date.today()).isoformat()
    return f"""# Vibe Lens Record

This is the source record for Vibe Lens.
The script combines this record with Git diff data to generate a visual review sandbox.

Plain English: this file is not a task judge. It shows current questions, historical questions, code changes, evidence, and iteration path.

## Guardrails

- Do not rename these headings: `## Issue Pool`, `## Active Work`, `## Follow-up Flow Notes`, `## Iteration Log`.
- Do not move the table under `## Issue Pool` to another section.
- Do not rank issues or tell the operator what must be done first from this file alone.
- Treat `Priority` as legacy display metadata only.
- You can edit row content, add rows, and add extra sections.

## Current Product Direction

- Positioning: a review sandbox for messy middle-stage vibe-coding projects.
- Users: solo developers, coding beginners, AI product-manager learners, and AI coding agent users.
- Current focus: display information without scheduling tasks or assigning weights.

## Issue Pool

| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | First question to review | operator | open | Replace this row with a real question | docs/iteration-record.md |

## Active Work

| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| {current_date} | Initialize Vibe Lens record | docs/iteration-record.md | in progress | Replace this row after the first real work |

## Follow-up Flow Notes

| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Multiple AI chats edit one project | Each chat may hold different context | Parallel changes can conflict | Show active work and touched areas as neutral signals |

## Iteration Log

### {current_date}: Initialize Vibe Lens record
Goal:
- Create the source record for the visual review sandbox.

Discovered Issues:
- Manual file creation is too much friction for first-time users.

Decisions:
- Use `docs/iteration-record.md` as the default input record.
- Markdown is the source record; the HTML report is the display surface.

Completed:
- Initialized the Vibe Lens record.

Verification:
- Run the lens snapshot script and confirm it can read this file.

Unfinished:
- Replace example rows with real project questions and evidence.
"""


def record_template(today: date | None = None, record_language: str = "zh") -> str:
    if record_language == "en":
        return record_template_en(today)
    return record_template_zh(today)


def init_record(
    project_root: Path,
    record_path: Path | None = None,
    record_language: str = "zh",
) -> Path:
    record = record_path or project_root / DEFAULT_RECORD
    record.parent.mkdir(parents=True, exist_ok=True)
    if not record.exists():
        record.write_text(record_template(record_language=record_language), encoding="utf-8")
    ensure_settings(project_root)
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
    parser.add_argument(
        "--record-language",
        choices=["auto", "zh", "en"],
        default="auto",
        help="Language for --init record template; auto defaults to zh for CLI use",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    parser.add_argument("--html", action="store_true", help="Generate a static HTML Vibe Lens report")
    parser.add_argument("--output", help="HTML output path, defaults to docs/vibe-lens-report.html")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    record_path = Path(args.record).resolve() if args.record else None

    if args.init:
        language = "zh" if args.record_language == "auto" else args.record_language
        record_path = init_record(project_root, record_path, language)

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
