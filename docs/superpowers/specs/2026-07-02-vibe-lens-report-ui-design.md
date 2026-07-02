# Vibe Lens Report UI Design

Date: 2026-07-02

## Purpose

This spec captures the approved direction for the Vibe Lens HTML report UI. The report is a review sandbox: it shows facts, evidence, code changes, direction, and conflict signals. It must not rank tasks, assign priority, or imply what the operator must do next.

The approved base direction is the evidence-board layout from the visual companion session. The accepted tooltip design is the v4 tooltip sketch: a compact numeric band plus the v5-style explanatory text.

## Language

The report should support Chinese and English.

- Provide a visible language switch in the report header.
- Interface labels, section titles, empty states, and tooltips should switch language.
- User-authored record content can remain in the language in which it was written.
- The default language can be inferred later, but the UI must allow manual switching.

## Overall Layout

Use the evidence-board layout.

The page should contain:

- Header with product name, short positioning text, generated time, and language switch.
- Overview metrics: current questions, historical questions, changed files, and code churn.
- Legend explaining visual symbols.
- Current questions/tasks.
- Code Diff section with a donut chart and file-level diff table.
- Iteration Direction section.
- Evidence Chain / Conflict Signals section.
- Historical questions can remain lower on the page or in a compact table.

The report should stay neutral. It can show status, evidence, code churn, and incomplete information, but it must not present those as priority or scheduling advice.

## Visual Semantics

### Global Code Diff Donut

The large donut chart represents project-level Git diff totals.

- Green = added lines.
- Red = deleted lines.
- Center text shows the concise total, for example `+2324 / -1633`.
- Hover opens a compact tooltip with exact added/deleted values and percentages.

The donut explains change volume, not quality.

### Question Item Mini Donut

Each question/task item can have a small donut on the left.

The small donut represents code diff associated with that specific question, when such association is available.

- Green = added lines related to the question.
- Red = deleted lines related to the question.
- Gray = no associated code diff or not enough data.
- It must not represent priority, risk, or task importance.

Hover opens the compact tooltip described below.

### Evidence Completeness Bar

Use the term "证据完整度条" in Chinese and "Evidence meter" in English.

This is a clean horizontal bar under the question text. Do not use diagonal stripe textures.

The bar summarizes how much review material exists for a question:

- The issue is recorded.
- Evidence exists.
- Related code exists.
- Some information is still missing.

The bar is informational only. It must not be described as task completion progress or priority.

## Tooltip Design

Accepted tooltip style: v4 "percent matches main number color".

Each tooltip has two zones:

1. Numeric data band.
2. Explanatory text area.

### Numeric Data Band

The data band should be compact: one to two rows only.

It should contain numbers and percentages, not long labels. Related percentages should use the same color as their main number.

Example for a mini code-diff donut:

- Green data block: `+689` with `100%`.
- Red data block: `-0` with `0%`.
- Neutral data block: `4` with `files`.

Example for an evidence meter:

- Blue data block: `1/1` with `25%`.
- Green data block: `1/2` with `25%`.
- Orange data block: `1/3` with `8%`.
- Gray data block: `42%` with `todo`.
- Gray data block: `58%` with `total`.

The exact counts can evolve when the data model improves, but the tooltip structure should remain compact.

### Explanatory Text Area

Keep the v5-style natural-language explanation below the numeric band.

Examples:

- `关联代码差异：较多。涉及脚本、HTML 模板、测试和文档。`
- `证据完整度：问题已记录；有 PR 合并证据；缺少仓库改名完成证据。`

The text should explain what the numbers mean in plain language. It should not add scheduling advice.

## Section Title Hover

Large section titles should support hover explanations.

Add hover explanations to:

- Legend.
- Current Questions / Tasks.
- Code Diff.
- Iteration Direction.
- Evidence Chain / Conflict Signals.

These tooltips should explain the section's meaning and boundary. They should be short and beginner-friendly.

Examples:

- Code Diff: "来自 Git diff 的事实统计。绿色是新增行，红色是删除行；不评价改动好坏。"
- Current Questions / Tasks: "展示当前仍未关闭的问题。顺序来自记录，不自动排序，不代表优先级。"
- Evidence Chain / Conflict Signals: "证据链解释结论从哪里来；冲突线索提示多个会话或文件区域是否重叠。它只提示，不调度。"

## Interaction Rules

- Keep detailed numbers out of the main text area when they would make the item visually noisy.
- Use hover for precision details.
- Use color consistently between charts, numeric bands, and percentages.
- Do not rely on color alone for essential meaning in the final implementation; use titles, labels, and tooltips for accessibility.
- On mobile or touch screens, hover content should be available by tap or focus.

## Implementation Boundary

This spec is design-only. It does not authorize implementation yet.

Before implementation, create a plan that covers:

- How language strings will be represented.
- How tooltip data will be derived from the snapshot JSON.
- How question-to-file diff association will be represented when exact mapping is unavailable.
- How keyboard focus and touch behavior will expose tooltip content.
- Which existing tests need updates.

## Out of Scope For This Iteration

- Task ranking.
- Priority scoring.
- Automatic scheduling.
- A full relationship map between questions, files, and evidence.
- A second-stage task arrangement platform.

The relationship map remains a later design topic.
