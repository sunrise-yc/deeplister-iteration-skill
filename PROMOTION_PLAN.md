# vibe-lens-skill Promotion Plan

Goal: turn `vibe-lens-skill` from a personal workflow into a small open-source tool that other AI builders can understand, install, try, and critique.

## Core Positioning

One sentence:

> A Codex skill that turns messy vibe-coding projects into a visual review sandbox: current questions, historical questions, Git diff stats, iteration direction, evidence, and conflict signals.

Do not market it as a full project-management system. The useful promise is smaller and sharper:

- Not a Jira / Linear / Notion replacement.
- Not an automatic priority engine.
- A local source record plus visual HTML review surface.
- A way to review code changes and project direction after AI-assisted work.
- A way to make parallel AI-session overlap visible without scheduling the work.

## Audience

- Solo builders using Codex or similar AI coding agents.
- Beginners building their first larger AI product.
- People who like vibe coding but hit the messy middle: too many questions, fragmented context, hard-to-review code changes.
- Users who are not ready for a heavy PM tool but need a clearer review surface than chat memory.

## Key Message

中文：

```text
vibe coding 一开始很爽，但项目到中后期会乱：问题散在聊天、文档和代码里，多个 AI 对话还可能互相冲突。

vibe-lens 把项目记录和 Git diff 变成一个复盘沙盘：当前问题、历史问题、代码增删、迭代方向、证据链和冲突线索都能看见。

它展示局面，不替你排优先级。
```

English:

```text
Vibe coding is fast at the start, but the middle gets messy.

vibe-lens turns a project record plus Git diff into a visual review sandbox.

It shows the board. It does not rank the work.
```

## First Two-Week Plan

| Day | Action | Output |
|---|---|---|
| 1 | Finish rename and first-run UX | `vibe-lens`, `--init`, README |
| 2 | Refresh social preview and screenshots | New images with correct name |
| 3 | Record 60-second demo | Show `--init -> snapshot -> HTML report` |
| 4 | Publish GitHub repo update | README, issue templates, roadmap |
| 5 | Write Chinese story post | Why vibe coding needs a review sandbox |
| 6 | Write technical tutorial | How the skill reads Markdown and Git diff |
| 7 | Ask for install feedback | GitHub Issues and small communities |
| 8-14 | Fix first feedback | Release small updates |

## Platform Notes

### GitHub

Make the README answer four questions quickly:

1. What pain does it solve?
2. How do I install it?
3. How do I create the first source record without manual setup?
4. What does the HTML report show?

### X / Twitter

Lead with the problem:

```text
I built a tiny Codex skill for the messy middle of vibe coding.

It turns a project record + Git diff into a visual review sandbox:
current questions, historical questions, added/deleted code stats, direction, evidence, and conflict signals.

It shows the board. It does not rank the work.
```

### 中文平台

Good titles:

- 《vibe coding 到中后期为什么会乱？我做了一个复盘沙盘》
- 《不用 Jira，先把 AI 写代码后的问题和代码差异看清楚》
- 《AI 写代码越来越快，但项目复盘不能只靠聊天记录》

## 产品学习闭环

每次真实使用之后，记录这 5 个问题：

1. 当前问题和历史问题是否更容易看清？
2. Git diff 可视化是否帮助复盘代码变化？
3. HTML 报告是否比 Markdown 更容易读？
4. 冲突线索有没有帮助发现多对话重叠？
5. 哪些地方仍然让 Agent 误以为它应该排优先级？

先把这些发现写进 `docs/iteration-record.md`，等结论稳定后，再提炼到 README 或 ROADMAP。
