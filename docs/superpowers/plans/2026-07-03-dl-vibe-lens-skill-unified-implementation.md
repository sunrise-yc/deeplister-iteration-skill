# DL-vibe-lens-skill Unified Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved unified spec for `DL-vibe-lens-skill`: rename the installable skill, make the reply entry behavior explicit, stabilize the code-diff card, and make new records follow the operator's working language.

**Architecture:** Keep Markdown as the source record and HTML as the display surface. The installable skill directory and frontmatter become `dl-vibe-lens-skill`; the UI brand and report file remain `Vibe Lens` and `docs/vibe-lens-report.html`. The Python snapshot script owns deterministic initialization, settings creation, language-specific record templates, Git diff data, and static HTML generation.

**Tech Stack:** Python standard library, Markdown source records, static HTML/CSS/JS, `unittest`, Codex skill metadata.

---

## File Structure

- Rename: `vibe-lens/` -> `dl-vibe-lens-skill/`
- Modify: `dl-vibe-lens-skill/SKILL.md`
- Modify: `dl-vibe-lens-skill/agents/openai.yaml`
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/assets/report_template.html`
- Modify: `dl-vibe-lens-skill/references/lens-record-format.md`
- Modify: `tests/test_lens_snapshot.py`
- Modify: `README.md`
- Modify: `docs/INSTALLATION_TROUBLESHOOTING.md`
- Modify: `docs/DEMO_SCRIPT.md`
- Modify: `docs/LAUNCH_CHECKLIST.md`
- Modify: `docs/PROJECT_CONTEXT.md`
- Modify: `docs/RELATED_WORK.md`
- Modify: `docs/iteration-record.md`
- Modify: `examples/vibe-lens-record.example.md`
- Modify: `assets/quickstart-01-install.svg`
- Modify: `assets/quickstart-02-init.svg`
- Modify: `CHANGELOG.md`
- Modify: `PROMOTION_PLAN.md`
- Generate: `docs/vibe-lens-report.html`
- Create outside repo after verification: `C:\Users\23184\.codex\skills\dl-vibe-lens-skill`

---

### Task 1: Add Failing Tests For Unified Naming, Settings, Language, And Diff Layout

**Files:**
- Modify: `tests/test_lens_snapshot.py`

- [ ] **Step 1: Update the script path test target**

Change the script constant to the future directory so the suite fails before the rename:

```python
SCRIPT = ROOT / "dl-vibe-lens-skill" / "scripts" / "lens_snapshot.py"
```

- [ ] **Step 2: Add metadata and docs trigger test**

Add this test near the other HTML/interface tests:

```python
    def test_skill_metadata_and_docs_use_dl_trigger(self):
        skill_md = (ROOT / "dl-vibe-lens-skill" / "SKILL.md").read_text(encoding="utf-8")
        openai_yaml = (ROOT / "dl-vibe-lens-skill" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("name: dl-vibe-lens-skill", skill_md)
        self.assertIn("$dl-vibe-lens-skill", openai_yaml)
        self.assertIn("dl-vibe-lens-skill/", readme)
        self.assertIn("$dl-vibe-lens-skill", readme)
        self.assertNotIn("$vibe-lens", readme)
        self.assertNotIn(".codex\\skills\\vibe-lens", readme)
```

- [ ] **Step 3: Add settings and Chinese initialization test**

Add this test after `test_init_creates_lens_record_without_manual_file_setup`:

```python
    def test_init_creates_settings_and_chinese_record_by_default(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(self.tmp), "--init"],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        settings = self.tmp / "docs" / "vibe-lens-settings.json"

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(record.exists())
        self.assertTrue(settings.exists())
        text = record.read_text(encoding="utf-8")
        config = json.loads(settings.read_text(encoding="utf-8"))
        self.assertIn("# Vibe Lens 记录", text)
        self.assertIn("## 问题池", text)
        self.assertIn("## 当前工作", text)
        self.assertIn("## 迭代记录", text)
        self.assertEqual(config["reply_entry_mode"], "always")
        self.assertEqual(config["record_language"], "auto")
```

Also add `import json` at the top of the test file.

- [ ] **Step 4: Add English initialization test**

Add this test to prove the CLI can still create English records when an agent chooses English:

```python
    def test_init_can_create_english_record_when_requested(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(self.tmp),
                "--init",
                "--record-language",
                "en",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        self.assertEqual(result.returncode, 0, result.stderr)
        text = record.read_text(encoding="utf-8")
        self.assertIn("# Vibe Lens Record", text)
        self.assertIn("## Issue Pool", text)
        self.assertIn("## Active Work", text)
        self.assertIn("## Iteration Log", text)
```

- [ ] **Step 5: Add HTML layout and entry behavior assertions**

Extend `test_html_report_contains_confirmed_lens_interface` with:

```python
        self.assertIn("diff-card", html)
        self.assertIn("diff-body", html)
        self.assertIn("diff-file-list", html)
        self.assertIn("reply_entry_mode", html)
        self.assertIn("默认每轮回复末尾显示入口", html)
```

- [ ] **Step 6: Run tests and verify RED**

Run:

```powershell
python -m unittest tests.test_lens_snapshot
```

Expected: fail because `dl-vibe-lens-skill/scripts/lens_snapshot.py` and the new settings/layout behaviors do not exist yet.

---

### Task 2: Rename The Installable Skill And Metadata

**Files:**
- Rename: `vibe-lens/` -> `dl-vibe-lens-skill/`
- Modify: `dl-vibe-lens-skill/SKILL.md`
- Modify: `dl-vibe-lens-skill/agents/openai.yaml`

- [ ] **Step 1: Rename the directory**

Run:

```powershell
git mv vibe-lens dl-vibe-lens-skill
```

- [ ] **Step 2: Update SKILL.md frontmatter and overview**

In `dl-vibe-lens-skill/SKILL.md`, set:

```markdown
---
name: dl-vibe-lens-skill
description: Use when a vibe-coding project needs a review sandbox, retrospective, issue history view, Git diff visualization, iteration direction map, evidence trail, verification trail, or neutral conflict signals across AI coding sessions.
---

# DL Vibe Lens Skill
```

Replace the overview paragraph with:

```markdown
Turn a messy vibe-coding project into a neutral review sandbox. `DL` points back to DeepLister, where this workflow started. `Vibe Lens` means a lens over vibe coding: it focuses scattered questions, Git diff statistics, iteration path, evidence, verification, and conflict signals so the operator and Agent can see the situation clearly. It does not rank tasks, assign weights, or decide what the operator must do next.
```

- [ ] **Step 3: Update command examples in SKILL.md**

Replace every installed path:

```text
$env:USERPROFILE\.codex\skills\vibe-lens\scripts\lens_snapshot.py
```

with:

```text
$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py
```

- [ ] **Step 4: Update reply-entry guidance in SKILL.md**

Replace the HTML report bullet about conversation entry with:

```markdown
- Include the conversation-entry setting panel. In a project that has enabled DL Vibe Lens, the default mode appends a compact `Open Vibe Lens` entry at the end of every Agent reply. If the operator says "do not show the Vibe Lens entry this turn", do not append it for that turn. If the operator disables it persistently, respect the project setting.
```

Replace the common mistake row:

```markdown
| Showing a long raw report URL in replies | Use a compact Markdown entry such as `Open Vibe Lens` |
```

- [ ] **Step 5: Update OpenAI agent metadata**

Set `dl-vibe-lens-skill/agents/openai.yaml` to:

```yaml
interface:
  display_name: "DL Vibe Lens"
  short_description: "复盘沙盘：问题、代码差异、证据和路径"
  default_prompt: "Use $dl-vibe-lens-skill to initialize or inspect this project, generate the visual sandbox, and show questions, Git diff, evidence, conflict signals, and iteration path without ranking tasks."
```

- [ ] **Step 6: Run targeted RED/GREEN check**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_skill_metadata_and_docs_use_dl_trigger
```

Expected after this task: it still fails on README until Task 5 updates public docs.

---

### Task 3: Implement Settings File And Record Language Support

**Files:**
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/references/lens-record-format.md`

- [ ] **Step 1: Add settings constants**

Near the existing defaults in `lens_snapshot.py`, add:

```python
DEFAULT_SETTINGS = Path("docs") / "vibe-lens-settings.json"
DEFAULT_SETTINGS_DATA = {
    "reply_entry_mode": "always",
    "record_language": "auto",
}
```

- [ ] **Step 2: Add settings writer**

Add this helper near `resolve_record`:

```python
def ensure_settings(project_root: Path) -> Path:
    settings = project_root / DEFAULT_SETTINGS
    settings.parent.mkdir(parents=True, exist_ok=True)
    if not settings.exists():
        settings.write_text(
            json.dumps(DEFAULT_SETTINGS_DATA, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return settings
```

- [ ] **Step 3: Split record templates by language**

Rename the current `record_template` body to `record_template_zh` and make its headings Chinese:

```python
def record_template_zh(today: date | None = None) -> str:
    current_date = (today or date.today()).isoformat()
    return f"""# Vibe Lens 记录

这是 Vibe Lens 的数据源文件。
脚本会把这里的记录和 Git diff 数据合在一起，生成一个可视化复盘沙盘。

大白话：这里不是任务裁判，不替你排优先级；它负责把当前问题、历史问题、代码差异、证据和迭代路径展示出来。

## 保护说明

- 不要改名这些标题：`## 问题池`、`## 当前工作`、`## 追问流程专项记录`、`## 迭代记录`。
- 不要把 `## 问题池` 里的表格搬到别的地方。
- 不要只根据这个文件给问题排序，`优先级` 只能当旧字段展示。
- 你可以改表格内容、增加行、增加自己的说明段落。

## 当前产品方向

- 定位：给中后期开始变乱的 vibe-coding 项目做复盘沙盘。
- 使用者：独立开发者、代码新手、正在学习 AI 产品经理的人，以及使用 AI coding agent 的人。
- 当前重点：展示信息，不安排任务，不施加权重。

## 问题池

| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-001 | 第一个需要复盘的问题 | operator | open | 把这一行替换成真实问题 | docs/iteration-record.md |

## 当前工作

| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| {current_date} | 初始化 Vibe Lens 记录 | docs/iteration-record.md | in progress | 第一次真实工作完成后，可以替换这一行 |

## 追问流程专项记录

| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 多个 AI 对话同时改一个项目 | 每个对话可能持有不同上下文 | 并行修改容易冲突 | 把活跃工作和涉及区域作为中性线索展示 |

## 迭代记录

### {current_date}: 初始化 Vibe Lens 记录
目标：
- 创建能喂给可视化复盘沙盘的数据源文件。

发现的问题：
- 手动建文件对第一次使用的人来说太麻烦。

决策：
- 使用 `docs/iteration-record.md` 作为默认输入记录。
- Markdown 只作为数据源，最终展示面是 HTML 报告。

完成：
- 初始化 Vibe Lens 记录。

验证：
- 运行 lens snapshot 脚本，确认它能读这个文件。

未完成：
- 把示例行替换成当前项目真实的问题和证据。
"""
```

Create an English template by moving the current English-heading template to:

```python
def record_template_en(today: date | None = None) -> str:
    current_date = (today or date.today()).isoformat()
    return f"""# Vibe Lens Record
...
"""
```

The English template can keep the current English headings and English field names.

- [ ] **Step 4: Add record_template dispatcher**

Add:

```python
def record_template(today: date | None = None, record_language: str = "zh") -> str:
    if record_language == "en":
        return record_template_en(today)
    return record_template_zh(today)
```

- [ ] **Step 5: Add CLI argument**

Add to `main()` parser:

```python
    parser.add_argument(
        "--record-language",
        choices=["auto", "zh", "en"],
        default="auto",
        help="Language for --init record template; auto defaults to zh for CLI use",
    )
```

- [ ] **Step 6: Use language and settings during init**

Change the init block to:

```python
    if args.init:
        record = resolve_record(project_root, Path(args.record) if args.record else None)
        record.parent.mkdir(parents=True, exist_ok=True)
        if record.exists() and not args.force:
            print(f"Record already exists: {record}")
        else:
            language = "zh" if args.record_language == "auto" else args.record_language
            record.write_text(record_template(record_language=language), encoding="utf-8")
            print(f"Initialized Vibe Lens record: {record}")
        settings = ensure_settings(project_root)
        print(f"Initialized Vibe Lens settings: {settings}")
        return 0
```

If the existing init block does not return an exit code, keep the existing function shape and only preserve equivalent behavior.

- [ ] **Step 7: Include settings in snapshot**

In `build_snapshot`, add:

```python
    settings_path = project_root / DEFAULT_SETTINGS
    settings = DEFAULT_SETTINGS_DATA.copy()
    if settings_path.exists():
        settings.update(json.loads(settings_path.read_text(encoding="utf-8")))
```

and include:

```python
        "settings": settings,
```

- [ ] **Step 8: Update record format reference**

In `dl-vibe-lens-skill/references/lens-record-format.md`, add a short language section:

```markdown
## Record Language

New records should follow the current conversation language. Agents should call `--record-language zh` in Chinese conversations and `--record-language en` in English conversations. Existing English rows must not be silently translated by the HTML report; translate and write back only when the operator explicitly asks.
```

- [ ] **Step 9: Run language tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_init_creates_settings_and_chinese_record_by_default
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_init_can_create_english_record_when_requested
```

Expected: both pass.

---

### Task 4: Update HTML Report Entry Copy And Code-Diff Layout

**Files:**
- Modify: `dl-vibe-lens-skill/assets/report_template.html`

- [ ] **Step 1: Add fixed-height diff card classes**

Change the code diff card wrapper to include:

```html
<div class="card diff-card">
```

Change the inner diff markup so the donut and stats live in a two-column body and the file list scrolls below:

```html
<div class="diff-body">
  <div class="big-donut" id="diffDonut">
    <strong id="diffDonutText"></strong>
  </div>
  <div class="diff-stats" id="diffStats"></div>
</div>
<div class="diff-file-list" id="diffFiles"></div>
```

- [ ] **Step 2: Add CSS for stable layout**

Add CSS near existing `.big-donut` and `.file-row` rules:

```css
    .diff-card {
      height: 326px;
      display: flex;
      flex-direction: column;
      min-height: 0;
    }

    .diff-body {
      display: grid;
      grid-template-columns: 176px 1fr;
      gap: 14px;
      align-items: center;
      min-height: 186px;
      flex: 0 0 auto;
    }

    .diff-card .big-donut { margin: 0; }

    .diff-stats {
      display: grid;
      gap: 8px;
      min-width: 0;
    }

    .diff-stat {
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      background: #f8fafc;
      padding: 8px 10px;
      font-size: 12px;
    }

    .diff-stat strong {
      display: block;
      font-size: 18px;
      line-height: 1.1;
    }

    .diff-stat.added strong { color: var(--green); }
    .diff-stat.deleted strong { color: var(--red); }
    .diff-stat.files strong { color: var(--muted); }

    .diff-file-list {
      min-height: 0;
      overflow-y: auto;
      padding-right: 4px;
      scrollbar-width: thin;
      scrollbar-color: rgba(100,116,139,.34) transparent;
    }
```

- [ ] **Step 3: Render colored diff stats outside the donut**

In `renderDiff()`, after setting `diffDonutText`, add:

```javascript
      byId("diffStats").innerHTML = `
        <div class="diff-stat added"><span>${esc(t("addedLines"))}</span><strong>+${esc(diff.total_added || 0)}</strong></div>
        <div class="diff-stat deleted"><span>${esc(t("deletedLines"))}</span><strong>-${esc(diff.total_deleted || 0)}</strong></div>
        <div class="diff-stat files"><span>${esc(t("changedFiles"))}</span><strong>${esc(diff.changed_file_count || 0)}</strong></div>
      `;
```

Change the file slice from:

```javascript
const files = (diff.files || []).slice(0, 6);
```

to:

```javascript
const files = diff.files || [];
```

- [ ] **Step 4: Add i18n labels**

Add to `labels.zh`:

```javascript
        addedLines: "新增行",
        deletedLines: "删除行",
```

Add to `labels.en`:

```javascript
        addedLines: "Added lines",
        deletedLines: "Deleted lines",
```

- [ ] **Step 5: Update entry setting copy**

Change Chinese `entryIntro` to:

```javascript
entryIntro: "默认每轮回复末尾显示入口，方便随时打开复盘沙盘。也可以在提示词里说“本轮不要显示 Vibe Lens 入口”临时关闭，或在项目设置里改为只在使用时显示/关闭。",
```

Change English `entryIntro` to:

```javascript
entryIntro: "By default, enabled projects show a compact entry at the end of every agent reply. The user can also say “do not show the Vibe Lens entry this turn,” or change the project setting to when-used/off.",
```

- [ ] **Step 6: Run HTML interface test**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_contains_confirmed_lens_interface
```

Expected: pass.

---

### Task 5: Update Public Docs, Examples, Assets, And Project Record

**Files:**
- Modify: `README.md`
- Modify: `docs/INSTALLATION_TROUBLESHOOTING.md`
- Modify: `docs/DEMO_SCRIPT.md`
- Modify: `docs/LAUNCH_CHECKLIST.md`
- Modify: `docs/PROJECT_CONTEXT.md`
- Modify: `docs/RELATED_WORK.md`
- Modify: `docs/iteration-record.md`
- Modify: `examples/vibe-lens-record.example.md`
- Modify: `assets/quickstart-01-install.svg`
- Modify: `assets/quickstart-02-init.svg`
- Modify: `CHANGELOG.md`
- Modify: `PROMOTION_PLAN.md`

- [ ] **Step 1: Update README name explanation**

In `README.md`, replace the opening behavior paragraph with:

```markdown
当 vibe coding 项目进入中后期，问题会散在聊天、文档、代码 diff 和半成品想法里；如果同时开多个 AI coding 对话，还可能出现文件重叠、方向不一致、上下文互相打架。`DL-vibe-lens-skill` 做的事很克制：把这些信息展示出来，让操作者和 Agent 看清局面。

`DL` 来自 DeepLister：这个想法最早是在 DeepLister 项目推进到中后期、问题开始堆叠时长出来的。保留 `DL`，既是来源标记，也方便记忆和调取。

`Vibe Lens` 顾名思义，就是给 vibe coding 过程装上一枚复盘镜头：它不替你驾驶项目，而是把当前问题、历史问题、代码差异、证据和迭代路径聚焦出来，让人和 Agent 都能看清“现在局面长什么样”。
```

- [ ] **Step 2: Replace public install and trigger paths**

Across current public docs, replace:

```text
vibe-lens/
```

with:

```text
dl-vibe-lens-skill/
```

Replace:

```text
$vibe-lens
```

with:

```text
$dl-vibe-lens-skill
```

Replace installed paths:

```text
.codex\skills\vibe-lens
~/.codex/skills/vibe-lens
```

with:

```text
.codex\skills\dl-vibe-lens-skill
~/.codex/skills/dl-vibe-lens-skill
```

- [ ] **Step 3: Keep report/product names unchanged**

Do not replace these:

```text
Vibe Lens
docs/vibe-lens-report.html
vibe-lens-language
vibe-lens-entry-enabled
```

- [ ] **Step 4: Update project record with a new Chinese entry**

In `docs/iteration-record.md`, add a new row:

```markdown
| VL-010 | 统一 skill 名为 DL-vibe-lens-skill | operator | resolved | 用户希望保留 DeepLister 来源，并让调用名更好记 | README.md, dl-vibe-lens-skill/SKILL.md, docs/ |
```

Add a new active work row:

```markdown
| 2026-07-03 | 统一 skill 命名 | dl-vibe-lens-skill/, README.md, docs/, examples/, assets/, tests/ | completed | 展示名保留 `DL-vibe-lens-skill`，实际 skill 机器名用规范小写 `dl-vibe-lens-skill` |
```

Add a new iteration heading:

```markdown
### 2026-07-03: 统一 Skill 名为 DL-vibe-lens-skill
Goal:
- 把传播名、安装目录、Skill frontmatter 和触发提示词统一到 `DL-vibe-lens-skill` 方向。

Evidence:
- 用户明确要求 “skill 改为 DL-vibe-lens-skill”。
- Skill 命名规范要求机器名使用小写字母、数字和连字符。

Code Changes:
- 将 skill 目录从 `vibe-lens/` 改为 `dl-vibe-lens-skill/`。
- 将 `SKILL.md` frontmatter 改为 `name: dl-vibe-lens-skill`。

Verification:
- 待运行。

Unfinished:
- 将本地已安装 skill 同步到 `C:\Users\23184\.codex\skills\dl-vibe-lens-skill`。
```

- [ ] **Step 5: Update SVG text**

In `assets/quickstart-01-install.svg`, update visible text to `dl-vibe-lens-skill`.

In `assets/quickstart-02-init.svg`, update the command path to:

```text
$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py
```

- [ ] **Step 6: Run docs trigger test**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_skill_metadata_and_docs_use_dl_trigger
```

Expected: pass.

---

### Task 6: Validate, Regenerate Report, And Sync Installed Skill

**Files:**
- Generate: `docs/vibe-lens-report.html`
- Create outside repo: `C:\Users\23184\.codex\skills\dl-vibe-lens-skill`

- [ ] **Step 1: Run full unit tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot
```

Expected: all tests pass.

- [ ] **Step 2: Compile the script**

Run:

```powershell
python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py
```

Expected: no output and exit code 0.

- [ ] **Step 3: Validate skill structure with UTF-8 mode**

Run:

```powershell
python -X utf8 C:\Users\23184\.codex\skills\.system\skill-creator\scripts\quick_validate.py dl-vibe-lens-skill
```

Expected: validation succeeds. UTF-8 mode is required on this Windows setup because the skill contains Chinese text.

- [ ] **Step 4: Regenerate the HTML report**

Run:

```powershell
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
```

Expected: `docs/vibe-lens-report.html` is regenerated and still uses the `Vibe Lens` page brand.

- [ ] **Step 5: Run the snapshot on the example record**

Run:

```powershell
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
```

Expected: command prints issue counts and no recommended next task.

- [ ] **Step 6: Sync the installed local skill**

Create or replace the installed new-name skill folder:

```powershell
$source = Resolve-Path "dl-vibe-lens-skill"
$target = Join-Path $env:USERPROFILE ".codex\skills\dl-vibe-lens-skill"
if (Test-Path $target) { Remove-Item -LiteralPath $target -Recurse -Force }
Copy-Item -LiteralPath $source -Destination $target -Recurse
```

Do not delete the old installed `C:\Users\23184\.codex\skills\vibe-lens` folder in this task; leaving it avoids breaking old chats while the new trigger is adopted.

- [ ] **Step 7: Verify installed new-name skill**

Run:

```powershell
python "$env:USERPROFILE\.codex\skills\dl-vibe-lens-skill\scripts\lens_snapshot.py" --project-root .
```

Expected: command reads this repository's `docs/iteration-record.md`.

- [ ] **Step 8: Check whitespace and status**

Run:

```powershell
git diff --check
git status -sb
```

Expected: `git diff --check` exits 0. `git status -sb` shows only intended files.

- [ ] **Step 9: Commit implementation**

Run:

```powershell
git add .
git commit -m "Rename skill to dl-vibe-lens-skill"
```

Expected: commit succeeds on branch `codex/vibe-lens-report-ui-spec`.

---

## Plan Self-Review

- Spec coverage: naming, reply entry default, code-diff layout, record language, tests, and installation sync are covered by Tasks 1-6.
- Scope: the plan does not implement the second-stage platform, translation cache, localStorage migration, or report brand rename because the spec excludes them.
- Type and path consistency: implementation paths use `dl-vibe-lens-skill`; product/report names remain `Vibe Lens` and `docs/vibe-lens-report.html`.
- TDD order: behavior tests are written before directory rename, settings implementation, language support, and HTML layout changes.
