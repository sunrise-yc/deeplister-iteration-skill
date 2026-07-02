# 演示脚本

这是一份 60 秒演示脚本，用来给第一次看到 `DL-vibe-lens-skill` 的人快速讲明白它。

## 演示目标

让观众看到一条完整链路：

1. vibe-coding 项目到了中后期，问题开始散乱。
2. 运行 `--init` 自动创建 `docs/iteration-record.md`。
3. 运行 snapshot，读取当前问题、历史问题、活跃工作和 Git diff。
4. 生成 HTML 复盘沙盘。
5. 强调 Vibe Lens 展示证据，不替人排优先级。

## 时间线

| 时间 | 画面 | 旁白 |
|---|---|---|
| 0-8 秒 | 展示一堆聊天、TODO、代码 diff | vibe coding 一开始很快，但项目到中后期会乱：问题散在聊天、文档和代码里。 |
| 8-18 秒 | 运行 `--init` | 用户不应该手动搭结构化 Markdown，一个命令就生成记录文件。 |
| 18-28 秒 | 打开 `docs/iteration-record.md` | 这里是数据源：问题池、活跃工作、追问记录、迭代日志。 |
| 28-40 秒 | 运行 snapshot | 脚本读取记录和 Git diff，只展示事实，不挑“赢家”。 |
| 40-52 秒 | 打开 HTML 报告 | 报告是复盘沙盘：当前问题、历史问题、代码差异、证据链和迭代路径。 |
| 52-60 秒 | 展示边界说明 | Vibe Lens 把事实和 Agent 判断分开。你可以问建议，但建议不会伪装成事实。 |

## 命令

初始化：

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --init
```

查看文本快照：

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root .
```

生成 HTML：

```powershell
python "$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py" --project-root . --html
```

触发提示词：

```text
Use $vibe-lens to initialize or inspect this project, generate the visual sandbox, and show questions, Git diff, evidence, conflict signals, and iteration path without ranking tasks.
```

## 短旁白

```text
我做了一个 Codex Skill，专门处理 vibe coding 的“中后期混乱”。

项目一大，问题会散在聊天、文档和代码 diff 里。如果同时开几个 AI 对话，还可能互相改到同一片区域。

Vibe Lens 把项目记录和 Git diff 变成一个复盘沙盘：当前问题、历史问题、代码增删、迭代路径、证据链和冲突线索都能看到。

它不是项目管理系统，不替你排优先级。它的作用是先把局面摆清楚。
```

## 小红书文案

```text
vibe coding 一开始很爽，但项目到中后期会乱。

我做了一个 Codex Skill：Vibe Lens。

它把项目记录 + Git diff 变成复盘沙盘：
- 当前问题
- 历史问题
- 代码新增/删除
- 迭代路径
- 证据链
- 冲突线索

它展示局面，不替你排优先级。
```
