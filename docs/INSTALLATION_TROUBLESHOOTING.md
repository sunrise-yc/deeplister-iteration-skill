# 安装排错

更新时间：2026-07-03

这份文档给第一次安装 `DL-vibe-lens-skill` 的用户看。

## 1. 先确认文件夹放对了

把整个 `dl-vibe-lens-skill/` 文件夹复制到 Codex skills 目录。

Windows:

```text
C:\Users\<your-user>\.codex\skills\dl-vibe-lens-skill
```

macOS / Linux:

```text
~/.codex/skills/dl-vibe-lens-skill
```

最终结构应该是：

```text
dl-vibe-lens-skill/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
```

如果路径变成这样，就多套了一层，Codex 可能发现不了：

```text
~/.codex/skills/DL-vibe-lens-skill/dl-vibe-lens-skill/SKILL.md
```

## 2. Codex 没发现 Skill

检查三件事：

1. `SKILL.md` 是否直接在 `dl-vibe-lens-skill/` 下面。
2. 是否重启了 Codex，或者新开了一个对话。
3. 提示词是否用了正确名字：

```text
Use $dl-vibe-lens-skill to initialize or inspect this project, generate the visual sandbox, and show questions, Git diff, evidence, conflict signals, and iteration path without ranking tasks.
```

## 3. 没有记录文件

不要手动创建。运行：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --init
```

它会创建：

```text
docs/iteration-record.md
docs/vibe-lens-settings.json
```

生成的文件里会写清楚哪些标题不要改名，以及 Vibe Lens 为什么不替你排优先级。
设置文件里会默认写入 `reply_entry_mode: "always"`，表示项目启用后每轮回复末尾都显示简约入口。

## 4. 脚本跑不起来

先确认你在目标项目根目录里，再运行：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root .
```

如果只是想测试这个仓库自带的示例：

```powershell
$env:PYTHONIOENCODING='utf-8'; python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
```

正常输出里应该能看到类似：

```text
Questions: 3 total, 2 open
Code diff:
Latest iteration:
```

## 5. HTML 报告没出现

显式生成：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --html
```

默认会写到：

```text
docs/vibe-lens-report.html
```

这个文件可以直接用浏览器打开。第一阶段是静态 HTML，不是线上网站。

## 6. Windows 终端中文乱码

有时 PowerShell 只是显示编码不对，文件本身没坏。先运行：

```powershell
$env:PYTHONIOENCODING='utf-8'
```

再重新跑 snapshot 命令。

如果 Markdown 在编辑器里显示正常，那通常就是终端显示问题，不是文件损坏。

## 7. Git diff 数字看起来不对

Vibe Lens 读取的是 Git 数据，数字取决于比较范围。

默认规则：

- 如果仓库有 commit，就比较当前工作区和 `HEAD`。
- 未跟踪文件会单独列出来。
- 二进制文件不会假装有行数。

想指定比较范围，可以用：

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root . --diff-ref main
```

## 8. 旧记录兼容

脚本仍然能读：

```text
docs/迭代记录.md
```

也能读旧字段：

```md
| ID | Issue | Impact | Priority | Status | Next Step |
| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
```

`Priority` 只当旧字段展示，不用于排序。

## 9. 提 Issue 时带什么

如果还是卡住，建议带上：

- 操作系统：Windows / macOS / Linux
- 使用环境：Codex 桌面版、CLI、IDE 或其他
- 安装路径
- 运行的命令
- 终端报错或截图
- 脱敏后的 `docs/iteration-record.md` 示例

Issue 类型建议：

- 安装问题：`Installation problem`
- 脚本 / 解析 / 报告生成问题：`Bug report`
- 新能力建议：`Feature request`
- 真实使用场景反馈：`User story / use case`
