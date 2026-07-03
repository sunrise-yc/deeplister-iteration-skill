# Vibe Lens 示例记录

这是 `DL-vibe-lens-skill` 的示例数据源。脚本会读取这份 Markdown，再结合 Git diff 数据生成 HTML 复盘沙盘。

## 保护说明

- 不要改名这些标题：`## 问题池`、`## 当前工作`、`## 追问流程专项记录`、`## 迭代记录`。
- 不要把 `## 问题池` 里的表格搬到其他位置。
- `优先级` 或 `Priority` 只能作为旧字段展示，不能当成任务排序命令。

## 当前产品方向

- 定位：给中后期开始变乱的 vibe-coding 项目做复盘沙盘。
- 当前重点：展示问题、代码差异、证据和路径，不替操作者安排任务。

## 问题池

| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-001 | 手动创建记录文件太重 | operator | open | 第一次使用的人不应该手动搭表格 | dl-vibe-lens-skill/scripts/lens_snapshot.py |
| VL-002 | 代码变化需要可视化 diff 统计 | agent | open | Git 可以在边界明确时准确给出新增/删除行数 | dl-vibe-lens-skill/assets/report_template.html |
| VL-003 | 旧优先级字段可能误导 Agent | operator | resolved | Skill 说明已改为只展示事实，不负责排序 | dl-vibe-lens-skill/SKILL.md |

## 当前工作

| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| 2026-07-03 | 构建复盘沙盘 | dl-vibe-lens-skill/, README.md, tests/ | in progress | 当前会话负责报告和命名同步 |

## 追问流程专项记录

| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 多个 AI 对话同时工作 | 每个对话可能持有不同上下文 | 可能改到同一文件 | 展示当前工作和涉及文件，作为中性冲突线索 |

## 迭代记录

### 2026-07-03: 更新为 DL-vibe-lens-skill
目标：
- 把公开传播名、安装目录、触发名和文档说明统一到新命名。

证据：
- 用户希望保留 DeepLister 来源，并让调用名更好记。

代码变化：
- 将 skill 目录改为 `dl-vibe-lens-skill/`。
- 更新 `SKILL.md`、README 和示例记录。

验证：
- 运行 `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md --html`。

未完成：
- 后续再做完整交互平台。
