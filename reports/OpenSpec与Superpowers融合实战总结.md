# OpenSpec + Superpowers 融合实战总结

> 本文是两篇微信公众号文章的融合总结，把上下篇融成一份连贯、可速读的知识体系，而非简单拼接。
>
> - **上篇**：《OpenSpec + Superpowers：Spec-Driven 落地的真实经验》（作者 Dolphin7）
>   [mp.weixin.qq.com/s/23saLJYoQM6KsKD-DaXfnw](https://mp.weixin.qq.com/s/23saLJYoQM6KsKD-DaXfnw)
>   —— 讲 **What / Why / 架构总览**。
> - **下篇**：《OpenSpec + Superpowers 融合实战（下篇）：从原理到一行命令跑通》（作者 dolphin07）
>   [mp.weixin.qq.com/s/Xvx-mS7AYshz2ru6PwlhXg](https://mp.weixin.qq.com/s/Xvx-mS7AYshz2ru6PwlhXg)
>   —— 讲 **原理 / 落地 / 未来判断**。
>
> 一句话核心结论：
>
> **OpenSpec 治 What（需求层），Superpowers 治 How（执行层），唯一硬契约是「Scenario 名 1:1」机器契约；二者经 Slash Command 桥接层粘合，不动双方源码、升级安全，是当下 Spec-Driven 落地的 80 分天花板。**

---

## 目录

1. [为什么 Spec-Driven 很火，却真正落地不多](#一为什么-spec-driven-很火却真正落地不多)
2. [两个工具的定性](#二两个工具的定性)
3. [融合架构总览](#三融合架构总览)
4. [灵魂契约：1 Scenario = 1 test](#四灵魂契约1-scenario--1-test)
5. [融合后的标准流程：4 阶段](#五融合后的标准流程4-阶段)
6. [Slash Command 粘合层：不改源码，升级安全](#六slash-command-粘合层不改源码升级安全)
7. [新人一行命令实战](#七新人一行命令实战)
8. [边界与反模式](#八边界与反模式)
9. [不是银弹：能解决什么 / 不能解决什么](#九不是银弹能解决什么--不能解决什么)
10. [未来判断：AI 越强，流程越轻](#十未来判断ai-越强流程越轻)
11. [一句话总结](#十一一句话总结)

---

## 一、为什么 Spec-Driven 很火，却真正落地不多

过去一年，Spec-Driven 成为 AI 编码圈的热门话题：GitHub 推出 **Spec Kit**、Amazon 推出 **Kiro IDE**、Anthropic 推 **Skills**，几乎每个圈子都在讨论 spec 如何与 AI 协作。OpenSpec 和 Superpowers 也各自走红：

- **OpenSpec 很火** —— Fission-AI 开源 npm 包（45k+ stars），把 spec 做成版本化的 living document，**解决需求层**：spec 演化、change 治理、archive 状态机。
- **Superpowers 也很火** —— Anthropic 官方插件市场收录的 Claude Code 工程纪律包，**解决执行层**：TDD、verification、code review、systematic-debugging 等纪律。

**但真正落地的不多**，作者归结为 3 个根本原因：

| 落地难点 | 典型表现 |
| --- | --- |
| ❌ **流程太重** | Spec Kit 一个 feature 走 7 阶段、800 行文档，团队评审压力大 |
| ❌ **与工具脱节** | spec 写在飞书/Notion，AI 编码工具不会自动读，写了等于没写 |
| ❌ **缺执行纪律** | spec 写完没人 follow，半年后 spec 与 code 严重 drift，反向误导 |

OpenSpec 解决前两个（**轻量 + AI 友好**，对比 Spec Kit 的 7 阶段和 Kiro 的一体化 IDE），Superpowers 解决第三个。**单独用任何一个都不够，组合才完整** —— 这正是融合架构存在的根本理由。

---

## 二、两个工具的定性

理解融合的第一步，是先看清两者各自的定位与边界：

|  | 🔵 OpenSpec | 🟣 Superpowers |
| --- | --- | --- |
| **是什么** | Spec 协议层（治理 change 目录生命周期） | Claude Code 工程纪律 plugin pack |
| **核心抽象** | spec（living doc）+ change（版本化提案） | skill（可触发的方法包） |
| **治理什么** | 所有 `changes/<id>/`、`specs/`、`archive/` 内文件（含 proposal / design / tasks / delta） | 实施纪律（TDD / verification / review / debug / subagent） |
| **不治理什么** | 文件内容写什么（只提供模板）；不教方法 | 任何持久 spec / change 文件 |
| **产物默认** | 持久化（git tracked） | 临时（仅 test / src 持久，但本身不是 SP 产的） |

> **关键分辨：OpenSpec 治理文件 ≠ OpenSpec 决定内容。**
> design.md 由 OpenSpec 治理（提供模板、纳入 change、archive 时一起搬走），但**内容写什么由 Dev 决定**。

### 各自的原生流程

- **OpenSpec 原生**：3 阶段状态机（change → validate → archive）。它**不教方法** —— `apply` 只看 tasks.md 是否勾完，不管 TDD 与否。
- **Superpowers 原生**：按需触发的 skill 集。它**没有持久 spec 概念** —— 产物默认临时，文档与代码会迅速 drift。

> 正是因为两者各有缺口，单独使用都拿不到完整闭环。

### 内容层归属判断法

> **换了语言/架构后还成立 → 需求层；会变 → 执行层。**
> 按此原则：scenario 是需求层；design / tasks 是执行层（虽然都放在 OpenSpec 目录里）。

---

## 三、融合架构总览

### 一句话定义

> **融合架构 = 需求层（OpenSpec）+ 执行层（Superpowers）+ 中间「双向流转契约」**

光说"两个工具叠加"还不构成架构 —— **架构 = 它们之间有契约**。架构图呈对称结构：左右两个大方框是两层定位，中间双向流转契约是融合的灵魂，底部横条是三件套循环。

### 能力矩阵：为什么必须融合

矩阵图的关键结论是：**任何单工具都拿不到完整闭环 —— 融合后才闭环**。这是融合架构存在的根本理由。

### 治理边界（清晰，不重合）

| 治理方 | 范围 |
| --- | --- |
| 🔵 OpenSpec | 所有 `changes/<id>/`、`specs/`、`archive/` 文件的生命周期 |
| 🟣 Superpowers | 实施过程的纪律（不产持久文件） |
| 都不治理 | `src/` 和 `tests/` —— 开发产物，由 git 治理 |

### 真重合的 2 处（必须取舍）

| 重合点 | OpenSpec | Superpowers | **融合用谁** |
| --- | --- | --- | --- |
| **方案文档** | proposal + design（持久） | writing-plans 出 plan.md（临时） | **OpenSpec**（持久化优先） |
| **任务清单** | tasks.md（持久静态） | executing-plans 拆子任务（动态） | **OpenSpec 拆 + Superpowers 按 tasks 编排** |

### 互补的 2 处（不是重合，都用上）

| 互补点 | OpenSpec 做 | Superpowers 做 |
| --- | --- | --- |
| **执行纪律** | 不做（`apply` 是被动） | 强制 TDD 红绿循环 |
| **完成验证** | `validate` 查 spec 格式合法 | `verification` 查 test 全绿、行为对齐 |

### 融合原则（3 条 + 一个硬契约）

1. **真重合 → OpenSpec 主导**（持久化优先于临时）
2. **互补 → 都用**（双跑不冲突）
3. **治理 ≠ 内容**：design.md 由 OpenSpec 治理，但内容是技术决策，Dev 主导写

第 4 条"硬契约"见下一节，它是整套方案的灵魂。

---

## 四、灵魂契约：1 Scenario = 1 test

融合架构的精髓在于：**所有协作最终落到一个机器可断言的物理交点**。

OpenSpec 的 Scenario 用 WHEN/AND/THEN 句式，**本身就是 test 的伪代码**：

🟦 **OpenSpec 的 Scenario**（业务规则形式化）：

```
Scenario: 普通 @ 提及
- WHEN 用户提交 "@张三 看下这个"
- AND 张三是有效用户
- THEN mentions 字段含张三的 user_id
- AND 张三收到 1 条通知
```

🟢 **Superpowers TDD 直接 1:1 翻译为 test**：

```python
def test_at_提及_existing_user():
    user = create_user("张三")
    comment = submit_comment("@张三 看下这个")
    assert user.id in comment.mentions
    assert notification_sent_to(user)
```

**约定：1 Scenario = 1 test 函数，命名带 Scenario 名。** 这意味着 **spec ↔ test 永远 1:1 可追溯**：

| 场景 | 效果 |
| --- | --- |
| 半年后看代码 | 能直接对回 spec |
| 改 spec 时 | 立刻知道哪些 test 要更新 |
| spec 和 code drift | 在 CI 自动挂红 |

> spec 不再是另一份会过期的文档，而是 **test 的蓝图**。

### 双向反查 diff = 0（CI 可阻断的硬契约）

```bash
# spec / test 任一改名，diff 立刻红
diff <(grep '^#### Scenario:' specs/*/spec.md | sed 's/#### Scenario: //') \
     <(grep "test\('(normal|edge|error)_" tests/ | sed -E "s/.*test\('([^']+)'.*/\1/")
# Expected: 0 lines
```

这是 **OpenSpec 跟 Superpowers 唯一不靠口头约定、不靠 review 自觉的硬契约** —— 防漂移的最强单一指标，CI 可据此阻断 PR。

---

## 五、融合后的标准流程：4 阶段

融合后是一条 4 阶段主链路，每阶段对应明确的桥接命令、工具与产物：

| # | 阶段 | 桥接命令 | 🔵 OpenSpec 工具 | 🟣 Superpowers skill | 产物 |
| --- | --- | --- | --- | --- | --- |
| ① | 提案 | `/flow:propose` | `openspec new change` + `instructions` + `validate --strict` | brainstorming（可选） | `changes/<id>/{proposal,design,tasks}.md` + `specs/<cap>/spec.md` |
| ② | 实现 | `/flow:apply` | 读 `changes/<id>/` contextFiles | **test-driven-development**（必）+ verification（每 task） | `src/` + `tests/` + 每 task 1 commit |
| ③ | 验证 | `/flow:verify` | `validate --strict` | **verification-before-completion**（必）+ 6 项命令 | 验证报告 + 双向反查 diff = 0 |
| ④ | 归档 | `/flow:archive` | `archive --yes` | verification（前置守门） | `specs/<cap>/spec.md` baseline + `archive/<date>-<id>/` |

> **稳定性的来源**：所有协作不靠运行时通信，都靠物理文件落到 `changes/` `specs/` `tests/`。

### 两个不可妥协的人在回路卡点（★）

- ★ **方案确认** —— 对齐"做什么"
- ★ **Code Review** —— 对齐"做对没"

（上篇主链路表里这两处标为 ★ 人工卡点；下篇的 `/flow:run` 自动化版把决策收敛为 stage-gate 点击，但 review 最终 git log 仍是人。）

---

## 六、Slash Command 粘合层：不改源码，升级安全

### 结论先行

> **桥接层用 Slash Command 实现，不改 OpenSpec / Superpowers 任何源码。**

3 个理由：

1. **工具单一职责** —— OpenSpec / Superpowers 都不该感知对方
2. **升级安全** —— 改它们的源码，下次升级会被冲掉；桥接层放团队 git 永不被覆盖
3. **团队定制** —— 不同团队严密性标准不同，桥接层留团队自由度

### 4 个桥接命令调什么

| 桥接命令 | 🔵 调用 OpenSpec | 🟣 调用 Superpowers Skill | 团队补充约束 |
| --- | --- | --- | --- |
| `/flow:propose` | `openspec new change` + `instructions` + `validate` | brainstorming（可选） | 4 件套 format 校验（SHALL / 4 hashtags） |
| `/flow:apply` | 读 `changes/<id>/` contextFiles | **test-driven-development**（强制）+ verification（每 task） | 1 task 1 commit；commit 前必须 fresh jest evidence |
| `/flow:verify` | `validate --strict` | **verification-before-completion**（强制） | 6 项命令 + 双向反查 diff = 0 |
| `/flow:archive` | `archive --yes` | verification（前置守门） | 拒绝 diff > 0 的归档 + Purpose 必填 |

### 3 类文件归属（落地后的项目目录）

| 颜色 | 区域 | 谁创建 | 团队改吗 | 升级影响 |
| --- | --- | --- | --- | --- |
| 🟡 黄 | `.claude/commands/flow/` + `CLAUDE.md` + `docs/workflow/` | 团队（写一次复用） | ✅ 自由改 | 🟢 不受影响 |
| 🔵 蓝 | `.claude/commands/opsx/` + `.claude/skills/openspec-*/` | OpenSpec init 自动 | ❌ 不动 | 🟡 升级时重生成 |
| ⭐ 数据 | `openspec/` + `src/` + `tests/` | 业务流程产生 | ✅ 自然演化 | 🟢 不受影响 |

### 真实案例：修 bug 验证"不改 skill"的好处

实测中 `/flow:archive` 的双向反查 grep 漏了 baseline 路径，触发误报。修复**只改 1 个文件**（团队桥接层）：

```bash
# .claude/commands/flow/archive.md（团队桥接层）
- grep -h '^#### Scenario:' openspec/changes/<id>/specs/*/spec.md
+ grep -h '^#### Scenario:' \
+   openspec/changes/<id>/specs/*/spec.md \
+   openspec/specs/*/spec.md 2>/dev/null
```

**OpenSpec / Superpowers 一行未动**。修复进团队 git，下次升级两者也不会冲掉这个修复。**桥接层完全是团队的代码资产**。

---

## 七、新人一行命令实战

讲完原理，看真实跑通 —— **全程 `/flow:run` 一行命令**。

**场景**：给 SOP 引擎 HTTP API 加 `GET /instances` endpoint，返回当前所有实例数组（无参；空时返回 `[]`）。

```
/flow:run "加 GET /instances endpoint，返回当前所有实例的数组（无参数；空时返回 []）"
```

### 用户实际做的事

| # | 动作 | 用时 |
| --- | --- | --- |
| 1 | 输入 `/flow:run "..."` | 30 秒 |
| 2 | Stage 1 stage-gate 选 "Skip brainstorming" | 点击 |
| 3 | Stage 1 stage-gate 选 "Continue to apply" | 点击 |
| 4 | Stage 3 stage-gate 选 "Continue to archive" | 点击 |
| 5 | review 最终 git log 确认 commit 节奏 | 1 分钟 |

> **用户真正的工作 = 决策 + review，不是手动跑命令。**

### AI 自动跑的 4 阶段（节选关键节点）

**Stage 2 Apply —— 严格 RED→GREEN**：

```
─── Task 1.1 ───
Scenario: normal_get_all_instances_returns_list
  [AI 写 test] [npx jest -t ...] [FAIL: 404, expected 200]  ← RED ✓
  [AI 写 GET route] [npx jest -t ...] [PASS]                ← GREEN ✓
  [勾 [x] tasks.md / commit "feat(api): GET /instances ... (task 1.1, Sc 1)"]

─── Task 1.2 ───
Scenario: edge_get_all_instances_empty_returns_empty_array
  [AI 加 test / PASS]   ← Lock-style（task 1.1 GREEN 已覆盖）
  [commit "test: lock GET /instances empty (task 1.2, Sc 2)"]
```

**Stage 3 Verify —— 6 项验证报告**：

| # | Check | Threshold | Actual | Result |
|---|---|---|---|---|
| 1 | npm test | N/N pass | 32/32 | ✅ |
| 2 | coverage stmt | ≥ 90% | 95.20% | ✅ |
| 3 | tsc --noEmit | clean | exit 0 | ✅ |
| 4 | tasks unchecked | = 0 | 0 | ✅ |
| 5 | openspec validate --strict | PASS | PASS | ✅ |
| 6 | bidirectional diff | 0 lines | 0 lines | ✅ |

**Stage 4 Archive —— 自动 sync delta**：`openspec archive add-list-instances-api --yes`

### 跑完看到什么

```
git log --oneline | head -4
# 0e8ee46 chore(openspec): archive add-list-instances-api
# c0a2e09 test: lock GET /instances empty store returns []
# 54f62b5 feat(api): GET /instances returns sorted list
# c1ebc66 feat(openspec): propose add-list-instances-api
```

> **总耗时 18 min / 用户总打字 30 字 / 4 个原子 commit / spec ⇌ test diff = 0。**
> 这才是 AI 协作工程化的样子 —— **人做决策，AI 做执行；约束机器化，纪律自动化。**

---

## 八、边界与反模式

### 跑链路时最易踩的 3 个反模式

| ❌ 反模式 | 后果 |
| --- | --- |
| 让 AI 全权写 Scenario | 业务规则跑偏，你不知道偏在哪 |
| 把 How 塞进 proposal | 业务方看不懂、技术评审散落两地 |
| 让 Superpowers 重写 plan.md | 与 proposal+design 重复，团队不知道看哪份 |

### 适用边界

✅ **适合**：

- 工程严密项目（金融 / 医疗 / 内核库 / 中后台）
- 多人协作代码库，需要标准化 review 抓手
- 想给团队建立 AI 协作规约，但不想被 vendor lock 死的场景
- TypeScript + jest 技术栈（基础设施已 battle-tested）

⚠️ **不一定适合**：

- 一次性原型 / hackathon（流程 overhead 不值得）
- 纯 frontend / UI 重的项目（spec 难拆 Scenario）
- 团队还在自由探索阶段，没法对齐流程标准的早期阶段

❌ **不适合**：

- 生命周期短于 1 个月的项目
- 团队极度反对结构化的极速迭代项目

---

## 九、不是银弹：能解决什么 / 不能解决什么

把边界说清楚，比吹它能干什么更重要。

### 能解决什么（80 分核心价值）

| ✅ 解决的痛点 | 怎么解的 |
| --- | --- |
| **意图 drift** | spec 跟代码一起进 git，不再分离在飞书/Notion |
| **AI 瞎猜** | 1 Scenario = 1 test 强契约，AI 必须按 spec 写 |
| **跨 session 失忆** | spec 是 AI 的外挂记忆，新对话直接读懂 |
| **执行无纪律** | Superpowers TDD 强制红绿循环 + verification 强制自检 |
| **改动不可追溯** | archive 留档每次 change，半年后能查"当时为什么" |

### 不能解决什么（精度悖论决定）

| ❌ 解不了的 | 本质原因 |
| --- | --- |
| **消除业务复杂度** | 复杂状态机 / 条件响应 / 动态契约还是要写代码 |
| **替代代码** | spec 精确到能消除歧义时它就是代码（**精度悖论**） |
| **反向感知 runtime** | spec 不知道线上 P99 / 错误率 / 容量 |
| **从故障自动学习** | 复盘报告归档完事，经验回不到 spec |
| **多源 drift 自治** | 人盯不住 spec / code / test / runtime 的一致性 |

> 剩下 10 分能拿，但**绝不是再给团队加人工 SOP** —— 团队会瘫痪。

---

## 十、未来判断：AI 越强，流程越轻

### 下一步是 AI Agent 自驱 Loop（不是人工流程）

剩下 10 分的关键差别是"AI 自闭环"，而非"团队多 4 个流程"。3 条 AI 自驱反向流：

- **Runtime 监控**：AI 自己读告警 → 发现 spec 承诺与现实不符 → 自动开 change 提案
- **故障复盘**：AI 自己读复盘报告 → 提取红线规则 → 反向加固 spec
- **CI drift 检测**：AI 自己跑多源一致性 → 自动挂红 → 尝试修复

### 这套方案 6-12 个月后大概率过时

当下写 5 个 slash command 强制 AI 走，是因为**当下的 AI 不会自动叠加 TDD + 双向反查严密性**。但能力在演进：

| AI 能力变化 | 这套方案变成什么 |
| --- | --- |
| AI 能从需求**直接生 TDD spec + 跑红绿** | `/flow:apply` 7 步精简到 2 步 |
| AI **主动推断**该 invoke 哪些 skill | `MANDATORY invoke` 不再需要 |
| AI **自动维护**双向反查 | diff = 0 是默认而非检查 |
| OpenSpec **native 集成** Superpowers 严密性 | 桥接层可能消失 |

### 但 3 条原则不会过时

| 原则 | 为什么不会过时 |
| --- | --- |
| **spec 是单一真相源** | 业务契约必须有唯一定义点。无论 AI 多强，多份 spec 永远会打架 |
| **1 Scenario = 1 test 是契约** | 机器可断言的协作契约是工程领域的硬通货 |
| **fresh evidence over claims** | 没跑过的 verification 等于没验证。这是工程伦理，跟 AI 强弱无关 |

> **工具会过时，原则不会。**

### 实操建议：每季度问 3 个问题

| 时间窗口 | 推荐做法 |
| --- | --- |
| 现在 - 3 个月 | 全套用 `/flow:*`，体感最强 |
| 3-6 个月 | 主用 `/flow:run`，老用户可继续用 `/opsx:*` 但走团队 review |
| 6-12 个月 | **半年 review 一次**：检查 AI 进步在哪、桥接层哪些 step 已多余 |
| 12 个月+ | **预期桥接层 50% 步骤被 AI 自主性 absorb**，重写 v2 |

每季度 3 问：

1. AI 现在不需要桥接层提醒就能严守 TDD 了吗？
2. OpenSpec 是否原生支持 TDD / 双向反查？
3. 这套桥接层让团队**变快**还是**变慢**？

> **任一题答"是"，就该改桥接层。**

> 这套方案是**当下 AI 能力 + 当下工具能力**的最优补丁 —— 能用 6-12 个月。
> 不要刻舟求剑。**建立工程纪律的那一刻，比工具用什么更重要。**

---

## 十一、一句话总结

> OpenSpec 治 What，Superpowers 治 How，唯一交点是「Scenario 名 1:1」机器契约。
> 5 个 `/flow:*` slash command 是团队桥接 —— **引用** Superpowers skill + **包装** OpenSpec CLI + **加** 团队约束，**不动两者源码**，升级安全。
> 新人一行命令 `/flow:run "<想法>"` 跑通完整流程。
> 半年后这套会过时；但 spec 真相源 + 1 Sc = 1 test + fresh evidence 这 3 条原则不会。
> **工具是脚手架，原则是地基。**

最后一句送给所有评估这条路的团队：

> AI 时代，**写代码不再是瓶颈，对齐才是**。
> 把 80 分这件事先做扎实 —— 它是 AI Agent 自驱 Loop 的物理基础。
> **没有 spec，再多 AI 也是瞎跑。**
