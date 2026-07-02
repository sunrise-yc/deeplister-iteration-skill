# 项目上下文

更新时间：2026-07-03

这份文件给后续维护者看。真正的项目复盘数据源在 [iteration-record.md](iteration-record.md)。

## 维护者

- 用户：杨晨
- GitHub：https://github.com/sunrise-yc
- 偏好：代码相关内容用中文大白话解释。
- 学习方向：AI 产品经理。

## 项目

- 当前本地目录：`C:\Users\23184\Desktop\deeplister-iteration-skill`
- 当前公开仓库名：`DL-vibe-lens-skill`
- 项目类型：Codex Skill
- Skill 名：`vibe-lens`
- 默认数据源：`docs/iteration-record.md`
- 旧记录兼容：`docs/迭代记录.md`

## 产品定位

`vibe-lens` 是一个给 vibe-coding 项目用的复盘沙盘。

它展示：

- 当前问题；
- 历史问题；
- Git diff 代码差异；
- 迭代路径；
- 证据和验证记录；
- 多个 AI 对话之间可能存在的冲突线索。

它不做：

- 自动排序；
- 自动加权；
- 自动安排任务；
- 替代测试或代码审查；
- 替代 Jira、Linear、Notion。

## 当前决定

- 公开项目名统一为 `DL-vibe-lens-skill`。
- Skill 文件夹仍叫 `vibe-lens/`，方便用 `$vibe-lens` 触发。
- 第一次使用必须走 `--init`，不能让新手手动建记录文件。
- HTML 报告默认中文，可切英文。
- 报告要有主页入口、详情页跳转、沙盘演示、迭代路径和对话入口设置。
- `Priority` 只当旧字段展示，不当排序依据。

## 验证命令

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile vibe-lens\scripts\lens_snapshot.py
python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python vibe-lens\scripts\lens_snapshot.py --project-root .
git diff --check
```

## 相关文档

- `README.md`：公开项目介绍。
- `ROADMAP.md`：产品路线图。
- `CHANGELOG.md`：变更记录。
- `docs/iteration-record.md`：当前复盘数据源。
- `docs/INSTALLATION_TROUBLESHOOTING.md`：安装排错。
- `docs/DEMO_SCRIPT.md`：演示脚本。
- `docs/RELATED_WORK.md`：相邻工具学习点。
