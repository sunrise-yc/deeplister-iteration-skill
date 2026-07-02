# Demo Script

This 60-second demo is for first-time viewers of `vibe-lens-skill`.

## Goal

Show one clear loop:

1. A vibe-coding project has too many scattered questions.
2. Run `--init` once to create `docs/iteration-record.md`.
3. Run the lens snapshot to read current questions, historical questions, active work, and Git diff.
4. Generate the HTML review sandbox.
5. Show that Vibe Lens displays evidence but does not rank tasks.

## Timeline

| Time | Visual | Narration |
|---|---|---|
| 0-8s | Show messy notes, chats, or a long issue list | Vibe coding is fast at the start, but the middle gets messy: questions scatter across chats, docs, and code changes. |
| 8-18s | Run `--init` | Users should not hand-build a special Markdown file. One command creates the source record. |
| 18-28s | Open `docs/iteration-record.md` | This is the source record: questions, active work, follow-up notes, and iteration log. |
| 28-40s | Run snapshot script | The script reads the record and Git diff. It shows what exists; it does not pick a winner. |
| 40-52s | Generate and open HTML report | The HTML report is the review sandbox: current questions, history, code diff, direction, evidence, and conflict signals. |
| 52-60s | Show guardrail text | Vibe Lens separates facts from Agent judgment. If you ask for advice, that advice is labeled separately. |

## Commands

Initialize:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --init
```

Snapshot:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
```

HTML report:

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

Example prompt:

```text
Use $vibe-lens to inspect the project record, Git diff, current questions, historical questions, iteration direction, and evidence trail without ranking or arranging tasks.
```

## Short Narration

```text
I built a Codex skill for the messy middle of vibe coding.

When a project grows, questions scatter across chats, docs, and code changes. If several AI sessions run at once, they can also touch the same files with different assumptions.

Vibe Lens creates a review sandbox. It shows current questions, historical questions, Git diff stats, direction changes, evidence, verification, and possible conflict signals.

It is not a PM system and it does not rank tasks. It helps the operator and Agent see the board clearly before making judgment calls.
```

## Social Copy

```text
I built vibe-lens, a Codex skill for the messy middle of vibe coding.

It turns a project record + Git diff into a visual review sandbox:
- current questions
- historical questions
- added/deleted code stats
- iteration direction
- evidence and verification trail
- conflict signals

It displays the board. It does not rank the work.
```
