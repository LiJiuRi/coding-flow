# OpenSpec × Superpowers 桥接原理分析报告

> 问题：哪个子项目采用"桥接"方式结合 OpenSpec 与 Superpowers？桥接的原理是什么？
> 分析对象：`openflow`（编排器）｜`spec-superflow`（融合器）｜`comet`（平台）
> 证据基线：三份详细分析报告 + 当前 checkout 的子项目源码（`skills/`、`docs/`、`templates/`、`src/parsing/`）
> 生成日期：2026-07-05
> 配套文档：[工作流对比分析报告](./工作流对比分析报告.md)｜[openflow 详细分析报告](./openflow-详细分析报告.md)｜[spec-superflow 详细分析报告](./spec-superflow-详细分析报告.md)

---

## TL;DR（结论先行）

1. **三个子项目都结合了 OpenSpec + Superpowers**，但结合策略是光谱分布的三种：`openflow`（编排器）→ `spec-superflow`（融合器）→ `comet`（平台），从轻到重。
2. **真正"采用桥接方式结合 OpenSpec 和 Superpowers"的是 `openflow`** —— 它是松耦合的**系统间桥接**：两个上游系统保持各自独立完整，openflow 自己不嵌入任何上游代码，只作为中间的"桥"做调度、翻译、状态读取。
3. **"桥接"一词在仓库里有两层含义，必须区分**，否则会把 `spec-superflow` 误判成"桥接项目"：
   - **系统间桥接**（`openflow`）：在两个独立的外部上游之间架桥，松耦合，谁都不吃掉谁。
   - **阶段间桥接**（`spec-superflow` 的 `contract-builder` / `execution-contract.md`）：项目**内部**"规划阶段 → 执行阶段"的交接层。spec-superflow **结合两个上游的方式是"源码级融合"，不是桥接**；它的"桥接"指的是自家工作流阶段之间的桥。
4. `comet` 是"调用 + 自带引擎 + Skill 创作"的平台，与"桥接"范式无关。

---

## 1. 为什么这个问题需要先澄清"桥接"的含义

用户问的是"哪个子项目**采用桥接的方式结合** openspec 和 superpower"。这里有两个容易混淆的点：

| 混淆点 | 真相 |
|---|---|
| "三个项目都结合了 OpenSpec+Superpowers，所以三个都是桥接？" | ❌ 否。结合方式分**编排 / 融合 / 平台**三种，只有"编排"是严格意义的桥接。 |
| "spec-superflow 的 README/state-machine 里到处写着 `bridging`、`contract-builder 桥接层`，它不就是桥接项目吗？" | ⚠️ 张冠李戴。spec-superflow 的"桥接"指**它内部规划→执行的阶段交接**；它结合两个上游的方式是**融合**（吸收源码），不是桥接。 |

软件工程里 **bridge（桥接）模式** 的本质是：**让两个独立子系统协作，同时保持各自可独立变化**——中间加一层适配/翻译，谁都不把谁吃掉。用这个定义去对照三个项目，只有 `openflow` 完全符合。

---

## 2. 三种整合策略光谱（理解"桥接"的总钥匙）

> 引自 [`reports/工作流对比分析报告.md`](./工作流对比分析报告.md) §2。

三者同源（都引用 `Fission-AI/OpenSpec` + `obra/superpowers`），但对"如何整合 + 整合到什么程度"给出了从轻到重的三个答案：

```
   轻 ◀──────────────────────────────────────────────▶ 重
   │                                                    │
   openflow            spec-superflow              comet
  编排器  ────────────  融合器  ──────────────────  平台
 (Orchestrator)   (Source-Level Fusion)        (Platform)

 与上游关系：  调用            吸收                调用 + 自带引擎
 上游是否独立： 是（两端独立）   否（被吃进体内）     部分（OpenSpec 独立 / 引擎自带）
 是否"桥接"：  ✅ 是             ❌ 融合              ❌ 平台
 自身代码量：  极小              较大（含引擎）       最大
```

| 维度 | openflow（桥接） | spec-superflow（融合） | comet（平台） |
|---|---|---|---|
| **与上游的关系** | 调用 | 吸收源码 | 调用 + 自带引擎 |
| **上游是否独立保留** | ✅ 两端各自完整 | ❌ 引擎被重写进自身 | 部分 |
| **是否需要预装上游** | ✅ 必须（缺失则降级） | ❌ 不需要（自包含） | archive 依赖 OpenSpec |
| **上游版本跟随** | 自动（调最新 CLI） | 手动（重新吸收） | OpenSpec 自动 / Superpowers 经 `npx skills add` |
| **结合方式的范式** | **桥接（bridge）** | 融合（fusion） | 平台（platform） |

> 一句话：**"桥接"要求两端独立，而 spec-superflow 把两端融进了自己——所以它不是桥接项目，尽管它内部有个叫"桥接"的阶段。**

---

## 3. 主答案：openflow 的桥接原理

### 3.1 桥接的本质：松耦合、不嵌入、只调度

`openflow/README.zh-CN.md` 明确宣告（证据：`README.zh-CN.md:181`）：

> "openflow 是**独立编排器** — 不捆绑、不分叉、不嵌入任何项目的代码。依赖在 init/运行时检测，任一缺失时降级为手动模式。"

代码层面坐实这一点：`openflow/package.json:45-51` 的 dependencies 只有 5 个 UI/解析库（`chalk`/`commander`/`inquirer`/`ora`/`yaml`），**没有任何 OpenSpec 或 Superpowers 代码依赖**。openflow 的"桥"不持有任何一端的实现，只持有"如何让两端在正确时刻出场"的指令。

### 3.2 桥的拓扑：两端独立 + 中间极薄层

```
        ┌─────────────────────────┐         ┌──────────────────────────┐
        │   端 A：OpenSpec        │         │   端 B：Superpowers      │
        │   （规划引擎）           │         │   （执行纪律）            │
        │                         │         │                          │
        │ • 外部进程 openspec CLI  │         │ • 文件系统中的 skill 文件 │
        │ • 通过 PATH 调用         │         │ • <skillsDir>/           │
        │ • 产物：proposal/specs/ │         │   writing-plans/SKILL.md │
        │   design/tasks          │         │ • TDD / 子代理驱动        │
        └────────────▲────────────┘         └─────────────▲────────────┘
                     │                                      │
                     │ ① 探测存在          ③ 委托执行
                     │   (cmdExists)         (build 委托 writing-plans)
                     │                                      │
        ┌────────────┴──────────────────────────────────────┴────────────┐
        │                      openflow（桥）                              │
        │                                                                  │
        │  桥墩①：dependency-check.ts   ← 探测两端是否在位                  │
        │  桥墩②：skill-generator.ts    ← 把 9 个模板(指令)分发到 AI 工具   │
        │  桥墩③：workflow-status.ts    ← 读文件系统状态做门禁             │
        │  桥面 ：plan-ready.md          ← 把 A 的规格语言翻译给 B          │
        └──────────────────────────────────────────────────────────────────┘
```

桥的核心特征：
- **两端不知道彼此存在**，也不知道桥的存在。OpenSpec 不知道有个 Superpowers，反之亦然。
- **桥不持有任何一端的代码**，只持有调度指令（markdown 模板）和翻译产物（plan-ready.md）。
- **两端可独立升级/替换**：OpenSpec 升级到新版本，openflow 自动用最新规则（调用最新 CLI）；换一个 TDD 框架，只要 build.md 模板改委托目标即可。

### 3.3 桥墩①：依赖检测——不嵌入，只探测

桥的第一职责是确认"两端在不在"。openflow 对两端用**完全不同**的探测策略（证据：`src/core/dependency-check.ts`、`src/utils/shell.ts:44-59`）：

| 端 | 探测策略 | 代码 |
|---|---|---|
| **OpenSpec** | PATH 遍历找 `openspec` 可执行文件 + `openspec --version` | `cmdExists('openspec')` |
| **Superpowers** | 文件存在性检测 `<skillsDir>/writing-plans/SKILL.md` | `fs.accessSync` |

注意这是"探测"不是"依赖"——npm 依赖表里没有它们。任一端缺失，桥不崩，而是**降级**（OpenSpec 缺 → 手动建 `openspec/changes/`；Superpowers 缺 → 手动拆解 plan-ready.md 步骤）。

> ⚠️ 桥的一个已知结构缺陷：`cmdExists` 不尝试 Windows 的 `.cmd` 扩展名（`shell.ts:51`），而 npm 全局包在 win32 上通常是 `openspec.cmd`——**这正是"调用外部进程"这种桥接方式必须承担的代价**（融合器 spec-superflow 就没有这个问题，因为它把引擎吃进去了）。

### 3.4 桥墩②：模板分发——指令即桥面

openflow 自身代码不写任何业务逻辑，只把 9 个 markdown 模板（`templates/*.md`）分发到各 AI 工具的 skills 目录（`.claude/skills/`、`.codex/skills/`、`.cursor/skills/`、`.opencode/commands/`）。

真正的"产品逻辑"——每个阶段做什么、产出什么、禁止什么、如何调用两端——**全部写在 markdown 里，由 AI 在运行时执行**（证据：`src/core/skill-generator.ts`）。

> 这意味着桥的"约束"是**软约束**：依赖 AI 忠实执行 markdown 指令去调用两端。这是松耦合桥接的根本代价——没有运行时强制，只有事后冲突检测（`workflow-status.ts` 的 `detectWorkflowConflicts`）。

### 3.5 桥墩③：状态读取——文件系统是唯一事实源

桥不维护自己的状态数据库，而是**从两端的产物文件推断状态**（证据：`src/core/workflow-status.ts`）。状态来源优先级：`workflow-status.md` > 文件系统扫描 > 会话记忆。

文件推断回退阶梯（`synthesizeWorkflowStatus`）展示桥如何"读懂"两端进度：

| 优先级 | 文件系统条件 | 推断状态 | 推荐下一步 |
|---|---|---|---|
| 1 | 实现计划全勾选 | build / ready | `/openflow close` |
| 2 | 计划存在未全勾 | build / in_progress | `/openflow build` |
| 3 | `plan-ready.md` 存在 | spec / ready | `/openflow build` |
| 4 | `proposal.md` 存在 | capture / ready | `/openflow spec` |
| 5 | 全无 | capture / pending | `/openflow proposal` |

桥通过读 OpenSpec 端的 `proposal.md`/`specs/`/`tasks.md` 和 Superpowers 端的 plan checkbox，拼出整条流水线的位置——这只有在"两端独立、产物落盘"的桥接拓扑下才成立。

### 3.6 桥面：plan-ready.md 翻译层（桥接的核心机制）

**这是 openflow 桥接最重的设计**，也是理解"桥接原理"的关键。

**为什么要翻译？** 因为两端语言不通——`templates/spec.md:82` 反复强调：

> "Superpowers 本身不会自动读取 `openspec/config.yaml`；上下文必须通过 `plan-ready.md` 传递给 `writing-plans`。"

即：**如果不显式把 OpenSpec 端的规格/规则翻译复制进 plan-ready.md，这些信息就会在 Superpowers 端执行时丢失**。这是"桥接两个独立系统"必须付出的代价——也正是 `plan-ready.md` 作为"桥面"存在的根本理由。

**桥面如何承载翻译？** spec 阶段把 OpenSpec 规格按 7 条规则翻译成 plan-ready.md，强制 12 段结构（证据：`templates/spec.md:86-177`）：

```
plan-ready.md（桥面：OpenSpec 规格 ──翻译──▶ Superpowers handoff）
├── ## 来源                         ← 追溯到 OpenSpec change
├── ## Project Context              ← 从 config.yaml 显式复制（防 Superpowers 丢失）
├── ## Applicable OpenSpec Rules    ← 从 config.yaml 显式复制
├── ## Goal / Non-Goals
├── ## Source Coverage              ← OpenSpec requirement/scenario/task → 验收点 → 实现切片
├── ## File Responsibility Map      ← 文件 → 操作 → 职责 → 关联切片
├── ## Implementation Slices        ← 每切片含 TDD 3 步、验证命令、完成标准（按执行依赖排序！）
├── ## Verification Plan
├── ## Blockers / Clarifications
└── ## Superpowers Handoff          ← 明确告诉 Superpowers writing-plans 如何消费
```

**翻译的 7 条铁律**（`templates/spec.md:86-93`）节选：
1. 覆盖每个 requirement/scenario/task，不得只转写 tasks.md 标题
2. 每 Task 拆成可独立交付的 implementation slices
3. 明确 TDD 期望（先写失败测试 → 实现 → 验证）
4. **按执行依赖排序，不是按功能模块排序**
5. 记录来源路径和 task/requirement/scenario 映射
6. 不确定项写入 Blockers，不得隐藏为模糊步骤

桥面之所以是"桥面"，因为它**同时被两端理解**：OpenSpec 端（spec 阶段）按规则生成它，Superpowers 端（build 阶段）按它展开成 2-5 分钟 checkbox 步骤执行 TDD。它消除了两端语言不通的问题。

### 3.7 桥的两端如何被驱动

| 阶段 | 桥驱动哪一端 | 如何驱动 |
|---|---|---|
| init | OpenSpec | `openspec init --tools ...`（PATH 调用 CLI） |
| spec | OpenSpec | `openspec validate <change> --strict` + 生成 plan-ready.md（翻译） |
| build | **Superpowers** | 委托 `writing-plans` skill，以 plan-ready.md 为输入生成实现计划并 TDD 执行 |
| close | OpenSpec | `openspec archive <change> --yes`（PATH 调用 CLI） |

桥的 8 阶段流水线本质是"**交替唤醒两端**"：规划阶段唤醒 OpenSpec 端，执行阶段唤醒 Superpowers 端，归档阶段再回到 OpenSpec 端。plan-ready.md 是规划端→执行端交接处的那块桥板。

### 3.8 端到端桥接数据流

```
[OpenSpec 端]                          [桥：openflow]                       [Superpowers 端]
config.yaml ──────▶ init 沉淀项目上下文 ──────────────────────────────────▶ (无)
proposal.md ──────▶ proposal 捕获需求   ──────────────────────────────────▶ (无)
specs/design/tasks▶ spec 调 OpenSpec validate ──▶ plan-ready.md（翻译）────▶ (等待)
                   │                                                   │
                   │  ◇ 用户确认 plan-ready ◇                           │
                   ▼                                                   ▼
                   │  build 把 plan-ready 作为 handoff  ──────────────▶ writing-plans 生成计划
                   │                                                   │  → TDD RED/GREEN/REFACTOR
                   │                                                   │  → 每 task 一 commit
tasks.md 勾选 ◀────┤  close 读两端状态做一致性校验 ◀──────────────────── plan checkbox 全勾
archive ◀──────────┴─ `openspec archive --yes`（含归档依赖检查门禁）
```

### 3.9 桥接的代价

松耦合桥接不是免费的，openflow 付出了三类代价（这也是它与融合器/平台的本质差距）：

| 代价 | 表现 |
|---|---|
| **约束是软的** | 全部门禁写在 markdown，依赖 AI 服从；只有事后冲突检测，无运行时强制（对比：spec-superflow 有 guard.mjs exit code，comet 有 PreToolUse 物理拦截）。 |
| **依赖外部环境** | 必须预装 OpenSpec（+推荐 Superpowers），且有 Windows PATHEXT 检测隐患（`shell.ts:51`）。 |
| **桥面翻译是手动的** | plan-ready.md 需 AI 按规则生成，一旦翻译不全（漏复制 config.yaml 规则），Superpowers 端就丢失上下文——这是双系统桥接的结构性脆弱点。 |

---

## 4. 对照：spec-superflow 的"桥接"是另一回事

这一节防止最常见的误读：**看到 spec-superflow 满屏 `bridging`/`contract-builder 桥接层` 就以为它是"桥接结合 OpenSpec+Superpowers"的项目。**

### 4.1 它结合两个上游的方式是"融合"，不是"桥接"

证据（`spec-superflow/README.md`，当前 v0.8.9）：

> "源码级融合 OpenSpec 规划引擎 + Superpowers 执行纪律的 AI 编程工作流插件"
> "自包含插件，**不需要运行时安装 OpenSpec 或 Superpowers**"

源码层面坐实：
- **吸收 OpenSpec 引擎**：`src/schema/`、`src/parsing/`、`src/validation/` 用 TypeScript 重实现了 schema/parsing/validation（OpenSpec 的核心被重写进自身，不再是外部进程）。
- **吸收 Superpowers 纪律**：把 TDD/根因调试/验证铁律改写进 9 个 `skills/*/SKILL.md`（Superpowers 的执行纪律被内化，不再是外部 skill 文件）。
- **零运行时依赖**：clone 即用，两端都不需要预装。

**这与 openflow 完全相反**——openflow 不嵌入任何上游代码（两端独立），spec-superflow 把两端都吃进自己（两端消失）。所以 spec-superflow 结合 OpenSpec+Superpowers 的方式是 **fusion（融合）**，不是 bridge（桥接）。

### 4.2 但它内部确实有一个"桥接层"——含义完全不同

spec-superflow 的 `bridging` 是**它自家工作流状态机里的一个阶段**（证据：`docs/state-machine.md`），`contract-builder` 是这个阶段的 skill，`execution-contract.md` 是产物。

```
spec-superflow 内部状态机（这是"阶段间桥接"，不是"系统间桥接"）：

  exploring → specifying → [bridging] → approved-for-build → executing → closing
                              │
                              └─ contract-builder skill 产出 execution-contract.md
                                 把 4 份规划工件压缩成"执行契约"
```

这里的"桥接"指的是：**把"规划阶段"（OpenSpec 式的 proposal/specs/design/tasks）和"执行阶段"（Superpowers 式的 TDD/SDD/Review Gate）这两段工作流连接起来**。

`execution-contract.md` 这座"内部桥"的桥接机制（证据：`skills/contract-builder/SKILL.md`、`docs/artifact-contract.md`、`templates/execution-contract.md`）：

| 规划工件（桥的左端） | 提取 | execution-contract.md 字段（桥面） |
|---|---|---|
| `proposal.md` → Why + What Changes | → | **Intent Lock**（问题 + in/out scope） |
| `proposal.md` → Out of Scope | → | **Scope Fence** |
| `specs/` → 每个 `### Requirement:` | → | Approved Requirements / Test Obligations |
| `design.md` → Decisions | → | Architecture / Interface / Dependency Constraints |
| `tasks.md` → 编号任务组 | → | **Execution Batches** + 完成标准 + Review 时机 |

解析引擎（`src/parsing/requirement-blocks.ts`）用正则 `REQUIREMENT_HEADER_REGEX = /^###\s*Requirement:\s*(.+)\s*$/i` 抽取需求块，`change-parser.ts` 抽 Why/What Changes/Delta，自动完成"规划 → 契约"的桥面铺设，再经用户 DP-3 显式批准，才允许进入执行。

### 4.3 两层"桥接"概念对照表

| 维度 | openflow 的桥接（系统间） | spec-superflow 的桥接（阶段间） |
|---|---|---|
| **桥接对象** | OpenSpec 进程 ↔ Superpowers skill 文件（两个外部独立系统） | 规划阶段 ↔ 执行阶段（项目内部两段工作流） |
| **两端是否独立** | ✅ 各自完整、可单独升级 | ❌ 引擎已被吸收进自身 |
| **桥面产物** | `plan-ready.md`（规格→handoff 翻译） | `execution-contract.md`（4 工件→执行契约压缩） |
| **桥接的必要性** | 弥合"Superpowers 不读 config.yaml"的语言鸿沟 | 锁死意图 + 需求覆盖交叉校验 + 用户批准门禁 |
| **哲学** | 松耦合、不嵌入、可组合 | 高内聚、自包含、强约束 |
| **结合上游的方式** | **桥接**（bridge） | **融合**（fusion，不是桥接） |

> 一句话区分：**openflow 是"在 OpenSpec 和 Superpowers 之间架桥"；spec-superflow 是"把 OpenSpec 和 Superpowers 融进自己，再在自家的规划与执行之间架一座内部小桥"。**

---

## 4.4 contract-builder 桥接层实现剖析（深度）

> 配套架构图（自包含 HTML，浏览器打开后可一键导出 PNG / PDF）：
> - 🟥 [图① contract-builder 桥接层数据流与组件](./images/bridge-01-data-flow.html) — 4 工件 → 解析引擎 → contract-builder（映射 + 覆盖校验）→ execution-contract.md → DP-3 → build-executor 全链路
> - 🟥 [图② guard.mjs 硬门禁状态机](./images/bridge-02-guard-state-machine.html) — 转移矩阵 + 六维度 check + workflow 模式跳过 + 双层 stale 检测
> - 🟪 [图③ execution-contract.md 结构解剖](./images/bridge-03-contract-anatomy.html) — 7 大节 + Artifact Mapping 来源 + 消费方 + Coverage Check

这一节把 spec-superflow 内部那个"阶段间桥接层"从代码层面拆开。它解决的核心工程问题是：**如何把 4 份发散的规划工件，不可逆地压缩成一份可被强制执行、可被机器校验、且锁死意图的契约，作为"规划 → 执行"的唯一交接层。**

### 4.4.1 桥接层在状态机中的位置

`bridging` 是 spec-superflow 八状态机里**唯一连接规划与执行**的阶段（[`docs/state-machine.md`](../spec-superflow/docs/state-machine.md)）。它的活跃 skill 是 `contract-builder`，产物是 `execution-contract.md`。状态机对它施加最严的转移约束（见 4.4.6）——没有这个产物且未被用户批准，任何实现都不允许开始。

> 见 [图①](./images/bridge-01-data-flow.html) 中部 rose 色虚线框「bridging 桥接阶段」。

### 4.4.2 输入：4 份规划工件（spec-writer 产出）

桥接的左端是 `spec-writer` 在 `specifying` 阶段产出的 4 份工件（[`skills/spec-writer/SKILL.md`](../spec-superflow/skills/spec-writer/SKILL.md)），每份都有强结构约束，且须通过 **DP-2 工件审查**门禁：

| 工件 | 强制结构 |
|---|---|
| `proposal.md` | `## Why`(>50字) + `## What Changes` + `## Scope`(In/Out) + `## Impact` + `## Capabilities` |
| `specs/` | 每需求 `### Requirement:` 用 SHALL/MUST + 至少一个 `#### Scenario:` WHEN/THEN，分组在 ADDED/MODIFIED/REMOVED/RENAMED Requirements 下 |
| `design.md` | `## Context` + `## Goals` + `## Decisions`(Choice+Rationale+Alternatives) + `## Risks And Trade-Offs` |
| `tasks.md` | `## File Structure` + `## Interfaces`(跨批 Consumes/Produces) + 编号任务(每步 2-5min、TDD 5 步、零占位、显式依赖) |

工件逐个生成、逐个 DP-2 确认，防止"proposal 有错 → 下游全错"的级联漂移。

### 4.4.3 解析引擎：自动提取而非手工抄写

contract-builder 不是让 AI 凭印象抄写 4 份工件，而是**用内嵌的解析引擎自动提取字段**（`src/parsing/`）——这正是 spec-superflow"源码级融合 OpenSpec 引擎"的落点：

- [`requirement-blocks.ts`](../spec-superflow/src/parsing/requirement-blocks.ts)：用正则 `^###\s*Requirement:\s*(.+)\s*$` 抽取每个需求块；`parseDeltaSpec` 解析 ADDED/MODIFIED/REMOVED/RENAMED 四类增量，含 `parseRemovedNames`（被删需求名）与 `parseRenamedPairs`（FROM/TO 重命名对）。
- [`change-parser.ts`](../spec-superflow/src/parsing/change-parser.ts)：`extractSection` 抽 `## Why` / `## What Changes`，正则 `\b${heading}\b` 支持**双语标题**（如 `## 背景（Why）`），让中文 spec 也能解析；并抽 delta 段。

> 这是 spec-superflow 与 openflow 的根本差异之一：openflow 把解析完全委托给外部 `openspec` CLI；spec-superflow 把解析逻辑吃进了自己（含中英文 tokenizer）。

### 4.4.4 contract-builder skill 的三步工作

[`skills/contract-builder/SKILL.md`](../spec-superflow/skills/contract-builder/SKILL.md) 定义桥接 skill 做三件事：

1. **Artifact Mapping**（工件 → 字段映射）——把 4 份工件结构化映射到契约字段：

   | 来源 | 提取 | → 契约字段 |
   |---|---|---|
   | `proposal.md` Why + What Changes | → | Intent Lock（问题 + scope）|
   | `proposal.md` Out of Scope | → | Scope Fence |
   | `specs/` 每个 `### Requirement:` | → | Approved Requirements + Scenarios + Test Obligations |
   | `design.md` `## Decisions` | → | Architecture / Interface / Dependency Constraints |
   | `tasks.md` 编号任务组 | → | Execution Batches + 完成标准 + Review 时机 |

2. **需求覆盖交叉校验（Coverage Check）**——桥接层最关键的防漏机制：
   - 列出 `specs/` 中**每一个** SHALL/MUST；
   - 验证每个都有 ① Approved Behavior 条目 ② 测试义务 ③ 出现在至少一个 batch；
   - **未映射需求 → flag 到 §9 Escalation Rules，不静默丢弃**；
   - 标注跨 batch 依赖。

3. **压缩生成 execution-contract.md**：原则是**压缩优先，不复述规划细节**——只留"可被 guard 检查、可被执行消费"的执行输入。

> Guardrails（铁律）：模糊未决 → 不放行；不替用户批准；不因规划文档"看起来完整"就跳过；不静默丢需求。

### 4.4.5 产物：execution-contract.md 的 7 大节

[`templates/execution-contract.md`](../spec-superflow/templates/execution-contract.md) 定义桥接产物的强制结构（见 [图③](./images/bridge-03-contract-anatomy.html)）：

| § | 节 | 作用 | 来源 → 消费 |
|---|---|---|---|
| 1 | **Intent Lock** | 锁死 变更名/问题/范围内/范围外 | proposal → build-executor |
| 2 | **Approved Behavior** | 需求摘要 + 场景 + 验收 + **Coverage Check** | specs → build-executor |
| 3 | **Design Constraints** | 架构/接口/依赖/数据约束 | design → build-executor |
| 4 | **Task Batches** | 每批 目标/输入/输出/完成标准/依赖/并行性 | tasks → build-executor |
| 5 | **Test Obligations** | 必须先失败测试的行为 + 边界 + 回归敏感区 | specs(SHALL/MUST) → build-executor(TDD) |
| 6 | **Execution Mode** | Inline / Batch Inline / SDD + 理由（DP-4） | tasks 规模 → build-executor |
| 7 | **Verification Dimensions** | Completeness / Correctness / Coherence 三维 | → code-reviewer / release |
| — | **Review Gates** | 强制审查点 + 阻塞类别(Critical/Important) | → code-reviewer |
| — | **Escalation Rules** | 何时回退 specifying/bridging/不得继续 | → release-archivist |

### 4.4.6 硬门禁：DP-3 + guard.mjs 转移矩阵

桥接层的约束力来自两层：**软约束**（SKILL.md 铁律）+ **硬约束**（guard.mjs exit code）。

**DP-3 契约批准**（[`docs/decision-points.md`](../spec-superflow/docs/decision-points.md)）：contract-builder 生成契约后，必须暂停、向用户呈现全文、等待**显式 approve**，记录到 `dp_3_result`。这是硬门禁，不可跳过。

**guard.mjs 转移矩阵**（[`scripts/guard/guard.mjs`](../spec-superflow/scripts/guard/guard.mjs) `TRANSITION_CHECKS`）——每条状态转移要求若干 check 维度，任一失败 `exit 1` 拦截（见 [图②](./images/bridge-02-guard-state-machine.html)）：

| 转移 | 要求的 check 维度 |
|---|---|
| `specifying → bridging` | artifacts-exist + schema-valid |
| **`bridging → approved-for-build` ★** | artifacts-exist + schema-valid + **contract-fresh** + **dp-gate-passed** |
| `approved-for-build → executing` | artifacts-exist + contract-fresh + dp-gate-passed |
| `executing → closing` | tasks-complete + tests-passing |

`bridging → approved-for-build` 是**最严的一跳**（4 维度全要求）。两个桥接专属维度：

- **contract-fresh**（[`checks/contract-fresh.mjs`](../spec-superflow/scripts/guard/checks/contract-fresh.mjs)）：调 `isContractFresh()`，比对 `.spec-superflow.yaml` 中存的 `artifacts_hash` 与当前工件 hash；不匹配 → "execution-contract.md is stale... Re-run contract-builder"。
- **dp-gate-passed**（[`checks/dp-gate-passed.mjs`](../spec-superflow/scripts/guard/checks/dp-gate-passed.mjs)）：`bridging→approved-for-build` 要求 `dp_3_result` 非空；`approved-for-build→executing` 要求 `dp_4_result` 非空。

### 4.4.7 双层 stale 检测（防漂移）

contract-fresh 体现 spec-superflow 的**双层过时检测**哲学（对比 openflow 只用文件存在性/时间戳推断）：

- **快层 · 哈希**：`.spec-superflow.yaml` 存 `artifacts_hash`（4 工件 SHA256）+ `contract_hash`（契约 SHA256），比对 O(1)。
- **慢层 · 语义回退**：内容级判断——proposal scope 变了 / specs 需求改了 / design 约束变了 / tasks 批次变了 → 视为过时。

状态文件注释明确：`# Derived data. Always rebuildable from artifacts. Lost/corrupt → fall back to content-level detection.`——状态文件本身是派生数据，丢失/损坏可从工件重建，**不把状态文件当唯一事实源**。drift 一旦检出 → rewind 回 bridging 重生契约。

### 4.4.8 workflow 模式：维度跳过

`guard.mjs --workflow <mode>` 让小型变更跳过部分维度（`applyWorkflowMode`）：

| 模式 | 跳过的维度 | 含义 |
|---|---|---|
| `full`（默认） | — | 全维度，大型变更 |
| `hotfix`（≤2 文件） | schema-valid | 跳过 schema 校验；最小契约仅需 Intent Lock + Tasks + DP-3 |
| `tweak`（≤4 文件 纯配置/文档） | schema-valid + contract-fresh + artifacts-exist | 跳过规划 + 桥接，直接编辑 |

跳过的维度标记 `skipped:true, pass:true`——**不阻塞但显式留痕**，不静默放过。无效 workflow 值 → `exit 2`（参数白名单 `full|hotfix|tweak`）。

### 4.4.9 真实实例：v0.6.0-fast-and-aware

以仓库内真实变更 [`changes/v0.6.0-fast-and-aware/`](../spec-superflow/changes/v0.6.0-fast-and-aware/) 为例：

- `.spec-superflow.yaml`：`state: approved`、`workflow: full`，`artifacts_hash` + `contract_hash` 均已落盘（SHA256）。
- `execution-contract.md`（10.2KB）Coverage Check 实测：**15 requirements → 15 mapped to test obligations ✅ → all represented in batches ✅ → 0 unmapped**。
- 5 个 batch（含并行性 DAG：Batch 2/3 可并行），Execution Mode 选 `SDD`（理由：Batch 2/3 仅依赖 Batch 1，可分派子代理）。

这印证 Coverage Check 不是文档口号，而是生成时强制、可被检查的约束。

### 4.4.10 消费侧：build-executor 如何工作

契约经 DP-3 批准后，`build-executor` 以它为 authority 执行（[`skills/build-executor/SKILL.md`](../spec-superflow/skills/build-executor/SKILL.md)）：

- **Law 1 Contract First**：契约是 approved handoff，非聊天记录。
- **Law 2 TDD 铁律**：无失败测试先于产码（RED → GREEN → REFACTOR）。
- **Law 3 Review Before Drift**：拦截逻辑缺陷 / 规格违反 / 缺测试 / scope 膨胀。
- **Law 4 Rewind on Contract Break**：新行为 / 接口变 / 假设失败 → 回 bridging 重生契约。

执行模式按契约 §6 自动选：Inline（≤3 任务）/ Batch Inline（同模块）/ SDD（多 batch，子代理驱动 + 双层审查）。每 task 一 commit，进度写 `.superpowers/sdd/progress.md` 防会话压缩丢失。

### 4.4.11 小结：这个"内部桥接层"的工程价值

spec-superflow 的 contract-builder 桥接层把"规划 → 执行"这个最容易跑偏的交接点，做成了**一份可校验、可批准、可追溯、防漂移的硬契约**：

- **可校验**：解析引擎自动提取 + Coverage Check 不漏需求 + guard.mjs exit code 强制；
- **可批准**：DP-3 硬门禁保留用户最终决策权；
- **可追溯**：每个字段可回溯到源工件，每条转移有 check 证据；
- **防漂移**：双层 stale 检测 + rewind 机制，契约过时强制重生。

这是它与 openflow（`plan-ready.md` 软翻译）、comet（`design-context.json` handoff + SHA256）在"规划→执行桥梁"维度上最差异化的工程化创新——横向对比详见 [《工作流对比分析报告》§4.2](./工作流对比分析报告.md)。

---

## 5. comet 为何不是桥接

`comet` 把自己定位为"Agent Skill 运行时平台"（`comet/docs/architecture/ARCHITECTURE.md:7`）：

- **Node-only runtime**：7 个 `.mjs` 启动器由 TS 源码 esbuild 打包，自带确定性状态机引擎（8 transition 事件 + Classic Resolver + 12 step evidence 契约，纯函数无 LLM）。
- **调用 + 自带并存**：archive 仍调用外部 `openspec archive` CLI（像 openflow 那样调用），但状态机/引擎/校验全部自带（像 spec-superflow 那样拥有），是两者的混合策略。
- **独有 Skill 创作与分发**：`/comet-any` + Bundle 控制平面，能造自己的 Skill 并分发到 33 个平台——这是 openflow 和 spec-superflow 都没有的维度。

comet 是"平台"范式：既不是纯桥接（它自带引擎），也不是纯融合（它仍调用外部 OpenSpec），更不是"两者结合"那么简单——它把工作流做成可创作、可分发、可校验、可恢复的运行时平台。详见 [`reports/工作流对比分析报告.md`](./工作流对比分析报告.md) §2.3、§4.7。

---

## 6. 总结

### 6.1 三者与"桥接"的关系

| 项目 | 结合 OpenSpec+Superpowers 的方式 | 是不是"桥接结合"？ |
|---|---|---|
| **openflow** | 松耦合编排，两端独立，中间翻译 | ✅ **是（系统间桥接）** |
| **spec-superflow** | 源码级融合，吸收两端引擎 | ❌ 融合（但内部有阶段间桥接层） |
| **comet** | 调用 + 自带引擎 + Skill 创作 | ❌ 平台 |

### 6.2 桥接原理（openflow）一句话总结

> **openflow 是一座架在 OpenSpec（规划引擎）和 Superpowers（执行纪律）之间的"极薄之桥"：它不嵌入任何一端的代码，只做三件事——探测两端是否在位（dependency-check）、把调度指令分发出去（9 个 markdown 模板）、读两端产物推断状态（workflow-status）；并用 `plan-ready.md` 作为桥面，把 OpenSpec 的规格语言翻译成 Superpowers 能消费的实现交接文档，让两个彼此不知道对方存在的独立系统，通过这座桥交替出场，拼成一条 spec→build→close 的完整流水线。代价是：约束是软的（依赖 AI 服从 markdown）、依赖外部环境（PATH/PATHEXT）、桥面翻译必须人工保证完整。**

### 6.3 一个值得注意的趋势

三者的优势其实互补：**openflow 的松耦合（可组合）+ spec-superflow 的 execution-contract 意图锁（阶段间桥接）+ comet 的 hook-guard 物理门禁与确定性状态机（强约束与可恢复）**，理论上可以融合成"轻量编排 + 意图契约 + 物理级硬门禁 + 确定性可恢复"的更优形态。（详见对比报告 §9.3、§结论。）

---

## 附：证据索引

**openflow（桥接）**
- `openflow/README.zh-CN.md:181` —— "独立编排器，不捆绑、不分叉、不嵌入任何项目的代码"
- `openflow/package.json:45-51` —— dependencies 只有 5 个 UI/解析库，零上游代码依赖
- `openflow/src/core/dependency-check.ts` —— OpenSpec（cmdExists）/ Superpowers（文件存在性）双策略探测
- `openflow/src/utils/shell.ts:44-59` —— cmdExists 实现 + Windows PATHEXT 隐患
- `openflow/src/core/skill-generator.ts` —— 9 模板分发到 4 平台 skills 目录
- `openflow/src/core/workflow-status.ts` —— 双源解析 + 文件推断回退阶梯 + 冲突检测
- `openflow/templates/spec.md:82-177` —— "Superpowers 不读 config.yaml" + plan-ready 翻译 7 规则 + 12 段结构
- `openflow/templates/build.md` —— 委托 Superpowers `writing-plans` 以 plan-ready 为输入 TDD 执行
- 完整证据链见 [`reports/openflow-详细分析报告.md`](./openflow-详细分析报告.md)

**spec-superflow（融合 + 内部阶段桥接）**
- `spec-superflow/README.md` —— "源码级融合""自包含，不需要运行时安装 OpenSpec 或 Superpowers"
- `spec-superflow/docs/state-machine.md` —— `bridging` 状态定义与转移图
- `spec-superflow/docs/artifact-contract.md` —— 5 工件角色 + planning→execution 映射
- `spec-superflow/skills/contract-builder/SKILL.md` —— contract-builder 桥接 skill（Artifact Mapping + 需求覆盖交叉校验 + DP-3 批准门禁）
- `spec-superflow/templates/execution-contract.md` —— 桥接产物模板（Intent Lock / Approved Behavior / Constraints / Batches / Test Obligations / Review Gates / Escalation Rules）
- `spec-superflow/src/parsing/requirement-blocks.ts` —— `### Requirement:` 块解析引擎
- `spec-superflow/src/parsing/change-parser.ts` —— Why/What Changes/Delta 抽取
- `spec-superflow/changes/v0.6.0-fast-and-aware/execution-contract.md` —— 真实桥接产物实例

**横向分类**
- [`reports/工作流对比分析报告.md`](./工作流对比分析报告.md) §2（编排器/融合器/平台）、§4.2（规划→执行桥梁三态对比）、§4.3（引擎策略）、§4.4（约束力光谱）
