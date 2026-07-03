# 变更记录

这个文件记录项目的重要变化。

## Unreleased

### 新增

- 增加 `DL-vibe-lens-skill` 方向：给 vibe-coding 项目使用的中性复盘沙盘。
- 增加 `dl-vibe-lens-skill/scripts/lens_snapshot.py`。
- 增加 Git diff 统计：新增行、删除行、变更 tracked 文件、未跟踪文件和文件状态。
- 增加 JSON 输出和静态 HTML 报告生成。
- 增加 `dl-vibe-lens-skill/assets/report_template.html`。
- 增加 `docs/vibe-lens-settings.json` 设置设计，默认 `reply_entry_mode: "always"`。
- 增加测试：中性问题展示、Git diff 统计、自动初始化、旧中文记录兼容、HTML 报告生成。
- 增加 `docs/superpowers/` 下的中文设计稿和执行计划。

### 变更

- 项目从 `vibe-iteration` 的任务选择方向，转为 `DL-vibe-lens-skill` 的信息展示方向。
- Skill 机器名和安装目录统一为 `dl-vibe-lens-skill`，触发名统一为 `$dl-vibe-lens-skill`。
- 删除脚本默认输出“推荐下一步任务”的行为。
- 将 `Priority` 重新定义为旧字段展示信息，不作为决策规则。
- README、安装排错、演示脚本、发布清单和项目上下文改为中文新用户说明。
- HTML 代码差异卡片改为固定高度：左侧圆环、右侧彩色数字、下方文件列表内部滚动。

### 说明

- `docs/iteration-record.md` 仍是默认数据源。
- 旧中文路径 `docs/迭代记录.md` 仍可读取。
- 页面产品名继续叫 `Vibe Lens`，默认报告文件仍是 `docs/vibe-lens-report.html`。
- 旧安装目录如 `deeplister-iteration`、`vibe-iteration`、`vibe-lens` 可以保留兼容，但新文档和新使用方式统一推荐 `dl-vibe-lens-skill`。

## 0.1.0 - 2026-07-01

### 新增

- 创建第一版 DeepLister 专用迭代 Codex Skill。
- 增加读取本地 Markdown 记录的 snapshot 脚本，可以输出问题数量、推荐任务、最新迭代记录和追问流程数量。
- 增加示例迭代记录。
- 增加 README、路线图、发布清单、演示脚本、推广计划、安装排错和 GitHub Issue 模板。

### 变更

- 第一版公开方向从 `deeplister-iteration` 改为 `vibe-iteration`。
- 增加 `--init`，自动创建 `docs/iteration-record.md`。
- 增加带 `## Issue Pool`、`## Active Work`、`## Follow-up Flow Notes`、`## Iteration Log` 的默认英文记录模板。
- 增加旧 `docs/迭代记录.md` 记录兼容。
