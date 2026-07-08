# Vibe Lens Visual Cognition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Vibe Lens 0.2 so existing report cards share one visual cognition language: evidence, verification, explanation, file change tags, and data-driven iteration path nodes.

**Architecture:** Keep the current static-report architecture. `lens_snapshot.py` enriches Markdown and Git facts into explicit JSON signals; `report_template.html` renders those signals without guessing; `tests/test_lens_snapshot.py` protects old records, no-ranking behavior, and the new visual cognition layer.

**Tech Stack:** Python standard library, Markdown tables parsed by existing helpers, Git CLI, static HTML/CSS/JavaScript, `unittest`.

## Global Constraints

- The whole Lens helps users understand coding; do not add a standalone “理解 Coding” card.
- Do not display an Agent cognition model; display project facts that help the operator form their own model.
- All visual indicators are information signals, not quality scores, priority scores, or task completion scores.
- Do not automatically sort tasks, schedule work, assign weights, or recommend a next task.
- Do not guess issue-file relationships. If no explicit relationship exists, show `未关联` / `Unlinked`.
- Keep Markdown as the source record and HTML as the reading surface.
- Preserve old record compatibility when `验证` and `解释状态` fields are absent.
- Use Chinese-facing copy by default and keep the existing English UI switch.
- Verification commands must include `python -m unittest tests.test_lens_snapshot`, `python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py`, and HTML regeneration.

---

## File Structure

- Modify `dl-vibe-lens-skill/scripts/lens_snapshot.py`
  - Add field aliases for verification and explanation.
  - Add issue signal helpers that compute evidence, verification, and explanation completeness.
  - Add file cognition helpers that mark changed files as linked or unlinked without guessing.
  - Add iteration entry parsing and data-driven path node data.

- Modify `dl-vibe-lens-skill/assets/report_template.html`
  - Replace the current one-dimensional evidence meter with compact evidence / verification / explanation signals.
  - Add file-level cognition tags in the code diff file list and code detail page.
  - Change evidence summary into fact-type / gap signals.
  - Render the path visualization from `iteration_direction.nodes` instead of fixed decorative nodes.

- Modify `tests/test_lens_snapshot.py`
  - Add snapshot tests for new fields and backward compatibility.
  - Add HTML tests that assert the visual cognition layer exists and no standalone “理解 Coding” card appears.
  - Add path tests that assert real iteration titles drive path nodes.

- Modify `dl-vibe-lens-skill/references/lens-record-format.md`
  - Document optional `验证` / `Verification` and `解释状态` / `Explanation Status` fields.
  - Define “问题有证据” as traceable, checkable, and reviewable.

- Modify `README.md` and `docs/FEATURE_INTRO_ZH.md`
  - Update product copy after implementation so users understand the new visual signals.

- Modify `docs/iteration-record.md`
  - Record the completed implementation, verification, and any remaining visual limitations after the feature is implemented.

---

### Task 1: Add Issue Cognition Signals To Snapshot Data

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`

**Interfaces:**
- Consumes: existing `parse_markdown_table(block: str) -> list[dict[str, str]]` and `value(row: dict[str, str], field: str, default: str = "") -> str`
- Produces: `issue_signal_breakdown(issue: dict[str, str]) -> dict[str, Any]`
- Produces: `enrich_issue(issue: dict[str, str]) -> dict[str, Any]`
- Produces: `build_cognition_summary(issues: list[dict[str, Any]]) -> dict[str, int]`

- [ ] **Step 1: Write the failing snapshot test**

Add this test method inside `LensSnapshotTest` in `tests/test_lens_snapshot.py`:

```python
    def test_snapshot_builds_visual_cognition_signals(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-101 | 总览详情入口混乱 | operator | open | 用户指出四个指标跳到同一详情页 | dl-vibe-lens-skill/assets/report_template.html | python -m unittest tests.test_lens_snapshot | 已解释 |
| VL-102 | 路径图还是演示图 | operator | open | 用户指出路径图落地残缺 | dl-vibe-lens-skill/assets/report_template.html |  | 解释不足 |

## 当前工作
| 会话 | 任务 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|---|
| 2026-07-09 | 设计可视化认知层 | docs/ | discussing | 计划阶段 |

## 迭代记录
### 2026-07-09: 设计可视化认知层
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        first = snapshot["open_questions"][0]["__lens"]
        second = snapshot["open_questions"][1]["__lens"]

        self.assertEqual(first["evidence"]["complete"], 3)
        self.assertEqual(first["evidence"]["total"], 3)
        self.assertEqual(first["evidence"]["percent"], 100)
        self.assertEqual(first["verification"]["percent"], 100)
        self.assertEqual(first["explanation"]["label"], "已解释")
        self.assertEqual(first["overall_percent"], 100)

        self.assertEqual(second["verification"]["percent"], 0)
        self.assertIn("验证", second["verification"]["missing"])
        self.assertEqual(second["explanation"]["label"], "解释不足")
        self.assertLess(second["overall_percent"], 100)

        self.assertEqual(snapshot["cognition_summary"]["issues_with_evidence"], 2)
        self.assertEqual(snapshot["cognition_summary"]["issues_with_verification"], 1)
        self.assertEqual(snapshot["cognition_summary"]["issues_with_full_explanation"], 1)
```

- [ ] **Step 2: Run the new test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_snapshot_builds_visual_cognition_signals
```

Expected: FAIL with a missing `__lens` key or missing `cognition_summary`.

- [ ] **Step 3: Add field aliases and cognition helpers**

In `dl-vibe-lens-skill/scripts/lens_snapshot.py`, extend `FIELD_ALIASES`:

```python
    "verification": ["Verification", "Validation", "验证", "验证记录"],
    "explanation_status": ["Explanation Status", "Explanation", "解释状态", "解释"],
```

Add these helpers after `is_open_issue`:

```python
EMPTY_VALUES = {"", "-", "none", "None", "NONE", "n/a", "N/A", "无", "暂无", "未记录", "unknown"}
FULL_EXPLANATION_VALUES = {"explained", "full", "complete", "已解释", "完整解释"}
PARTIAL_EXPLANATION_VALUES = {"partial", "部分解释"}
WEAK_EXPLANATION_VALUES = {"insufficient", "missing", "解释不足", "缺解释", "未解释"}


def has_meaningful_text(raw: str) -> bool:
    return raw.strip() not in EMPTY_VALUES


def percent(complete: int, total: int) -> int:
    if total <= 0:
        return 0
    return round((complete / total) * 100)


def issue_signal_breakdown(issue: dict[str, str]) -> dict[str, Any]:
    source_present = has_meaningful_text(value(issue, "source"))
    evidence_present = has_meaningful_text(value(issue, "evidence")) or has_meaningful_text(value(issue, "impact"))
    files_present = has_meaningful_text(value(issue, "files"))
    verification_present = has_meaningful_text(value(issue, "verification"))

    evidence_checks = [
        ("来源", source_present),
        ("证据", evidence_present),
        ("关联文件", files_present),
    ]
    evidence_complete = sum(1 for _name, present in evidence_checks if present)
    evidence_missing = [name for name, present in evidence_checks if not present]

    verification_missing = [] if verification_present else ["验证"]

    explanation_raw = value(issue, "explanation_status").strip()
    explanation_normalized = explanation_raw.lower()
    if explanation_raw in FULL_EXPLANATION_VALUES or explanation_normalized in FULL_EXPLANATION_VALUES:
        explanation_label = "已解释"
        explanation_complete = 1
        explanation_missing: list[str] = []
    elif explanation_raw in PARTIAL_EXPLANATION_VALUES or explanation_normalized in PARTIAL_EXPLANATION_VALUES:
        explanation_label = "部分解释"
        explanation_complete = 0
        explanation_missing = ["完整解释"]
    elif explanation_raw in WEAK_EXPLANATION_VALUES or explanation_normalized in WEAK_EXPLANATION_VALUES:
        explanation_label = "解释不足"
        explanation_complete = 0
        explanation_missing = ["解释"]
    elif has_meaningful_text(explanation_raw):
        explanation_label = explanation_raw
        explanation_complete = 1
        explanation_missing = []
    else:
        explanation_label = "未记录"
        explanation_complete = 0
        explanation_missing = ["解释"]

    total_complete = evidence_complete + (1 if verification_present else 0) + explanation_complete
    total_possible = 5

    return {
        "evidence": {
            "complete": evidence_complete,
            "total": 3,
            "percent": percent(evidence_complete, 3),
            "missing": evidence_missing,
        },
        "verification": {
            "complete": 1 if verification_present else 0,
            "total": 1,
            "percent": 100 if verification_present else 0,
            "missing": verification_missing,
        },
        "explanation": {
            "complete": explanation_complete,
            "total": 1,
            "percent": 100 if explanation_complete else 0,
            "label": explanation_label,
            "missing": explanation_missing,
        },
        "overall_percent": percent(total_complete, total_possible),
    }


def enrich_issue(issue: dict[str, str]) -> dict[str, Any]:
    enriched: dict[str, Any] = dict(issue)
    enriched["__lens"] = issue_signal_breakdown(issue)
    return enriched


def build_cognition_summary(issues: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "issues_with_evidence": sum(1 for issue in issues if issue["__lens"]["evidence"]["percent"] > 0),
        "issues_with_verification": sum(1 for issue in issues if issue["__lens"]["verification"]["percent"] > 0),
        "issues_with_full_explanation": sum(1 for issue in issues if issue["__lens"]["explanation"]["label"] == "已解释"),
        "issues_with_gaps": sum(1 for issue in issues if issue["__lens"]["overall_percent"] < 100),
    }
```

- [ ] **Step 4: Use enriched issues in the snapshot**

In `build_snapshot`, replace the current issue construction:

```python
    issues = parse_markdown_table(section_any(text, SECTION_ALIASES["issue_pool"]))
    open_questions = [issue for issue in issues if is_open_issue(issue)]
    issue_counts = Counter(value(issue, "status", "unknown") for issue in issues)
```

with:

```python
    raw_issues = parse_markdown_table(section_any(text, SECTION_ALIASES["issue_pool"]))
    issues = [enrich_issue(issue) for issue in raw_issues]
    open_questions = [issue for issue in issues if is_open_issue(issue)]
    issue_counts = Counter(value(issue, "status", "unknown") for issue in raw_issues)
```

Add `cognition_summary` to the returned dictionary:

```python
        "cognition_summary": build_cognition_summary(issues),
```

- [ ] **Step 5: Run the focused test and then the full suite**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_snapshot_builds_visual_cognition_signals
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/scripts/lens_snapshot.py
git commit -m "Add issue cognition signals to Vibe Lens snapshot"
```

---

### Task 2: Add File Cognition Tags Without Guessing

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`

**Interfaces:**
- Consumes: enriched issues from Task 1 and `git_diff["files"]`
- Produces: `split_file_refs(raw: str) -> list[str]`
- Produces: `build_file_cognition(issues: list[dict[str, Any]], files: list[dict[str, Any]]) -> list[dict[str, Any]]`
- Adds: `git_diff["file_cognition"]`

- [ ] **Step 1: Write the failing file cognition test**

Add this test method:

```python
    def test_file_cognition_marks_only_explicitly_linked_files(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-201 | 脚本需要认知信号 | operator | open | 用户要求可视化减轻负担 | app.py | python -m unittest tests.test_lens_snapshot | 已解释 |
| VL-202 | 文档需要更新 | operator | open | 用户要求记录边界 | docs/plan.md |  | 解释不足 |

## 迭代记录
### 2026-07-09: 文件认知标记
"""
        )
        self.run_git("init")
        self.run_git("config", "user.email", "test@example.com")
        self.run_git("config", "user.name", "Test User")
        (self.tmp / "app.py").write_text("one\n", encoding="utf-8")
        (self.tmp / "other.py").write_text("base\n", encoding="utf-8")
        self.run_git("add", "app.py", "other.py", "docs/iteration-record.md")
        self.run_git("commit", "-m", "initial")
        (self.tmp / "app.py").write_text("one\ntwo\n", encoding="utf-8")
        (self.tmp / "other.py").write_text("base\nchanged\n", encoding="utf-8")

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        by_path = {row["path"]: row for row in snapshot["git_diff"]["file_cognition"]}

        self.assertEqual(by_path["app.py"]["relation_status"], "已关联")
        self.assertEqual(by_path["app.py"]["explanation_status"], "已解释")
        self.assertEqual(by_path["app.py"]["verification_status"], "有验证")
        self.assertEqual(by_path["app.py"]["linked_issue_ids"], ["VL-201"])

        self.assertEqual(by_path["other.py"]["relation_status"], "未关联")
        self.assertEqual(by_path["other.py"]["explanation_status"], "未关联")
        self.assertEqual(by_path["other.py"]["verification_status"], "未关联")
        self.assertEqual(by_path["other.py"]["linked_issue_ids"], [])
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_file_cognition_marks_only_explicitly_linked_files
```

Expected: FAIL with missing `file_cognition`.

- [ ] **Step 3: Add file cognition helpers**

Add these helpers after `build_cognition_summary`:

```python
def split_file_refs(raw: str) -> list[str]:
    return [part.strip() for part in re.split(r"[,，]", raw) if part.strip()]


def file_matches_ref(path: str, ref: str) -> bool:
    normalized_path = path.replace("\\", "/")
    normalized_ref = ref.replace("\\", "/")
    return normalized_path == normalized_ref or normalized_path.endswith(normalized_ref) or normalized_ref.endswith(normalized_path)


def build_file_cognition(issues: list[dict[str, Any]], files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for file in files:
        path = file["path"]
        linked = []
        for issue in issues:
            refs = split_file_refs(value(issue, "files"))
            if any(file_matches_ref(path, ref) for ref in refs):
                linked.append(issue)

        if not linked:
            rows.append(
                {
                    "path": path,
                    "relation_status": "未关联",
                    "explanation_status": "未关联",
                    "verification_status": "未关联",
                    "linked_issue_ids": [],
                }
            )
            continue

        explanations = [issue["__lens"]["explanation"]["label"] for issue in linked]
        if "已解释" in explanations:
            explanation_status = "已解释"
        elif "部分解释" in explanations:
            explanation_status = "部分解释"
        else:
            explanation_status = "解释不足"

        verification_status = (
            "有验证"
            if any(issue["__lens"]["verification"]["percent"] > 0 for issue in linked)
            else "缺验证"
        )

        rows.append(
            {
                "path": path,
                "relation_status": "已关联",
                "explanation_status": explanation_status,
                "verification_status": verification_status,
                "linked_issue_ids": [value(issue, "id", "-") for issue in linked],
            }
        )
    return rows
```

- [ ] **Step 4: Attach file cognition to Git diff data**

In `build_snapshot`, change:

```python
    return {
```

to:

```python
    git_diff = collect_git_diff(project_root, diff_ref)
    git_diff["file_cognition"] = build_file_cognition(issues, git_diff.get("files", []))

    return {
```

Then replace the existing return field:

```python
        "git_diff": collect_git_diff(project_root, diff_ref),
```

with:

```python
        "git_diff": git_diff,
```

- [ ] **Step 5: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_file_cognition_marks_only_explicitly_linked_files
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/scripts/lens_snapshot.py
git commit -m "Add file cognition tags without guessing"
```

---

### Task 3: Add Data-Driven Iteration Path Nodes

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`

**Interfaces:**
- Produces: `parse_iteration_entries(block: str) -> list[dict[str, str]]`
- Produces: `build_iteration_nodes(entries: list[dict[str, str]]) -> list[dict[str, Any]]`
- Preserves: `snapshot["latest_iteration"]`
- Extends: `snapshot["iteration_direction"]["nodes"]`

- [ ] **Step 1: Write the failing path-node test**

Add this test method:

```python
    def test_iteration_path_nodes_are_built_from_real_entries(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-301 | 路径图需要真实数据 | operator | open | 用户指出当前路径图像演示 | dl-vibe-lens-skill/assets/report_template.html |

## 迭代记录
### 2026-07-09: 记录可视化认知层
验证：
- 已运行 snapshot。
未完成：
- 路径图还需要节点展开。

### 2026-07-08: 记录理解 coding 定位
证据：
- 用户明确纠正产品定位。
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        nodes = snapshot["iteration_direction"]["nodes"]

        self.assertEqual(nodes[0]["title"], "2026-07-09: 记录可视化认知层")
        self.assertIn("测试验证", nodes[0]["markers"])
        self.assertIn("解释不足", nodes[0]["markers"])
        self.assertEqual(nodes[1]["title"], "2026-07-08: 记录理解 coding 定位")
        self.assertIn("记录事实", nodes[1]["markers"])
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_iteration_path_nodes_are_built_from_real_entries
```

Expected: FAIL with missing `nodes`.

- [ ] **Step 3: Replace title-only parsing with entry parsing while preserving title output**

Keep `parse_iterations` for compatibility, but add:

```python
def parse_iteration_entries(block: str) -> list[dict[str, str]]:
    pattern = re.compile(r"^###\s+(.+?)\s*$", flags=re.MULTILINE)
    matches = list(pattern.finditer(block))
    entries = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        entries.append({"title": match.group(1).strip(), "body": block[start:end].strip()})
    return entries


def build_iteration_nodes(entries: list[dict[str, str]]) -> list[dict[str, Any]]:
    nodes = []
    for index, entry in enumerate(entries[:10]):
        body = entry["body"]
        markers = ["记录事实"]
        if "验证" in body or "Verification" in body:
            markers.append("测试验证")
        if "未完成" in body or "不清楚" in body or "缺口" in body:
            markers.append("解释不足")
        if "风险" in body or "冲突" in body:
            markers.append("风险线索")
        nodes.append(
            {
                "title": entry["title"],
                "index": index,
                "kind": "latest" if index == 0 else "main",
                "markers": markers,
                "summary": body.splitlines()[0] if body.splitlines() else "",
            }
        )
    return nodes
```

- [ ] **Step 4: Attach nodes to snapshot**

In `build_snapshot`, replace:

```python
    iterations = parse_iterations(section_any(text, SECTION_ALIASES["iteration_log"]))
```

with:

```python
    iteration_block = section_any(text, SECTION_ALIASES["iteration_log"])
    iteration_entries = parse_iteration_entries(iteration_block)
    iterations = [entry["title"] for entry in iteration_entries]
```

Add nodes inside `iteration_direction`:

```python
            "nodes": build_iteration_nodes(iteration_entries),
```

- [ ] **Step 5: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_iteration_path_nodes_are_built_from_real_entries
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/scripts/lens_snapshot.py
git commit -m "Build iteration path nodes from real records"
```

---

### Task 4: Render Evidence, Verification, And Explanation Signals In Current Questions

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/assets/report_template.html`

**Interfaces:**
- Consumes: `row.__lens.evidence.percent`, `row.__lens.verification.percent`, `row.__lens.explanation.label`, and `row.__lens.overall_percent`
- Produces: HTML with `signal-row`, `signal-chip`, `evidenceSignal`, `verificationSignal`, and `explanationSignal`

- [ ] **Step 1: Write the failing HTML test**

Add this test method:

```python
    def test_html_report_renders_visual_cognition_signals_without_new_card(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-401 | 当前问题需要信息信号 | operator | open | 用户要求可视化减轻负担 | README.md | python -m unittest tests.test_lens_snapshot | 已解释 |

## 迭代记录
### 2026-07-09: HTML 信息信号
验证：
- 已生成 HTML。
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)
        html = output.read_text(encoding="utf-8")

        self.assertIn("signal-row", html)
        self.assertIn("evidenceSignal", html)
        self.assertIn("verificationSignal", html)
        self.assertIn("explanationSignal", html)
        self.assertIn("信息完整度", html)
        self.assertNotIn(">理解 Coding<", html)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_renders_visual_cognition_signals_without_new_card
```

Expected: FAIL with missing `signal-row` or labels.

- [ ] **Step 3: Add compact signal CSS**

In `report_template.html`, near the current `.meter` styles, add:

```css
    .signal-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
      margin-top: 8px;
    }
    .signal-chip {
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 6px;
      background: rgba(255,255,255,.68);
    }
    .signal-label {
      display: flex;
      justify-content: space-between;
      gap: 6px;
      color: var(--muted);
      font-size: 11px;
      line-height: 1.2;
    }
    .signal-bar {
      height: 5px;
      margin-top: 5px;
      border-radius: 999px;
      background: #e5e7eb;
      overflow: hidden;
    }
    .signal-fill {
      height: 100%;
      border-radius: inherit;
      background: var(--blue);
    }
    .signal-fill.verify { background: var(--green); }
    .signal-fill.explain { background: var(--orange); }
```

- [ ] **Step 4: Add labels**

Inside the Chinese labels object, add:

```javascript
        evidenceSignal: "证据",
        verificationSignal: "验证",
        explanationSignal: "解释",
        infoCompleteness: "信息完整度",
```

Inside the English labels object, add:

```javascript
        evidenceSignal: "Evidence",
        verificationSignal: "Verification",
        explanationSignal: "Explanation",
        infoCompleteness: "Info completeness",
```

- [ ] **Step 5: Add JS helpers for signal rendering**

Near `issueCompleteness(row)`, add:

```javascript
    const lensSignals = (row) => row.__lens || {
      evidence: { percent: issueCompleteness(row), missing: [] },
      verification: { percent: 0, missing: ["验证"] },
      explanation: { percent: 0, label: "未记录", missing: ["解释"] },
      overall_percent: issueCompleteness(row)
    };

    function renderSignalChip(label, percentValue, className, tip) {
      const width = Math.max(0, Math.min(100, Number(percentValue || 0)));
      return `
        <div class="signal-chip" data-tip-zh="${esc(tip.zh)}" data-tip-en="${esc(tip.en)}">
          <div class="signal-label"><span>${esc(label)}</span><strong>${width}%</strong></div>
          <div class="signal-bar"><div class="signal-fill ${esc(className)}" style="width:${width}%"></div></div>
        </div>
      `;
    }
```

- [ ] **Step 6: Replace the current one-line meter in `renderQuestions`**

In `renderQuestions`, replace the existing `meter-label` and `meter` block:

```javascript
              <div class="meter-label"><span>${esc(t("evidence"))}</span><span>${completeness}%</span></div>
              <div class="meter" data-tip-zh="证据完整度：按 ID、问题、状态、证据、关联文件是否存在粗略估算，为展示信号，不是质量评分。" data-tip-en="Evidence completeness: a rough display signal based on ID, issue, status, evidence, and related files. It is not a quality score.">
                <div class="meter-fill" style="width:${completeness}%">
                </div>
              </div>
```

with:

```javascript
              <div class="meter-label"><span>${esc(t("infoCompleteness"))}</span><span>${esc(signals.overall_percent || completeness)}%</span></div>
              <div class="signal-row">
                ${renderSignalChip(t("evidenceSignal"), signals.evidence?.percent || 0, "", {
                  zh: `证据完整度：表示来源、证据和关联文件是否清楚；不是优先级或质量评分。缺口：${(signals.evidence?.missing || []).join("、") || "无"}`,
                  en: `Evidence signal: source, evidence, and related files. It is not priority or quality scoring. Missing: ${(signals.evidence?.missing || []).join(", ") || "none"}`
                })}
                ${renderSignalChip(t("verificationSignal"), signals.verification?.percent || 0, "verify", {
                  zh: `验证信号：表示是否有测试、运行结果、截图或人工确认。缺口：${(signals.verification?.missing || []).join("、") || "无"}`,
                  en: `Verification signal: tests, runtime result, screenshot, or operator confirmation. Missing: ${(signals.verification?.missing || []).join(", ") || "none"}`
                })}
                ${renderSignalChip(t("explanationSignal"), signals.explanation?.percent || 0, "explain", {
                  zh: `解释信号：${signals.explanation?.label || "未记录"}。它表示是否写清为什么这样改，不展示 Agent 的认知模型。`,
                  en: `Explanation signal: ${signals.explanation?.label || "not recorded"}. It shows whether the reason is recorded, not the agent cognition model.`
                })}
              </div>
```

Also add this line after `const completeness = issueCompleteness(row);`:

```javascript
        const signals = lensSignals(row);
```

- [ ] **Step 7: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_renders_visual_cognition_signals_without_new_card
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 8: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/assets/report_template.html
git commit -m "Render visual cognition signals in questions"
```

---

### Task 5: Render File Cognition Tags And Fact-Type Evidence Summary

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/assets/report_template.html`

**Interfaces:**
- Consumes: `data.git_diff.file_cognition`
- Produces: `file-cognition-tags`, `fact-chip`, and localized fact/gap labels

- [ ] **Step 1: Write the failing HTML test**

Add this test method:

```python
    def test_html_report_renders_file_cognition_tags_and_fact_types(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-501 | 文件标记需要可追溯 | operator | open | 用户要求不猜文件关系 | app.py | python -m unittest tests.test_lens_snapshot | 已解释 |

## 迭代记录
### 2026-07-09: 文件标签
验证：
- 已运行测试。
"""
        )
        self.run_git("init")
        self.run_git("config", "user.email", "test@example.com")
        self.run_git("config", "user.name", "Test User")
        (self.tmp / "app.py").write_text("one\n", encoding="utf-8")
        self.run_git("add", "app.py", "docs/iteration-record.md")
        self.run_git("commit", "-m", "initial")
        (self.tmp / "app.py").write_text("one\ntwo\n", encoding="utf-8")

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)
        html = output.read_text(encoding="utf-8")

        self.assertIn("file-cognition-tags", html)
        self.assertIn("已解释", html)
        self.assertIn("有验证", html)
        self.assertIn("fact-chip", html)
        self.assertIn("Git 事实", html)
        self.assertIn("缺验证", html)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_renders_file_cognition_tags_and_fact_types
```

Expected: FAIL with missing `file-cognition-tags`.

- [ ] **Step 3: Add tag CSS**

In `report_template.html`, near `.diff-file-list`, add:

```css
    .file-cognition-tags {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 4px;
      min-width: 96px;
    }
    .mini-tag, .fact-chip {
      display: inline-flex;
      align-items: center;
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 2px 7px;
      font-size: 11px;
      color: var(--muted);
      background: rgba(255,255,255,.72);
      white-space: nowrap;
    }
    .mini-tag.good, .fact-chip.good { color: #166534; background: #dcfce7; border-color: #bbf7d0; }
    .mini-tag.warn, .fact-chip.warn { color: #92400e; background: #fef3c7; border-color: #fde68a; }
    .mini-tag.muted, .fact-chip.muted { color: #64748b; background: #f1f5f9; }
    .fact-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }
```

- [ ] **Step 4: Add labels and helpers**

Add Chinese labels:

```javascript
        gitFact: "Git 事实",
        recordFact: "记录事实",
        testVerification: "测试验证",
        operatorConfirmed: "操作者确认",
        agentJudgment: "Agent 判断",
        missingEvidence: "缺证据",
        missingVerification: "缺验证",
        insufficientExplanation: "解释不足",
        linked: "已关联",
        unlinked: "未关联",
```

Add English labels:

```javascript
        gitFact: "Git fact",
        recordFact: "Record fact",
        testVerification: "Test verification",
        operatorConfirmed: "Operator confirmed",
        agentJudgment: "Agent judgment",
        missingEvidence: "Missing evidence",
        missingVerification: "Missing verification",
        insufficientExplanation: "Insufficient explanation",
        linked: "Linked",
        unlinked: "Unlinked",
```

Add helpers near `relatedDiff(row)`:

```javascript
    function cognitionByPath(path) {
      const rows = data.git_diff?.file_cognition || [];
      return rows.find((row) => row.path === path) || {
        relation_status: t("unlinked"),
        explanation_status: t("unlinked"),
        verification_status: t("unlinked"),
        linked_issue_ids: []
      };
    }

    function tagClass(value) {
      if (["已解释", "有验证", "已关联", "Linked"].includes(value)) return "good";
      if (["解释不足", "缺验证", "Insufficient explanation", "Missing verification"].includes(value)) return "warn";
      return "muted";
    }

    function renderMiniTag(value) {
      return `<span class="mini-tag ${esc(tagClass(value))}">${esc(value)}</span>`;
    }
```

- [ ] **Step 5: Render tags in the diff file list**

In `renderDiff`, replace each file row body:

```javascript
          <span class="mono">${esc(file.path)}</span>
          <strong class="added">+${esc(file.added ?? "bin")}</strong>
          <strong class="deleted">-${esc(file.deleted ?? "bin")}</strong>
```

with:

```javascript
          <span class="mono">${esc(file.path)}</span>
          <strong class="added">+${esc(file.added ?? "bin")}</strong>
          <strong class="deleted">-${esc(file.deleted ?? "bin")}</strong>
          <span class="file-cognition-tags">
            ${renderMiniTag(cognitionByPath(file.path).explanation_status)}
            ${renderMiniTag(cognitionByPath(file.path).verification_status)}
          </span>
```

- [ ] **Step 6: Render fact-type summary**

In `renderSandboxAndEvidence`, replace the current `evidenceSummary` content with:

```javascript
      const summary = data.cognition_summary || {};
      byId("evidenceSummary").innerHTML = `
        <div class="fact-row">
          <span class="fact-chip good">${esc(t("gitFact"))}: ${esc(diff.changed_file_count || 0)}</span>
          <span class="fact-chip good">${esc(t("recordFact"))}: ${esc(data.issue_count || 0)}</span>
          <span class="fact-chip good">${esc(t("testVerification"))}: ${esc(summary.issues_with_verification || 0)}</span>
          <span class="fact-chip warn">${esc(t("missingVerification"))}: ${esc((data.issue_count || 0) - (summary.issues_with_verification || 0))}</span>
          <span class="fact-chip warn">${esc(t("insufficientExplanation"))}: ${esc(summary.issues_with_gaps || 0)}</span>
        </div>
        <div class="file-row"><span>${esc(t("latestEvidence"))}</span><strong>${esc(latest)}</strong><strong></strong></div>
        <div class="file-row"><span>${esc(t("conflictSignals"))}</span><strong>${esc((data.conflict_signals || []).length)}</strong><strong>${esc(t("signals"))}</strong></div>
      `;
```

- [ ] **Step 7: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_report_renders_file_cognition_tags_and_fact_types
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 8: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/assets/report_template.html
git commit -m "Render file cognition tags and fact signals"
```

---

### Task 6: Render Data-Driven Iteration Path Visualization

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/assets/report_template.html`

**Interfaces:**
- Consumes: `data.iteration_direction.nodes`
- Produces: `renderPathViz()` and path nodes with `data-node-index`

- [ ] **Step 1: Write the failing HTML path test**

Add this test method:

```python
    def test_html_path_visualization_uses_real_iteration_nodes(self):
        self.write_record(
            """# Vibe Lens 记录

## 问题池
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 |
|---|---|---|---|---|---|
| VL-601 | 路径图要来自记录 | operator | open | 用户要求路径图不再只是演示 | dl-vibe-lens-skill/assets/report_template.html |

## 迭代记录
### 2026-07-09: 真实节点一
验证：
- 已运行测试。

### 2026-07-08: 真实节点二
未完成：
- 还有解释缺口。
"""
        )

        snapshot = lens_snapshot.build_snapshot(self.tmp)
        output = self.tmp / "lens-report.html"
        lens_snapshot.write_html_report(snapshot, output)
        html = output.read_text(encoding="utf-8")

        self.assertIn("renderPathViz", html)
        self.assertIn("data-node-index", html)
        self.assertIn("真实节点一", html)
        self.assertIn("真实节点二", html)
        self.assertNotIn("可展开节点：报告 UI、沙盘入口、代码差异展示等方向调整。", html)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_path_visualization_uses_real_iteration_nodes
```

Expected: FAIL with missing `renderPathViz`.

- [ ] **Step 3: Replace static path nodes with containers**

In `report_template.html`, inside `.timeline-viz`, keep the SVG axis but replace the hard-coded `<span class="node ...">` elements with:

```html
          <div id="timelineNodes"></div>
```

- [ ] **Step 4: Add `renderPathViz()`**

Add this function before `renderDetails()`:

```javascript
    function markerClass(markers) {
      if ((markers || []).includes("风险线索")) return "abandon";
      if ((markers || []).includes("解释不足")) return "choice";
      if ((markers || []).includes("测试验证")) return "done";
      return "done";
    }

    function renderPathViz() {
      const nodes = data.iteration_direction?.nodes || [];
      const container = byId("timelineNodes");
      if (!container) return;
      if (!nodes.length) {
        container.innerHTML = "";
        return;
      }
      const count = Math.max(1, nodes.length - 1);
      container.innerHTML = nodes.map((node, index) => {
        const left = 7 + (index / count) * 86;
        const top = index % 2 === 0 ? 55 : 28;
        const markers = node.markers || [];
        const tipZh = `${node.title}｜${markers.join("、") || "记录事实"}`;
        const tipEn = `${node.title} | ${markers.join(", ") || "record fact"}`;
        return `<span class="node ${esc(markerClass(markers))}" data-node-index="${esc(index)}" style="left:${left.toFixed(1)}%;top:${top.toFixed(1)}%" data-tip-zh="${esc(tipZh)}" data-tip-en="${esc(tipEn)}"></span>`;
      }).join("");
    }
```

- [ ] **Step 5: Render path detail with markers**

In `renderDetails`, replace:

```javascript
      const headings = data.iteration_direction?.headings || [];
      byId("pathDetailList").innerHTML = headings.length ? headings.map((title, index) => `
        <div class="path-node-detail ${index > 3 ? "abandoned" : ""}">
          <strong>${esc(title)}</strong>
          <div class="detail-item">${esc(index === 0 ? (data.iteration_direction?.current_direction || t("pathScaleText")) : t("pathScaleText"))}</div>
        </div>
      `).join("") : `<div class="detail-item">${esc(t("none"))}</div>`;
```

with:

```javascript
      const nodes = data.iteration_direction?.nodes || [];
      byId("pathDetailList").innerHTML = nodes.length ? nodes.map((node, index) => `
        <div class="path-node-detail ${index > 3 ? "abandoned" : ""}">
          <strong>${esc(node.title)}</strong>
          <div class="fact-row">${(node.markers || []).map((marker) => `<span class="fact-chip ${esc(tagClass(marker))}">${esc(marker)}</span>`).join("")}</div>
          <div class="detail-item">${esc(index === 0 ? (data.iteration_direction?.current_direction || t("pathScaleText")) : (node.summary || t("pathScaleText")))}</div>
        </div>
      `).join("") : `<div class="detail-item">${esc(t("none"))}</div>`;
```

- [ ] **Step 6: Call `renderPathViz()`**

In `renderAll()`, add:

```javascript
      renderPathViz();
```

between `renderSandboxAndEvidence();` and `renderDetails();`.

- [ ] **Step 7: Run focused and full tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_html_path_visualization_uses_real_iteration_nodes
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 8: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/assets/report_template.html
git commit -m "Render iteration path from record nodes"
```

---

### Task 7: Update Record Format, Public Docs, And Templates

**Files:**
- Modify: `tests/test_lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/scripts/lens_snapshot.py`
- Modify: `dl-vibe-lens-skill/references/lens-record-format.md`
- Modify: `README.md`
- Modify: `docs/FEATURE_INTRO_ZH.md`

**Interfaces:**
- Extends generated record templates with `验证` and `解释状态`
- Documents optional fields while keeping old records valid

- [ ] **Step 1: Write the failing init-template test**

Add this test method:

```python
    def test_init_template_mentions_visual_cognition_fields(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project-root", str(self.tmp), "--init"],
            text=True,
            capture_output=True,
            check=False,
        )

        record = self.tmp / "docs" / "iteration-record.md"
        self.assertEqual(result.returncode, 0, result.stderr)
        text = record.read_text(encoding="utf-8")
        self.assertIn("验证", text)
        self.assertIn("解释状态", text)
        self.assertIn("认知变化", text)
        self.assertIn("信息完整度", text)
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_init_template_mentions_visual_cognition_fields
```

Expected: FAIL with missing `解释状态` or `认知变化`.

- [ ] **Step 3: Update Chinese record template**

In `record_template_zh`, replace the issue table with:

```markdown
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-001 | 第一个需要复盘的问题 | operator | open | 把这一行替换成真实问题 | docs/iteration-record.md | 暂无 | 解释不足 |
```

Add this paragraph under the plain-language intro:

```markdown
信息完整度说明：`证据` 表示问题是否可追溯、可核对、可复盘；`验证` 表示是否有测试、运行结果、截图或人工确认；`解释状态` 表示是否说清为什么这样改。它们都不是优先级。
```

Add this block in the default iteration entry:

```markdown
认知变化：
- 本轮之后更清楚了什么：
- 仍然不清楚什么：
- 下次接手前应该先看什么：
```

- [ ] **Step 4: Update English record template**

In `record_template_en`, replace the issue table with:

```markdown
| ID | Issue | Source | Status | Evidence | Related Files | Verification | Explanation Status |
|---|---|---|---|---|---|---|---|
| VL-001 | First question to review | operator | open | Replace this row with a real question | docs/iteration-record.md | none | insufficient |
```

Add this paragraph under the plain-language intro:

```markdown
Info completeness: `Evidence` means the issue is traceable, checkable, and reviewable; `Verification` means tests, runtime output, screenshots, or operator confirmation exist; `Explanation Status` means the reason for the change is recorded. These are not priorities.
```

Add this block in the default iteration entry:

```markdown
Cognition Change:
- What became clearer after this turn:
- What is still unclear:
- What to inspect before the next handoff:
```

- [ ] **Step 5: Update record format reference**

In `dl-vibe-lens-skill/references/lens-record-format.md`, update the recommended issue table to:

```markdown
| 编号 | 问题 | 来源 | 状态 | 证据 | 关联文件 | 验证 | 解释状态 |
|---|---|---|---|---|---|---|---|
| VL-001 | 简短问题标题 | operator | open | 这个问题为什么存在 | src/app.py | python -m unittest | 已解释 |
```

Add this explanation:

```markdown
“问题有证据”不是说问题一定正确，而是说它可追溯、可核对、可复盘。证据可以来自用户反馈、Git diff、测试结果、截图、日志、历史决策或运行现象。
```

- [ ] **Step 6: Update public docs**

In `README.md`, add a short section after “HTML 报告能看什么”:

```markdown
## 信息完整度不是评分

Vibe Lens 0.2 的进度条和标签只表示复盘信息是否充分：问题是否有证据、改动是否验证过、原因是否解释清楚。它们不是质量评分、优先级评分，也不会替你安排下一步。
```

In `docs/FEATURE_INTRO_ZH.md`, add a matching paragraph under “当前问题”:

```markdown
“问题有证据”表示这个问题可追溯、可核对、可复盘，不代表它一定正确或更重要。证据可以来自用户反馈、Git diff、测试结果、截图、日志、历史决策或运行现象。
```

- [ ] **Step 7: Run tests**

Run:

```powershell
python -m unittest tests.test_lens_snapshot.LensSnapshotTest.test_init_template_mentions_visual_cognition_fields
python -m unittest tests.test_lens_snapshot
```

Expected: PASS.

- [ ] **Step 8: Commit**

```powershell
git add tests/test_lens_snapshot.py dl-vibe-lens-skill/scripts/lens_snapshot.py dl-vibe-lens-skill/references/lens-record-format.md README.md docs/FEATURE_INTRO_ZH.md
git commit -m "Document Vibe Lens visual cognition fields"
```

---

### Task 8: Final Verification And Vibe Lens Record Update

**Files:**
- Modify: `docs/iteration-record.md`
- Generated: `docs/vibe-lens-report.html`

**Interfaces:**
- Consumes: all completed tasks
- Produces: updated local iteration record and refreshed HTML report

- [ ] **Step 1: Run full verification**

Run:

```powershell
python -m unittest tests.test_lens_snapshot
python -m py_compile dl-vibe-lens-skill\scripts\lens_snapshot.py
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --record examples\vibe-lens-record.example.md
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .
git diff --check
```

Expected:

- Unit tests pass.
- Python compile passes.
- Example record snapshot succeeds.
- HTML report regenerates.
- Project snapshot succeeds.
- `git diff --check` has no whitespace errors other than Windows LF/CRLF warnings.

- [ ] **Step 2: Manually inspect generated HTML**

Open:

```text
docs/vibe-lens-report.html
```

Check:

- There is no standalone “理解 Coding” card.
- Current question rows show evidence, verification, and explanation signals.
- Code diff file rows show explanation and verification tags.
- Unlinked files are marked `未关联`, not guessed.
- Evidence summary uses fact and gap tags.
- Timeline nodes use real iteration titles.
- Language switch still works.
- Detail pages still route from overview metrics.
- Setting panel still opens and closes.

- [ ] **Step 3: Update Vibe Lens record**

Append this entry near the top of `docs/iteration-record.md` under `## 迭代记录`:

```markdown
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
```

- [ ] **Step 4: Refresh HTML after record update**

Run:

```powershell
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root . --html --output docs\vibe-lens-report.html
python dl-vibe-lens-skill\scripts\lens_snapshot.py --project-root .
```

Expected: snapshot reads the new 2026-07-09 iteration entry.

- [ ] **Step 5: Commit final feature**

```powershell
git add dl-vibe-lens-skill/scripts/lens_snapshot.py dl-vibe-lens-skill/assets/report_template.html dl-vibe-lens-skill/references/lens-record-format.md tests/test_lens_snapshot.py README.md docs/FEATURE_INTRO_ZH.md docs/iteration-record.md docs/vibe-lens-report.html
git commit -m "Implement Vibe Lens visual cognition layer"
```

---

## Plan Self-Review

Spec coverage:

- The plan keeps the whole Lens as the cognition surface instead of adding a standalone “理解 Coding” card: Task 4 tests this directly.
- Evidence, verification, and explanation signals are implemented in Task 1 and rendered in Task 4.
- File tags avoid guessing by marking unlinked files as `未关联`: Task 2 and Task 5.
- Path nodes come from real iteration records: Task 3 and Task 6.
- Documentation explains “问题有证据”: Task 7.
- Final Vibe Lens record and regenerated report are included: Task 8.

Type consistency:

- `issue_signal_breakdown(issue)` returns a nested dictionary consumed through `row.__lens`.
- `build_file_cognition(issues, files)` attaches rows under `git_diff.file_cognition`.
- `build_iteration_nodes(entries)` attaches rows under `iteration_direction.nodes`.
- HTML helper names consume those exact keys.

Scope check:

- The plan does not implement the second-stage interaction platform.
- The plan does not implement drag-and-drop, automatic task scheduling, complex graph generation, or Loop replay.
- The plan keeps the implementation inside the existing script, template, tests, and docs.
