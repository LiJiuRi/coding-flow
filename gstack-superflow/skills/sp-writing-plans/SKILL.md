---
name: sp-writing-plans
description: gstack-superflow 执行段（minimal 版）。读取已批准的 handoff-contract.md，把任务切片展开为实现计划 plan.md（每个 slice 含 TDD 三步），交由 executing-plans 执行。计划 2 替换为 vendor 的 Superpowers writing-plans 完整版。
---

# sp-writing-plans（minimal）

> 本期是自包含 minimal 版。上游来源：obra/superpowers 的 writing-plans（MIT），计划 2 vendor 完整版并记录上游 commit。

## 前置
- `handoff-contract.md` 存在且 `.gstack-superflow.yaml` 中 `handoff_approved: true`。
- 否则停止：`guard.canExecute` 会拒绝执行。

## 步骤
1. 读 `handoff-contract.md`，提取 task_slices、test_obligations、review_gates。
2. 为每个 slice 展开为 TDD 三步任务（红 → 绿 → 重构），写入 `plan.md`。
3. 把 test_obligations 标为必跑测试，review_gates 标为完成后须 review。
4. 交由 Superpowers `executing-plans` / `subagent-driven-development` 执行。

## 铁律
- 不得超出 intent_lock.in_scope 范围（guard 通过 handoff 监督）。
