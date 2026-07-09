# Vibe Lens 记录

这是 Vibe Lens 复盘沙盘的数据源文件。
Codex 会把它和 Git diff 数据一起读取，用来展示问题、历史、方向、证据和冲突线索。

中文大白话：这是项目复盘沙盘的原始记录本。它不是任务裁判，不替你排优先级；它把局面摆出来，让人和 Agent 自己判断。

## 保护说明

- 不要改名这些标题：`## 问题池`、`## 当前工作`、`## 追问流程专项记录`、`## 迭代记录`。
- 不要把 `## 问题池` 里的表格搬到其他位置。
- 不要只根据这个文件给问题排序，也不要告诉操作者“必须先做哪个”。
- `Priority` 或 `优先级` 只当旧字段展示。
- 可以自由编辑行内容、添加新行、添加额外章节。
- 如果 AI coding 会话开始大范围工作，先在 `## 当前工作` 记录涉及文件或区域。

## 当前产品方向

- 定位：给中后期开始变乱的 vibe-coding 项目做复盘沙盘和信息展现。
- 主要用户：独立开发者、代码新手、正在学习 AI 产品经理的人，以及使用 Codex 或其他 AI coding agent 的人。
- 核心任务：展示当前问题、历史问题、代码差异、迭代路径、证据链和冲突线索。
- 当前重点：`DL-vibe-lens-skill` 的 RedSkill 传播版已经打包并推到 GitHub PR；后续重点是详细迭代路径和第二阶段平台。
- 明确不做：默认排序优先级、安排任务、替操作者做权重判断。

## 问题池

| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-001 | 将项目重新定位为复盘沙盘 | operator | resolved | 用户明确说 skill 应展示信息，而不是决定优先级 | README.md, dl-vibe-lens-skill/SKILL.md |
| VL-002 | 可视化展示 Git diff 统计 | operator | resolved | `git diff --numstat` 能提供新增/删除行数 | dl-vibe-lens-skill/scripts/lens_snapshot.py, dl-vibe-lens-skill/assets/report_template.html |
| VL-003 | 第一次使用必须自动初始化 | operator | resolved | 让新手手动建记录文件太重 | dl-vibe-lens-skill/scripts/lens_snapshot.py |
| VL-004 | 同步公开文档和示例到 Vibe Lens 定位 | agent | resolved | 公开文档、示例、Issue 模板和图片已使用复盘沙盘定位 | README.md, docs/, examples/, assets/ |
| VL-005 | 重命名 GitHub 仓库、remote 和本地路径 | agent | resolved | 本地 remote 已指向 `sunrise-yc/DL-vibe-lens-skill`，分支和 PR 已推送 | GitHub remote, PR #4 |
| VL-006 | 第二阶段交互平台后续再做 | operator | open | Markdown 不足以承载任务编排和冲突建议 | ROADMAP.md |
| VL-007 | 将确认后的 HTML 报告界面打包进 Skill | operator | resolved | 模板已包含中英切换、主页入口、详情页、路径标签和对话入口设置 | dl-vibe-lens-skill/assets/report_template.html, tests/test_lens_snapshot.py |
| VL-008 | 准备中文公开介绍和快速上手图 | operator | resolved | README 已说明定位、安装、初始化、报告流程，并嵌入三张快闪图 | README.md, assets/quickstart-*.svg |
| VL-009 | 详细可展开路径图和平台后续再做 | operator | open | 第一阶段报告只做路径概览，完整展开/收起和平台编排属于后续阶段 | ROADMAP.md, dl-vibe-lens-skill/assets/report_template.html |
| VL-010 | 统一 Skill 名为 DL-vibe-lens-skill | operator | resolved | 用户希望保留 DeepLister 来源，并让调用名更好记 | README.md, dl-vibe-lens-skill/SKILL.md, docs/ |
| VL-011 | 总览指标应跳到对应详情 | operator | resolved | 用户指出当前问题、历史问题、变更文件、代码变化不应都进入同一个总览详情 | dl-vibe-lens-skill/assets/report_template.html, tests/test_lens_snapshot.py |
| VL-012 | 准备 RedSkill 上传材料和功能图 | operator | resolved | 用户要求推送 GitHub，并提供功能介绍文档、界面图、上传步骤和整理后的上传包 | docs/FEATURE_INTRO_ZH.md, assets/feature-*.png, dist/redskill/ |
| VL-013 | RedSkill 包说明中文化并生成小红书分步图 | operator | resolved | 用户指出上传包里仍是英文说明，并要求基于当前真实界面生成一整套功能介绍图 | dl-vibe-lens-skill/SKILL.md, dl-vibe-lens-skill/agents/openai.yaml, assets/xhs/, dist/redskill/ |
| VL-014 | 可视化认知层 review 反馈需要修复 | agent | resolved | 最终 review 指出解释不足统计、文件详情标签、多语言标签和文件行布局仍有缺口 | dl-vibe-lens-skill/scripts/lens_snapshot.py, dl-vibe-lens-skill/assets/report_template.html, tests/test_lens_snapshot.py |

## 当前工作

| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| 2026-07-02 | 重新定位为 Vibe Lens 复盘沙盘 | dl-vibe-lens-skill/, README.md, docs/, examples/, tests/ | completed | GitHub remote 重命名已作为外部事项处理 |
| 2026-07-02 | 发布干净的 Vibe Lens 分支和 PR | GitHub branch, PR #3 | completed | 分支 `codex/vibe-lens-review-sandbox-clean` 已推送，PR #3 可合并 |
| 2026-07-03 | 打包 RedSkill 传播版 Vibe Lens | dl-vibe-lens-skill/, README.md, ROADMAP.md, docs/, assets/, tests/ | completed | 分支 `codex/vibe-lens-report-ui-spec` 已推到 `sunrise-yc/DL-vibe-lens-skill`，草稿 PR #4 已打开 |
| 2026-07-03 | 统一 Skill 命名和入口设置 | dl-vibe-lens-skill/, README.md, docs/, examples/, assets/, tests/ | completed | 展示名保留 `DL-vibe-lens-skill`，实际 skill 机器名用规范小写 `dl-vibe-lens-skill` |
| 2026-07-03 | 修正总览详情入口 | dl-vibe-lens-skill/assets/report_template.html, tests/test_lens_snapshot.py | completed | 四个总览指标分别进入对应详情页；入口设置支持点击空白关闭 |
| 2026-07-03 | 准备 GitHub 推送和 RedSkill 上传材料 | README.md, docs/FEATURE_INTRO_ZH.md, assets/feature-*.png, dist/redskill/ | completed | 中文功能介绍已配功能截图；上传包排除缓存和临时报告 |
| 2026-07-03 | 中文化 RedSkill 包并生成小红书分步图 | dl-vibe-lens-skill/SKILL.md, dl-vibe-lens-skill/agents/openai.yaml, assets/xhs/, dist/redskill/ | completed | RedSkill 包内说明已改中文；小红书图基于当前真实 HTML 报告截图生成 |
| 2026-07-09 | 修复可视化认知层 review 反馈 | dl-vibe-lens-skill/scripts/lens_snapshot.py, dl-vibe-lens-skill/assets/report_template.html, tests/test_lens_snapshot.py | completed | 区分整体缺口和解释不足；文件认知标签支持详情页和中英切换 |

## 追问流程专项记录

| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 多个 AI 对话同时改一个项目 | 每个对话可能持有不同上下文 | 并行修改容易冲突 | 展示当前工作和涉及区域，作为中性冲突线索 |
| 第一次安装 Skill | 用户过去需要手动创建记录文件 | 对新手来说启动成本太高 | 提供 `--init`，缺文件时报错也提示初始化 |
| 项目进入中后期 | 问题散在聊天、文档和代码里 | 复盘变难 | 用 Vibe Lens 展示问题、代码差异、方向和证据 |
| Agent 看到旧 `Priority` 字段 | Agent 可能把它当命令 | Skill 会过度影响决策 | 将 priority 当旧元数据展示，区分事实和 Agent 判断 |
| RedSkill 访客打开 GitHub | 需要快速理解和试用 | 长英文文档会劝退中文新手 | 使用中文 README 和快速上手图 |
| Agent 使用过 Vibe Lens | 用户可能想随时回到报告 | 每次贴长链接很丑且打断阅读 | 默认用简约入口，持久行为由 `reply_entry_mode` 控制 |

## 迭代记录

### 2026-07-09: 修复 Vibe Lens 可视化认知层 review 反馈
目标：
- 修复最终 review 发现的可视化认知层残缺。
- 让“解释不足”和“整体信息缺口”分开统计，避免误导阅读。
- 让文件认知标签在主页和详情页保持一致，并支持中英切换。

证据：
- 最终 review 指出：解释不足 fact chip 错用整体缺口、详情页没有文件认知标签、带标签文件行仍是三列布局、英文界面仍显示中文状态。
- 用户要求这些可视化残缺用 DL 记录，后续继续解决。

代码变化：
- `lens_snapshot.py` 为文件认知状态增加稳定 key，并新增 `issues_with_insufficient_explanation`。
- `report_template.html` 用稳定 key 渲染中英标签，主页和文件详情页复用同一个文件行渲染函数。
- `tests/test_lens_snapshot.py` 增加统计分离、状态 key、多语言标签和占位词大小写测试。

验证：
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 通过。
- `git diff --check` 无实际 whitespace 错误，仅有 Windows LF/CRLF 提醒。

未完成：
- 应用内浏览器拦截了新版本地 `file://` 报告地址，因此本轮没有完成浏览器内点击验证；当前由自动化测试和 HTML 生成验证覆盖。

### 2026-07-09: 实现 Vibe Lens 可视化认知层
目标：
- 让现有总览、当前问题、代码差异、证据链和迭代路径共同服务“理解 coding”。
- 使用进度条、圆环、标签和真实路径节点降低信息负担。
- 保持 Vibe Lens 的中性边界：展示事实，不排序任务，不展示 Agent 认知模型。

证据：
- 用户确认：整个 Lens 都用于帮助理解 coding，不应新增削弱其他卡片职责的“理解 Coding”独立卡片。
- 设计文档：`docs/superpowers/specs/2026-07-08-vibe-lens-visual-cognition-design.md`。
- 实施计划：`docs/superpowers/plans/2026-07-09-vibe-lens-visual-cognition.md`。

代码变化：
- `lens_snapshot.py` 增加问题信息完整度、文件认知标签和真实迭代路径节点数据。
- `report_template.html` 展示证据、验证、解释信号，文件认知标签和数据驱动路径图。
- `tests/test_lens_snapshot.py` 增加可视化认知层行为保护。
- README 和记录格式说明补充“问题有证据”的含义。

验证：
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .` 通过。
- `git diff --check` 无实际 whitespace 错误。

未完成：
- 完整交互平台、拖拽编排、复杂分叉路径和 Loop 回放仍不在本阶段范围内。

### 2026-07-03: 中文化 RedSkill 包并生成小红书分步图
目标：
- 将 RedSkill 上传包里的说明改成中文。
- 将本地安装的 `dl-vibe-lens-skill` 也同步成中文说明。
- 基于当前版本 HTML 报告真实截图，生成一整套适合小红书发布的分步功能介绍图。
- 每张图加入 GitHub 仓库地址和求 Star 文案。

证据：
- 用户指出 RedSkill 上传包里仍然是英文说明。
- 用户明确要求不是生成单张小红书首图，而是根据功能介绍文档生成一整套分步介绍图。
- 用户强调图中界面必须是当前版本，不是过去草图。

代码变化：
- 将 `dl-vibe-lens-skill/SKILL.md` 改为中文说明。
- 将 `dl-vibe-lens-skill/agents/openai.yaml` 默认提示词改为中文。
- 同步更新本地安装目录 `C:\Users\23184\.codex\skills\dl-vibe-lens-skill`。
- 重新生成 `dist/redskill/DL-vibe-lens-skill-redskill.zip`。
- 新增 `assets/xhs/01-cover-review-sandbox.png` 到 `assets/xhs/06-quick-start-star.png` 六张小红书分步图。

验证：
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py dl-vibe-lens-skill` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 已重新生成报告。
- `tar -xOf dist\redskill\DL-vibe-lens-skill-redskill.zip SKILL.md` 确认包内说明为中文。
- 已抽查 `assets/xhs/` 中的功能图，确认使用真实 HTML 报告截图、包含 GitHub 地址和求 Star 文案。

未完成：
- 如果要发布到小红书，还需要操作者在小红书后台选择图片并填写正文。

### 2026-07-03: 准备 GitHub 推送和 RedSkill 上传材料
目标：
- 给 RedSkill 上传准备一份中文功能介绍文档。
- 为功能介绍配上当前 HTML 报告界面图。
- 整理一个不含缓存和临时报告的上传包。
- 将整理结果推送到 GitHub。

证据：
- 用户要求“现在推送到 GitHub 上”，并要求“给一个功能介绍文档，配上相应功能的界面图”。
- 用户还要求整理 skill 文件，方便上传到小红书的 RedSkill，并说明上传步骤。

代码变化：
- 新增 `docs/FEATURE_INTRO_ZH.md`，集中放功能介绍、界面图、推荐文案和上传步骤。
- 新增 `assets/feature-*.png` 功能截图。
- 在 `README.md` 增加中文功能介绍入口。
- 生成 `dist/redskill/DL-vibe-lens-skill-redskill.zip` 作为上传包。

验证：
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py dl-vibe-lens-skill` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 已重新生成报告。
- `git diff --check` 没有 whitespace 错误，仅有 Windows LF/CRLF 提醒。
- `http://127.0.0.1:60964/docs/vibe-lens-report.html` 返回 HTTP 200。

未完成：
- RedSkill 网页端上传需要操作者在平台上完成。

### 2026-07-03: 修正总览详情入口
目标：
- 让“当前问题、历史问题、变更文件、代码变化”分别进入对应详情页。
- 让对话入口设置面板在点击空白处时关闭。

证据：
- 用户指出四个总览指标不应该都跳到同一个 `总览详情`。
- 用户要求开启对话入口设置后，点击空白处退出设置。

代码变化：
- 将总览指标目标拆成 `current-detail`、`history-detail`、`files-detail`、`code-detail`。
- 为四个详情页分别填充对应数据。
- 为设置面板增加外部点击关闭逻辑。

验证：
- `python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_contains_confirmed_lens_interface` 通过。
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py dl-vibe-lens-skill` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 已重新生成报告。
- `http://127.0.0.1:60964/docs/vibe-lens-report.html` 返回 HTTP 200。

未完成：
- 无。

### 2026-07-03: 统一 Skill 名为 DL-vibe-lens-skill
目标：
- 把传播名、安装目录、Skill frontmatter 和触发提示词统一到 `DL-vibe-lens-skill` 方向。
- 把本项目的记录和公开文档改成中文默认，避免中文界面展示英文源数据。

证据：
- 用户明确要求 “skill 改为 DL-vibe-lens-skill”。
- 用户确认记录语言应默认跟随当前对话语言。
- Skill 命名规范要求机器名使用小写字母、数字和连字符。

代码变化：
- 将 skill 目录从 `vibe-lens/` 改为 `dl-vibe-lens-skill/`。
- 将 `SKILL.md` frontmatter 改为 `name: dl-vibe-lens-skill`。
- 增加 `docs/vibe-lens-settings.json` 设置设计，默认 `reply_entry_mode: "always"`。
- 调整 HTML 代码差异卡片：圆环、彩色统计和文件列表分区展示。

验证：
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py` 通过。
- `python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py dl-vibe-lens-skill` 通过。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md` 能读取中文示例记录。
- `python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 已重新生成报告。
- `python C:\Users\23184\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .` 验证本地安装的新 skill。
- `git diff --check` 只有 Windows LF-to-CRLF 提醒，没有 whitespace 错误。

未完成：
- 第二阶段完整平台和详细可展开路径图仍放在后续阶段。

### 2026-07-03: 打包 RedSkill 传播版 Skill
目标：
- 完成可用的 `DL-vibe-lens-skill` 包装。
- 把已经确认的 UI 行为从草图迁移到真实 HTML 模板。
- 准备中文公开介绍和快速上手图。
- 把剩余产品问题放进后续优化，不让第一阶段过载。

证据：
- 用户要求为 RedSkill 活动做最终包装。
- 用户确认主页应保留证据看板风格，并把总览、沙盘和迭代路径作为入口。
- 用户要求报告可以选择中文或英文。
- 用户要求 Skill 可以在对话末尾显示简约入口。

代码变化：
- 先增加报告界面测试，再更新 `report_template.html` 直到测试通过。
- 更新 `vibe-lens/SKILL.md` 和 `agents/openai.yaml`，说明初始化、HTML 报告和可选对话入口。
- 将 README 改写为中文公开介绍。
- 在 `assets/quickstart-*.svg` 增加快速上手图。
- 将路线图、发布清单、演示脚本和项目上下文等支持文档改成中文。

验证：
- `python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_contains_confirmed_lens_interface` 通过。
- `python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile vibe-lens\scripts\lens_snapshot.py` 通过。
- `python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py vibe-lens` 通过。
- `python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 生成报告。
- 浏览器验证 `http://127.0.0.1:60961/docs/vibe-lens-report.html`，确认主页模块、详情跳转、英文切换、设置面板和 hash 路由可用。
- `python C:\Users\23184\.codex\skills\vibe-lens\scripts\lens_snapshot.py --project-root .` 验证本地已安装 skill。
- `git diff --check` 只有 LF-to-CRLF 提醒，没有实际 whitespace 错误。
- `git push -u origin codex/vibe-lens-report-ui-spec` 在合并 GitHub connector 提交后成功。
- GitHub 草稿 PR #4 已打开：`https://github.com/sunrise-yc/DL-vibe-lens-skill/pull/4`，GitHub 显示可合并。

未完成：
- 后续阶段再做详细可展开路径图和完整交互平台。

### 2026-07-02: 发布干净的 Vibe Lens PR
目标：
- 接续本地提交后的 GitHub 同步工作。
- 把发布证据保存在 Vibe Lens 源记录里。
- 用基于最新 `main` 的干净 PR 替换旧的混合历史 PR。

证据：
- 本地分支 `codex/vibe-lens-review-sandbox-clean` 跟踪 `origin/codex/vibe-lens-review-sandbox-clean`。
- PR #3 已打开：`https://github.com/sunrise-yc/deeplister-iteration-skill/pull/3`。
- 旧草稿 PR #2 因为混入早期分支历史而关闭。
- PR #3 已标记为 ready for review，GitHub 显示 `mergeable: true`。
- 当时仓库仍使用旧公开名 `deeplister-iteration-skill`。

验证：
- `git push -u origin codex/vibe-lens-review-sandbox-clean` 成功。
- GitHub connector 返回草稿 PR #3，head SHA 为 `c6545cc38628005fac4571cd5dbb84c85343d239`。
- `git merge-base --is-ancestor origin/main HEAD` 确认干净分支基于最新 `origin/main`。
- `git merge-tree $(git merge-base HEAD origin/main) HEAD origin/main` 没有输出冲突。

未完成：
- 当时还需要把 GitHub 仓库改名为 `vibe-lens-skill`。
- 仓库改名后再更新本地 checkout 文件夹和 remote URL。

### 2026-07-02: 重新定位为 Vibe Lens 复盘沙盘
目标：
- 将项目从任务选择转为中性信息展示。
- 将公开方向改名为 `vibe-lens`。
- 增加 Git diff 统计和 HTML 报告生成。

提出的问题：
- 当前有哪些问题，谁提出的？
- 过去提出过哪些问题？
- 解决问题时添加和删除了哪些代码？
- 项目方向发生了什么变化？
- 变化背后有哪些证据和验证？

证据：
- 用户明确说这个 skill 应该是信息展示、复盘界面或沙盘，而不是优先级裁判。
- `git diff --numstat` 在边界明确时能准确提供新增/删除行数。
- `KKKKhazix/khazix-skills` 提供了可参考模式：Skill 触发脚本，脚本生成 HTML 报告或本地服务。

代码变化：
- 将 skill 文件夹改名为 `vibe-lens`。
- 用 `lens_snapshot.py` 替换 `iteration_snapshot.py`。
- 增加静态 HTML 报告生成。
- 增加中性问题展示、Git diff 统计、初始化、旧中文记录兼容和 HTML 报告生成测试。
- 将产品文档改向复盘沙盘定位。

验证：
- 增加新行为测试后，`python -m unittest tests.test_lens_snapshot` 通过。
- `python -m py_compile vibe-lens\scripts\lens_snapshot.py` 通过。
- `python vibe-lens\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md` 能读取示例记录。
- `python vibe-lens\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html` 生成静态 HTML 报告。
- `python vibe-lens\scripts\lens_snapshot.py --project-root .` 能读取本仓库源记录。
- `python C:\Users\23184\.codex\skills\vibe-lens\scripts\lens_snapshot.py --project-root .` 验证本地安装 skill。
- `python C:\Users\23184\.codex\skills\vibe-lens\scripts\lens_snapshot.py --project-root C:\Users\23184\Desktop\DeepLister` 验证 DeepLister 源记录。
- `git diff --check` 只有 LF-to-CRLF 提醒。

未完成：
- 账号工具可用后再重命名 GitHub 仓库和本地 remote。
- 第二阶段交互平台后续再做。

历史说明：
- 下面的条目记录更早的 `deeplister-iteration` 和 `vibe-iteration` 方向，只作为历史保留，不代表当前产品行为。

### 2026-07-01: 将学习点改成中文
目标：
- 让相关工具的学习点更方便杨晨阅读、复盘，并能用于 AI 产品经理思维训练。

完成：
- 将 README 里的相关工具学习点改成中文。
- 将 `docs/RELATED_WORK.md` 改成中文，包含定位、来源、学习点、不足，以及为什么不能手动建文件。
- 将 `PROMOTION_PLAN.md` 里的产品学习闭环改成中文。
- 在这份迭代记录里补充中文大白话说明。

验证：
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root .` 仍能成功读取这份记录。
- `python -m unittest tests.test_iteration_snapshot` 通过。

下一步建议：
- 在另一个 AI 对话开始大范围改动前，继续让 VI-004 保持可见。

### 2026-07-01: 改名为 vibe-iteration 并增加初始化
目标：
- 将 skill 从 DeepLister 专用迭代助手，改成能处理混乱 vibe-coding 项目的轻量工作流。
- 第一次使用时，不再要求用户手动创建记录文件。
- 让本仓库使用自己的迭代记录。

发现的问题：
- 旧公开名让项目看起来太窄。
- 手动搭 Markdown 对目标新手用户来说太脆弱。
- 社交预览图和 snapshot 图片仍带着旧产品语言。
- 本地没有安装 GitHub CLI，所以当时不能在这个环境直接重命名远程仓库。

决策：
- 使用 `vibe-iteration` 作为 skill 名，预期仓库名为 `vibe-iteration-skill`。
- 使用 `docs/iteration-record.md` 作为新默认文件。
- 保留旧 `docs/迭代记录.md` 兼容。
- 增加 `## Active Work`，让并行 AI coding 会话更可见。

完成：
- 将 skill 文件夹和元数据改为 `vibe-iteration`。
- 增加 `--init`，自动生成 `docs/iteration-record.md`。
- 增加英文默认记录、旧中文记录和初始化测试。
- 创建本仓库自己的 `docs/iteration-record.md`。
- 更新 README、路线图、变更记录、发布清单、演示脚本、推广计划、排错文档、项目上下文、Issue 模板、示例记录和图片资产。
- 将新 skill 安装到 `C:\Users\23184\.codex\skills\vibe-iteration`。
- 增加 `docs/RELATED_WORK.md`，记录相邻工具的学习点和不足。
- 复制 DeepLister 现有记录到 `C:\Users\23184\Desktop\DeepLister\docs\iteration-record.md`，让新默认路径读取真实项目任务。

验证：
- `python -m unittest tests.test_iteration_snapshot` 通过。
- `python -m py_compile vibe-iteration\scripts\iteration_snapshot.py` 通过。
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root . --record examples\vibe-iteration-record.example.md` 读取 2 个问题，并推荐 `VI-001`。
- `python vibe-iteration\scripts\iteration_snapshot.py --project-root .` 在本次日志更新前能读取本仓库记录并推荐 `VI-001`。
- 在 `C:\Users\23184\Desktop\DeepLister` 中运行 `python ...\vibe-iteration\scripts\iteration_snapshot.py --project-root .`，从 `docs/iteration-record.md` 读取 9 个问题并推荐 `DL-001`。
- `git diff --check` 只报告 Windows LF-to-CRLF 提醒，没有 whitespace 错误。

未完成：
- 当时远程 GitHub 仓库仍指向 `sunrise-yc/deeplister-iteration-skill`，因为本地没有 `gh`，可用 GitHub connector 也没有 rename 工具。
- 本地 checkout 文件夹仍叫 `deeplister-iteration-skill`，在远程仓库改名前可以接受。
- 旧安装的 `deeplister-iteration` skill 仍保留兼容。

下一步建议：
- 在 GitHub 设置里把仓库名改为 `vibe-iteration-skill`，再更新本地 remote URL。

### 2026-07-01: 初始化 vibe iteration 记录
目标：
- 创建一个共享项目记忆，用来记录任务选择、优先级、当前工作和复盘。

发现的问题：
- 第一次使用时手动搭记录文件有摩擦。

决策：
- 使用 `docs/iteration-record.md` 作为默认记录路径。
- 让文件保持轻量，优先使用 Markdown。

完成：
- 初始化迭代记录。

验证：
- 运行 snapshot 脚本，确认它能读取这份文件。

未完成：
- 将 starter 问题池替换成真实项目任务。

下一步建议：
- 添加最高优先级真实问题作为 `P0`。
