# Roadmap

This roadmap keeps the project focused on one product promise:

> Show the state of a messy vibe-coding project as a visual review sandbox without ranking or arranging the work.

## Product Principles

- Show facts before judgment.
- Keep Agent advice separate from evidence.
- Use Git for code-change statistics instead of AI guessing.
- Keep first use automatic through `--init`.
- Keep Markdown as the source record and HTML as the review surface.

## Stage 1: Review Sandbox

Current focus:

- Rename the public project direction from `vibe-iteration` to `vibe-lens`.
- Generate `docs/iteration-record.md` automatically.
- Read current and historical questions from the source record.
- Collect Git diff statistics: added lines, deleted lines, changed files, and untracked files.
- Generate a static HTML report with:
  - project overview;
  - current questions;
  - historical questions;
  - code diff visualization;
  - iteration direction;
  - evidence and verification trail;
  - conflict signals.
- Keep legacy DeepLister and `vibe-iteration` records readable.

## Stage 1.5: Better Evidence

Next:

- Add clearer examples for evidence and verification fields.
- Improve conflict-signal display for multiple active AI sessions.
- Add optional diff range selection examples.
- Refresh screenshots and social preview to use the `vibe-lens` name.
- Collect first install and report-generation feedback through GitHub Issues.

## Stage 2: Interactive Platform

Later:

- Add a local interactive platform instead of only static HTML.
- Allow filtering by status, source, file area, and iteration.
- Let the operator arrange questions visually.
- Let Agent suggestions appear in a separate layer from facts.
- Detect possible conflicts from overlapping files, dependencies, and contradictory assumptions.
- Require evidence links for every Agent arrangement suggestion.

## Integrations To Consider

- GitHub Issues and PR data.
- Notion or Airtable exports.
- Data Analytics dashboard rendering for richer charts.
- Figma or static design artifacts for product-review presentations.

## Not Planned For Stage 1

- Automatic priority ranking.
- Automatic task scheduling.
- Team permissions, due dates, or assignments.
- Jira, Linear, or Notion replacement.
- Automatic code review or testing replacement.
