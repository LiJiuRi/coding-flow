# gstack-superflow 设计文档

| 项 | 值 |
|---|---|
| 日期 | 2026-07-06 |
| 状态 | 设计已批准，待实现计划 |
| 项目名 | gstack-superflow |
| 范式 | 融合自包含型（对标 spec-superflow） |
| 仓库位置 | 一期：`coding-flow` 总仓内 `gstack-superflow/` 子目录原型；成熟后迁独立仓库开源发布 |

---

## 1. 背景与动机

### 1.1 本仓现状

`coding-flow` 是一个总仓（meta repository），通过 git submodule 引用三个同源开源工作流项目，并在 `reports/` 收录对它们的分析报告：

| 子项目 | 范式 | 整合对象 |
|---|---|---|
| openflow | 编排器（松耦合调用） | OpenSpec + Superpowers |
| spec-superflow | 融合器（源码吸收） | OpenSpec + Superpowers |
| comet | 平台（自带引擎 + Skill 创作） | OpenSpec + Superpowers |

三者回答同一个工程问题：**如何把规划纪律与执行纪律统一到 AI 编程工作流中**。三者规划端都用 OpenSpec。

### 1.2 本项目的出发点

- [Gstack](https://github.com/garrytan/gstack)（Garry Tan 开源，MIT）是另一条"规划/spec"路线，且偏产品/设计/多角色评审专长，与 OpenSpec 的纯规划引擎互补。
- 社区已在探索 "Gstack + Superpowers" 组合，但缺一个工程化、自包含、有约束的整合插件。
- 本项目要做的事：**把 spec-superflow 的成功范式（融合自包含 + 桥接层 + guard）移植到「Gstack + Superpowers」组合上**，作为 coding-flow 总仓的第四个研究/孵化案例。

### 1.3 Gstack 与 OpenSpec 的关键差异（决定整合方式不同）

| 维度 | OpenSpec | Gstack |
|---|---|---|
| 形态 | 带 CLI 引擎（schema/parsing/validation） | markdown skills + binary tools |
| 覆盖范围 | 纯规划 | **端到端 sprint**（Think→Plan→Build→Review→Test→Ship→Reflect） |
| 与 Superpowers 重叠 | 几乎无 | **大量重叠**（调试/评审/规划/执行/验证） |
| "吸收"可行性 | 可重实现引擎（spec-superflow 走通） | 指令可 vendor，但 binary 依赖不可重实现 |

**结论**：本项目不能照搬 spec-superflow 的"全吸收"思路，核心难题是**化解 Gstack 与 Superpowers 的全流程重叠**。

---

## 2. 目标与非目标

### 2.1 目标

1. 做一个 Claude Code 插件，clone 即用，对标 spec-superflow 可上架 marketplace。
2. 用**桥接转换层**把 Gstack 的规划产物转换为 Superpowers 可执行任务（本项目核心机制）。
3. 化解 Gstack 与 Superpowers 的重叠，定义清晰分工路由。
4. 叠加 guard（软 + 硬），保证"无批准 handoff 不允许执行"等纪律。
5. 工程化：CLI、状态机、基础测试、Windows 兼容。

### 2.2 非目标（YAGNI）

- 不自研确定性状态机引擎（那是 comet 范式）。
- 不做 Skill 创作与分发平台（那是 comet 独有能力）。
- 一期不做 Conductor 并行编排、不做浏览器 QA 集成（二期可选）。
- 不重写 Gstack 的 binary 依赖类能力（/browse、/design-shotgun 等）。

---

## 3. 核心架构：分工路由 + 桥接转换

```
[Gstack 规划段] ──产物──▶ ✦ 桥接转换层 ✦ ──可执行任务──▶ [Superpowers 执行段]
  /office-hours            handoff-contract.md             writing-plans
  /autoplan                (产物 → 任务 切片)               executing-plans
  /spec                                                    subagent-driven-dev
  /plan-*-review                                           + TDD + verification
```

### 3.1 重叠项裁决表

| 能力 | 主用 | 吸收对方什么 |
|---|---|---|
| 需求澄清 | Gstack `/office-hours`（产品级拷问） | Superpowers `brainstorming` 作为可选补充（深度技术方案探索时） |
| spec/计划 | Gstack `/spec` + `/autoplan` | Superpowers `writing-plans` 消费桥接层产出 |
| 调试 | Superpowers `systematic-debugging` | Gstack `/investigate` 的 Iron Law + 3 失败停止 |
| 规划期评审 | Gstack `/autoplan`（CEO→design→eng→DX 多角色） | — |
| 实现期评审 | Superpowers `code-reviewer` agent | 可选叠加 Gstack `/review` |
| 验证收口 | Superpowers `verification-before-completion` | Gstack `/ship` 测试门 + PR |
| 安全护栏 | 本插件 `guard.mjs` | Gstack `/careful`/`/freeze`/`/guard` 理念 |

---

## 4. 工作流状态机（8 状态）

| 状态 | 触发动作 | 退出条件 |
|---|---|---|
| `thinking` | Gstack `/office-hours` | design doc 产出 |
| `planning` | Gstack `/autoplan` | reviewed plan 产出 |
| `specifying` | Gstack `/spec`（五阶段） | spec 文件产出并归档 |
| `bridging` | `bridge-builder` 生成 `handoff-contract.md` | 用户显式批准 |
| `executing` | Superpowers `writing-plans` → `executing-plans`/SDD + TDD | plan 完成 + 测试通过 |
| `reviewing` | Superpowers `code-reviewer`（+可选 `/review`） | review 通过 |
| `debugging` | bug 时强制进入 Superpowers `systematic-debugging` | 根因修复并验证 |
| `closing` | Superpowers `verification` + Gstack `/ship` | 验证通过 + PR |

**入口**：单一 `workflow-start` skill，内容级状态检测（比较 Gstack 产物范围 vs handoff 意图锁，不看文件时间戳），路由到正确状态，阻止非法跳转。

**快速路径**（参考 spec-superflow）：
- `hotfix`（≤2 文件、无新模块）：跳过完整规划，走最小 handoff → inline 执行
- `tweak`（≤4 文件、纯配置/文档）：跳过规划+桥接，直接编辑

---

## 5. 桥接转换层（核心创新）

`handoff-contract.md` 是**转换器**，不是简单契约。它把 Gstack 的三类产物重组为 Superpowers 可执行的任务结构。

### 5.1 输入（Gstack 产物）

| Gstack 产物 | 提供什么 |
|---|---|
| `/office-hours` design doc | 产品决策、capabilities、approaches、重构后的需求 framing |
| `/autoplan` reviewed plan | 架构决策、数据流、test plan、多角色评审结论 |
| `/spec` 五阶段 spec | **scope**（in/out）、technical（含代码阅读）、**file 清单**、draft |

### 5.2 转换（提取 + 重组为 4 类字段）

| 输出字段 | 来源 | 用途 |
|---|---|---|
| **意图锁 Intent Lock** | spec scope + autoplan 决策 | 锁死 in/out scope，执行期防跑偏 |
| **任务切片 Task Slices** | spec file 清单 + autoplan 架构 | 每切片含 TDD 三步（红/绿/重构），对接 `executing-plans` |
| **测试义务 Test Obligations** | spec technical + autoplan eng review 的 test plan | 强制测试覆盖点 |
| **Review Gates** | 切片标记 | 标记哪些切片完成后需 review |

### 5.3 输出对接

`handoff-contract.md` 直接对接 Superpowers：
- 给 `writing-plans` 作为输入 → 生成最终 `plan.md`，或
- 切片结构已足够时，直接给 `executing-plans`/`subagent-driven-development` 消费

### 5.4 纪律保障

- **过时检测**（内容级，非时间戳）：Gstack 产物内容变了（scope 变/架构变/file 清单变）→ handoff 标记失效 → 强制回 `bridging` 重生。
- **批准门禁**：handoff 必须用户显式批准（对应 spec-superflow DP-3），否则 `guard.mjs` 拦截进入 `executing`。

---

## 6. 组件清单

| 组件 | 类型 | 职责 |
|---|---|---|
| `workflow-start` | skill | 入口路由，内容级状态检测，8 状态路由，阻止非法跳转（编排者） |
| Gstack vendor skills（7 个） | skill | `/office-hours`/`/autoplan`/`/spec`/`/plan-ceo-review`/`/plan-eng-review`/`/plan-design-review`/`/plan-devex-review`——吸收改写，分别承载 `thinking`/`planning`/`specifying` 状态，由 `workflow-start` 直接路由（不再单设编排层） |
| `bridge-builder` | skill | **转换器**：解析 Gstack 产物 → 生成 `handoff-contract.md` |
| `sp-executor` | skill | 路由 Superpowers `writing-plans`→`executing-plans`→SDD+TDD |
| `sp-reviewer` | skill | 路由 Superpowers `code-reviewer`，可选叠加 Gstack `/review` |
| `debug-router` | skill | 路由 Superpowers `systematic-debugging`，吸收 `/investigate` Iron Law |
| `release-closer` | skill | Superpowers `verification` + Gstack `/ship`（测试门 + PR） |
| `guard.mjs` | 脚本 | 硬门禁：状态转移合法性 + handoff 存在/批准检查，exit code 拦截 |
| `state-loader.mjs` | 脚本 | 读写 `.gstack-superflow.yaml` 状态文件 |
| `gsf` CLI | 工具 | `list/validate/doctor/state/inject/version`，对标 `ssf` |

---

## 7. Gstack skills 融合策略（已选：A 混合方案）

### 7.1 Vendor 吸收 + 改写裁剪（纯指令型，规划主干）

这些是 markdown 指令、无 binary 依赖，复制改写进本插件包，并在衔接点增强（如 `/spec` 产出后强制进 `bridge-builder`）：

- `/office-hours`、`/autoplan`
- `/spec`
- `/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/plan-devex-review`

### 7.2 运行时检测 + 可选路由（依赖 binary/浏览器/外部服务）

这些依赖 Gstack 的运行时基础设施，无法纯 vendor。本插件检测 Gstack 是否安装：装了则在对应状态可选调用，没装则降级跳过（不影响主干流程）：

- `/qa`、`/qa-only`、`/browse`、`/open-gstack-browser`（浏览器）
- `/design-shotgun`、`/design-html`（设计管线，依赖 GPT Image/Pretext）
- `/cso`（安全审计）
- `/review`（可选叠加评审）
- `/investigate`（Iron Law 吸收进 `debug-router`，运行时可选）
- `/ship`（测试门 + PR，作为 `release-closer` 的运行时增强）
- `/careful`/`/freeze`/`/guard`（理念吸收进 `guard.mjs`）

### 7.3 Superpowers 执行纪律（吸收改写）

spec-superflow 已证明可吸收改写 Superpowers 的纪律 skills，本项目同样吸收：

- `writing-plans`、`executing-plans`、`subagent-driven-development`
- `test-driven-development`、`systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`、`receiving-code-review`
- `brainstorming`（可选补充，见 §3.1 重叠裁决）

---

## 8. guard 与约束（三层）

1. **软约束**：各 SKILL.md 铁律（大写直引 + Red Flags），靠 AI 自觉。
2. **硬约束**：`guard.mjs` exit code 拦截——
   - 无 `handoff-contract.md` 或未被批准 → 拦截进入 `executing`
   - 非法状态转移 → exit=1
   - handoff 内容级过时 → 拦截执行，回 `bridging`
3. **会话引导**：session-start hooks 自动注入 `workflow-start`（参考 spec-superflow）。

---

## 9. 工程化

### 9.1 形态

- Claude Code plugin（marketplace 分发）+ npm CLI（`gsf`）。
- 多平台 manifest 单源：一期 Claude Code，预留 Cursor/Codex/OpenCode。

### 9.2 测试（吸收 spec-superflow "测试薄"教训）

- `guard.mjs` / `state-loader.mjs` / `bridge-builder` 必须有单元测试。
- 1 个 e2e 黑盒（完整跑 thinking→closing）。
- 覆盖率目标：核心脚本 ≥80%。

### 9.3 Windows 兼容

- `guard`/CLI 用 Node-only（避免 openflow 的 PATHEXT 隐患）。
- 注意 Gstack 在 Windows 需 Bun + Node（binary 类 skill 的运行时检测要处理这点）。

### 9.4 状态文件

`.gstack-superflow.yaml`：记录当前状态、handoff hash、批准标志等（参考 spec-superflow 的 26 字段 + SHA256，字段数按实际裁剪）。

---

## 10. 分期与范围

### 一期 MVP

- Claude Code 插件骨架 + plugin.json/marketplace.json
- `workflow-start` + 8 状态路由 + 内容级状态检测
- Gstack 规划段 7 个 skill（vendor 吸收）
- `bridge-builder` 桥接转换层（核心）
- Superpowers 执行段 skill（吸收改写）
- `guard.mjs` + `state-loader.mjs`
- `gsf` CLI 基础命令
- 核心脚本单测 + 1 个 e2e

### 二期（可选）

- 多平台 manifest（Cursor/Codex/OpenCode）
- Conductor 并行编排集成
- 浏览器 QA（`/qa`）运行时集成
- `/design-*` 设计管线运行时集成

### 不做

- 自研状态机引擎、Skill 创作平台（comet 范式）。

---

## 11. 命名、仓库、许可证

- **项目名**：`gstack-superflow`（对称 spec-superflow）。
- **许可证**：MIT（Gstack MIT、Superpowers MIT，吸收改写合规）。
- **仓库**：一期在 `coding-flow/gstack-superflow/` 子目录开发原型（总仓自有内容，类似 `reports/`，非 submodule）；成熟后迁独立 GitHub 仓库开源发布，并可反加为 coding-flow 的第四个 submodule。

---

## 12. 风险与未决

| 风险 | 严重度 | 缓解 |
|---|---|---|
| Gstack skills 更新需手动跟随（vendor 部分） | 中 | 在 `gsf doctor` 中加版本一致性检查；记录吸收的 Gstack commit |
| Gstack binary 类能力依赖用户预装 | 中 | 运行时检测 + 降级，主干流程不强依赖 |
| Gstack/SP 重叠裁决在实际使用中可能不顺 | 中 | 一期聚焦主干（thinking→closing），重叠项先按 §3.1 裁决，二期据反馈调整 |
| Windows 下 Gstack 需 Bun+Node | 低 | binary 类 skill 检测时提示；主干 Node-only |
| handoff 转换格式需与 Superpowers plan 对齐 | 中 | 一期先对接 `writing-plans` 输入格式，验证后考虑直连 `executing-plans` |

---

## 13. 验收标准（一期 MVP）

1. clone `coding-flow/gstack-superflow/` 后，按 README 能在 Claude Code 中加载插件。
2. 一句话（如"用 workflow-start 开始"）能进入工作流，状态检测正确路由。
3. 走完一个示例变更的 thinking→closing 全流程，产出 handoff-contract.md 并被 guard 拦截/放行正确。
4. `gsf validate/doctor` 能验证工件完整性与版本一致性。
5. 核心脚本单测通过 + 1 个 e2e 通过。

---

## 附：上游参考

- Gstack：https://github.com/garrytan/gstack （MIT）
- Superpowers：https://github.com/obra/superpowers （MIT）
- spec-superflow（范式范本）：https://github.com/MageByte-Zero/spec-superflow
- 本仓分析报告：`reports/spec-superflow-详细分析报告.md`、`reports/工作流对比分析报告.md`
