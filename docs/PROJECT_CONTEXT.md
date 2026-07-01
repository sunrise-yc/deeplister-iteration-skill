# deeplister-iteration-skill 项目上下文

更新时间：2026-07-01

这个文件用来保存当前 Codex 对话里的项目背景、已完成事项和下一步计划。它不是正式用户文档，更像一个“接力卡片”：以后继续维护这个项目时，先看这里，可以快速知道我们做到哪一步。

## 维护人背景

- 用户：杨晨
- GitHub：<https://github.com/sunrise-yc>
- 当前偏好：代码相关内容尽量用大白话解释。
- 学习方向：想成为 AI 产品经理，所以沟通时可以带产品思维，解释为什么这样排优先级、为什么这样设计反馈闭环。

## 项目信息

- 本地仓库：`C:\Users\23184\Desktop\deeplister-iteration-skill`
- GitHub 仓库：<https://github.com/sunrise-yc/deeplister-iteration-skill>
- 项目类型：Codex skill
- 核心定位：给第一次做大项目、任务多又乱的新手，用 Markdown 管理迭代记录，让 Codex 每次先看问题池、选下一步任务、做完后更新记录。

一句话产品定位：

> 一个给 Codex 使用的轻量迭代管理 skill，适合早期个人项目用 Markdown 记录问题池、下一步任务和每次迭代结果。

## 不要做什么

- 不要把它宣传成 Jira、Linear、Notion 的替代品。
- 不要改 DeepLister 主项目；这个仓库只维护 `deeplister-iteration-skill`。
- 不要一上来做复杂协作能力，比如权限、分派、截止日期、燃尽图。

## 当前已完成

- 已阅读并理解 `README.md` 和 `PROMOTION_PLAN.md`。
- 已在 Codex 里为这个项目立项，目标是：维护并推广 `deeplister-iteration-skill`，先完成 GitHub 门面优化、Issue templates、README/Demo/social preview 等早期推广基础。
- 已优化 `README.md`：
  - 新增“快速开始”。
  - 新增脚本运行结果截图。
  - 新增“普通 prompt 和 skill 的区别”。
  - 新增反馈与路线图入口。
  - 新增英文 Quick Start、Prompt vs Skill、Feedback and Roadmap。
- 已新增 GitHub Issue templates：
  - 安装问题：`.github/ISSUE_TEMPLATE/installation_problem.yml`
  - Bug 反馈：`.github/ISSUE_TEMPLATE/bug_report.yml`
  - 功能建议：`.github/ISSUE_TEMPLATE/feature_request.yml`
  - 使用场景反馈：`.github/ISSUE_TEMPLATE/use_case_feedback.yml`
  - Issue 配置：`.github/ISSUE_TEMPLATE/config.yml`
- 已新增产品节奏文档：
  - `ROADMAP.md`
  - `CHANGELOG.md`
- 已新增推广素材：
  - `assets/social-preview.png`
  - `assets/snapshot-output.png`
- 已新增推广与迭代方案：
  - `PROMOTION_PLAN.md`
- 已新增发布前清单：
  - `docs/LAUNCH_CHECKLIST.md`
- 已新增 60 秒 demo 文案与分镜：
  - `docs/DEMO_SCRIPT.md`
- 已新增安装排障指南：
  - `docs/INSTALLATION_TROUBLESHOOTING.md`

## 已验证

已做过这些轻量验证：

- `python -m py_compile deeplister-iteration\scripts\iteration_snapshot.py`
- `python deeplister-iteration\scripts\iteration_snapshot.py --project-root . --record examples\deeplister-iteration-record.example.md`
- Issue template YAML 能被解析。
- README 中引用的图片文件存在。
- 图片尺寸检查：
  - `assets/social-preview.png` 是 1280 x 640。
  - `assets/snapshot-output.png` 是 1280 x 720。
- `git diff --check` 没有发现空白错误；只出现 Windows 下 LF/CRLF 换行提示。

## 当前工作区状态

最近一次检查时，`main` 分支上有未提交改动：

- 修改：`README.md`
- 新增：`.github/`
- 新增：`assets/`
- 新增：`CHANGELOG.md`
- 新增：`ROADMAP.md`
- 新增：`PROMOTION_PLAN.md`
- 新增：`docs/PROJECT_CONTEXT.md`
- 新增：`docs/LAUNCH_CHECKLIST.md`
- 新增：`docs/DEMO_SCRIPT.md`
- 新增：`docs/INSTALLATION_TROUBLESHOOTING.md`

提交前建议再跑一次验证命令，并检查 `git diff`。

## 下一步建议

按产品优先级看，下一步先做这些：

1. 提交当前这一批“门面基础设施”改动。
2. 在 GitHub 仓库设置里上传 `assets/social-preview.png` 作为 social preview。
3. 给 GitHub 仓库设置 topics：
   - `codex`
   - `codex-skill`
   - `ai-agent`
   - `workflow`
   - `markdown`
   - `iteration`
   - `productivity`
   - `beginner-friendly`
4. 按 `docs/DEMO_SCRIPT.md` 录制 60 秒 demo 或制作 GIF。
5. 写第一篇中文推广文章：
   - 标题建议：《我为什么给 Codex 做了一个迭代管理 skill》

更细的发布前步骤见 `docs/LAUNCH_CHECKLIST.md`。
安装失败或脚本跑不通时，先看 `docs/INSTALLATION_TROUBLESHOOTING.md`。

## 产品判断

这个项目早期最重要的不是功能多，而是让第一次来的用户完成 4 件事：

1. 看懂它解决什么问题。
2. 知道自己是不是适合用。
3. 能装上并跑通第一次。
4. 遇到问题时知道怎么反馈。

所以近期优先级应该是：

- P0：安装、运行、README 看懂。
- P1：反馈入口、路线图、更新记录。
- P2：截图、social preview、demo。
- P3：通用化、同步 GitHub Issues / Notion、改名为更通用的 local iteration tracker。
