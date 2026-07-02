---
name: vibe-lens
description: Use when a vibe-coding project needs a review sandbox, retrospective, issue history view, Git diff visualization, iteration direction map, evidence trail, verification trail, or neutral conflict signals across AI coding sessions.
---

# Vibe Lens

## Overview

Turn a messy vibe-coding project into a neutral review sandbox. Vibe Lens displays questions, history, code changes, direction, evidence, verification, and conflict signals. It does not rank tasks, assign weights, or decide what the operator must do next.

The default source record is `docs/iteration-record.md`; the legacy Chinese path `docs/迭代记录.md` is still readable. Use `references/lens-record-format.md` if the record is missing, malformed, or needs a new section.

## Quick Start

1. Confirm you are in the project root.
2. Run the snapshot helper:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
```

3. If the record is missing, initialize it:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --init
```

4. Generate the visual sandbox when the user needs a reviewable view:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

## Guardrails

- Display evidence; do not impose priority.
- Treat `Priority` as legacy descriptive metadata only.
- Do not choose the next task unless the user explicitly asks for an agent judgment.
- If asked for a recommendation, separate facts from judgment: first summarize the lens evidence, then label any advice as the agent's interpretation.
- Show possible conflicts as signals, not as scheduling commands.
- Keep Markdown as the source record and HTML as the review surface.

## What To Show

Use the snapshot and optional HTML report to surface:

- Current questions raised by the operator or Agent.
- Historical questions and iteration headings.
- Git diff statistics: added/deleted lines, changed files, untracked files.
- Iteration direction from recent log entries and product-direction notes.
- Evidence and verification trails from record rows, follow-up notes, and Git state.
- Conflict signals from active sessions touching the same files or areas.

## Record Update Rules

After meaningful work, update the record as evidence for the next review:

- Add or update rows in `## Issue Pool` for current and historical questions.
- Update `## Active Work` when another session needs to see touched files or areas.
- Add a dated entry under `## Iteration Log`.
- Record evidence, verification, unfinished uncertainty, and changed files.
- Keep any recommendation language out of the record unless it is clearly labeled as an operator or Agent opinion.

## Verification

Before claiming the lens view is ready:

1. Run the smallest relevant test or command for the change.
2. Run the snapshot helper again to confirm the record is readable.
3. Generate the HTML report when visual review is part of the task.
4. Mention any verification that could not be run.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Starting from chat memory only | Run the snapshot first |
| Treating `Priority` as an instruction | Treat it as legacy metadata |
| Saying what must be done next | Show facts; label any advice as agent judgment |
| Updating code but not evidence | Update the record with changed files and verification |
| Manually creating the record from scratch | Use `--init` |
| Keeping everything in Markdown | Generate the HTML report for visual review |
