---
name: dl-vibe-lens-skill
description: 当 vibe-coding 项目需要复盘沙盘、问题历史、Git diff 可视化、迭代路径、证据链、验证记录，或多个 AI coding 会话之间的中性冲突线索时使用。
---

# DL Vibe Lens Skill

## 定位

把已经变得混乱的 vibe-coding 项目，整理成一个中性的复盘沙盘。

`DL` 指向 DeepLister：这个工作流最早是在 DeepLister 项目进入中后期、问题开始堆叠时长出来的。`Vibe Lens` 可以理解为给 vibe coding 过程装上一枚镜头：把散落的问题、Git diff 统计、迭代路径、证据、验证记录和冲突线索聚焦出来，让操作者和 Agent 看清局面。

它不做任务排序，不施加权重，不替操作者决定下一步必须做什么。

默认记录文件是：

```text
docs/iteration-record.md
```

默认设置文件是：

```text
docs/vibe-lens-settings.json
```

旧中文路径仍可读取：

```text
docs/迭代记录.md
```

只有在需要解释记录格式时，才读取：

```text
references/lens-record-format.md
```

## 快速开始

1. 确认当前目录是项目根目录。

2. 如果记录文件不存在，直接初始化，不要让第一次使用的人手动从零创建文件：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --init
```

3. 读取当前项目状态：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root .
```

4. 生成可视化复盘沙盘：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --html
```

5. 告诉用户 HTML 写到了哪里，通常是：

```text
docs/vibe-lens-report.html
```

6. 最终回复前读取 `docs/vibe-lens-settings.json`。如果 `reply_entry_mode` 是 `"always"`，在回复末尾追加简约 Vibe Lens 入口；如果是 `"when_used"`，只有本轮使用了 Vibe Lens 才追加；如果是 `"off"`，不要追加。

## 使用边界

- 展示证据，不施加优先级。
- `Priority` 只当旧字段或描述性元数据，不当命令。
- 除非用户明确要求 Agent 判断，否则不要替用户选择下一步任务。
- 如果用户要求建议，先展示 Vibe Lens 看到的事实，再明确标注“以下是 Agent 判断”。
- 冲突只展示为线索，不展示成排期命令。
- Markdown 记录是数据源，HTML 报告是主要阅读界面。
- 第一次使用不要让用户手动建文件，运行 `--init`。

## 应该展示什么

使用 snapshot 和 HTML 报告展示这些信息：

- 操作者和 Agent 当前提出的问题。
- 历史问题和历史迭代标题。
- Git diff 统计：新增行、删除行、变更文件、未跟踪文件。
- 从迭代记录和产品方向中整理出的迭代路径。
- 来自记录行、追问记录和 Git 状态的证据链与验证线索。
- 多个会话碰到同一文件或区域时产生的中性冲突线索。

## HTML 报告行为

当用户要求可视化、复盘、review、dashboard 或沙盘时，HTML 报告应该作为主要展示界面。

- 默认中文界面，同时保留英文切换。
- 主页保持紧凑：总览指标、当前问题、代码差异、沙盘演示、证据/冲突线索、迭代路径。
- 总览、沙盘演示、迭代路径都可以进入对应详情页。
- 标题、圆环、进度条、路径节点和设置项应有鼠标悬浮解释。
- Git diff 用圆环和文件行展示；Git 是证据来源，不要编造行数。
- 主页迭代路径展示大阶段；竖线是阶段刻度，不是精确日期。
- 包含对话入口设置面板。项目启用 DL Vibe Lens 后，默认可在每轮 Agent 回复末尾附带一个简约入口。
- 如果操作者说“本轮不要显示 Vibe Lens 入口”，本轮不要追加入口。
- 如果操作者持久关闭入口，要尊重项目设置。
- 入口应该是 Markdown 简约链接，例如 `[⌕ Vibe Lens](...)` 或 `[Vibe Lens](...)`，不要贴很长的裸 URL。
- 静态 HTML 里的设置面板只是展示辅助；真正持久生效的设置来自用户提示词或 `docs/vibe-lens-settings.json`。

## 记录更新规则

完成有意义的工作后，更新记录，让下一次复盘有证据：

- 在 `## 问题池` 中新增或更新当前问题和历史问题。
- 当另一个会话需要看到可能涉及的文件或区域时，更新 `## 当前工作`。
- 在 `## 迭代记录` 下添加带日期的条目。
- 新记录和新增条目默认跟随当前对话语言，除非操作者明确要求另一种语言。
- HTML 报告不要偷偷把源记录里的英文条目机器翻译后展示。
- 如果已有英文条目需要中文化，必须明确执行“翻译并写回记录”或“生成翻译缓存”。
- 记录证据、验证、未完成的不确定性和改动文件。
- 不要把建议写成事实。如果必须记录建议，要标成“Agent 判断”或“操作者决策”。
- 未完成的设计或产品想法放进记录或路线图，不能变成隐藏行为。

## 验证

声称 Lens 视图已经就绪前，至少做这些检查：

1. 运行与改动相关的最小测试或命令。
2. 再跑一次 snapshot helper，确认记录仍能读取。
3. 如果视觉复盘是本轮需求，重新生成 HTML 报告。
4. 如果 HTML 行为有变化，打开报告确认页面跳转、语言切换、设置面板和核心交互。
5. 说清楚哪些验证没能运行。

## 常见错误

| 错误 | 正确做法 |
|---|---|
| 只靠聊天记忆开始分析 | 先运行 snapshot |
| 把 `Priority` 当命令 | 只当旧元数据展示 |
| 直接告诉用户必须先做什么 | 先展示事实；建议要标注为 Agent 判断 |
| 改了代码但没更新证据 | 把改动文件和验证写进记录 |
| 第一次使用还让用户手动建记录 | 用 `--init` 初始化 |
| 所有内容都塞进 Markdown | 需要视觉复盘时生成 HTML 报告 |
| 回复里贴很长的裸链接 | 用 `[⌕ Vibe Lens](...)` 这样的简约入口 |
