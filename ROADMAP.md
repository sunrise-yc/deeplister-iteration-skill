# Roadmap

This roadmap keeps the project focused on one product promise:

> Help beginner builders keep early project iterations organized in Markdown, so Codex can pick the next task and record what changed.

## Priority Rules

| Priority | Meaning | Example |
| --- | --- | --- |
| P0 | Blocks first successful use | Install path is unclear, Codex cannot discover the skill, snapshot script fails on the example record |
| P1 | Makes regular use smoother | README explains prompts better, snapshot output is easier to read, fewer manual edits are needed |
| P2 | Improves trust or promotion | Demo GIF, social preview, screenshots, more examples |
| P3 | Long-term expansion | Notion sync, GitHub Issues sync, Claude Code variant, full generic rename |

## Now

- Make the GitHub repository easier to understand in the first 30 seconds.
- Add Issue templates so real users can report install problems, bugs, feature ideas, and use cases.
- Add a clear first-run path for copying or creating `docs/迭代记录.md`.
- Upload `assets/social-preview.png` as the GitHub social preview image.
- Record one short demo GIF or video from `docs/DEMO_SCRIPT.md`.

## Next

- Add `--record-path` as a friendlier alias for the existing `--record` option.
- Add an install troubleshooting section for Windows, macOS, and Linux.
- Add a short demo script that shows: issue pool -> recommended next task -> iteration log update.
- Add a guide for adapting the skill to a different project name.

## Later

- Consider a more generic `local-iteration-tracker` version.
- Support richer issue statuses such as `进行中`, `阻塞`, and `已验证` in docs and examples.
- Produce stable JSON output for other automation workflows.
- Explore optional GitHub Issues or Notion integration after the local Markdown workflow is proven.

## Not Planned Yet

- A full Jira, Linear, or Notion replacement.
- Team permissions, due dates, assignments, or burndown charts.
- Automatic code review or testing replacement.
