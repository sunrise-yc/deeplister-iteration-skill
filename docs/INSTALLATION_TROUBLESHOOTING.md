# 安装排障指南

更新时间：2026-07-01

这份文档给第一次安装 `deeplister-iteration-skill` 的用户使用。目标是帮你快速判断：文件放对了吗？Codex 识别到了吗？脚本能跑吗？

## 1. 正确的安装位置

把整个 `deeplister-iteration/` 文件夹复制到 Codex skills 目录。

Windows 通常是：

```text
C:\Users\<你的用户名>\.codex\skills\deeplister-iteration
```

macOS / Linux 通常是：

```text
~/.codex/skills/deeplister-iteration
```

注意：最终目录里应该直接看到这些文件和文件夹：

```text
deeplister-iteration/
  SKILL.md
  agents/
  references/
  scripts/
```

如果路径变成了下面这样，就多套了一层文件夹，Codex 可能识别不到：

```text
~/.codex/skills/deeplister-iteration-skill/deeplister-iteration/SKILL.md
```

## 2. Codex 没有识别到 skill

先检查 3 件事：

1. `SKILL.md` 是否在 `deeplister-iteration/` 文件夹第一层。
2. 是否重启了 Codex，或新开了一个 Codex 会话。
3. 你说的是不是准确的 skill 名：

```text
Use $deeplister-iteration to pick the next DeepLister task.
```

中文也可以：

```text
用 deeplister-iteration 看一下下一步该做什么。
```

如果还是识别不到，先把安装路径截图或复制到 Issue 里，用 `Installation problem` 模板反馈。

## 3. 脚本跑不起来

先确认你是在目标项目根目录运行命令。比如你的 DeepLister 项目里应该有：

```text
docs/迭代记录.md
```

然后运行：

```powershell
python "$env:USERPROFILE\.codex\skills\deeplister-iteration\scripts\iteration_snapshot.py" --project-root .
```

如果你只是想测试这个仓库里的示例，可以在 `deeplister-iteration-skill` 仓库根目录运行：

```powershell
$env:PYTHONIOENCODING='utf-8'; python deeplister-iteration\scripts\iteration_snapshot.py --project-root . --record examples\deeplister-iteration-record.example.md
```

正常输出里应该看到：

```text
Issues: 2 total, 2 unresolved
Recommended next task:
  - DL-001 [P0] 追问判断过度依赖关键词和长度
```

## 4. 中文显示乱码

Windows 终端有时会用本地编码，中文可能显示不稳定。

可以先运行：

```powershell
$env:PYTHONIOENCODING='utf-8'
```

然后再运行 snapshot 脚本。

如果只是终端显示乱码，但 README 或 Markdown 文件本身正常，一般不是文件坏了，而是终端编码显示问题。

## 5. 找不到 `docs/迭代记录.md`

这个 skill 默认读取：

```text
docs/迭代记录.md
```

如果你的项目还没有这个文件，可以先复制示例：

```text
examples/deeplister-iteration-record.example.md
```

复制到你的项目里，并改名为：

```text
docs/迭代记录.md
```

最小结构至少要包含：

```md
# DeepLister 迭代记录

## 问题池

| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
|---|---|---|---|---|---|
| DL-001 | 示例问题 | 为什么重要 | P0 | 待处理 | 下一步动作 |

## 迭代记录
```

## 6. 推荐任务不符合预期

当前推荐逻辑比较简单：

1. 读取 `## 问题池` 下的 Markdown 表格。
2. 排除状态是 `已解决`、`完成`、`done`、`closed`、`resolved` 的任务。
3. 按优先级排序，默认 `P0` 最高。
4. 同优先级时，按编号排序。

所以如果推荐结果不对，先检查：

- `优先级` 是否写成了 `P0`、`P1`、`P2` 这类格式。
- `状态` 是否写错。
- 表格列名是否还是：`编号 | 问题 | 影响 | 优先级 | 状态 | 下一步`。

## 7. 开 Issue 时请带上这些信息

如果你还是卡住，可以开 Issue。为了更快定位问题，建议带上：

- 操作系统：Windows / macOS / Linux
- Codex 使用环境：桌面版、CLI，或其他
- 你的安装路径
- 你运行的命令
- 终端报错或截图
- 一小段去掉隐私信息的 `docs/迭代记录.md` 示例

对应模板：

- 安装失败：`Installation problem`
- 脚本或推荐结果错误：`Bug report`
- 想要新能力：`Feature request`
- 想分享真实使用体验：`User story / use case`
