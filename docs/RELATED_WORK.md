# 相关工具、学习点与不足

这份文档记录 `DL-vibe-lens-skill` 应该从哪些相邻工具里学习，以及它和这些工具的刻意差异。

## 定位

`DL-vibe-lens-skill` 应该保持中性：

> 一个给 vibe coding 项目用的复盘沙盘，把问题、历史、代码差异、方向和证据展示出来。

它不应该变成完整的 Jira、Linear、Notion，也不应该变成自动任务裁判。它要解决的产品缺口更小：当问题、对话和代码改动开始散落时，先把局面展示清楚。

## 来源与学习点

| 来源 | 它解决什么 | 我们要学什么 | 为什么 |
|---|---|---|---|
| [OpenAI Codex Agent Skills](https://developers.openai.com/codex/skills) | 把一套 Codex 工作流封装成可复用的 skill，里面可以放说明、参考资料和脚本 | `SKILL.md` 要聚焦；能确定执行的逻辑尽量放进脚本 | 这样 skill 才容易被稳定触发，不需要依赖很长的聊天记忆 |
| [KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) | 用 Skill 触发脚本，再生成本地 HTML 报告或服务 | 学它的“Skill + 脚本 + JSON + HTML 展示平台”结构 | Markdown 很适合做源记录，但复杂信息应该进入可视化报告 |
| [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) | 用看板、工作区、分支、终端和 review 流程管理 AI coding agent | 增加“当前正在做什么”的可见记录 | 多个 AI 对话并行时，如果看不到当前工作，很容易互相改同一块 |
| [Task Master](https://github.com/eyaltoledano/claude-task-master) | 初始化项目、解析 PRD、管理任务，并推荐下一步任务 | 学初始化体验，不学默认替用户排任务 | 本项目第一阶段只展示信息；第一次使用仍然必须一条命令跑通 |
| [CCPM](https://github.com/automazeio/ccpm) | 用 PRD、epic、GitHub Issues 和 worktree 支持并行 Claude Code 工作 | 保留可追踪性，但一开始不要做太重的配置 | GitHub Issues 和 worktree 对团队有价值，但新手更需要一个小的本地闭环 |
| [Archon](https://github.com/coleam00/Archon) | 用阶段、验证关卡和产物让 AI coding 流程更确定 | 把验证结果当成复盘沙盘的一部分 | 如果没有验证，记录就只是“今天做了什么”的日记，不是能帮助复盘的证据链 |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 用持久化项目文件保存计划和上下文 | 先用文件记忆，再考虑复杂集成 | Markdown 文件不怕上下文丢失，也方便新手打开检查 |
| 本机 `gstack-retro` / `gstack-diagram` / `baoyu-infographic` 等 Skill | 复盘、图表、信息图、设计稿和浏览器验证 | 作为工具箱使用，不作为产品边界 | 它们能帮助生成图或做复盘，但不能让 `DL-vibe-lens-skill` 变成大而全平台 |

## 当前不足

| 不足 | 为什么重要 | 产品处理方式 |
|---|---|---|
| 需要手动创建记录文件 | 新手可能还没第一次成功就放弃 | 保留 `--init`，缺文件时报错时明确提示使用它 |
| 旧名字像迭代管理工具 | 容易误导 Agent 去排优先级或安排任务 | 改名为 `DL-vibe-lens-skill`，保留 DeepLister 来源，同时强调观察和展示 |
| Markdown 不够直观 | 代码差异、方向变化、证据链很难靠文字快速看清 | 增加静态 HTML 报告，后续再做交互平台 |
| 代码差异需要准确边界 | Git 能准确统计，但必须知道从哪里到哪里 | 默认看工作区相对 `HEAD`，并支持 `--diff-ref` |
| 冲突线索容易被误解为命令 | 用户不希望 skill 擅自安排任务 | 第一阶段只展示冲突信号，不输出编排结论 |
| 暂时没有外部平台同步 | GitHub、Notion、Airtable 会增加复杂度 | 先做本地小闭环，真实需求稳定后再接 |

## 为什么不能让用户手动建文件

对这个产品来说，要求用户手动创建 `docs/iteration-record.md` 是产品缺陷，不只是文档没写清楚。

原因：

1. 目标用户包括代码新手。
2. 记录文件有固定标题，用户手动创建时很容易写错。
3. 第一次成功应该靠一个命令完成。
4. 自动生成的文件可以自带保护说明，告诉用户哪些标题不要改名，以及这个 skill 不负责排优先级。

后续原则：

> 如果 skill 工作前必须有一份结构化记录，那 skill 就必须提供初始化命令。
