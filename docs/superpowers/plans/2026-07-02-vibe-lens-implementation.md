# Vibe Lens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition and implement this project as `vibe-lens`: a Codex skill that generates a visual, evidence-based project sandbox without ranking or arranging tasks.

**Architecture:** Keep the skill small and deterministic. The Skill instructs Codex to initialize/read a Markdown-backed record, run a Python snapshot/report script, and render JSON/HTML for a local visual review. Markdown remains an input and backup, while the HTML report becomes the user-facing view.

**Tech Stack:** Python 3 standard library, Markdown tables, Git CLI, static HTML/CSS/JS, `unittest`.

---

## File Map

- Rename `vibe-iteration/` to `vibe-lens/`.
- Rename `vibe-iteration/scripts/iteration_snapshot.py` to `vibe-lens/scripts/lens_snapshot.py`.
- Create `vibe-lens/assets/report_template.html` for the static visual sandbox.
- Update `vibe-lens/SKILL.md` so it displays information and explicitly avoids priority decisions.
- Update `vibe-lens/references/iteration-record-format.md` into a lens record format reference.
- Update `vibe-lens/agents/openai.yaml` with user-facing `Vibe Lens` metadata.
- Update `tests/test_lens_snapshot.py` into lens snapshot tests.
- Update examples and public docs: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `PROMOTION_PLAN.md`, `docs/*.md`, `.github/ISSUE_TEMPLATE/*.yml`.
- Update `docs/iteration-record.md` to dogfood the new positioning.
- Copy the finished `vibe-lens/` folder to `C:\Users\23184\.codex\skills\vibe-lens`.

## Task 1: Write Lens Behavior Tests

**Files:**
- Modify: `tests/test_lens_snapshot.py`

- [ ] Add tests that import `vibe-lens/scripts/lens_snapshot.py`, falling back to `vibe-iteration` only for legacy compatibility during migration.
- [ ] Add a test that snapshot output keeps issue counts and top open questions but does not include `recommended_next`.
- [ ] Add a test that Git diff statistics are collected from a temporary Git repo using `--numstat`.
- [ ] Add a test that `--init` creates a beginner-safe record with guardrails saying the headings should not be renamed and the lens should not rank tasks.
- [ ] Add a test that static HTML report generation creates an HTML file containing the JSON payload and visual section labels.
- [ ] Run `python -m unittest tests.test_lens_snapshot` and confirm the new tests fail before implementation.

## Task 2: Rename and Reframe the Skill

**Files:**
- Move: `vibe-iteration/` -> `vibe-lens/`
- Move: `vibe-lens/scripts/iteration_snapshot.py` -> `vibe-lens/scripts/lens_snapshot.py`
- Modify: `vibe-lens/SKILL.md`
- Modify: `vibe-lens/agents/openai.yaml`

- [ ] Rename the folder and script.
- [ ] Rewrite frontmatter to `name: vibe-lens`.
- [ ] Make the description trigger on project review, retrospectives, code-diff visualization, issue history, and vibe-coding sandbox needs.
- [ ] Remove priority-selection and "recommended next task" instructions.
- [ ] Add explicit guardrails: display facts, do not rank, do not arrange tasks, separate future Agent suggestions from evidence.
- [ ] Update commands to use `vibe-lens/scripts/lens_snapshot.py`.

## Task 3: Implement Snapshot Data and Diff Stats

**Files:**
- Modify: `vibe-lens/scripts/lens_snapshot.py`

- [ ] Rename script terminology from iteration snapshot to lens snapshot.
- [ ] Keep legacy `docs/iteration-record.md` and `docs/迭代记录.md` parsing.
- [ ] Preserve Markdown table parsing for existing records.
- [ ] Replace `recommended_next` with neutral fields such as `open_questions`, `question_counts`, `latest_iteration`, and `conflict_signals`.
- [ ] Add Git diff collection using `git diff --numstat`, `git diff --name-status`, and `git status --short`.
- [ ] Add bounded JSON output suitable for HTML embedding.
- [ ] Add `--html` and `--output` arguments to generate a static report.
- [ ] Keep all code in Python standard library.

## Task 4: Add Static Report Template

**Files:**
- Create: `vibe-lens/assets/report_template.html`

- [ ] Build a static HTML report with sections for overview, current questions, historical questions, code diff stats, iteration direction, evidence chain, and conflict signals.
- [ ] Use embedded JSON from the script.
- [ ] Use simple CSS and JS only; no external dependencies.
- [ ] Avoid wording that implies priority decisions.

## Task 5: Update Record Format, Example, and Docs

**Files:**
- Modify: `vibe-lens/references/iteration-record-format.md`
- Rename or replace: `examples/vibe-iteration-record.example.md` -> `examples/vibe-lens-record.example.md`
- Modify: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `PROMOTION_PLAN.md`
- Modify: `docs/DEMO_SCRIPT.md`, `docs/INSTALLATION_TROUBLESHOOTING.md`, `docs/LAUNCH_CHECKLIST.md`, `docs/PROJECT_CONTEXT.md`, `docs/RELATED_WORK.md`, `docs/iteration-record.md`

- [ ] Update public positioning from iteration management to review sandbox.
- [ ] Remove "pick next highest-priority task" language.
- [ ] Explain that Git diff statistics come from Git and are accurate when the range is clear.
- [ ] Keep first-use setup automatic through `--init`.
- [ ] Document the HTML report command.
- [ ] Keep legacy DeepLister and `vibe-iteration` compatibility notes.

## Task 6: Update Tests, Local Install, and Verification

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Create/update: `C:\Users\23184\.codex\skills\vibe-lens`

- [ ] Run focused unit tests.
- [ ] Run Python compile check.
- [ ] Run the script against the example record.
- [ ] Generate an HTML report for the repository.
- [ ] Run the script against the repository's own record.
- [ ] Copy `vibe-lens/` to the local Codex skills directory.
- [ ] Run the installed skill script from `C:\Users\23184\.codex\skills\vibe-lens`.
- [ ] Run `git diff --check`.
