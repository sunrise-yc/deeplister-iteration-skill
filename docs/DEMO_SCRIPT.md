# 60 秒 Demo 脚本

更新时间：2026-07-01

这个 demo 面向第一次看到 `deeplister-iteration-skill` 的用户。目标不是炫技术，而是让用户 60 秒内看懂：

1. 它解决什么问题。
2. 第一次怎么跑通。
3. 为什么它不是 Jira / Notion，而是一个轻量迭代习惯工具。

## 推荐标题

中文：

```text
第一次做大项目，怎么让 Codex 帮你找到下一步任务？
```

英文：

```text
A tiny Codex skill that picks your next task from a Markdown iteration log
```

## 视频结构

| 时间 | 画面 | 旁白 |
| --- | --- | --- |
| 0-5 秒 | 展示一堆任务或打开 `docs/迭代记录.md` 的问题池 | 第一次做大项目时，任务很容易散在聊天、文档和代码里。最难的不是写代码，而是不知道下一步先做什么。 |
| 5-12 秒 | 放大 `## 问题池` 表格，展示 P0/P1 和状态 | 我把任务放进一个 Markdown 迭代记录里，用优先级和状态先管起来。 |
| 12-22 秒 | 运行 snapshot 命令 | 这个 Codex skill 会先读这个文档，用脚本提取当前快照。 |
| 22-32 秒 | 展示 `Recommended next task` 输出 | 它会推荐当前最该做的任务，比如优先处理 P0，而不是随便挑一个看起来顺手的任务。 |
| 32-45 秒 | 展示对 Codex 的 prompt | 然后我可以直接对 Codex 说：用 deeplister-iteration 看下一步该做什么。 |
| 45-55 秒 | 展示迭代记录新增一条记录 | 做完后，Codex 会把改了什么、怎么验证、下次建议写回迭代记录。 |
| 55-60 秒 | 展示 GitHub 仓库首页或 social preview | 它不是完整项目管理系统，只是帮早期个人项目养成一个好习惯：先看问题池，做完留记录。 |

## 屏幕操作步骤

### 1. 打开示例迭代记录

展示文件：

```text
examples/deeplister-iteration-record.example.md
```

重点展示：

```md
## 问题池

| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
|---|---|---|---|---|---|
| DL-001 | 追问判断过度依赖关键词和长度 | 可能误判有效短回答。 | P0 | 待处理 | 建立追问评估集。 |
| DL-002 | README 与当前代码结构不一致 | 新用户可能困惑。 | P1 | 待处理 | 同步 README。 |
```

产品讲法：

> 这里的重点不是表格多漂亮，而是把任务、影响、优先级、下一步放在同一个地方。

### 2. 运行快照脚本

在仓库根目录运行：

```powershell
$env:PYTHONIOENCODING='utf-8'; python deeplister-iteration\scripts\iteration_snapshot.py --project-root . --record examples\deeplister-iteration-record.example.md
```

期望看到：

```text
Issues: 2 total, 2 unresolved
Recommended next task:
  - DL-001 [P0] 追问判断过度依赖关键词和长度
    Next: 建立追问评估集。
Latest iteration: 2026-07-01：建立迭代台账
Follow-up flow cases: 1
```

产品讲法：

> 这一步相当于给 Codex 一张当前项目小地图。它不用重新翻聊天记录，就知道下一步应该先看哪个任务。

### 3. 展示给 Codex 的一句话

中文：

```text
用 deeplister-iteration 看一下下一步该做什么，并在做完后更新迭代记录。
```

英文：

```text
Use $deeplister-iteration to pick the next DeepLister task.
```

产品讲法：

> 普通 prompt 是每次都重新解释规则；skill 是把固定工作流沉淀下来，让 Codex 每次按同一套规则行动。

### 4. 展示迭代记录写回

展示一条新增记录的结构：

```md
### 2026-07-01：建立迭代台账

本次目标：

- 建立轻量迭代记录。

已完成：

- 创建 `docs/迭代记录.md`。

验证：

- 运行 `iteration_snapshot.py` 能读取问题池。

下次建议：

- 优先处理 `DL-001`。
```

产品讲法：

> 做完后留下记录，下一次继续时就不会从零开始。这对第一次做大项目的新手特别重要。

## 60 秒旁白完整版

```text
第一次做大项目时，任务很容易散在聊天、文档和代码里。
时间一久，最难的不是写代码，而是不知道下一步先做什么。

我做了一个很小的 Codex skill，叫 deeplister-iteration-skill。
它不替代 Jira，也不替代 Notion，只做一件事：
让 Codex 每次动手前先看 Markdown 问题池，选出当前最该做的任务。

这里有一个迭代记录，里面写了问题、影响、优先级、状态和下一步。
我运行 snapshot 脚本后，它会告诉我当前有几个未解决问题，以及推荐下一步任务。

比如这里，它优先推荐 P0 任务，而不是随便挑一个顺手的改。

接下来我只要对 Codex 说：
用 deeplister-iteration 看一下下一步该做什么，并在做完后更新迭代记录。

做完后，Codex 会把本次目标、完成内容、验证和下次建议写回文档。

它不是完整项目管理系统。
它只是帮早期个人项目养成一个好习惯：
每次迭代前知道下一步，做完后留下记录。
```

## 15 秒短版

适合 X / 小红书 / B 站开头剪辑：

```text
我做了一个很小的 Codex skill。
它会读你的 Markdown 迭代记录，从问题池里找出下一步任务。
适合第一次做大项目、任务太多太乱的新手。
不是 Jira，不是 Notion，只是一个轻量迭代习惯工具。
```

## 发布文案

中文：

```text
我做了一个很小的 Codex skill，给第一次做大项目、被任务压住的新手用。

它会读取本地 Markdown 迭代记录，从问题池里推荐下一步任务，并提醒 Codex 做完后更新记录。

不是 Jira/Notion，只是一个轻量迭代习惯工具。

GitHub: https://github.com/sunrise-yc/deeplister-iteration-skill
```

英文：

```text
I built a tiny Codex skill for beginner projects that feel buried under messy tasks.

It reads a local Markdown iteration log, recommends the next task, and reminds Codex to write back what changed.

Not a PM platform. Just a small workflow guardrail.

GitHub: https://github.com/sunrise-yc/deeplister-iteration-skill
```

## 拍摄注意事项

- 不要一次展示太多代码。用户先看懂流程，再看实现细节。
- 优先展示 `问题池 -> Recommended next task -> 迭代记录写回` 这条主线。
- 视频里不要承诺“自动完成所有项目管理”。它只是轻量辅助。
- 如果录 Windows 终端，建议先设置：

```powershell
$env:PYTHONIOENCODING='utf-8'
```

这样中文输出更稳定。
