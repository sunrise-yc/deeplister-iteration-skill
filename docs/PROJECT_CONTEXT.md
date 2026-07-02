# vibe-lens-skill Project Context

Updated: 2026-07-02

This file is a maintainer handoff note. The active source record lives in `docs/iteration-record.md`.

## Maintainer

- User: 杨晨
- GitHub: https://github.com/sunrise-yc
- Preference: explain code in plain Chinese and include product-thinking context.
- 学习方向：AI 产品经理。

## Project

- Local repository: `C:\Users\23184\Desktop\deeplister-iteration-skill`
- Intended GitHub repository name: `vibe-lens-skill`
- Project type: Codex skill
- Skill name: `vibe-lens`
- Default source record: `docs/iteration-record.md`
- Legacy readable record: `docs/迭代记录.md`

## Product Positioning

`vibe-lens` is a visual review sandbox for the messy middle of vibe coding.

It helps Codex and the operator inspect:

- current questions;
- historical questions;
- Git diff statistics;
- iteration direction;
- evidence and verification trails;
- conflict signals across active AI coding sessions.

It does not rank work, assign weights, or decide what must happen next.

## Current Decisions

- Rename public direction from `vibe-iteration` to `vibe-lens`.
- Keep `docs/iteration-record.md` as the default source record for compatibility.
- Keep legacy `docs/迭代记录.md` support for older DeepLister users.
- Keep `--init`; manual record creation is not acceptable for a beginner-facing workflow.
- Add static HTML report generation as the first review surface.
- Treat `Priority` as legacy descriptive metadata only.
- Keep old installed skills around temporarily for compatibility; new use should prefer `vibe-lens`.

## Verification Commands

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile vibe-lens\scripts\lens_snapshot.py
python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python vibe-lens\scripts\lens_snapshot.py --project-root .
git diff --check
```

## Related Docs

- `README.md`: public product page.
- `ROADMAP.md`: product plan.
- `CHANGELOG.md`: release notes.
- `docs/iteration-record.md`: active source record.
- `docs/INSTALLATION_TROUBLESHOOTING.md`: first-run support.
- `docs/DEMO_SCRIPT.md`: demo outline.
- `docs/superpowers/specs/2026-07-02-vibe-lens-design.md`: approved design.
- `docs/superpowers/plans/2026-07-02-vibe-lens-implementation.md`: implementation plan.
