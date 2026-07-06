---
name: workflow-start
description: gstack-superflow 唯一入口。读取 .gstack-superflow.yaml 判断当前状态（thinking/planning/specifying/bridging/executing/reviewing/debugging/closing），结合 Gstack 产物与 handoff-contract 内容做内容级判断，路由到下一个正确的 skill。阻止非法跳转（由 guard.mjs 强制）。
---

# workflow-start

你是 gstack-superflow 的状态路由器。每次会话开始或不确定状态时，先跑这里。

## 路由规则（内容级，非时间戳）
读取 `.gstack-superflow.yaml` 得当前 `phase`，再按产物内容判断真实位置：

| 当前 phase | 判断条件 | 路由到 |
|---|---|---|
| thinking | 无 design doc | Gstack `/office-hours` |
| planning | 有 design doc，无 reviewed plan | Gstack `/autoplan` |
| specifying | 有 reviewed plan，无 spec | Gstack `/spec` |
| bridging | 有 spec，无 handoff-contract.md | `bridge-builder` |
| bridging | 有 handoff 但 `handoff_approved: false` | 请用户批准（DP-3） |
| executing | handoff 已批准，plan 未完成 | Superpowers `writing-plans` → `executing-plans` |
| reviewing | plan 完成 | Superpowers `code-reviewer` |
| debugging | 发现 bug | Superpowers `systematic-debugging` |
| closing | review 通过 | Superpowers `verification` + Gstack `/ship` |

## 铁律
- 进入 `executing` 前必须确认 `handoff_approved: true`，否则 `guard.canExecute` 拒绝。
- 调用 guard 校验每次转移：
  ```bash
  gsf validate
  ```
  退出码非 0 则停止，修正状态。

## 快速路径（一期预留，计划 2 实现）
- hotfix（≤2 文件）：最小 handoff → inline 执行
- tweak（≤4 文件，纯配置/文档）：跳过规划+桥接
