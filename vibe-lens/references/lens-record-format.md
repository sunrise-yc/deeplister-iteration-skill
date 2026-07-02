# Vibe Lens Record Format

Use this reference when `docs/iteration-record.md` is missing, malformed, or needs a new section. Run the helper with `--init` instead of creating the file by hand.

## Default Path

```text
docs/iteration-record.md
```

The snapshot script also reads the legacy path `docs/迭代记录.md` for older DeepLister and `vibe-iteration` projects.

## Required Sections

The first four data headings should not be renamed because the script reads them.

```md
# Vibe Lens Record

## Guardrails
## Current Product Direction
## Issue Pool
## Active Work
## Follow-up Flow Notes
## Iteration Log
```

Legacy Chinese headings are still supported:

```md
## 问题池
## 追问流程专项记录
## 迭代记录
```

## Issue Pool

Use one Markdown table under `## Issue Pool`.

Preferred lens columns:

```md
| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | Short question title | operator | open | Why this question exists | src/app.py |
```

Supported legacy columns:

```md
| ID | Issue | Impact | Priority | Status | Next Step |
| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
```

`Priority` is retained only as legacy descriptive metadata. Vibe Lens displays it when present but must not use it to rank work.

Recommended status values:

| Status | Meaning |
|---|---|
| `open` | Question is still visible |
| `discussing` | Question is being clarified |
| `in progress` | Work connected to the question has started |
| `blocked` | Cannot proceed without user input or external change |
| `resolved` | Answered or handled and verified |
| `done` | Legacy done status |

Legacy values such as `待处理`, `进行中`, `阻塞`, `已解决`, and `完成` are fine.

## Active Work

Use `## Active Work` to show possible overlap between parallel AI coding sessions.

```md
| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| 2026-07-02 | Build lens report | vibe-lens/, README.md | in progress | Current chat owns this change |
```

This section creates conflict signals only. It does not tell the operator which task must happen first.

## Iteration Entry

Append new entries under `## Iteration Log` with the newest entry near the top.

```md
### YYYY-MM-DD: Iteration title
Goal:
- 

Questions Raised:
- 

Evidence:
- 

Code Changes:
- 

Verification:
- 

Unfinished:
- 
```

Avoid unlabeled recommendation language. If a recommendation is necessary, label it as an operator decision or Agent judgment, not as a Vibe Lens fact.

## Follow-Up Flow Notes

Use `## Follow-up Flow Notes` for behavior examples, question patterns, evidence gaps, and conflict signals.

```md
| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Two AI chats edit one project | Each chat has different context | Changes can conflict | Show active files or areas before broad edits |
```

## When To Add A Visual Report

Generate HTML when:

- The issue pool is hard to scan.
- Code changes need visual diff statistics.
- Several iterations changed direction.
- The user asks for a review, sandbox, dashboard, or visual overview.
- Multiple AI sessions may be working in parallel.
