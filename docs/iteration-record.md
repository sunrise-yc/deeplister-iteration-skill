# Vibe Lens Record

This file is the source record for the Vibe Lens review sandbox.
Codex reads it together with Git diff data to display questions, history, direction, evidence, and conflict signals.

中文大白话：这是项目复盘沙盘的原始记录本。它不是任务裁判，不替你排优先级；它把局面摆出来，让人和 Agent 自己判断。

## Guardrails

- Do not rename these headings: `## Issue Pool`, `## Active Work`, `## Follow-up Flow Notes`, `## Iteration Log`.
- Do not rename legacy Issue Pool columns when they exist: `ID`, `Issue`, `Impact`, `Priority`, `Status`, `Next Step`.
- Do not rank issues or tell the operator what must be done first from this file alone.
- Treat `Priority` as legacy descriptive metadata only.
- You can freely edit row content, add new rows, and add extra sections.
- If an AI coding session starts work, record touched files or areas under `## Active Work` before broad changes.

## Current Product Direction

- 定位：给中后期开始变乱的 vibe-coding 项目做复盘沙盘和信息展现。
- 主要用户：独立开发者、代码新手、正在学习 AI 产品经理的人，以及使用 Codex 或其他 AI coding agent 的人。
- 核心任务：展示当前问题、历史问题、代码差异、迭代方向、证据链和冲突线索。
- 当前重点：把项目从 `vibe-iteration` 的任务选择口径改成 `vibe-lens` 的中性 review sandbox，并生成 HTML 可视化报告。
- 明确不做：默认排序优先级、安排任务、替操作者做权重判断。

## Issue Pool

| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | Reposition project as a review sandbox | operator | resolved | User clarified the skill should display information, not decide priority | README.md, vibe-lens/SKILL.md |
| VL-002 | Show Git diff statistics visually | operator | resolved | Git can provide added/deleted lines through `git diff --numstat` | vibe-lens/scripts/lens_snapshot.py, vibe-lens/assets/report_template.html |
| VL-003 | Keep first use automatic | operator | resolved | Manual file creation is too much friction for beginners | vibe-lens/scripts/lens_snapshot.py |
| VL-004 | Sync public docs and examples to Vibe Lens | agent | resolved | Public docs, examples, issue templates, and images now use Vibe Lens positioning | README.md, docs/, examples/, assets/ |
| VL-005 | Rename GitHub repository, remote, and local checkout path | agent | open | Draft PR #2 exists, but the repository and checkout folder still carry the old `deeplister-iteration-skill` name | GitHub settings, local remote |
| VL-006 | Design second-stage interactive platform later | operator | open | Markdown is not enough for task arrangement and conflict advice | ROADMAP.md |

## Active Work

| Session | Task | Files Or Areas | Status | Notes |
|---|---|---|---|---|
| 2026-07-02 | Reposition as Vibe Lens review sandbox | vibe-lens/, README.md, docs/, examples/, tests/ | completed | GitHub remote rename remains an external follow-up |
| 2026-07-02 | Publish Vibe Lens branch and draft PR | GitHub branch, PR #2 | completed | Branch `codex/vibe-lens-review-sandbox` pushed; draft PR opened against `main` |

## Follow-up Flow Notes

| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Multiple AI chats work on the same project | Each chat may hold a different mental model | Parallel edits can conflict | Show active work and touched areas as neutral conflict signals |
| First-time user installs the skill | User must manually create the record file | Too much setup friction for a beginner-facing tool | Provide `--init` and make Codex suggest it when the file is missing |
| Project reaches middle stage | Issues are scattered across chats, docs, and code | Review becomes hard | Use Vibe Lens to show questions, code diff, direction, and evidence |
| Agent sees old `Priority` fields | Agent may treat them as commands | The skill may oversteer decisions | Treat priority as legacy metadata and separate facts from Agent judgment |

## Iteration Log

### 2026-07-02: Publish Vibe Lens draft PR
Goal:
- Continue the unfinished GitHub synchronization work after the local commit.
- Keep the publication evidence in the Vibe Lens source record.

Evidence:
- Local branch `codex/vibe-lens-review-sandbox` tracks `origin/codex/vibe-lens-review-sandbox`.
- Draft PR #2 was opened at `https://github.com/sunrise-yc/deeplister-iteration-skill/pull/2`.
- The repository still uses the old public name `deeplister-iteration-skill`.

Verification:
- `git push -u origin codex/vibe-lens-review-sandbox` succeeded.
- GitHub connector returned draft PR #2 with head SHA `543936096e443021578dc34b1cf8eda6c8f49f51`.

Unfinished:
- Rename the GitHub repository to `vibe-lens-skill`.
- Update the local checkout folder and remote URL after the repository is renamed.

### 2026-07-02: Reposition as Vibe Lens review sandbox
Goal:
- Shift the project from task selection to neutral information display.
- Rename the public direction to `vibe-lens`.
- Add Git diff statistics and HTML report generation.

Questions Raised:
- What questions are current, and who raised them?
- What questions were raised in the past?
- Which code was added or deleted while solving them?
- How has the project direction changed?
- What evidence and verification support the changes?

Evidence:
- User explicitly said the skill should be information display, a review surface, or a sandbox, not a priority judge.
- `git diff --numstat` can provide accurate added/deleted line counts when the diff boundary is clear.
- `KKKKhazix/khazix-skills` shows a useful pattern: Skill triggers scripts, scripts generate an HTML report or local service.

Code Changes:
- Renamed the skill folder to `vibe-lens`.
- Replaced `iteration_snapshot.py` with `lens_snapshot.py`.
- Added static HTML report generation.
- Updated tests for neutral question display, Git diff stats, initialization, legacy Chinese records, and HTML report generation.
- Updated product docs toward review-sandbox positioning.

Verification:
- `python -m unittest tests.test_lens_snapshot` passed after adding the new behavior tests.
- `python -m py_compile vibe-lens\scripts\lens_snapshot.py` passed.
- `python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md` read the example record.
- `python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` generated the static HTML report.
- `python vibe-lens\scripts\lens_snapshot.py --project-root .` read this repository's source record.
- `python C:\Users\23184\.codex\skills\vibe-lens\scripts\lens_snapshot.py --project-root .` verified the installed local skill.
- `python C:\Users\23184\.codex\skills\vibe-lens\scripts\lens_snapshot.py --project-root C:\Users\23184\Desktop\DeepLister` verified the DeepLister source record.
- `git diff --check` exited 0 with only LF-to-CRLF warnings.

Unfinished:
- Rename the GitHub repository and local remote when account tooling is available.
- Build the second-stage interactive platform later.

Legacy note:
- Entries below this point describe earlier `deeplister-iteration` and `vibe-iteration` directions. They are preserved as history, not as current product behavior.

### 2026-07-01: 将学习点改成中文
目标：
- 让相关工具的学习点更方便杨晨阅读、复盘，并能用于 AI 产品经理思维训练。

完成：
- 将 README 里的相关工具学习点改成中文。
- 将 `docs/RELATED_WORK.md` 改成中文，包含定位、来源、学习点、不足，以及为什么不能手动建文件。
- 将 `PROMOTION_PLAN.md` 里的产品学习闭环改成中文。
- 在这份迭代记录里补充中文大白话说明。

验证：
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root .` still reads this record successfully.
- `python -m unittest tests.test_iteration_snapshot` passed.

下一步建议：
- 在另一个 AI 对话开始大范围改动前，继续让 VI-004 保持可见。

### 2026-07-01: Rename to vibe-iteration and add initialization
Goal:
- Reposition the skill from a DeepLister-specific iteration helper to a lightweight workflow for messy vibe-coding projects.
- Make first use work without manually creating a record file.
- Make this repository use its own iteration record.

Discovered Issues:
- The old public name made the project look too narrow.
- Manual Markdown setup was too fragile for the target beginner user.
- The social preview and snapshot image still carried old product language.
- The GitHub CLI is not installed locally, so the remote repository could not be renamed from this environment.

Decisions:
- Use `vibe-iteration` as the skill name and `vibe-iteration-skill` as the intended repository name.
- Use `docs/iteration-record.md` as the new default file.
- Keep legacy `docs/迭代记录.md` support for older DeepLister records.
- Add `## Active Work` to make parallel AI coding sessions more visible.

Completed:
- Renamed the skill folder and metadata to `vibe-iteration`.
- Added `--init` to generate `docs/iteration-record.md`.
- Added tests for English default records, legacy Chinese records, and initialization.
- Created this repository's own `docs/iteration-record.md`.
- Updated README, roadmap, changelog, launch checklist, demo script, promotion plan, troubleshooting guide, project context, issue templates, example record, and image assets.
- Installed the new skill locally at `C:\Users\23184\.codex\skills\vibe-iteration`.
- Added `docs/RELATED_WORK.md` with lessons and gaps from adjacent tools.
- Added `C:\Users\23184\Desktop\DeepLister\docs\iteration-record.md` by copying the existing DeepLister record so the new default path reads real project tasks.

Verification:
- `python -m unittest tests.test_iteration_snapshot` passed.
- `python -m py_compile vibe-iteration\scripts\iteration_snapshot.py` passed.
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root . --record examples\vibe-iteration-record.example.md` read 2 issues and recommended `VI-001`.
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root .` read this repo's record and recommended `VI-001` before this log update.
- `python ...\vibe-iteration\scripts\iteration_snapshot.py --project-root .` in `C:\Users\23184\Desktop\DeepLister` read 9 issues from `docs/iteration-record.md` and recommended `DL-001`.
- `git diff --check` reported only Windows LF-to-CRLF warnings, no whitespace errors.

Unfinished:
- The remote GitHub repository still points to `sunrise-yc/deeplister-iteration-skill` because `gh` is not installed locally and the available GitHub connector does not expose a rename tool.
- The local checkout folder is still `deeplister-iteration-skill`; this is acceptable until the remote repository is renamed.
- The old installed `deeplister-iteration` skill remains for compatibility.

Next Recommendation:
- Rename the GitHub repository to `vibe-iteration-skill` in GitHub settings, then update the local remote URL.

### 2026-07-01: Initialize vibe iteration record
Goal:
- Create a shared project memory for task selection, priority, active work, and review.

Discovered Issues:
- Manual setup is friction for first-time users.

Decisions:
- Use `docs/iteration-record.md` as the default record path.
- Keep this file lightweight and Markdown-first.

Completed:
- Initialized the iteration record.

Verification:
- Run the snapshot script and confirm it can read this file.

Unfinished:
- Replace the starter issue pool with project-specific tasks.

Next Recommendation:
- Add the highest-priority real issue as `P0`.
