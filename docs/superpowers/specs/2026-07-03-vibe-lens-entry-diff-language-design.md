# DL-vibe-lens-skill 命名、入口、代码差异和记录语言设计

## 背景

Vibe Lens 的定位是给 vibe-coding 项目做复盘沙盘。第一阶段仍然采用“Markdown 作为源记录，HTML 作为展示面”的结构。报告只展示事实，不做优先级判断，也不替操作者安排任务。

这次设计统一处理四个问题：

- skill 公开名、安装目录、触发名和页面产品名没有完全对齐。
- 对话入口被描述成简约快捷入口，但实际回复里没有自动出现；提醒后又暴露了很长的 URL。
- 代码差异文件列表会随着文件增多变长，导致代码差异板块比旁边板块更高。
- 中文界面里仍显示英文问题，因为源记录本身就是英文行。

## 已确认决策

### 0. 命名与调用入口

采用“传播名、机器名、页面名分层”的方案：

- 公开传播名：`DL-vibe-lens-skill`
- Skill 机器名和安装目录：`dl-vibe-lens-skill`
- 调用方式：`$dl-vibe-lens-skill`
- 页面产品名：`Vibe Lens`
- 默认报告文件名：`docs/vibe-lens-report.html`

原因：

- `DL` 来自 DeepLister。这个想法最早是在 DeepLister 项目进入中后期、问题和迭代方向开始变乱时产生的。保留 `DL`，既是来源标记，也方便用户记忆和调取。
- `Vibe Lens` 的含义是：给 vibe coding 过程装上一枚复盘镜头。它不替用户驾驶项目，不排优先级，不安排任务；它只把当前问题、历史问题、代码差异、证据、冲突线索和迭代路径聚焦出来。
- Skill 机器名使用小写 `dl-vibe-lens-skill`，是为了符合 skill 命名规范，避免大小写和特殊字符导致安装或触发不稳定。
- 报告文件名继续保留 `docs/vibe-lens-report.html`，因为它是页面产物，不是 skill 调用名。这样用户看到的页面品牌仍然简洁。

统一定位文案：

> DL-vibe-lens-skill 是一个给 vibe coding 项目使用的复盘沙盘。它像一枚镜头，把散落在对话、文档和代码 diff 里的问题、证据和迭代路径聚焦出来，帮助操作者和 Agent 看清局面，但不替他们排优先级，也不默认安排任务。

命名同步范围：

- Skill 文件夹：`vibe-lens/` 改为 `dl-vibe-lens-skill/`。
- `SKILL.md` frontmatter：`name: dl-vibe-lens-skill`。
- `agents/openai.yaml` 默认提示词：使用 `$dl-vibe-lens-skill`。
- README、安装排错、演示脚本、发布清单、项目上下文、快闪图和测试路径都使用新安装目录。
- 本项目自己的 `docs/iteration-record.md` 记录这次命名决策。

暂不跟随改名：

- HTML 页面品牌仍叫 `Vibe Lens`。
- 默认报告路径仍叫 `docs/vibe-lens-report.html`。
- `localStorage` key 可以暂时保留 `vibe-lens-*`，除非后续需要做迁移。
- 历史设计文档和历史迭代记录里的旧名字可以保留为历史，但当前说明和新用户入口必须使用新名字。

### 1. 对话入口

在已启用 Vibe Lens 的项目里，默认所有 agent 回复末尾都追加一个紧凑的 Markdown 入口：

```markdown
[⌕ Vibe Lens](http://127.0.0.1:<port>/docs/vibe-lens-report.html)
```

如果当前宿主环境对放大镜符号显示不好，使用文字兜底：

```markdown
[Vibe Lens](http://127.0.0.1:<port>/docs/vibe-lens-report.html)
```

入口不能在正文里暴露一整条很长的原始 URL。它应该作为答案末尾单独一行出现，看起来像一个小工具入口，而不是一段粘贴链接。

这里的“所有 agent 回复”有一个技术边界：它指能读取本项目说明、DL-vibe-lens-skill 或项目设置的 agent 回复。不能假设完全无关、没有加载项目上下文的 agent 也会自动遵守。

产品边界必须写清楚：

- 静态 HTML 页面里的 `localStorage` 设置，不能可靠地影响后续 agent 回复。
- 真正能影响 agent 行为的设置，必须来自本轮用户提示词，或者来自 agent 能读取到的项目配置文件。

第一阶段设计：

- 增加一个 agent 可读设置文件，建议路径：`docs/vibe-lens-settings.json`。
- 至少包含 `reply_entry_mode` 和 `record_language`。
- `reply_entry_mode` 默认值为 `"always"`，表示在已启用 Vibe Lens 的项目里，每次 agent 回复末尾都显示简约入口。
- `reply_entry_mode: "when_used"` 表示只有本轮明确使用 Vibe Lens 时才显示入口。
- `reply_entry_mode: "off"` 表示不显示入口。
- Agent 回复前先读取这个设置，再决定是否在回复末尾附带简约入口。
- HTML 设置面板仍然可以保留开关，但它不能误导用户“浏览器里的开关天然控制所有后续回复”。文案要说明：持久化行为由项目设置或明确提示词控制。
- 如果用户说“本轮不要显示 Vibe Lens 入口”，即使项目设置开启，本轮也不显示入口。
- 如果用户说“以后不要显示 Vibe Lens 入口”，agent 应把项目设置改成 `reply_entry_mode: "off"`，或在不能写入设置时明确说明没有持久化。

### 2. 代码差异板块

采用代码差异布局方案 B：

- 圆环放左侧。
- 彩色数字放右侧。
- 绿色表示新增行数。
- 红色表示删除行数。
- 灰色表示变更文件数。
- 文件列表放在圆环和统计数据下方。
- 文件列表内部滚动。
- 整个代码差异板块的初始高度与旁边的“当前问题 / 任务”板块一致。
- 文件再多，也不能撑高外层板块。

这个设计的目标是视觉稳定：主页不能因为本次 diff 文件很多，就突然把代码差异板块撑得比旁边高。

实现约束：

- 主页卡片主体使用固定高度或明确的响应式高度约束。
- 对需要内部滚动的 grid/flex 子元素使用 `min-height: 0`。
- 只在文件列表区域使用 `overflow-y: auto`。
- 保留圆环和文件行的鼠标悬浮说明。
- 不把所有数字都塞进圆环中心，因为数字变长时容易和圆环发生挤压或重叠。

### 3. 记录语言

源记录默认跟随当前对话语言。

规则：

- 如果用户用中文交流，新初始化的记录、新增的问题行、新增的迭代日志默认写中文。
- 如果用户用英文交流，新初始化的记录和新增记录默认写英文。
- 如果用户明确指定记录语言，以用户明确指定为准。
- HTML 报告不能偷偷把源记录里的问题标题或证据机器翻译后展示。
- 中文项目里已有英文行时，必须由 agent 明确执行一次操作：要么翻译并写回源记录，要么生成单独的翻译缓存。

对当前项目来说，优先修复方式是把已有英文问题行翻译成中文并写回 `docs/iteration-record.md`，因为用户已经明确要求项目文档采用中文。

## 用户体验

### 默认回复体验

1. Agent 正常回答当前问题。
2. 如果项目已启用 Vibe Lens，且 `reply_entry_mode` 为 `"always"`，agent 在回复末尾追加一个简约入口。
3. 如果本轮用户明确说不要显示入口，本轮不追加。
4. 如果本地报告 URL 已变化，agent 使用当前可访问的报告 URL，而不是旧链接。

```markdown
[⌕ Vibe Lens](http://127.0.0.1:<port>/docs/vibe-lens-report.html)
```

除非用户明确要求，否则不要在正文里展示原始 localhost 长链接。

### 正常调用 Vibe Lens

1. Agent 通过 `$dl-vibe-lens-skill` 或项目脚本运行 snapshot，读取当前记录和 Git diff。
2. 如果需要视觉展示，agent 生成或刷新 HTML 报告。
3. Agent 给出简短状态摘要。
4. Agent 按 `reply_entry_mode` 决定是否追加简约入口。默认 `"always"` 下应追加。

### 代码差异主页

代码差异卡片一眼看过去应该是：

- 左侧：圆环，表达新增与删除的大致比例。
- 右侧：彩色数字统计。
- 下方：内部可滚动的变更文件列表。

“当前问题 / 任务”和“代码差异”两个卡片在主页初始状态下高度一致。

### 语言行为

如果 UI 是中文，但问题行仍是英文，Vibe Lens 应该把它识别为“源记录语言与当前对话语言不一致”，而不是在 HTML 里偷偷修饰。

下一步 agent 行为应该是明确询问或执行：

- “我检测到记录语言和当前对话语言不一致，要不要把现有英文条目翻译并写回记录？”

当前项目中，用户已经确认：源数据不能在 HTML 中被偷偷翻译。

## 数据流

### Snapshot

`dl-vibe-lens-skill/scripts/lens_snapshot.py` 继续解析 `docs/iteration-record.md` 和 Git diff 数据。

### 设置文件

建议新增设置文件：

```json
{
  "reply_entry_mode": "always",
  "record_language": "auto"
}
```

`reply_entry_mode` 支持三个值：

- `"always"`：默认值。项目启用 Vibe Lens 后，每次 agent 回复末尾都显示简约入口。
- `"when_used"`：只有本轮明确调用或更新 Vibe Lens 时显示入口。
- `"off"`：不显示入口。

`record_language: "auto"` 表示：除非用户明确指定，否则 agent 使用当前对话语言写入新记录。

### HTML 报告

HTML 报告可以展示当前设置状态，但静态 HTML 不能作为后续 agent 回复行为的唯一来源。

如果第一阶段仍然保留静态设置面板，面板文案必须避免暗示“浏览器里的开关直接控制所有后续回复”。它应该说明：持久化行为以项目设置和用户提示词为准。

## 测试

需要增加聚焦测试：

- HTML 报告包含简约入口相关文案，并且不声称浏览器本地状态可以独立控制所有后续回复。
- Skill 校验通过：`SKILL.md` 的 `name` 是 `dl-vibe-lens-skill`。
- README、安装排错、演示脚本、发布清单和 OpenAI 元数据里的触发词是 `$dl-vibe-lens-skill`。
- 测试和验证命令使用 `dl-vibe-lens-skill/scripts/lens_snapshot.py`。
- HTML 报告标题和入口文本仍可显示 `Vibe Lens`。
- 设置文件缺失时，初始化后的默认值是 `reply_entry_mode: "always"`。
- `reply_entry_mode: "always"` 时，普通回复末尾也追加简约入口。
- `reply_entry_mode: "when_used"` 时，只有本轮调用 Vibe Lens 才追加入口。
- `reply_entry_mode: "off"` 时，不追加入口。
- 代码差异卡片包含可滚动的文件列表容器。
- 代码差异统计拆分为新增、删除、文件数三个独立值。
- 初始化记录模板在中文对话/中文配置下使用中文。
- 报告展示源记录内容，不在 HTML 中偷偷翻译已有条目。

手动浏览器检查：

- 当文件列表超过可见区域时，只在文件列表内部滚动。
- 代码差异卡片和当前问题卡片初始高度一致。
- 在桌面和窄屏视口下，圆环与数字统计不重叠。
- 回复末尾的 Vibe Lens 入口看起来像简约工具入口，而不是粘贴的长链接。

## 不在本次范围

- 完整平台模式，即 HTML UI 可以直接写入项目设置。
- 静态报告内自动翻译所有问题行。
- 为每一行问题维护完整中英双字段。
- 第二阶段任务编排或冲突调度。
- 把页面品牌和报告文件名改成 `DL-vibe-lens-skill`。
- 迁移旧 `localStorage` key。

## 实现注意事项

- 改名时先处理安装目录、frontmatter、默认提示词和测试路径，再处理宣传文案。
- 对外文案使用 `DL-vibe-lens-skill`，对用户解释时可以说页面产品名是 `Vibe Lens`。
- 命令、路径和 skill 触发名统一使用小写 `dl-vibe-lens-skill`。
- 如果用户仍使用 `$vibe-lens`，agent 可以提示“新名字是 `$dl-vibe-lens-skill`”，但不要让新文档继续推荐旧名字。
- 如果本地报告 URL 因 HTTP 端口变化而改变，agent 必须使用当前可访问的报告 URL 生成简约入口。
- 如果没有本地服务在运行，agent 应优先启动本地服务或刷新报告；如果不能可靠打开，再退回到本地文件路径。
- 如果缺少 `docs/vibe-lens-settings.json`，初始化 Vibe Lens 时应创建设置文件，并使用 `reply_entry_mode: "always"`。
- 如果暂时拿不到可点击报告地址，agent 不应该把一整条长 URL 硬塞进正文；应先说明报告暂不可用，并给出下一步修复动作。
