# Installation Troubleshooting

Updated: 2026-07-02

This guide is for first-time users of `vibe-lens-skill`.

## 1. Correct Install Location

Copy the whole `vibe-lens/` folder into your Codex skills directory.

Windows:

```text
C:\Users\<your-user>\.codex\skills\vibe-lens
```

macOS / Linux:

```text
~/.codex/skills/vibe-lens
```

The final folder should directly contain:

```text
vibe-lens/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

If the path looks like this, there is one folder too many and Codex may not discover the skill:

```text
~/.codex/skills/vibe-lens-skill/vibe-lens/SKILL.md
```

## 2. Codex Does Not Discover The Skill

Check:

1. `SKILL.md` is directly inside `vibe-lens/`.
2. Codex was restarted, or a new Codex session was opened.
3. The prompt uses the correct skill name:

```text
Use $vibe-lens to inspect the project record, Git diff, current questions, historical questions, iteration direction, and evidence trail without ranking or arranging tasks.
```

## 3. No Source Record Exists

Do not create the file by hand. Run the initializer:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --init
```

This creates:

```text
docs/iteration-record.md
```

The generated file includes guardrails that explain which headings should not be renamed and why the lens should not rank work.

## 4. Snapshot Script Does Not Run

Make sure you are in the target project root, then run:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
```

To test this repository's example:

```powershell
$env:PYTHONIOENCODING='utf-8'; python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
```

Expected output should include:

```text
Questions: 3 total, 2 open
Code diff:
Latest iteration:
```

## 5. HTML Report Does Not Appear

Generate it explicitly:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

By default this writes:

```text
docs/vibe-lens-report.html
```

Open that file in a browser. The first version is static HTML, not a hosted web app.

## 6. Chinese Text Looks Broken In Windows Terminal

Sometimes the Windows terminal displays UTF-8 text with the wrong local encoding. First try:

```powershell
$env:PYTHONIOENCODING='utf-8'
```

Then run the snapshot command again.

If the Markdown file itself looks normal in your editor, this is usually a terminal display issue, not file corruption.

## 7. Git Diff Numbers Look Unexpected

Vibe Lens reads Git data. The numbers depend on the selected boundary.

Default behavior:

- If the repo has commits, compare the working tree against `HEAD`.
- Show untracked files separately.
- Show binary files without pretending line counts are available.

To use a different boundary, pass `--diff-ref`:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --diff-ref main
```

## 8. Legacy Records

The script still reads:

```text
docs/迭代记录.md
```

It also understands older columns such as:

```md
| ID | Issue | Impact | Priority | Status | Next Step |
| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
```

`Priority` is displayed only as legacy metadata. It is not used to rank tasks.

## 9. What To Include In A GitHub Issue

If you are still stuck, include:

- Operating system: Windows / macOS / Linux
- Codex surface: desktop app, CLI, IDE, or other
- Install path
- Command you ran
- Terminal error or screenshot
- A privacy-safe sample of `docs/iteration-record.md`

Use:

- `Installation problem` for setup issues.
- `Bug report` for script, parsing, or report-generation issues.
- `Feature request` for new capabilities.
- `User story / use case` for real workflow feedback.
