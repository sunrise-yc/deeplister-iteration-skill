# deeplister-iteration-skill 发布前清单

更新时间：2026-07-01

这个清单用于把项目从“本地已经准备好”推进到“GitHub 上别人能看懂、能试用、能反馈”。

## 1. 仓库门面

- [x] README 说明项目解决什么问题。
- [x] README 说明适合谁、不适合谁。
- [x] README 增加快速开始。
- [x] README 增加脚本输出截图。
- [x] README 解释普通 prompt 和 skill 的区别。
- [x] README 链接路线图和更新记录。
- [x] 增加 `ROADMAP.md`。
- [x] 增加 `CHANGELOG.md`。
- [x] 增加 `PROMOTION_PLAN.md`。
- [x] 增加 `docs/PROJECT_CONTEXT.md`，方便后续接着维护。

## 2. 反馈入口

- [x] 安装问题 Issue 模板。
- [x] Bug 反馈 Issue 模板。
- [x] 功能建议 Issue 模板。
- [x] 使用场景反馈 Issue 模板。
- [x] Issue template 配置文件。

产品判断：这一步的价值是让用户“遇到问题时知道怎么说”。新手用户如果不知道怎么反馈，问题就会消失在聊天记录里，项目也很难迭代。

## 3. 视觉素材

- [x] 生成 GitHub social preview 图片：`assets/social-preview.png`
- [x] 生成脚本输出截图：`assets/snapshot-output.png`
- [ ] 在 GitHub 仓库设置中上传 social preview。
- [x] 准备 60 秒 demo 文案与分镜：`docs/DEMO_SCRIPT.md`
- [ ] 根据 `docs/DEMO_SCRIPT.md` 录制 demo 视频或 GIF。

GitHub social preview 建议上传路径：

```text
Settings -> General -> Social preview
```

如果页面位置变化，就在仓库 Settings 里搜索 `Social preview`。

## 4. GitHub 仓库设置

- [ ] 设置仓库 description：

```text
A tiny Codex skill for keeping beginner projects organized with a Markdown iteration log.
```

- [ ] 设置仓库 website，可先留空，后续如果有文章或 demo 页再补。
- [ ] 设置 topics：

```text
codex
codex-skill
ai-agent
workflow
markdown
iteration
productivity
beginner-friendly
```

产品判断：topics 不是装饰，它们是 GitHub 内部的“分类标签”。对开源小项目来说，topics 能帮用户知道它属于哪类工具，也能增加被搜索到的概率。

## 5. Demo 内容

推荐先做“第一次跑通型 demo”，不要先做复杂技术拆解。

完整脚本见 `docs/DEMO_SCRIPT.md`。下面是摘要版。

60 秒结构：

| 时间 | 画面 | 旁白重点 |
| --- | --- | --- |
| 0-5 秒 | 展示任务很多、下一步不清楚 | 第一次做大项目时，任务很容易散掉。 |
| 5-15 秒 | 展示 `docs/迭代记录.md` 的问题池 | 先把问题、优先级、下一步写在一个 Markdown 文件里。 |
| 15-30 秒 | 运行 snapshot 脚本 | 脚本读问题池，找出当前最该做的任务。 |
| 30-45 秒 | 展示 Codex 使用 skill 选择任务 | Codex 不再靠聊天记忆猜，而是按规则看文档。 |
| 45-60 秒 | 展示迭代记录更新 | 做完后把改动、验证和下次建议写回记录。 |

一句话结尾：

```text
它不是 Jira，也不是 Notion。它只是帮早期个人项目养成一个好习惯：每次迭代前知道下一步，做完后留下记录。
```

## 6. 第一批推广内容

- [ ] GitHub README 完成后，先发一条中文短帖。
- [ ] 准备知乎/掘金故事文章：《我为什么给 Codex 做了一个迭代管理 skill》。
- [ ] 准备 V2EX 帖子，重点求安装、README、通用性反馈。
- [ ] 准备英文 Reddit 帖子，等 README 和 demo 更稳后再发。

中文短帖草稿：

```text
我做了一个很小的 Codex skill，给第一次做大项目、被一堆任务压住的新手用。

它不替代 Jira/Notion，只做一件事：
让 Codex 每次动手前先看 Markdown 问题池，选出下一步任务，做完后更新迭代记录。

适合个人项目早期，不想一上来就搞复杂项目管理的人。

GitHub: https://github.com/sunrise-yc/deeplister-iteration-skill
```

## 7. 提交前验证

每次提交前建议跑：

```powershell
python -m py_compile deeplister-iteration\scripts\iteration_snapshot.py
$env:PYTHONIOENCODING='utf-8'; python deeplister-iteration\scripts\iteration_snapshot.py --project-root . --record examples\deeplister-iteration-record.example.md
git diff --check
git status --short --branch
```

如果改了 Issue templates，再额外检查 YAML：

```powershell
@'
from pathlib import Path
import yaml
for path in sorted(Path('.github/ISSUE_TEMPLATE').glob('*.yml')):
    yaml.safe_load(path.read_text(encoding='utf-8'))
    print(f'OK {path}')
'@ | python -
```

## 8. 当前最推荐下一步

1. 跑一遍提交前验证。
2. 提交当前门面优化改动。
3. 上传 social preview。
4. 设置 GitHub topics。
5. 按 `docs/DEMO_SCRIPT.md` 录 demo 或做 GIF。
