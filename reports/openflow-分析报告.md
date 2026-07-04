# OpenFlow 项目分析报告

> 分析对象：`@lininn/openflow` v0.4.4 · 路径 `D:\2026_idea_project\openflow`
> 分析日期：2026-06-29 · 方法：源码逐文件精读 + 配置/模板/OpenSpec 治理文件核对

---

## 1. 项目概述

**OpenFlow 是一个面向 AI 编码工具的「规格驱动开发工作流编排器」（Spec-driven development workflow orchestrator）。**

它把两套开源体系粘合在一起，提供从**项目上下文 → 需求 → 规格 → 计划 → 实现 → 验证 → 归档**的完整闭环：

| 上游/下游 | 项目 | 作用 |
|-----------|------|------|
| 需求/规格 | [OpenSpec](https://github.com/Fission-AI/OpenSpec) (`@fission-ai/openspec`) | 生成结构化的 `proposal.md / design.md / specs/ / tasks.md` |
| 执行 | [Superpowers](https://github.com/obra/superpowers) (`writing-plans` skill) | 详细的实现计划 + TDD 执行纪律 |

OpenFlow 自身**不内嵌、不 fork**这两个项目，仅负责：检测依赖、生成可复用技能（skill）、维护工作流状态、翻译需求为工程交接物（`plan-ready.md`）。它本身又以 **npm CLI**（`openflow init/status/update`）和一组 **AI 技能**（`/openflow <phase>`）两种形态提供服务。

**核心价值**：让 Claude Code / Codex / Cursor / OpenCode 这四类 AI 编码工具，拥有一条统一、有阶段门控、有写入边界约束的规范开发路径。

---

## 2. 项目元信息

| 项 | 值 |
|----|----|
| 包名 | `@lininn/openflow` |
| 版本 | 0.4.4 |
| 许可 | MIT |
| 作者 | lininn |
| 仓库 | github.com/lininn/openflow |
| 语言 | TypeScript（strict）· Node.js ESM |
| Node 要求 | `>=18.0.0` |
| 入口 | `bin/openflow.js` → `dist/cli/index.js` |
| 测试框架 | Vitest ^4.1.8 |
| 当前分支 | main · 工作区干净（仅 `.idea/` 未跟踪） |

发布演进（CHANGELOG）：`0.3.2`(基线) → `0.3.3-beta`(测试/CI/原生API) → `0.3.4`(任务勾选同步) → `0.4.0`(grill 门控) → `0.4.1`(**workflow-status 模块**) → `0.4.2/0.4.3`(文档与图示) → `0.4.4`(close 防别名继承 guard，最近合并)。

---

## 3. 技术栈与依赖

### 运行时依赖

| 依赖 | 版本 | 实际用途 | 状态 |
|------|------|----------|------|
| `commander` | ^12.0.0 | CLI 命令装配（`init/status/update`） | ✅ 使用 |
| `inquirer` | ^13.4.3 | `openflow init` 的交互式确认提示 | ✅ 使用 |
| `chalk` | ^5.3.0 | logger 彩色前缀输出 | ✅ 使用 |
| `yaml` | ^2.4.0 | 解析 `openspec/config.yaml`（`hasTopLevelKey`） | ✅ 使用 |
| `ora` | ^8.0.0 | （loading spinner） | ⚠️ **声明但源码未使用** |

> ⚠️ **发现**：`ora` 在 `package.json` 声明，但全量检索 `src/` 无任何 import（仅 commander/inquirer/chalk/yaml 被引用）。属**未使用依赖**，可移除以减小安装体积。

### 开发依赖
`typescript@^5.5`、`vitest@^4.1.8`、`@types/node@^20`、`@types/inquirer@^9`。无 ESLint/Prettier——`npm run lint` 即 `tsc --noEmit`（类型检查即 lint，见第 12 节）。

---

## 4. 目录结构

```
openflow/
├── bin/openflow.js          # CLI 入口（5 行，调用 dist/cli/index.js）
├── src/                     # 源码（1940 行，16 文件）
│   ├── cli/                 # Command 装配 + 用户交互流程
│   │   ├── index.ts         # run()：注册 init/status/update
│   │   ├── init.ts          # 初始化主流程（218 行）
│   │   ├── status.ts        # 状态看板
│   │   └── update.ts        # 重新生成技能
│   ├── core/                # 业务规则与可持久化状态
│   │   ├── constants.ts     # 常量：依赖定义、工具路径
│   │   ├── dependency-check.ts   # 依赖检测 + 状态读写
│   │   ├── skill-generator.ts    # 技能模板生成（207 行）
│   │   └── workflow-status.ts    # 工作流状态机（354 行，核心）
│   └── utils/               # 可复用运行时助手
│       ├── shell.ts         # exec/cmdExists/fileExists/dirExists
│       └── logger.ts        # 分级日志（含 json/debug 模式）
├── templates/               # ★ 技能模板（生成内容的唯一真源）
│   ├── SKILL.md             # 主编排技能（路由/守卫/状态/边界）
│   ├── init.md proposal.md brainstorming.md grill.md
│   ├── spec.md amend.md build.md close.md   # 8 阶段文件
├── scripts/postinstall.js   # 安装后提示
├── openspec/                # ★ 项目自身的 OpenSpec 治理
│   ├── project.md           # 项目上下文
│   ├── specs/project/spec.md
│   └── changes/             # 活跃 + 归档变更
├── docs/superpowers/        # 实现计划/设计（Superpowers 产物）
├── graphify-out/            # 知识图谱分析产物（含 GRAPH_REPORT.md）
├── .github/workflows/ci.yml
├── openflow-architecture.{png,svg}  openflow-workflow.{png,svg}
└── package.json tsconfig.json vitest.config.mts
```

---

## 5. 架构分层与数据流

### 三层分层（严格职责边界）

```
┌──────────────────────────────────────────────────────────┐
│  cli/   Commander 装配 + 面向用户的交互/输出流程           │
│         （init.ts / status.ts / update.ts）               │
├──────────────────────────────────────────────────────────┤
│  core/  工作流生成、依赖状态、可持久化业务规则             │
│         （constants / dependency-check /                 │
│          skill-generator / workflow-status）             │
├──────────────────────────────────────────────────────────┤
│  utils/ 小型可复用运行时助手（shell / logger）            │
├──────────────────────────────────────────────────────────┤
│  templates/  生成技能内容的「唯一真源」                   │
│         （源码不得复制完整模板正文——project.md 明确约束） │
└──────────────────────────────────────────────────────────┘
```

### 关键数据流

```
openflow init ──► checkDependencies ──► ensureOpenSpecProjectContext
                   (OpenSpec/Superpowers)   (写 openspec/config.yaml)
                            │
                            ▼
                   generateSkills ──► 读 templates/*.md
                            │           ├ 注入工具上下文 ({{OPENFLOW_PROJECT_INIT_COMMAND}})
                            │           ├ 注入运行时依赖检测 (build.md / spec.md)
                            │           └ 生成阶段别名 (claude/codex/cursor)
                            ▼
                   .openflow/state.json  (记录初始化状态)

openflow status ──► readState ──► findActiveChanges ──► loadWorkflowStatus
                                                        ├ 有 workflow-status.md → 解析
                                                        └ 无 → synthesizeWorkflowStatus（文件推断）
                                                              │
                                                              ▼
                                                   detectWorkflowConflicts + renderWorkflowDashboard
```

---

## 6. 源码模块详解

| 文件 | 行数 | 职责 | 关键导出 |
|------|------|------|----------|
| `cli/index.ts` | 23 | 注册命令、读取 `package.json` 版本 | `run()` |
| `cli/init.ts` | 218 | 初始化 5 步流程（见 7.1） | `initCommand`, `ensureOpenSpecProjectContext()` |
| `cli/status.ts` | 66 | 依赖/项目/工作流三段式看板 | `statusCommand` |
| `cli/update.ts` | 38 | 基于 `state.json` 重新生成技能 | `updateCommand` |
| `core/constants.ts` | 36 | 依赖元数据 + 4 工具路径映射 | `DEPS`, `TOOL_PATHS`, `PKG_*` |
| `core/dependency-check.ts` | 119 | 依赖检测、自动安装、状态读写 | `checkDependencies()`, `readState()`, `writeState()` |
| `core/skill-generator.ts` | 207 | 模板渲染 + 注入 + 别名生成 | `generateSkills()` |
| `core/workflow-status.ts` | 354 | **工作流状态机（核心）** | `loadWorkflowStatus()`, `synthesizeWorkflowStatus()`, `detectWorkflowConflicts()`, `renderWorkflowDashboard()` |
| `utils/shell.ts` | 75 | 进程/文件系统原子操作 | `exec()`, `cmdExists()`, `fileExists()`, `dirExists()` |
| `utils/logger.ts` | 69 | 分级日志 + JSON/debug 模式 | `logger`, `createLogger()` |

每个 `src/*.ts` 均配有同名 `*.test.ts`，测试覆盖完整。

---

## 7. 三大核心机制

### 7.1 依赖检测与优雅降级（双层）

OpenFlow 的设计哲学是**「两个依赖都可以缺失，仍可工作」**。检测分两层：

**① Init 时检测**（`cli/init.ts` 五步流程）：
1. 检测 OpenSpec CLI（`cmdExists('openspec')`），缺失则询问是否 `npm i -g` 自动安装；
2. 检测 Superpowers（在各工具 local/global skills 目录下找 `writing-plans/SKILL.md`），缺失仅给安装提示；
3. 检测项目 OpenSpec 是否初始化，缺失则引导 `openspec init` 或创建无 CLI 元数据的脚手架；
4. 调 `ensureOpenSpecProjectContext` 写/补 `openspec/config.yaml`；
5. `generateSkills` + `writeState`。

**② 运行时检测**：通过 `skill-generator.ts` 的 `injectRuntimeDepCheck` / `injectSpecRuntimeCheck`，把依赖检测说明**注入生成的 `build.md` / `spec.md`**，使 AI 执行阶段也知道如何降级。

| 依赖 | 缺失时降级 |
|------|-----------|
| OpenSpec | spec 阶段手动创建 `openspec/changes/`；close 阶段手动 `mv` 归档 |
| Superpowers | build 阶段降级为「手动拆解 `plan-ready.md` 步骤逐条执行」 |

> ⚠️ **代码事实**：`injectRuntimeDepCheck(content, depStatus)` 与 `injectSpecRuntimeCheck(content, depStatus)` 的签名接收 `depStatus`，但函数体内**完全未使用该参数**——注入的是固定文本，不随实际安装状态定制。属「签名-行为不一致」的小瑕疵（不影响功能，但参数可移除或真正利用）。

### 7.2 技能生成机制（`skill-generator.ts`）

生成逻辑清晰、模板驱动：

- **真源单一**：所有内容来自 `templates/*.md`，`resolveSkillTemplateContent` 对缺失模板直接 `throw`（早期版本曾内联大段 fallback，已移除）。
- **每个工具生成 1 主文件 + 8 阶段文件**：`SKILL.md` + `{init,proposal,brainstorming,grill,spec,amend,build,close}.md`。
- **占位符替换**：`{{OPENFLOW_PROJECT_INIT_COMMAND}}` → `openflow init --tools <tool>`，使 CLI 命令与当前工具对齐。
- **阶段别名（Phase Alias）**：仅对 `claude / codex / cursor` 生成（`PHASE_ALIAS_TOOLS`），即 `openflow-<phase>/SKILL.md`，目的是让有补全能力的工具输入 `openflow` 就能发现各阶段；OpenCode 保留原生命令树 `/openflow/<phase>`。
- **项目初始化守卫**：`init / proposal / brainstorming` 三个别名会额外注入「先检查 `openspec/config.yaml`」的守卫指令（`PROJECT_INIT_GUARD_ALIAS_PHASES`）。

### 7.3 工作流状态机（`workflow-status.ts`，项目核心）

这是 0.4.1 引入、全仓库**最复杂、最核心**的模块（354 行）。它把"AI 工作流走到哪一步"从"靠 AI 记忆"变成"可推断、可校验、可渲染"的确定性状态。

**状态空间**：

| 维度 | 取值 |
|------|------|
| Phase | `capture \| spec \| build \| close \| archived` |
| Capture Mode | `proposal \| brainstorming \| none` |
| Overall Status | `pending \| in_progress \| blocked \| ready_for_next_phase \| completed` |
| Gate Status | `pending \| passed \| failed \| blocked \| not_applicable` |
| Task Status | `pending \| in_progress \| blocked \| implemented \| verified \| done \| superseded \| failed` |

**6 个阶段门控（Gates）**：Requirements captured → Specs validated → Plan ready → Implementation complete → Verification complete → Archived。

**双源状态读取**（`loadWorkflowStatus`）：
1. 优先解析 `openspec/changes/<id>/workflow-status.md`（权威）；
2. 缺失时 `synthesizeWorkflowStatus` **基于文件系统推断**，并明确标记 `inferred: true`。

**文件推断规则**（`synthesizeWorkflowStatus`）：

| 文件状态 | 推断 Phase | Status | Next |
|----------|-----------|--------|------|
| 有 `proposal.md`，无 `plan-ready.md` | capture | ready_for_next_phase | `/openflow spec` |
| 有 `plan-ready.md`，无实现计划 | spec | ready_for_next_phase | `/openflow build` |
| 实现计划 checkbox 未全勾 | build | in_progress | `/openflow build` |
| 实现计划 checkbox 全勾 | build | ready_for_next_phase | `/openflow close` |

**冲突检测**（`detectWorkflowConflicts`）：当 `workflow-status.md` 声称某 gate `passed`，但实际文件缺失（如称 Plan ready 却无 `plan-ready.md`），**显式列出冲突而非静默覆盖**——这是防止 AI "谎报进度"的关键护栏。

**Dashboard 渲染**（`renderWorkflowDashboard`）：聚合 gates/tasks 统计/blockers/conflicts/next，输出可读看板，供 `openflow status` 和 AI 路由共用。

---

## 8. OpenFlow 工作流模型（8 阶段流水线）

```
/openflow init ─── 项目上下文 → openspec/config.yaml
        │
        ▼
┌─ /openflow proposal ──────┐  (3-5 问，轻量收敛)
│  /openflow brainstorming ─┤  (多轮深度设计)
└───────────────────────────┘
        │              openspec/changes/<id>/proposal.md
        ▼
/openflow grill ──── 可选压力测试（反向追问假设）
        │
        ▼
/openflow spec ───── OpenSpec 生成 design/specs/tasks
        │            + 翻译层 → plan-ready.md（工程交接物）
        ▼
        │   workflow-status.md（状态导航）
        ▼
/openflow build ──── Superpowers 执行（TDD + checkpoint）
        │            ↑ 需求变更时切到 ↓
        │            └─► /openflow amend（受控修订需求/规格/计划）
        ▼
/openflow close ──── 验证一致性 + openspec archive
```

**状态转换**（Phase 机器）：`capture → spec → build → close → archived`，其中 `grill`、`amend` 是横向的"质量/修订"旁路，不改变主相位但影响产物。

---

## 9. 阶段写入边界（安全模型，最关键的设计约束）

这是 OpenFlow 区别于"放任 AI 改代码"的核心护栏。`templates/SKILL.md:52-65` 用一张表强制约束每个阶段**能写什么、不能写什么**：

| 阶段 | ✅ 允许写入 | ❌ 禁止写入 |
|------|-----------|-----------|
| init | `openspec/config.yaml`, `.openflow/state.json` | 任何代码/实现文件；不得创建 change |
| proposal | `openspec/changes/**/proposal.md` | 代码 |
| brainstorming | `proposal.md` | 代码 |
| grill | `proposal.md` | 代码 |
| spec | `openspec/changes/**`, `plan-ready.md` | 代码 |
| amend | `changes/**`, `plan-ready.md`, `docs/superpowers/plans/*.md` | 代码/测试/实现 |
| **build** | **代码、测试、tasks.md 勾选** | 规格文档（除非另开变更） |
| close | 归档、`close-issues.md`、tasks.md 勾选 | 代码/测试 |

**关键规则**：在 init/proposal/.../amend 任一阶段，即使用户说"就按这个做"、"继续"，也**不得进入 build 改代码**——必须先产出该阶段文档并提示下一步。`build` 是唯一允许修改实现文件的阶段。

**续接与中断恢复**（`SKILL.md:37-50`）：用户补充范围、回答确认、说"继续"时，默认续接上一阶段，不当作新编码请求；若在 build 中提出需求变更，自动切到 `amend` 而非直接改码。

---

## 10. 多工具适配

| 工具 | 本地路径 | 全局路径 | 阶段别名 |
|------|---------|---------|---------|
| `claude` | `.claude/skills/openflow/` | `~/.claude/skills/openflow/` | ✅ |
| `codex` | `.codex/skills/openflow/` | `~/.codex/skills/openflow/` | ✅ |
| `cursor` | `.cursor/skills/openflow/` | `~/.cursor/skills/openflow/` | ✅ |
| `opencode` | `.opencode/commands/openflow/` | `~/.opencode/commands/openflow/` | ❌（用原生 `/openflow/<phase>`） |

设计要点：CLI `openflow init` 负责安装/生成本地 skill；AI 工作流 `/openflow init` 负责交互式生成项目上下文——两层职责分离。

---

## 11. 项目自身的 OpenSpec 治理（"吃自己的狗粮"）

OpenFlow 用 OpenSpec 管理自身演进，仓库内可见其完整的规格驱动实践：

- **`openspec/project.md`**：项目上下文（技术栈、代码风格、架构模式、测试策略、领域上下文、硬约束）。注意它已被标记为 legacy——新规范从 `config.yaml` 注入，`init.ts:163` 会检测并提示迁移。
- **`openspec/specs/project/spec.md`**：持久化的"项目规格"，含 10 条 Requirement（版本单一来源、原生 API、cmdExists 不 shell-out、测试基线、CI、CHANGELOG 等），每条带 Scenario 验收。
- **活跃变更**：`openspec/changes/add-openflow-init-phase/`（即把 init 设为正式阶段的需求，已在 0.4.x 实现）。
- **归档变更**：`archive/2026-06-04-refactor-arch-optimize/`（含完整 `proposal/design/plan-ready/tasks/workflow-status/close-issues`），其 `workflow-status.md` 是状态机产物的真实样例——Phase=archived、6 gates 全 passed、14 tasks 全 done。

---

## 12. 测试 · CI · 构建发布

| 维度 | 配置 |
|------|------|
| 测试 | Vitest，`src/**/*.test.ts`，`passWithNoTests: true`，环境 node |
| Lint | `tsc --noEmit`（类型检查即 lint，无独立 ESLint） |
| 构建 | `tsc` → `dist/`，ES2022 / Node16 模块解析，输出 `.d.ts`，测试文件排除 |
| CI | GitHub Actions（`.github/workflows/ci.yml`），Node 22，`npm ci` → lint → build → test，push 全分支 + PR 触发 |
| 发布 | `prepublishOnly` 自动 build；`files` 精简打包（bin/dist/templates/scripts/图）；`postinstall` 仅打印提示 |

`npm run check` = `lint && build && test`，是完成实现的统一验证命令。

---

## 13. 设计亮点

1. **确定性状态机对抗 AI 记忆不确定性**：`workflow-status.ts` 用文件推断 + 冲突检测，让"进度"可校验、可恢复，是整个项目的灵魂。
2. **写入边界作为安全护栏**：用一张表把"能改代码"严格限制在 build 阶段，从源头防止 AI 越权修改。
3. **优雅降级到极致**：两个核心依赖都能缺失，且降级路径写入生成的技能，运行时也知晓。
4. **模板单一真源**：源码不复制模板正文，避免双重维护（0.3.3 已偿还此技术债）。
5. **原生 API 优先**：`fileExists/dirExists` 用 `fs.statSync`，`cmdExists` 遍历 `PATH` 用 `accessSync(X_OK)`，不 spawn shell——既快又安全（0.3.3 重构成果，已写进项目 spec）。
6. **自治理**：用自己编排的 OpenSpec 流程管理自身演进，规格/计划/归档齐全。

---

## 14. 风险 · 技术债 · 改进建议

| # | 类型 | 发现 | 建议 |
|---|------|------|------|
| 1 | 死依赖 | `ora@^8.0.0` 声明但源码 0 引用 | 移除或启用（spinner 用于耗时安装） |
| 2 | 签名冗余 | `injectRuntimeDepCheck/injectSpecRuntimeCheck` 的 `depStatus` 参数未使用 | 移除参数，或据此定制运行时检测文案（更优） |
| 3 | 文档债 | `openspec/specs/project/spec.md` 的 Purpose 仍为 `TBD`；其中"Workflow Status Draft Must Be Resolved"已在 0.4.1 满足但 spec 未更新 | 补全 Purpose，更新/关闭该 requirement |
| 4 | 错误吞噬 | `exec()` 失败时返回空字符串，调用方难区分"失败"与"成功空输出"（项目 spec 第 86-93 行已标记为 optional enhancement） | 优先用 `execResult()` 的 `ok` 字段判定 |
| 5 | 图谱债 | graphify 报告显示 57 个孤立节点、Package Config 社区内聚仅 0.07 | 非阻塞，反映依赖/字段文档化不足 |
| 6 | 安全（轻微） | `cmdExists` 已用正则 `^[A-Za-z0-9._-]+$` 限制命令名，good；但 `exec()` 直接拼接字符串执行（如 `openspec init --tools ${toolsFlag}`，tools 来自 `--tools` 参数） | 当前 tools 已被 `TOOL_PATHS` 白名单校验，风险可控；保持勿直接拼接用户自由文本 |

以上均为**非阻塞**改进，项目核心功能完整、测试齐备、CI 通过。

---

## 15. 代码规模统计

| 指标 | 数值 |
|------|------|
| 源码总行（src，含测试） | ~1940 行 / 16 文件 |
| 最大文件 | `workflow-status.ts`（354 行） |
| 生产代码 vs 测试 | 约 1:1（每个生产文件配测试） |
| import 语句 | 76 处 / 16 文件 |
| 技能模板 | 9 个（1 主 + 8 阶段） |
| 支持工具 | 4（claude/codex/cursor/opencode） |
| 知识图谱（graphify） | 124 节点 · 195 边 · 9 社区 · 0 环 |

---

## 16. 结论

OpenFlow 是一个**定位清晰、架构克制、约束严谨**的小型高质量 TypeScript CLI。它不是功能堆砌的工具，而是把"AI 该如何按规范开发"这一**流程问题**，转化为"状态机 + 写入边界 + 模板生成"的**工程问题**。

- **核心竞争力**：`workflow-status` 状态机 + 阶段写入边界——这两者共同提供了 AI 编码稀缺的"流程确定性"和"越权防护"。
- **工程质量**：分层清晰、测试完备、CI 在线、原生 API、模板单一真源，技术债主要集中于几处文档/参数清理。
- **成熟度**：v0.4.4，已迭代到 workflow 状态可视化与 close 阶段 guard，处于稳定可用阶段。

**一句话**：它把 OpenSpec（要做什么）与 Superpowers（怎么做）缝合成一条带护栏的流水线，并让这条流水线对四类主流 AI 编码工具开箱即用。

---

*说明：本报告基于工作区当前状态（main 分支，HEAD `a431556`）的全量源码与配置精读生成。*
