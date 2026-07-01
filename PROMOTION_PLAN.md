# deeplister-iteration-skill 推广与迭代方案

> 目标：让这个 skill 从“我自己能用的小工具”，逐步变成“别人也能看懂、装上、跑通、反馈问题、愿意给 Star 的开源小项目”。

## 1. 核心定位

一句话：

> 一个给 Codex 使用的轻量迭代管理 skill，适合第一次做大项目、任务又多又杂又乱的新手，用 Markdown 记录问题池、下一步任务和每次迭代结果。

不要把它宣传成完整项目管理系统。更准确的说法是：

- 不是 Jira / Linear / Notion 的替代品。
- 是给早期个人项目用的“迭代习惯插件”。
- 让 Codex 每次动手前先看问题池，做完后自动记录。
- 先解决“下一步做什么”和“做完后别忘记录”这两个小但高频的问题。

## 2. 日常使用中如何迭代更新

日常迭代不要靠灵感，靠固定动作。

### 每次真实使用后记录 4 件事

每次你用这个 skill 做 DeepLister 或其他项目时，结束前记录：

1. 这次它帮我省了什么？
2. 它哪里没帮上忙？
3. 它有没有误判下一步任务？
4. 新手照着 README 能不能复现这次流程？

建议把这些记录放在仓库 Issue 或本地 `CHANGELOG` / `ROADMAP` 中。早期不用复杂工具，GitHub Issues 足够。

### 每周做一次小版本复盘

每周固定看一次：

- README 是否还有读不懂的地方。
- 安装步骤是否缺图、缺命令、缺注意事项。
- `iteration_snapshot.py` 是否经常因为格式变化解析失败。
- skill 是否太绑定 DeepLister，别人迁移到自己项目时是否困难。
- 有没有用户反馈集中在同一个问题。

复盘后发一个小版本，比如：

- `v0.1.1`：修 README 安装说明。
- `v0.1.2`：增加中文示例。
- `v0.2.0`：支持自定义迭代记录路径。

### 日常更新优先级

优先改“会挡住第一次成功使用”的问题。

| 优先级 | 问题类型 | 例子 |
| --- | --- | --- |
| P0 | 装不上、跑不通、看不懂 | Windows 路径不清楚、编码报错、README 缺关键步骤 |
| P1 | 用得不顺 | 输出太啰嗦、推荐下一步任务不准、需要手动改太多地方 |
| P2 | 增强体验 | social preview 图、demo 动图、更多模板 |
| P3 | 长期扩展 | Notion/GitHub Issues 同步、Claude Code 版本、通用化重命名 |

## 3. 如何发现这款 skill 的不足

把不足分成 5 类看，不然容易只盯 Star 数。

### 1. 发现门面问题

观察指标：

- GitHub 访问量有，但 Star 很少。
- README 浏览后没人安装。
- 外部平台帖子有阅读，但没人点仓库。

可能原因：

- 标题不够清楚。
- 第一屏没有讲明白“我为什么需要它”。
- 没有截图、动图或真实使用例子。
- README 里安装路径对新手不友好。

### 2. 发现安装问题

观察指标：

- Issue 里反复有人问“放在哪里？”“为什么 Codex 没发现？”
- 不同系统路径说明不够清楚。
- Windows / macOS / Linux 表现不一致。

改进动作：

- 增加 `Installation troubleshooting`。
- 增加 Windows、macOS、Linux 三段独立说明。
- 做一个 60 秒安装动图。

### 3. 发现使用问题

观察指标：

- 用户装上了，但不知道第一句话该怎么对 Codex 说。
- 用户不知道怎么准备自己的 `docs/迭代记录.md`。
- 用户不知道跑脚本后应该看哪一行。

改进动作：

- 增加“从 0 到第一次成功使用”的教程。
- 提供最小模板。
- 提供 3 个常见 prompt：
  - “帮我看下一步任务。”
  - “做完后帮我更新迭代记录。”
  - “只输出当前项目快照。”

### 4. 发现产品价值问题

观察指标：

- 用户觉得它只是一个文档模板，不像 skill。
- 用户不知道它和普通 prompt 的区别。
- 用户用一次后没有复用。

改进动作：

- 在 README 中明确对比：普通 prompt vs skill。
- 加一个真实前后对比：
  - 以前：每次翻聊天记录找下一步。
  - 现在：脚本读问题池，Codex 直接给下一步。
- 展示一次“从需求到记录更新”的完整 demo。

### 5. 发现通用性问题

观察指标：

- 只有 DeepLister 能用，别人项目迁移成本高。
- 用户问“能不能换成我自己的项目名？”
- 用户想自定义迭代记录路径。

改进动作：

- 支持 `--record-path`。
- README 增加“用于其他项目”的改造说明。
- 中长期考虑拆成更通用的 `local-iteration-tracker-skill`。

## 4. 外部平台推广策略

早期不要全平台同时发。先用 3 类内容打穿：

1. 故事型：我为什么做这个 skill。
2. 教程型：如何安装、如何第一次跑通。
3. Demo 型：从一句需求到迭代记录自动更新。

### 推荐发布顺序

| 时间 | 重点 | 目标 |
| --- | --- | --- |
| 第 1 天 | 优化 GitHub 门面 | 让点进来的人看懂并愿意试 |
| 第 2 天 | 发故事文章 | 让别人理解痛点，不只是看到链接 |
| 第 3 天 | 发 demo 视频/GIF | 降低理解成本 |
| 第 4-7 天 | 每天一个小更新 | 制造持续活跃信号 |
| 第 8-14 天 | 投放到开发者社区 | 找第一批精准反馈 |
| 第 15 天后 | 再考虑 Product Hunt / Show HN | 等项目更通用、更容易试用 |

## 5. 平台打法

### GitHub

目标：把仓库变成可信的“项目主页”。

动作：

- 设置 topics：`codex`, `codex-skill`, `ai-agent`, `workflow`, `markdown`, `iteration`, `productivity`, `beginner-friendly`。
- 设置 social preview 图，建议做 1280 x 640。
- 增加 demo GIF 或截图。
- 增加 Issue templates：
  - Bug report
  - Installation problem
  - Feature request
  - User story / use case
- 增加 `CHANGELOG.md`。
- 增加 `ROADMAP.md`。

核心指标：

- Views
- Unique visitors
- Stars
- Forks
- Issues
- Referrers

### X / Twitter

目标：触达 AI builder、独立开发者、开源工具用户。

内容格式：

- 1 条主帖讲痛点。
- 1 条线程讲制作过程。
- 1 条短 demo 视频。
- 每次小更新发一条 changelog 风格帖子。

首发文案：

```text
I built a tiny Codex skill for beginners who are building their first big project and feel buried by messy tasks.

It reads a local Markdown iteration record, picks the next task, and reminds Codex to update the log after each change.

Not a PM tool. Just a small workflow guardrail.

GitHub: <repo-url>
```

中文版本：

```text
我做了一个很小的 Codex skill，给第一次做大项目、被一堆任务压住的新手用。

它不替代 Jira/Notion，只做一件事：
让 Codex 每次动手前先看问题池，选出下一步任务，做完后更新迭代记录。

适合个人项目早期，不想一上来就搞复杂项目管理的人。

GitHub: <repo-url>
```

### 知乎

目标：吃“问题解释”和“个人经历”的长尾搜索。

适合标题：

- 《我为什么给 Codex 做了一个迭代管理 skill》
- 《第一次做大项目，任务又多又乱时，我怎么让 AI 帮我找下一步》
- 《普通 prompt 不够用时，Codex skill 能解决什么问题？》

文章结构：

1. 我遇到的问题：任务散在聊天、文档、代码里。
2. 普通 prompt 的问题：每次都要重新解释上下文。
3. skill 的作用：把工作流固化下来。
4. 真实 demo：从问题池到下一步任务。
5. 适合谁，不适合谁。
6. GitHub 链接和欢迎 Star。

### 掘金 / CSDN

目标：让中文开发者能按教程复现。

适合内容：

- 安装教程。
- Windows 路径说明。
- `SKILL.md` 结构拆解。
- `iteration_snapshot.py` 脚本解释。
- 如何把它改成自己的项目迭代 skill。

标题建议：

- 《给 Codex 做一个项目迭代 skill：从任务池自动找下一步》
- 《代码小白也能用的 Codex skill：用 Markdown 管理项目迭代》
- 《我把项目迭代记录封装成了一个 Codex skill》

### B 站 / 小红书

目标：用可视化方式让新手一眼懂。

视频脚本：

1. 开场 5 秒：展示“任务太多，不知道下一步做什么”。
2. 展示 `docs/迭代记录.md`。
3. 对 Codex 说：用 deeplister-iteration 看下一步。
4. 展示脚本输出推荐任务。
5. 展示完成后自动补记录。
6. 结尾：适合第一次做大项目的新手，GitHub 链接在简介。

小红书标题：

- 《第一次做大项目，AI 也需要一个任务本》
- 《我给 Codex 做了个小插件，专治任务太乱》
- 《代码小白做 AI 产品，怎么避免项目越做越乱》

### V2EX

目标：找真实开发者反馈。

适合版块：

- `分享创造`
- `程序员`
- `AI`

发帖语气要朴素，不要营销味太重。

标题：

```text
做了一个给 Codex 用的轻量迭代管理 skill，适合个人项目早期用 Markdown 管任务
```

正文重点：

- 我为什么做。
- 它能做什么。
- 它现在的限制。
- 希望大家重点吐槽安装、README 和通用性。

### Reddit

目标：触达英文开发者和 AI 工具用户。

可考虑社区：

- r/OpenSource
- r/GitHub
- r/SideProject
- r/learnprogramming
- r/ChatGPTCoding
- r/ClaudeAI（如果后续做 Claude Code 版本）

注意：

- 先看每个 subreddit 的自推广规则。
- 不要一帖多发同文案。
- 最好带 demo、限制和问题请求。

英文标题：

```text
I built a tiny Codex skill that helps beginner projects pick the next task from a Markdown iteration log
```

### Hacker News / Show HN

目标：找技术深度反馈，不是单纯求 Star。

建议等到满足这些条件再发：

- README 已经足够清楚。
- 有 demo GIF 或短视频。
- 支持自定义项目名或记录路径。
- 新用户 5 分钟内能跑通。

标题：

```text
Show HN: A tiny Codex skill for managing project iterations in Markdown
```

首条评论重点：

- 为什么做。
- 和普通 prompt 的区别。
- 当前限制。
- 你最想要什么反馈。

### Product Hunt

目标：做一次正式“发布事件”。

建议不要太早上。等它至少具备：

- 漂亮 social preview。
- 1 分钟 demo。
- 清晰 landing README。
- 至少 3-5 个真实使用案例或模板。
- 有 `ROADMAP` 和 `CHANGELOG`。

Product Hunt 文案：

```text
Name: deeplister-iteration-skill
Tagline: A tiny Codex skill for keeping beginner projects organized
Description: Keep your early project iterations in one Markdown file. Let Codex pick the next task, follow priorities, and write back what changed after each session.
```

## 6. 14 天推广执行表

| 天数 | 动作 | 产出 |
| --- | --- | --- |
| Day 1 | 完善 GitHub 门面 | topics、social preview、README 截图区 |
| Day 2 | 写中文故事文章 | 知乎 / 掘金首发 |
| Day 3 | 录 60 秒 demo | B 站、小红书、X 可复用 |
| Day 4 | 增加 Issue templates | 方便用户反馈安装和功能问题 |
| Day 5 | 增加 `CHANGELOG.md` | 每次小更新有记录 |
| Day 6 | 写“如何改成自己的项目 skill” | 教程文章 |
| Day 7 | 发第一周复盘 | 讲数据、反馈、下一步 |
| Day 8 | 发 V2EX | 找技术反馈 |
| Day 9 | 发 Reddit 英文版 | 找英文反馈 |
| Day 10 | 修复第一批反馈 | 小版本发布 |
| Day 11 | 补英文教程 | 面向海外用户 |
| Day 12 | 做通用路径支持计划 | 为 v0.2.0 准备 |
| Day 13 | 准备 Show HN 草稿 | 不急着发 |
| Day 14 | 总结两周数据 | 决定是否 Product Hunt |

## 7. 每周复盘模板

```md
## 第 X 周推广复盘

### 本周发布
- 平台：
- 内容：
- 链接：

### 数据
- GitHub views：
- Unique visitors：
- Stars：
- Forks：
- Issues：
- 外部平台阅读/点赞/评论：

### 用户反馈
- 安装问题：
- README 问题：
- 使用问题：
- 价值不清楚的地方：

### 本周判断
- 哪个平台最有效：
- 哪类内容最有效：
- 当前最大阻碍：

### 下周动作
- P0：
- P1：
- P2：
```

## 8. 现在最值得做的 5 件事

1. 做一张 1280 x 640 的 GitHub social preview。
2. 给 README 加一张“运行脚本后的输出截图”。
3. 新增 Issue templates，尤其是安装失败和功能建议。
4. 写一篇中文故事文章：《我为什么给 Codex 做了一个迭代管理 skill》。
5. 录一个 60 秒 demo：从任务池到下一步推荐，再到迭代记录更新。

## 9. 参考资料

- GitHub Social Preview：<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview>
- GitHub Topics：<https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics>
- GitHub Issue Templates：<https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository>
- GitHub Traffic API：<https://docs.github.com/en/rest/metrics/traffic>
- Hacker News Show HN Guidelines：<https://news.ycombinator.com/showhn.html>
- Product Hunt Launch Guide：<https://www.producthunt.com/launch>
