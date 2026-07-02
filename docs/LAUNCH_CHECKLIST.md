# Launch Checklist

Use this checklist before publishing `vibe-lens-skill`.

## Repository

- [ ] Rename GitHub repository to `vibe-lens-skill`.
- [ ] Update local remote URL after the GitHub rename.
- [ ] Set repository description:
  `A Codex skill that turns messy vibe-coding projects into a visual review sandbox.`
- [ ] Set topics:
  - `codex`
  - `codex-skill`
  - `ai-agent`
  - `vibe-coding`
  - `retrospective`
  - `review`
  - `git-diff`
  - `dashboard`
- [ ] Refresh social preview image so it says `vibe-lens`.

## First-Run UX

- [ ] Install folder is `vibe-lens/`.
- [ ] Prompt uses `$vibe-lens`.
- [ ] `--init` creates `docs/iteration-record.md`.
- [ ] Missing-record error tells users to run `--init`.
- [ ] README does not ask users to manually create the source record.
- [ ] README explains that Vibe Lens does not rank or arrange tasks.

## Verification

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile vibe-lens\scripts\lens_snapshot.py
python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python vibe-lens\scripts\lens_snapshot.py --project-root .
git diff --check
```

## Demo

- [ ] Show messy project context.
- [ ] Run `--init`.
- [ ] Open `docs/iteration-record.md`.
- [ ] Run lens snapshot script.
- [ ] Generate HTML report.
- [ ] Explain Git diff statistics.
- [ ] Show that facts and Agent judgment are separate.

## Release Notes

- [ ] Explain rename from `vibe-iteration` to `vibe-lens`.
- [ ] Mention legacy DeepLister and `docs/迭代记录.md` compatibility.
- [ ] Mention `--init`.
- [ ] Mention Git diff statistics.
- [ ] Mention static HTML review sandbox.
- [ ] Mention this repository dogfoods `docs/iteration-record.md`.
