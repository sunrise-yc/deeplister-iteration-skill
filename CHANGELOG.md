# Changelog

All notable changes to this project will be documented here.

## Unreleased

### Added

- Added the `vibe-lens` skill direction: a neutral review sandbox for vibe-coding projects.
- Added `vibe-lens/scripts/lens_snapshot.py`.
- Added Git diff statistics from Git: added/deleted lines, changed tracked files, untracked files, and file status.
- Added JSON and static HTML report generation.
- Added `vibe-lens/assets/report_template.html`.
- Added tests for neutral question display, Git diff stats, initialization, legacy Chinese records, and HTML report generation.
- Added a design spec and implementation plan under `docs/superpowers/`.

### Changed

- Repositioned the project from `vibe-iteration` task selection to `vibe-lens` information display.
- Removed the default “recommended next task” behavior from the script output.
- Reframed `Priority` as legacy descriptive metadata, not a decision rule.
- Updated the public README, roadmap, skill metadata, and reference format around review-sandbox language.

### Notes

- `docs/iteration-record.md` remains the default source record for compatibility.
- The legacy Chinese path `docs/迭代记录.md` is still readable.
- The local repository folder may still be named `deeplister-iteration-skill` until the GitHub repository is renamed and the local checkout path is optionally moved.
- Old installed skills such as `deeplister-iteration` and `vibe-iteration` may remain for compatibility, but new use should prefer `vibe-lens`.

## 0.1.0 - 2026-07-01

### Added

- Created the first DeepLister-specific iteration Codex skill.
- Added a snapshot script that reads a local Markdown record and prints issue counts, recommended next task, latest iteration entry, and follow-up-flow case count.
- Added an example iteration record.
- Added README, roadmap, launch checklist, demo script, promotion plan, install troubleshooting, and GitHub Issue templates.

### Changed

- Renamed the first public direction from `deeplister-iteration` to `vibe-iteration`.
- Added `--init` to create `docs/iteration-record.md` automatically.
- Added default English iteration record support with `## Issue Pool`, `## Active Work`, `## Follow-up Flow Notes`, and `## Iteration Log`.
- Added legacy compatibility for older `docs/迭代记录.md` records.
