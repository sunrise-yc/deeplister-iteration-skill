# 发布清单

发布 `DL-vibe-lens-skill` 前，用这份清单过一遍。

## 仓库

- [ ] GitHub 仓库名是 `DL-vibe-lens-skill`。
- [ ] 本地 remote 指向新仓库地址。
- [ ] 仓库简介写清楚：
  `A Codex skill that turns messy vibe-coding projects into a visual review sandbox.`
- [ ] 仓库 topics 包含：
  - `codex`
  - `codex-skill`
  - `ai-agent`
  - `vibe-coding`
  - `retrospective`
  - `review`
  - `git-diff`
  - `dashboard`
- [ ] README 首屏能说明痛点和三步使用方法。
- [ ] README 有实操快闪照。

## 第一次使用

- [ ] 安装目录是 `dl-vibe-lens-skill/`。
- [ ] 触发提示词使用 `$dl-vibe-lens-skill`。
- [ ] `--init` 能创建 `docs/iteration-record.md`。
- [ ] `--init` 能创建 `docs/vibe-lens-settings.json`，默认 `reply_entry_mode` 是 `"always"`。
- [ ] 缺记录文件时，错误信息会提示运行 `--init`。
- [ ] README 不要求用户手动创建记录文件。
- [ ] README 说明 Vibe Lens 不排序、不安排任务。

## 验证

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .
git diff --check
```

## 演示

- [ ] 展示一个中后期变乱的 vibe-coding 项目。
- [ ] 运行 `--init`。
- [ ] 打开 `docs/iteration-record.md`。
- [ ] 运行 snapshot 命令。
- [ ] 生成 HTML 报告。
- [ ] 解释代码差异来自 Git。
- [ ] 展示事实和 Agent 判断是分开的。

## 发布说明

- [ ] 说明项目定位：复盘沙盘，不是任务管理器。
- [ ] 提到旧 `docs/迭代记录.md` 兼容。
- [ ] 提到 `--init`。
- [ ] 提到 Git diff 统计。
- [ ] 提到中文默认、可切英文的 HTML 报告。
- [ ] 提到本仓库自己也用 `docs/iteration-record.md` 做复盘。
