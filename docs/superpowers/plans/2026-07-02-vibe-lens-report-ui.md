# Vibe Lens Report UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved Vibe Lens HTML report UI: bilingual evidence-board layout, donut diff visuals, evidence meters, compact tooltips, and neutral review-sandbox language.

**Architecture:** Keep snapshot generation deterministic in Python and keep the report as a static HTML file with embedded JSON. The Python script should provide factual data only; the HTML template should handle presentation, language switching, charts, meters, and hover/focus interactions. The UI must not rank, score, or schedule tasks.

**Tech Stack:** Python 3 standard library, Git CLI, static HTML/CSS/JavaScript, `unittest`.

---

## File Map

- Modify `tests/test_lens_snapshot.py`: add report UI contract tests before changing the template.
- Modify `vibe-lens/assets/report_template.html`: replace the current basic report with the approved evidence-board UI, bilingual strings, donut charts, evidence meters, and bounded tooltips.
- Do not modify `vibe-lens/scripts/lens_snapshot.py` in this plan. The current snapshot already carries the factual fields needed by the approved UI.
- Do not modify `README.md` in this plan. It already documents the HTML report command.
- Do not modify `.superpowers/brainstorm/**`: those files are visual-session scratch assets and are ignored.

## Data Contract

The HTML template receives the existing `snapshot` object embedded as `const data = __LENS_DATA__;`.

The implementation may use these existing factual fields:

- `data.generated_at`
- `data.record`
- `data.issue_count`
- `data.open_question_count`
- `data.issues`
- `data.open_questions`
- `data.iteration_direction.headings`
- `data.iteration_direction.current_direction`
- `data.latest_iteration`
- `data.follow_up_case_count`
- `data.conflict_signals`
- `data.git_diff.total_added`
- `data.git_diff.total_deleted`
- `data.git_diff.changed_file_count`
- `data.git_diff.files`
- `data.git_diff.untracked_files`
- `data.git_diff.range`

The implementation must not add or render these fields:

- `recommended_next`
- `priority_score`
- `rank`
- `weight`
- `schedule_order`

## Task 1: Add Failing UI Contract Tests

**Files:**
- Modify: `tests/test_lens_snapshot.py`

- [ ] **Step 1: Add a test for the approved report UI shell**

Add this method to `LensSnapshotTest` after `test_generates_static_html_report`:

```python
    def test_html_report_contains_approved_ui_contract(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Source | Status | Evidence | Related Files |
|---|---|---|---|---|---|
| VL-001 | Render evidence board | operator | open | PR merged | vibe-lens/assets/report_template.html |

## Follow-up Flow Notes
| Scenario | Current Behavior | Issue | Improvement |
|---|---|---|---|
| Parallel chats | Context can drift | Conflicts are likely | Show neutral signals |

## Iteration Log
### 2026-07-02: HTML report UI
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)
        html = output.read_text(encoding="utf-8")

        required_fragments = [
            'id="languageToggle"',
            'data-i18n="section.currentQuestions"',
            'data-i18n="section.codeDiff"',
            'data-i18n="section.iterationDirection"',
            'data-i18n="section.evidenceChain"',
            'class="lens-donut"',
            'class="lens-mini-donut"',
            'class="lens-evidence-meter"',
            'class="lens-tooltip"',
            "function placeTooltip",
            "证据完整度条",
            "Evidence meter",
            "does not rank",
        ]

        for fragment in required_fragments:
            self.assertIn(fragment, html)
```

- [ ] **Step 2: Add a test that the report does not expose ranking fields**

Add this method after the UI shell test:

```python
    def test_html_report_keeps_review_sandbox_neutral(self):
        self.write_record(
            """# Vibe Lens Record

## Issue Pool
| ID | Issue | Impact | Priority | Status | Next Step |
|---|---|---|---|---|---|
| VL-001 | Keep report neutral | Avoid accidental task steering | P0 | open | Show facts only |

## Iteration Log
### 2026-07-02: Neutral report
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "neutral-report.html"
        lens_snapshot.write_html_report(snapshot, output)
        html = output.read_text(encoding="utf-8")

        forbidden_fragments = [
            "recommended_next",
            "priority_score",
            "schedule_order",
            "highest priority",
            "do this first",
        ]

        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, html)
```

- [ ] **Step 3: Run the focused tests and confirm they fail**

Run:

```powershell
python -m unittest tests.test_lens_snapshot -v
```

Expected result before implementation:

```text
FAIL: test_html_report_contains_approved_ui_contract
```

The existing report template does not yet contain the approved UI contract.

- [ ] **Step 4: Commit the failing tests**

Run:

```powershell
git add tests/test_lens_snapshot.py
git commit -m "test: define Vibe Lens report UI contract"
```

## Task 2: Build the Bilingual Evidence-Board Shell

**Files:**
- Modify: `vibe-lens/assets/report_template.html`
- Test: `tests/test_lens_snapshot.py`

- [ ] **Step 1: Replace the header and layout skeleton**

In `vibe-lens/assets/report_template.html`, keep `const data = __LENS_DATA__;` and replace the visible page structure with this shell:

```html
<body>
  <header class="lens-header">
    <div>
      <h1>Vibe Lens</h1>
      <p data-i18n="product.tagline">Review sandbox: shows facts, evidence, code changes, direction, and conflict signals; does not rank or arrange tasks.</p>
      <div class="lens-meta" id="meta"></div>
    </div>
    <div class="lens-language" id="languageToggle" role="group" aria-label="Language">
      <button type="button" data-lang="zh">中文</button>
      <button type="button" data-lang="en">English</button>
    </div>
  </header>

  <main class="lens-main">
    <section class="lens-grid lens-overview" id="overview"></section>

    <section class="lens-card">
      <h2 class="tooltip-trigger" tabindex="0" data-i18n="section.legend">
        Legend / Hover for meaning
        <span class="lens-help">?</span>
        <span class="lens-tooltip" data-tip="tip.legend"></span>
      </h2>
      <div class="lens-legend" id="legend"></div>
    </section>

    <section class="lens-two">
      <div class="lens-card">
        <h2 class="tooltip-trigger" tabindex="0" data-i18n="section.currentQuestions">
          Current Questions / Tasks
          <span class="lens-help">?</span>
          <span class="lens-tooltip" data-tip="tip.currentQuestions"></span>
        </h2>
        <div id="currentQuestions" class="lens-list"></div>
      </div>
      <div class="lens-card">
        <h2 class="tooltip-trigger edge-right" tabindex="0" data-i18n="section.codeDiff">
          Code Diff / 代码差异
          <span class="lens-help">?</span>
          <span class="lens-tooltip" data-tip="tip.codeDiff"></span>
        </h2>
        <div id="diffSummary"></div>
        <div id="diffFiles"></div>
      </div>
    </section>

    <section class="lens-two">
      <div class="lens-card">
        <h2 class="tooltip-trigger" tabindex="0" data-i18n="section.iterationDirection">
          Iteration Direction
          <span class="lens-help">?</span>
          <span class="lens-tooltip" data-tip="tip.iterationDirection"></span>
        </h2>
        <div id="direction"></div>
      </div>
      <div class="lens-card">
        <h2 class="tooltip-trigger edge-right" tabindex="0" data-i18n="section.evidenceChain">
          Evidence Chain / Conflict Signals
          <span class="lens-help">?</span>
          <span class="lens-tooltip" data-tip="tip.evidenceChain"></span>
        </h2>
        <div id="evidence"></div>
      </div>
    </section>

    <section class="lens-card">
      <h2 data-i18n="section.historicalQuestions">Historical Questions</h2>
      <div id="historicalQuestions"></div>
    </section>
  </main>
</body>
```

- [ ] **Step 2: Add bilingual strings**

Add this JavaScript object above `render()`:

```javascript
const i18n = {
  zh: {
    "product.tagline": "复盘沙盘：展示事实、证据、代码变化、迭代方向和冲突线索；不排序、不调度、不加权重。",
    "section.legend": "图例 / 鼠标悬浮可解释含义",
    "section.currentQuestions": "当前问题 / 任务",
    "section.codeDiff": "Code Diff / 代码差异",
    "section.iterationDirection": "迭代方向",
    "section.evidenceChain": "证据链 / 冲突线索",
    "section.historicalQuestions": "历史问题",
    "metric.totalQuestions": "问题总数",
    "metric.openQuestions": "当前问题",
    "metric.changedFiles": "变更文件",
    "metric.codeChurn": "代码变化",
    "legend.recorded": "问题已记录",
    "legend.evidence": "证据",
    "legend.relatedCode": "关联代码",
    "legend.missing": "待补充",
    "label.evidenceMeter": "证据完整度条",
    "tip.legend": "说明颜色和标记代表的资料类型。它不代表优先级、权重或任务顺序。",
    "tip.currentQuestions": "展示当前仍未关闭的问题。顺序来自记录，不自动排序，不代表优先级。",
    "tip.codeDiff": "来自 Git diff 的事实统计。绿色是新增行，红色是删除行；不评价改动好坏。",
    "tip.iterationDirection": "来自迭代记录中的阶段标题和产品方向，用来回看项目怎么变化，不自动安排下一步。",
    "tip.evidenceChain": "证据链解释结论从哪里来；冲突线索提示多个会话或文件区域是否重叠。它只提示，不调度。",
    "empty.currentQuestions": "没有记录中的当前问题。",
    "empty.historicalQuestions": "没有历史问题记录。",
    "empty.direction": "没有迭代方向记录。",
    "empty.diff": "所选 Git 范围内没有已跟踪文件差异。"
  },
  en: {
    "product.tagline": "Review sandbox: shows facts, evidence, code changes, direction, and conflict signals; does not rank or arrange tasks.",
    "section.legend": "Legend / Hover for meaning",
    "section.currentQuestions": "Current Questions / Tasks",
    "section.codeDiff": "Code Diff",
    "section.iterationDirection": "Iteration Direction",
    "section.evidenceChain": "Evidence Chain / Conflict Signals",
    "section.historicalQuestions": "Historical Questions",
    "metric.totalQuestions": "Total questions",
    "metric.openQuestions": "Current questions",
    "metric.changedFiles": "Changed files",
    "metric.codeChurn": "Code churn",
    "legend.recorded": "Recorded",
    "legend.evidence": "Evidence",
    "legend.relatedCode": "Related code",
    "legend.missing": "Missing",
    "label.evidenceMeter": "Evidence meter",
    "tip.legend": "Explains what colors and markers mean. It does not represent priority, weight, or task order.",
    "tip.currentQuestions": "Shows questions that are still open. Order comes from the record; it is not automatic priority.",
    "tip.codeDiff": "Facts from Git diff. Green means added lines, red means deleted lines; this does not judge quality.",
    "tip.iterationDirection": "Shows direction from iteration headings and product notes. It does not arrange next steps.",
    "tip.evidenceChain": "Shows where conclusions come from and whether sessions or file areas overlap. It only signals.",
    "empty.currentQuestions": "No current questions recorded.",
    "empty.historicalQuestions": "No historical questions recorded.",
    "empty.direction": "No iteration direction entries recorded.",
    "empty.diff": "No tracked file diff in the selected Git range."
  }
};

let currentLang = "zh";
const t = (key) => i18n[currentLang][key] || i18n.en[key] || key;
```

- [ ] **Step 3: Add language switching**

Add this function and call it from `render()`:

```javascript
function applyLanguage() {
  document.documentElement.lang = currentLang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.childNodes[0].textContent = t(node.dataset.i18n) + " ";
  });
  document.querySelectorAll("[data-tip]").forEach((node) => {
    node.textContent = t(node.dataset.tip);
  });
  document.querySelectorAll("#languageToggle button").forEach((button) => {
    const active = button.dataset.lang === currentLang;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

document.querySelectorAll("#languageToggle button").forEach((button) => {
  button.addEventListener("click", () => {
    currentLang = button.dataset.lang;
    render();
  });
});
```

- [ ] **Step 4: Run the contract test**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_contains_approved_ui_contract -v
```

Expected result after this task:

```text
ok
```

- [ ] **Step 5: Commit the shell**

Run:

```powershell
git add vibe-lens/assets/report_template.html
git commit -m "feat: add bilingual Vibe Lens report shell"
```

## Task 3: Implement Donuts, Evidence Meters, and Neutral Rendering

**Files:**
- Modify: `vibe-lens/assets/report_template.html`
- Test: `tests/test_lens_snapshot.py`

- [ ] **Step 1: Add chart and meter CSS**

Add these CSS rules to the report template:

```css
.lens-donut,
.lens-mini-donut {
  border-radius: 50%;
  background: conic-gradient(var(--green) 0 var(--added-pct), var(--red) var(--added-pct) 100%);
  position: relative;
  flex: 0 0 auto;
}
.lens-donut { width: 138px; height: 138px; margin: 8px auto 10px; }
.lens-mini-donut { width: 44px; height: 44px; }
.lens-donut::after,
.lens-mini-donut::after {
  content: "";
  position: absolute;
  border-radius: 50%;
  background: var(--card);
}
.lens-donut::after { inset: 24px; }
.lens-mini-donut::after { inset: 11px; }
.lens-mini-donut.empty {
  background: conic-gradient(#cbd5e1 0 100%);
}
.lens-evidence-meter {
  height: 9px;
  border: 1px solid #d7dee9;
  border-radius: 999px;
  background: #e7edf5;
  overflow: hidden;
}
.lens-evidence-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--blue) 0 34%, var(--green) 34% 76%, var(--orange) 76% 100%);
}
```

- [ ] **Step 2: Add factual helpers for percentages and evidence**

Add these JavaScript helpers:

```javascript
function percent(part, total) {
  if (!total) return 0;
  return Math.round((part / total) * 1000) / 10;
}

function diffParts(diff) {
  const added = Number(diff?.total_added || 0);
  const deleted = Number(diff?.total_deleted || 0);
  const total = Math.max(added + deleted, 1);
  return {
    added,
    deleted,
    files: Number(diff?.changed_file_count || 0),
    addedPct: percent(added, total),
    deletedPct: percent(deleted, total)
  };
}

function issueDiffParts(row) {
  const filesText = field(row, ["Related Files", "Files Or Areas", "关联文件", "涉及文件"], "");
  if (!filesText) {
    return { added: 0, deleted: 0, files: 0, addedPct: 0, deletedPct: 0, mapped: false };
  }
  const related = filesText.split(/[,，;]/).map((part) => part.trim()).filter(Boolean);
  const diffFiles = data.git_diff?.files || [];
  const matched = diffFiles.filter((file) => related.some((part) => file.path.includes(part) || part.includes(file.path)));
  const added = matched.reduce((sum, file) => sum + Number(file.added || 0), 0);
  const deleted = matched.reduce((sum, file) => sum + Number(file.deleted || 0), 0);
  const total = Math.max(added + deleted, 1);
  return {
    added,
    deleted,
    files: matched.length,
    addedPct: matched.length ? percent(added, total) : 0,
    deletedPct: matched.length ? percent(deleted, total) : 0,
    mapped: matched.length > 0
  };
}

function evidenceParts(row) {
  const recorded = 1;
  const evidenceText = field(row, ["Evidence", "Impact", "证据", "影响"], "");
  const filesText = field(row, ["Related Files", "Files Or Areas", "关联文件", "涉及文件"], "");
  const hasEvidence = evidenceText ? 1 : 0;
  const hasCode = filesText ? 1 : 0;
  const total = recorded + hasEvidence + hasCode;
  const pct = Math.round((total / 3) * 100);
  return {
    recorded: "1/1",
    evidence: `${hasEvidence}/1`,
    code: `${hasCode}/1`,
    todo: `${100 - pct}%`,
    total: `${pct}%`,
    pct
  };
}
```

- [ ] **Step 3: Render the global code diff donut**

Use this renderer inside `renderDiff()`:

```javascript
function renderDiff() {
  const parts = diffParts(data.git_diff);
  byId("diffSummary").innerHTML = `
    <div class="tooltip-trigger edge-right" tabindex="0">
      <div class="lens-donut" style="--added-pct:${parts.addedPct}%"></div>
      <span class="lens-donut-center">+${esc(parts.added)} / -${esc(parts.deleted)}</span>
      <span class="lens-tooltip">
        <strong>${currentLang === "zh" ? "全项目代码变化" : "Project code change"}</strong>
        ${dataBand([
          ["green", `+${parts.added}`, `${parts.addedPct}%`],
          ["red", `-${parts.deleted}`, `${parts.deletedPct}%`],
          ["gray", parts.files, "files"]
        ])}
        <span class="lens-tip-text">${currentLang === "zh"
          ? `全项目代码变化：新增 ${parts.added} 行，占 ${parts.addedPct}%；删除 ${parts.deleted} 行，占 ${parts.deletedPct}%；变更 ${parts.files} 个文件。`
          : `Project code change: ${parts.added} added lines (${parts.addedPct}%), ${parts.deleted} deleted lines (${parts.deletedPct}%), across ${parts.files} files.`}</span>
      </span>
    </div>
    ${renderDiffFiles(data.git_diff?.files || [])}
  `;
}
```

- [ ] **Step 4: Render question cards with mini donuts and evidence meters**

Use this structure in `renderCurrentQuestions()`:

```javascript
function renderQuestionCard(row) {
  const issueId = field(row, ["ID", "编号"], "-");
  const title = field(row, ["Issue", "Question", "问题"], "Untitled question");
  const status = field(row, ["Status", "状态"], "unknown");
  const evidence = field(row, ["Evidence", "Impact", "证据", "影响"], "not recorded");
  const diff = issueDiffParts(row);
  const evidenceStats = evidenceParts(row);
  const donutClass = diff.mapped ? "lens-mini-donut" : "lens-mini-donut empty";

  return `
    <article class="lens-question">
      <div class="tooltip-trigger" tabindex="0">
        <div class="${donutClass}" style="--added-pct:${diff.addedPct}%"></div>
        <span class="lens-tooltip">
          <strong>${currentLang === "zh" ? "关联代码差异" : "Related code diff"}</strong>
          ${dataBand([
            ["green", `+${diff.added}`, `${diff.addedPct}%`],
            ["red", `-${diff.deleted}`, `${diff.deletedPct}%`],
            ["gray", diff.files, "files"]
          ])}
          <span class="lens-tip-text">${diff.mapped
            ? (currentLang === "zh" ? "关联代码差异：来自记录中的关联文件和 Git diff 的交集。" : "Related code diff: derived from recorded related files intersecting with Git diff.")
            : (currentLang === "zh" ? "关联代码差异：暂无明确映射，不编造文件关系。" : "Related code diff: no explicit mapping, so no file relationship is invented.")}</span>
        </span>
      </div>
      <div>
        <div class="lens-question-title">${esc(issueId)}：${esc(title)}</div>
        <div class="lens-question-sub">${esc(status)} ｜ ${esc(evidence)}</div>
        ${renderEvidenceMeter(evidenceStats)}
      </div>
    </article>
  `;
}
```

- [ ] **Step 5: Add compact data band helpers**

Add:

```javascript
function dataBand(rows) {
  return `<div class="lens-data-band">${rows.map(([color, value, sub]) => `
    <span class="lens-data lens-${color}">
      ${esc(value)}<small>${esc(sub)}</small>
    </span>
  `).join("")}</div>`;
}

function renderEvidenceMeter(stats) {
  return `
    <div class="tooltip-trigger lens-meter-wrap" tabindex="0">
      <div class="lens-meter-label"><span>${esc(t("label.evidenceMeter"))}</span><span>${esc(stats.total)}</span></div>
      <div class="lens-evidence-meter"><div class="lens-evidence-fill" style="width:${stats.pct}%"></div></div>
      <span class="lens-tooltip">
        <strong>${esc(t("label.evidenceMeter"))}</strong>
        ${dataBand([
          ["blue", stats.recorded, "33%"],
          ["green", stats.evidence, "33%"],
          ["orange", stats.code, "34%"]
        ])}
        <div class="lens-data-band two">
          <span class="lens-data lens-gray">${esc(stats.todo)}<small>todo</small></span>
          <span class="lens-data lens-gray">${esc(stats.total)}<small>total</small></span>
        </div>
        <span class="lens-tip-text">${currentLang === "zh"
          ? "证据完整度：显示问题记录、证据和关联代码是否已经具备。"
          : "Evidence meter: shows whether the issue record, evidence, and related code are present."}</span>
      </span>
    </div>
  `;
}
```

- [ ] **Step 6: Run all unit tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot -v
```

Expected result:

```text
OK
```

- [ ] **Step 7: Commit the visual rendering**

Run:

```powershell
git add vibe-lens/assets/report_template.html tests/test_lens_snapshot.py
git commit -m "feat: render Vibe Lens report visuals"
```

## Task 4: Implement Tooltip Boundary, Focus, and Touch Behavior

**Files:**
- Modify: `vibe-lens/assets/report_template.html`
- Test: `tests/test_lens_snapshot.py`

- [ ] **Step 1: Add tooltip CSS with inward defaults**

Add:

```css
.tooltip-trigger {
  position: relative;
  cursor: help;
}
.lens-tooltip {
  pointer-events: none;
  opacity: 0;
  transform: translateY(5px);
  transition: opacity .15s ease, transform .15s ease;
  position: absolute;
  left: 0;
  top: calc(100% + 8px);
  width: min(280px, calc(100vw - 32px));
  border-radius: 8px;
  background: #17202a;
  color: #fff;
  padding: 10px;
  z-index: 80;
  box-shadow: 0 14px 28px rgba(0,0,0,.22);
  font-size: 12px;
  text-align: left;
}
.tooltip-trigger:hover .lens-tooltip,
.tooltip-trigger:focus-within .lens-tooltip,
.tooltip-trigger.is-open .lens-tooltip {
  opacity: 1;
  transform: translateY(0);
}
.edge-right .lens-tooltip,
.lens-card:nth-child(2) .lens-tooltip {
  left: auto;
  right: 0;
}
.lens-data-band {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px;
  margin: 8px 0;
}
.lens-data-band.two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.lens-data {
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 7px;
  padding: 7px 6px;
  text-align: center;
  font-variant-numeric: tabular-nums;
  font-weight: 850;
  line-height: 1.05;
  background: rgba(255,255,255,.04);
}
.lens-data small {
  display: block;
  margin-top: 4px;
  color: inherit;
  opacity: .88;
  font-size: 10px;
  font-weight: 700;
}
.lens-green { color: #48d597; }
.lens-red { color: #ff7b7b; }
.lens-blue { color: #8db7ff; }
.lens-orange { color: #ffc36b; }
.lens-gray { color: #cbd5e1; }
.lens-tip-text {
  display: block;
  color: #d7dee9;
  line-height: 1.45;
  border-top: 1px solid rgba(255,255,255,.14);
  padding-top: 8px;
}
```

- [ ] **Step 2: Add viewport clamp as a safety net**

Add:

```javascript
function placeTooltip(trigger) {
  const tip = trigger.querySelector(".lens-tooltip");
  if (!tip) return;
  const rect = trigger.getBoundingClientRect();
  const width = Math.min(280, window.innerWidth - 32);
  tip.style.width = `${width}px`;
  const tipRect = tip.getBoundingClientRect();
  const overflowRight = rect.left + width > window.innerWidth - 16;
  const overflowLeft = rect.left < 16;
  trigger.classList.toggle("edge-right", overflowRight && !overflowLeft);
  if (tipRect.top < 8) {
    tip.style.top = "calc(100% + 8px)";
  }
}

function bindTooltips() {
  document.querySelectorAll(".tooltip-trigger").forEach((trigger) => {
    trigger.addEventListener("mouseenter", () => placeTooltip(trigger));
    trigger.addEventListener("focusin", () => placeTooltip(trigger));
    trigger.addEventListener("click", () => trigger.classList.toggle("is-open"));
  });
}
```

Call `bindTooltips()` at the end of `render()`.

- [ ] **Step 3: Extend the contract test**

In `test_html_report_contains_approved_ui_contract`, add:

```python
            "function bindTooltips",
            "edge-right",
            "focus-within",
            "is-open",
```

- [ ] **Step 4: Run tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot -v
```

Expected result:

```text
OK
```

- [ ] **Step 5: Commit interaction behavior**

Run:

```powershell
git add vibe-lens/assets/report_template.html tests/test_lens_snapshot.py
git commit -m "feat: add bounded report tooltips"
```

## Task 5: Generate and Inspect the Report

**Files:**
- Generated only: `docs/vibe-lens-report.html`

- [ ] **Step 1: Generate the report from this repository**

Run:

```powershell
python vibe-lens/scripts/lens_snapshot.py --project-root . --html --output docs/vibe-lens-report.html
```

Expected output:

```text
HTML report: C:\Users\23184\Desktop\deeplister-iteration-skill\docs\vibe-lens-report.html
```

- [ ] **Step 2: Open the generated report locally**

Open:

```text
C:\Users\23184\Desktop\deeplister-iteration-skill\docs\vibe-lens-report.html
```

Check manually:

- Language switch changes section labels.
- Current questions show mini donuts.
- Code Diff shows a large donut.
- Evidence meter appears below question text.
- Hovering a donut or meter shows compact numeric data.
- Percentages use the same color as their main number.
- Large section titles show explanations.
- Tooltips stay inside the viewport near left and right edges.
- No section tells the user what to do first.

- [ ] **Step 3: Keep generated report out of Git**

Run:

```powershell
git status --short docs/vibe-lens-report.html
```

Expected result:

```text
```

The file should be ignored by `.gitignore`.

- [ ] **Step 4: Run final checks**

Run:

```powershell
python -m unittest tests.test_lens_snapshot -v
python -m py_compile vibe-lens/scripts/lens_snapshot.py
git diff --check
```

Expected result:

```text
OK
```

`py_compile` and `git diff --check` should exit with code `0`.

- [ ] **Step 5: Confirm there are no extra files to commit**

Run:

```powershell
git status --short
```

Expected result after committing implementation tasks:

```text
```

If `docs/vibe-lens-report.html` appears, confirm `.gitignore` still ignores generated reports before committing anything else.

## Self-Review

Spec coverage:

- Product positioning: covered by shell copy, neutral tests, and forbidden ranking strings.
- Chinese and English: covered by language toggle and bilingual strings.
- Evidence-board layout: covered by the shell task.
- Global code diff donut: covered by Task 3.
- Question item mini donut: covered by Task 3.
- Evidence meter: covered by Task 3.
- Tooltip v4 numeric band: covered by Task 3 and Task 4.
- Tooltip boundary rules: covered by Task 4.
- Section-title hover explanations: covered by Task 2 and Task 4.
- Data-source limits: covered by `issueDiffParts`, which only maps explicit related files and does not invent relationships.
- Out-of-scope ranking and scheduling: covered by neutral tests and forbidden fields.

Placeholder scan:

- This plan uses concrete file paths, commands, code snippets, and expected results.
- The plan does not require external libraries.
- The plan does not ask the implementer to invent priority, score, or schedule logic.

Type and naming consistency:

- CSS uses the `lens-*` prefix.
- Tooltip triggers consistently use `.tooltip-trigger`.
- Language keys use `section.*`, `metric.*`, `legend.*`, `label.*`, and `tip.*`.
- Test names match behavior and can be run individually with `python -m unittest`.
