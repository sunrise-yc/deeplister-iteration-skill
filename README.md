# vibe-lens-skill

A Codex skill for turning messy vibe-coding projects into a visual review sandbox.

When an AI-assisted project reaches the middle stage, questions scatter across chats, docs, code diffs, and half-finished ideas. Several AI coding sessions can also touch the same files with different assumptions. `vibe-lens` gives Codex a neutral way to inspect the project record, Git diff, current questions, historical questions, iteration direction, and evidence trail.

中文大白话：这是一个给 vibe coding 项目用的“复盘沙盘”。它把问题、历史、代码改动、方向和验证证据展示出来，帮人和 Agent 看清局面。它不是项目经理，不替你排优先级，也不默认安排任务。

## Quick Start

1. Copy the `vibe-lens/` folder into your Codex skills directory.
2. Restart Codex or start a new session so the skill can be discovered.
3. Inside your project, initialize the source record:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --init
```

4. Generate a text snapshot:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
```

5. Generate the visual sandbox:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

6. Ask Codex:

```text
Use $vibe-lens to inspect the project record, Git diff, current questions, historical questions, iteration direction, and evidence trail without ranking or arranging tasks.
```

The default source record is:

```text
docs/iteration-record.md
```

Manual file setup is intentionally not required. If the file is missing, run `--init`.

## What It Shows

- Current questions raised by the operator or Agent.
- Historical questions from the source record.
- Git diff statistics: added/deleted lines, changed files, and untracked files.
- Iteration direction from recent log entries.
- Evidence and verification trails.
- Conflict signals from active sessions touching the same files or areas.

## What It Does Not Do

- It does not automatically rank tasks.
- It does not assign weights.
- It does not tell the operator what must happen next.
- It does not replace tests, code review, or product judgment.
- It does not replace Jira, Linear, Notion, or a full planning system.

If the user explicitly asks for advice, Codex can still make an Agent judgment. That advice should be labeled as judgment, separate from the Vibe Lens evidence.

## Why Git Diff Stats Are Accurate

Code-change statistics come from Git, not from AI guessing.

`vibe-lens` reads commands such as:

```powershell
git diff --numstat
git diff --name-status
git status --short
```

This is accurate for tracked text files when the range is clear. The main product question is not whether Codex can count lines; Git already does that. The important part is defining the boundary: current working tree, since `HEAD`, or a specific Git ref/range.

Binary files, generated files, untracked files, and rename detection are shown separately when possible.

## How It Works

`docs/iteration-record.md` is the lightweight source record. The HTML report is the review surface.

The record can contain:

- `## Issue Pool`: current and historical questions.
- `## Active Work`: sessions and touched files or areas.
- `## Follow-up Flow Notes`: patterns, evidence gaps, and workflow observations.
- `## Iteration Log`: direction changes, evidence, code changes, verification, and unfinished uncertainty.

The helper script can print text, JSON, or HTML:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --json
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

The script still reads legacy records at `docs/迭代记录.md`, and it keeps compatibility with older `vibe-iteration` style records.

## Installation

Copy this folder:

```text
vibe-lens/
```

to your Codex skills directory.

Windows:

```text
C:\Users\<your-user>\.codex\skills\vibe-lens
```

macOS / Linux:

```text
~/.codex/skills/vibe-lens
```

The final folder should contain:

```text
vibe-lens/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

If Codex cannot discover the skill or the script does not run, see [docs/INSTALLATION_TROUBLESHOOTING.md](docs/INSTALLATION_TROUBLESHOOTING.md).

## Project Structure

```text
vibe-lens-skill/
  vibe-lens/
    SKILL.md
    agents/openai.yaml
    assets/report_template.html
    references/lens-record-format.md
    scripts/lens_snapshot.py
  docs/
    iteration-record.md
  examples/
    vibe-lens-record.example.md
  tests/
    test_lens_snapshot.py
```

This repository dogfoods its own workflow through [docs/iteration-record.md](docs/iteration-record.md). That file is the current source record for the project.

## Related Tools And Lessons

- [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills): keep `SKILL.md` focused and move deterministic behavior into scripts.
- [KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills): useful reference for the pattern “Skill triggers script, script produces an HTML report.”
- [Vibe Kanban](https://github.com/BloopAI/vibe-kanban): parallel AI work needs visible active work.
- [Task Master](https://github.com/eyaltoledano/claude-task-master): first use should be initialized by command, not by hand-built files.
- [Archon](https://github.com/coleam00/Archon): verification evidence matters; otherwise records become diaries.

More comparison and Chinese learning notes are in [docs/RELATED_WORK.md](docs/RELATED_WORK.md).

## Current Limits

- Parses simple Markdown tables only.
- Generates a static HTML report; the interactive platform is a later stage.
- Does not sync to GitHub Issues, Notion, Jira, or Linear yet.
- Keeps legacy DeepLister and `vibe-iteration` compatibility, but the public direction is now `vibe-lens`.

## Verification

Run:

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile vibe-lens\scripts\lens_snapshot.py
python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python vibe-lens\scripts\lens_snapshot.py --project-root .
```

## License

MIT
