---
name: deeplister-iteration
description: Use when working on DeepLister project iterations, selecting the next DeepLister task, updating the local iteration record, recording completed work, blockers, decisions, follow-up-flow findings, or summarizing DeepLister roadmap priorities.
---

# DeepLister Iteration

## Overview

Keep DeepLister iteration work grounded in the local iteration record. The record file lives under `docs/`; exact Chinese filename and section names are documented in `references/iteration-record-format.md`. This skill only defines how to read, choose, and update the record without loading unnecessary project history.

## Quick Start

1. Confirm the current repository is DeepLister. Look for `app.py`, `core/`, and the iteration record under `docs/`.
2. Run the snapshot helper when available:

```powershell
python "$env:USERPROFILE\.codex\skills\deeplister-iteration\scripts\iteration_snapshot.py" --project-root .
```

3. If the helper is not available or cannot parse the file, use `references/iteration-record-format.md` to find the expected filename and sections. Read only priority, issue-pool, latest-iteration, and follow-up-flow sections first.
4. Pick one task, state the intended change in plain language, then implement and verify it.
5. Before finishing, update the local iteration record with what changed, what was verified, what remains, and the recommended next task.

## Task Selection Rules

Prefer the highest-priority unresolved item in the issue pool:

| Priority | Meaning | Default action |
|---|---|---|
| `P0` | Blocks product trust, privacy, or core follow-up quality | Do first unless the user explicitly chooses another task |
| `P1` | Needed for maintainability, production readiness, or clear onboarding | Do after current P0 risk is controlled |
| `P2` | Useful polish or advanced analysis | Do after the base product loop is reliable |

Within the same priority, prefer the task that reduces uncertainty for later work. For example, a follow-up evaluation set usually comes before rewriting follow-up logic.

Do not silently skip a `P0` item. If choosing a lower-priority task, say why.

## Iteration Update Rules

After any meaningful DeepLister change:

- Add a new dated entry under the iteration log section.
- Record the goal, discovered issues, decisions, completed work, unfinished work, verification, and next recommendation.
- Update issue-pool status when an issue moves from not started to in progress, done, or blocked.
- Add new issues to the issue pool when the work reveals them.
- Update the follow-up-flow section when the work changes follow-up-question behavior or evaluation criteria.

Use `references/iteration-record-format.md` if the document is missing, malformed, or needs a new section.

## Verification

Before claiming the iteration is complete:

1. Run the smallest relevant test or command for the change.
2. Run the snapshot helper again to confirm the record is still readable.
3. Mention any verification that could not be run.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reading the whole repository before choosing a task | Start from the snapshot and only open files needed for the chosen task |
| Updating code but not the iteration record | Treat the record update as part of the task, not extra admin |
| Adding a large roadmap inside this skill | Keep history in the local iteration record; keep this skill small |
| Picking UI polish while P0 privacy or follow-up quality is unresolved | Explain the tradeoff or return to the P0 item |
