---
name: bridge-builder
description: 桥接转换层。读取 Gstack 规划段产物（spec / design doc），调用 contract-builder 引擎生成 handoff-contract.md（意图锁 + 任务切片 + 测试义务 + review gates），等待用户批准。在 Gstack spec 产出后、Superpowers 执行前调用。
---

# bridge-builder

你是 gstack-superflow 的桥接转换层。把 Gstack 的规划产物**转换**为 Superpowers 可执行的任务结构。

## 何时触发
- `specifying` 状态完成（Gstack `/spec` 已产出 spec 文件）后，进入 `bridging` 状态。

## 步骤
1. 读取当前项目的 Gstack 产物：
   - spec 文件（默认 `$GSTACK_STATE_ROOT/projects/$SLUG/specs/` 下最新，或项目内约定的 spec 路径）
   - design doc（`/office-hours` 产物，若存在）
2. 调用 gsf 生成 handoff（读 spec 文件，输出 handoff-contract.md 到当前目录）：
   ```bash
   gsf build-handoff <spec 文件路径>
   ```
3. 展示生成的 `handoff-contract.md` 给用户，逐项确认：意图锁、任务切片、测试义务、review gates。
4. **请求用户显式批准**（对应 spec DP-3 批准门禁）。未批准前，guard 会拦截进入 executing。
5. 用户批准后，更新 `.gstack-superflow.yaml`：`handoff_approved: true`、`handoff_path: handoff-contract.md`、`handoff_hash: <computeHandoffHash>`。

## 铁律
- 不得跳过用户批准直接进入 executing。
- Gstack 产物内容变化 → handoff 失效 → 必须重生并重新批准（`guard.isStale`）。
- handoff-contract.md 是规划→执行的**唯一**交接路径，禁止绕过它直接让 Superpowers 执行。
