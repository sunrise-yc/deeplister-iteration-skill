---
name: dl-vibe-lens-skill
description: Use when a vibe-coding project needs a review sandbox, retrospective, issue history view, Git diff visualization, iteration direction map, evidence trail, verification trail, or neutral conflict signals across AI coding sessions.
---

# DL Vibe Lens Skill

## Overview

Turn a messy vibe-coding project into a neutral review sandbox. `DL` points back to DeepLister, where this workflow started. `Vibe Lens` means a lens over vibe coding: it focuses scattered questions, Git diff statistics, iteration path, evidence, verification, and conflict signals so the operator and Agent can see the situation clearly. It does not rank tasks, assign weights, or decide what the operator must do next.

The default source record is `docs/iteration-record.md`; the default project settings file is `docs/vibe-lens-settings.json`; the legacy Chinese path `docs/迭代记录.md` is still readable. Use `references/lens-record-format.md` only when the record format needs explanation.

## Quick Start

1. Confirm you are in the project root.
2. If the record is missing, initialize it instead of asking the user to hand-build a file:

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --init
```

3. Read the current state:

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root .
```

4. Generate the visual sandbox:

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --html
```

5. Tell the user where the HTML was written, usually `docs/vibe-lens-report.html`.
6. Before the final reply, read `docs/vibe-lens-settings.json` when it exists. If `reply_entry_mode` is `"always"`, append a compact Vibe Lens entry. If it is `"when_used"`, append the entry only when this turn used Vibe Lens. If it is `"off"`, do not append it.

## Guardrails

- Display evidence; do not impose priority.
- Treat `Priority` as legacy descriptive metadata only.
- Do not choose the next task unless the user explicitly asks for an agent judgment.
- If asked for a recommendation, separate facts from judgment: first summarize the lens evidence, then label any advice as the agent's interpretation.
- Show possible conflicts as signals, not as scheduling commands.
- Keep Markdown as the source record and HTML as the review surface.
- Do not ask first-time users to manually create the record file; run `--init`.

## What To Show

Use the snapshot and optional HTML report to surface:

- Current questions raised by the operator or Agent.
- Historical questions and iteration headings.
- Git diff statistics: added/deleted lines, changed files, untracked files.
- Iteration path from recent log entries and product-direction notes.
- Evidence and verification trails from record rows, follow-up notes, and Git state.
- Conflict signals from active sessions touching the same files or areas.

## HTML Report Behavior

The generated report should be the primary review surface when the user asks to see the state visually.

- Default to Chinese UI, with an English toggle in the report.
- Keep the homepage compact: overview metrics, current questions, code diff, sandbox replay, evidence/conflict signals, and iteration path.
- Let overview, sandbox replay, and iteration path jump to detail pages.
- Use hover tooltips for titles, rings, progress bars, path nodes, and settings.
- Show Git diff as a ring and file rows. Git is the evidence source; do not invent line counts.
- Show the homepage path as broad stages. The vertical lines are stage marks, not exact dates.
- Include the conversation-entry setting panel. In a project that has enabled DL Vibe Lens, the default mode appends a compact `Open Vibe Lens` entry at the end of every Agent reply. If the operator says "do not show the Vibe Lens entry this turn", do not append it for that turn. If the operator disables it persistently, respect the project setting.
- The compact entry should be a Markdown link such as `[⌕ Vibe Lens](...)` or `[Vibe Lens](...)`, not a raw long URL.
- The static HTML setting panel is a display aid. Persistent reply behavior must come from the user prompt or `docs/vibe-lens-settings.json`.

## Record Update Rules

After meaningful work, update the record as evidence for the next review:

- Add or update rows in `## Issue Pool` for current and historical questions.
- Update `## Active Work` when another session needs to see touched files or areas.
- Add a dated entry under `## Iteration Log`.
- New records and new rows should follow the current conversation language unless the operator explicitly asks for another language.
- Existing English rows should not be silently machine-translated in the HTML report; translate and write back only when the operator asks.
- Record evidence, verification, unfinished uncertainty, and changed files.
- Keep any recommendation language out of the record unless it is clearly labeled as an operator or Agent opinion.
- Keep unresolved design/product ideas in the record or roadmap as future optimization, not as hidden behavior.

## Verification

Before claiming the lens view is ready:

1. Run the smallest relevant test or command for the change.
2. Run the snapshot helper again to confirm the record is readable.
3. Generate the HTML report when visual review is part of the task.
4. If HTML behavior changed, open the report and verify the expected screens, jumps, language toggle, and settings panel.
5. Mention any verification that could not be run.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Starting from chat memory only | Run the snapshot first |
| Treating `Priority` as an instruction | Treat it as legacy metadata |
| Saying what must be done next | Show facts; label any advice as agent judgment |
| Updating code but not evidence | Update the record with changed files and verification |
| Manually creating the record from scratch | Use `--init` |
| Keeping everything in Markdown | Generate the HTML report for visual review |
| Showing a long raw report URL in replies | Use a compact Markdown entry such as `Open Vibe Lens` |
