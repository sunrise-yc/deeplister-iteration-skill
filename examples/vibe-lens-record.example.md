# Vibe Lens Record

This is a small example for `vibe-lens`. It shows the Markdown source record that feeds the visual review sandbox.

## Guardrails

- Do not rename these headings: `## Issue Pool`, `## Active Work`, `## Follow-up Flow Notes`, `## Iteration Log`.
- Do not rank issues or tell the operator what must be done first from this file alone.
- Treat legacy `Priority` values as display metadata only.
- You can edit row content and add extra sections.

## Current Product Direction

The project is a vibe-coding prototype that has reached the messy middle stage: questions are scattered across chats, docs, and code changes. The current goal is to make the situation visible before any Agent or operator decides what to do next.

## Issue Pool

| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | Manual record setup is too much friction | operator | open | First-time users should not hand-build structured files | vibe-lens/scripts/lens_snapshot.py |
| VL-002 | Code changes need visual diff statistics | agent | open | Git can report added/deleted lines accurately when the range is clear | vibe-lens/assets/report_template.html |
| VL-003 | Old priority wording may oversteer agents | operator | resolved | Skill now says display facts and avoid ranking | vibe-lens/SKILL.md |

## Active Work

| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| 2026-07-02 | Build review sandbox | vibe-lens/, README.md, tests/ | in progress | Current session owns the rename and report flow |

## Follow-up Flow Notes

| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| A user has many questions across chats | Codex may focus on the latest chat only | Historical context gets lost | Show current and historical questions together |
| Two AI chats run at once | Each chat assumes it is the only worker | Conflicts become likely | Show active files or areas as conflict signals |
| A user wants to review progress | Markdown is hard to scan | Review takes too much mental effort | Generate an HTML report with charts and timelines |

## Iteration Log

### 2026-07-02: Reposition as Vibe Lens
Goal:
- Shift from task selection to neutral information display.

Questions Raised:
- What questions are current?
- What questions were raised in the past?
- Which code was added or deleted while solving them?
- How has the project direction changed?

Evidence:
- Git diff can provide line-level added/deleted statistics for tracked text files.
- The source record can keep questions, active work, and verification notes.

Code Changes:
- Rename the public skill direction to `vibe-lens`.
- Add a static HTML report.

Verification:
- Run `python -m unittest tests.test_lens_snapshot`.
- Run `python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md --html`.

Unfinished:
- Build the second-stage interactive platform later.
