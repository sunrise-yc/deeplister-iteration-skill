# Vibe Lens 基础实现计划

> **给 Agent 工作者的要求：** 如果继续执行本计划，必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`，并按任务逐项执行。步骤使用 checkbox（`- [ ]`）追踪。

**目标：** 将项目重新定位并实现为 `vibe-lens`：一个 Codex Skill，用来生成基于证据的可视化复盘沙盘，不做任务排序，也不安排执行顺序。

**架构：** Skill 保持小而稳定。Skill 负责告诉 Codex 何时初始化 / 读取 Markdown 记录，何时运行 Python 快照脚本，何时生成 JSON / HTML 复盘报告。Markdown 是输入源和备份，HTML 报告是用户主要查看界面。

**技术栈：** Python 3 标准库、Markdown 表格、Git CLI、静态 HTML/CSS/JS、`unittest`。

---

## 文件范围

- 将旧目录 `vibe-iteration/` 改为 `vibe-lens/`。
- 将旧脚本 `vibe-iteration/scripts/iteration_snapshot.py` 改为 `vibe-lens/scripts/lens_snapshot.py`。
- 创建 `vibe-lens/assets/report_template.html`，作为静态可视化沙盘模板。
- 更新 `vibe-lens/SKILL.md`，让它明确只展示信息，不做优先级决策。
- 更新 `vibe-lens/references/iteration-record-format.md`，作为 Vibe Lens 记录格式说明。
- 更新 `vibe-lens/agents/openai.yaml`，使用面向用户的 `Vibe Lens` 元数据。
- 更新 `tests/test_lens_snapshot.py`，覆盖快照、HTML 报告、自动初始化和 Git diff。
- 更新示例和公开文档：`README.md`、`ROADMAP.md`、`CHANGELOG.md`、`PROMOTION_PLAN.md`、`docs/*.md`。
- 更新 `docs/iteration-record.md`，让本项目自己使用 Vibe Lens 记录格式。
- 将完成后的 `vibe-lens/` 复制到 `C:\Users\23184\.codex\skills\vibe-lens`。

## 任务 1：编写 Lens 行为测试

**文件：**
- 修改：`tests/test_lens_snapshot.py`

- [ ] 测试能导入 `vibe-lens/scripts/lens_snapshot.py`。
- [ ] 测试快照输出保留问题数量和当前问题，但不包含 `recommended_next`。
- [ ] 测试 Git diff 统计来自临时 Git 仓库的 `--numstat`。
- [ ] 测试 `--init` 能创建新手友好的记录文档，并写明不要改章节名、不要让 Lens 排任务。
- [ ] 测试静态 HTML 报告能生成，并包含 JSON 数据和主要视觉板块。
- [ ] 运行 `python -m unittest tests.test_lens_snapshot`，确认实现前测试失败。

## 任务 2：重命名并重新定位 Skill

**文件：**
- 移动：`vibe-iteration/` -> `vibe-lens/`
- 移动：`vibe-lens/scripts/iteration_snapshot.py` -> `vibe-lens/scripts/lens_snapshot.py`
- 修改：`vibe-lens/SKILL.md`
- 修改：`vibe-lens/agents/openai.yaml`

- [ ] 重命名目录和脚本。
- [ ] 将 Skill frontmatter 改为 `name: vibe-lens`。
- [ ] 让描述触发于项目复盘、代码差异可视化、问题历史、vibe coding 沙盘等场景。
- [ ] 删除“选择最高优先级任务”和“推荐下一个任务”的指令。
- [ ] 添加明确边界：只展示事实，不排序，不编排任务；未来 Agent 建议必须和证据分层展示。
- [ ] 所有命令改用 `vibe-lens/scripts/lens_snapshot.py`。

## 任务 3：实现快照数据和 Git diff 统计

**文件：**
- 修改：`vibe-lens/scripts/lens_snapshot.py`

- [ ] 将脚本术语从 iteration snapshot 改为 lens snapshot。
- [ ] 保留对 `docs/iteration-record.md` 和旧记录文件的兼容。
- [ ] 保留 Markdown 表格解析能力。
- [ ] 删除 `recommended_next`，改为中立字段，例如 `open_questions`、`question_counts`、`latest_iteration`、`conflict_signals`。
- [ ] 通过 `git diff --numstat`、`git diff --name-status`、`git status --short` 收集 Git 事实数据。
- [ ] 输出适合 HTML 嵌入的有界 JSON。
- [ ] 添加 `--html` 和 `--output` 参数，用来生成静态报告。
- [ ] 保持 Python 标准库实现，不引入外部依赖。

## 任务 4：添加静态报告模板

**文件：**
- 创建：`vibe-lens/assets/report_template.html`

- [ ] 构建静态 HTML 报告，包含总览、当前问题、历史问题、代码差异、迭代方向、证据链和冲突线索。
- [ ] 使用脚本嵌入的 JSON 数据。
- [ ] 只使用简单 CSS 和 JS，不依赖外部库。
- [ ] 页面文案不能暗示优先级判断或任务安排。

## 任务 5：更新记录格式、示例和文档

**文件：**
- 修改：`vibe-lens/references/iteration-record-format.md`
- 替换：`examples/vibe-iteration-record.example.md` -> `examples/vibe-lens-record.example.md`
- 修改：`README.md`、`ROADMAP.md`、`CHANGELOG.md`、`PROMOTION_PLAN.md`
- 修改：`docs/DEMO_SCRIPT.md`、`docs/INSTALLATION_TROUBLESHOOTING.md`、`docs/LAUNCH_CHECKLIST.md`、`docs/PROJECT_CONTEXT.md`、`docs/RELATED_WORK.md`、`docs/iteration-record.md`

- [ ] 将公开定位从“迭代管理”改为“复盘沙盘”。
- [ ] 删除“挑选最高优先级任务”这类表达。
- [ ] 说明 Git diff 统计来自 Git，在统计范围明确时比较准确。
- [ ] 保留首次使用自动初始化能力，即 `--init`。
- [ ] 记录 HTML 报告生成命令。
- [ ] 保留 DeepLister 和 `vibe-iteration` 的兼容说明。

## 任务 6：测试、本地安装和验证

**文件：**
- 修改：`tests/test_lens_snapshot.py`
- 创建 / 更新：`C:\Users\23184\.codex\skills\vibe-lens`

- [ ] 运行聚焦单元测试。
- [ ] 运行 Python 编译检查。
- [ ] 用示例记录运行脚本。
- [ ] 为仓库生成 HTML 报告。
- [ ] 用仓库自己的记录文档运行脚本。
- [ ] 将 `vibe-lens/` 复制到本地 Codex skills 目录。
- [ ] 从 `C:\Users\23184\.codex\skills\vibe-lens` 运行已安装 Skill 的脚本。
- [ ] 运行 `git diff --check`。

## 当前状态说明

这份计划是项目基础改名和基础能力实现计划。当前仓库已经完成了其中大部分内容。

后续报告 UI 的圆环、证据完整度条、悬浮框、语言切换等细节，应以单独的报告 UI 规格和实现计划为准。
