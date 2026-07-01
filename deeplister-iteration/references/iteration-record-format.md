# DeepLister Iteration Record Format

Use this reference when `docs/迭代记录.md` is missing, malformed, or needs a new section.

## Required Sections

The record should contain these top-level sections:

```md
# DeepLister 迭代记录

## 怎么使用
## 当前产品状态
## 当前优先级
## 问题池
## 追问流程专项记录
## 迭代记录
## 何时进阶
## 每次迭代记录模板
```

## Issue Pool

Use one Markdown table under `## 问题池`.

```md
| 编号 | 问题 | 影响 | 优先级 | 状态 | 下一步 |
|---|---|---|---|---|---|
| DL-001 | Short problem title | Why it matters | P0 | 待处理 | Small next action |
```

Status values:

| Status | Meaning |
|---|---|
| `待处理` | Not started |
| `进行中` | Work has started |
| `已解决` | Done and verified |
| `阻塞` | Cannot proceed without user input or external change |

## Iteration Entry

Append new entries under `## 迭代记录` with the newest entry near the top.

```md
### YYYY-MM-DD：本次迭代标题

本次目标：

- 

发现的问题：

- 

做出的决定：

- 

已完成：

- 

验证：

- 

未完成：

- 

下次建议：

- 
```

## Follow-Up Flow Notes

Use `## 追问流程专项记录` for behavior examples in the core questioning flow.

```md
| 场景 | 当前表现 | 问题 | 优化方向 |
|---|---|---|---|
| 用户回答“一晚醒两三次” | 可能被当成回答太短 | 其实已经提供频率信息 | 检测层识别数字、频率、时间等有效信息 |
```

## When to Split the Record

Keep one file while the issue pool is small. Split into separate docs when:

- The issue pool exceeds 20 items.
- More than 3 directions are active at the same time.
- Real user feedback begins.
- The project needs separate bug, feature, privacy, and product-roadmap tracking.
- More people start collaborating.
