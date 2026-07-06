---
name: gstack-spec
description: gstack-superflow 规划段（minimal 版）。把模糊意图转为结构化 spec，产出文件须含 ## Why / ## Scope（**In scope:**、**Out of scope:**) / ## Technical / ## Files 四个 section，供 bridge-builder 解析。计划 2 替换为 vendor 的 Gstack /spec 五阶段完整版。
---

# gstack-spec（minimal）

> 本期是自包含 minimal 版。上游来源：garrytan/gstack 的 /spec（MIT），计划 2 vendor 完整版并记录上游 commit。

## 步骤
1. 与用户澄清：为什么做（Why）、范围（Scope）、技术约束（Technical）。
2. **必读相关代码**后再列文件清单（Files）。
3. 产出 spec 文件，结构严格如下（bridge-builder 依赖此结构解析）：

```markdown
# Spec: <功能名>

## Why
<动机>

## Scope
**In scope:**
- <要做的事>

**Out of scope:**
- <明确不做的事>

## Technical
- <技术决策>

## Files
- <将创建/修改的文件>
```

## 铁律
- Files 列表里测试文件名须含 `test` 或 `spec`（contract-builder 据此识别测试义务）。
- 产出后进入 `bridging` 状态，调用 `bridge-builder`。
