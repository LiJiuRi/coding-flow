# Comet 桥接机制详解与 dst-skill 差距分析

> **文档定位**：基于微信公众号文章《把 OpenSpec+Superpowers 做成 Agent Skill，Comet 一条命令跑通全流程》的完整解读，并对照本仓库（dst-bill-meta-repo）现有 `dst-task-*` / `dst-prd-plan` skill 体系，输出一份「Comet 是什么 + 怎么用 + 与 dst 的差距 + 演进建议」的详细分析报告。
>
> - **原始文章**：https://mp.weixin.qq.com/s/Pl9gco7jXXKa7whi0vCuZw
> - **分析对象**：开源项目 `rpamis/comet`（npm 包 `@rpamis/comet`，当前版本 0.3.8）
> - **对照对象**：本仓库 `.claude/skills/dst-plan-task` / `dst-task-continue` / `dst-task-exec` / `dst-task-verify` / `dst-task-archive` / `dst-prd-plan`
> - **编写日期**：2026-06-21

---

## 目录

- [第一部分　Comet 详解](#第一部分comet-详解)
  - [1.1 一句话本质：不是第三套框架，而是一层状态机](#11-一句话本质不是第三套框架而是一层状态机)
  - [1.2 它要解决的核心痛点](#12-它要解决的核心痛点)
  - [1.3 三层分工](#13-三层分工)
  - [1.4 安装与环境](#14-安装与环境)
  - [1.5 目录结构与 `.comet.yaml`](#15-目录结构与-cometyaml)
  - [1.6 单一入口与五阶段流水线](#16-单一入口与五阶段流水线)
  - [1.7 贯穿示例：支付回调幂等的五阶段落地](#17-贯穿示例支付回调幂等的五阶段落地)
  - [1.8 两个轻量入口：hotfix 与 tweak](#18-两个轻量入口hotfix-与-tweak)
  - [1.9 落地时要盯的 6 个信号](#19-落地时要盯的-6-个信号)
  - [1.10 推荐的团队接入流程](#110-推荐的团队接入流程)
  - [1.11 什么时候不用 Comet](#111-什么时候不用-comet)
  - [1.12 与手写桥接 skill 怎么选](#112-与手写桥接-skill-怎么选)
  - [1.13 新手只记这 5 句话](#113-新手只记这-5-句话)
- [第二部分　dst-task-* 现状梳理](#第二部分dst-task--现状梳理)
- [第三部分　差距分析（逐维度）](#第三部分差距分析逐维度)
- [第四部分　dst 演进优先级建议](#第四部分dst-演进优先级建议)
- [附录　参考资料与术语](#附录参考资料与术语)

---

## 第一部分　Comet 详解

### 1.1 一句话本质：不是第三套框架，而是一层状态机

> **Comet 的价值不在于又发明了一套 AI 编程方法，而是把 OpenSpec 的规格生命周期和 Superpowers 的执行纪律，用状态文件、脚本和 skill 串成一条可恢复流程。**

核心差异点：

- 手写桥接 skill 依赖 Agent **"记得做"**；
- Comet 尽量把"记得做"变成 **状态机 + 脚本检查**。

它不是只靠 prompt 记流程，而是做了几件工程化的事：

- 安装三组 skill（OpenSpec / Superpowers / Comet）；
- 生成 `.comet.yaml` 记录状态；
- 用 `comet-guard.sh` 做阶段退出检查；
- 用 `comet-handoff.sh` 做 OpenSpec 到 Superpowers 的上下文交接；
- 用 `comet-archive.sh` 做归档同步。

### 1.2 它要解决的核心痛点

第一次手写桥接 skill 很顺，**真正的麻烦是第二个月**：

> 一个 OpenSpec change 做到一半，Agent 会话断了；第二天回来，它不知道现在是 proposal / design / build / verify 哪个阶段。于是人又得手动提醒一遍流程。

**这套提醒只要漏一次，桥接就退化成"人肉流程"。**

→ Comet 的核心价值场景是：**断点恢复 + 流程漂移治理**。让 AI 在复杂需求里少靠记忆、多靠状态；少靠提醒、多靠闸门；少靠聊天记录、多靠可归档的工程证据。

### 1.3 三层分工

| 层 | 负责什么 | 常见产物 |
| --- | --- | --- |
| **OpenSpec** | 做什么、为什么、规格怎么归档 | `proposal.md`、`design.md`、`tasks.md`、`specs/` |
| **Superpowers** | 怎么设计、怎么计划、怎么 TDD、怎么审查 | Design Doc、Plan、测试、review、finish |
| **Comet** | 当前走到哪一步、谁接手、什么时候能推进 | `/comet`、`.comet.yaml`、guard、handoff、archive |

### 1.4 安装与环境

**Comet 不是业务依赖**，而是一套 AI 编码宿主的工作流基础设施。

前置条件：

```
Node.js 20+
npm/npx
Git
可运行 bash 的 shell 环境
```

环境自检：

```bash
node -v
npm -v
git --version
bash --version
```

查看当前版本：

```bash
npm view @rpamis/comet version   # 写本文时返回 0.3.8
```

安装与试用：

```bash
npm install -g @rpamis/comet

mkdir comet-demo && cd comet-demo
git init
comet init
```

`comet init` 做的事：

1. 提示选择 AI 平台
2. 选择项目级或全局安装
3. 选择中文或英文 skill
4. 安装 OpenSpec 技能
5. 安装 Superpowers 技能
6. 安装 Comet 技能
7. 项目级安装时创建 `docs/superpowers/specs` 和 `docs/superpowers/plans`

**关键坑（宿主适配）**：不同平台（Claude Code / Cursor / Codex / Gemini CLI / Windsurf / Cline / RooCode / Continue / GitHub Copilot / Qwen Code / Lingma / Qoder / Antigravity 等）skill 目录不同，项目级和全局也不同。装完必须诊断：

```bash
comet doctor
comet status
```

要确认的不是"npm 包装上了"，而是 **当前项目里三组 skill 是否都能被你的 Agent 宿主读取**——否则 `/comet` 只是好看的命令名。

> 备选安装方式：`npx skills add rpamis/comet`（仅装 skill 包，不跑 init）。普通团队建议先用 `comet init`，因为它一次性处理三组安装。

### 1.5 目录结构与 `.comet.yaml`

项目级初始化后的典型结构（不同宿主目录名不同，如 `.claude/`、`.codex/`、`.cursor/`、`.gemini/`，但核心关系一致）：

```
your-project/
  .comet/
    config.yaml

  openspec/
    config.yaml
    changes/
      <change-name>/
        .openspec.yaml        ← OpenSpec 的状态（spec 生命周期 / change 元数据）
        .comet.yaml           ← Comet 的状态（工作流阶段 / 构建模式 / 验证结果 / 归档状态）
        proposal.md
        design.md
        tasks.md
        specs/
          <capability>/spec.md

  docs/
    superpowers/
      specs/
      plans/

  <agent-platform>/
    skills/
      comet/
      comet-open/
      comet-design/
      comet-build/
      comet-verify/
      comet-archive/
      openspec-*/
      brainstorming/
      ...
```

两个状态文件最重要：

- `.openspec.yaml` —— OpenSpec 关心 spec 生命周期和 change 元数据；
- `.comet.yaml` —— Comet 关心工作流阶段、构建模式、验证结果、归档状态。

一个典型的 `.comet.yaml`：

```yaml
workflow: full
auto_transition: true
phase: build
build_mode: subagent-driven-development
build_pause: null
isolation: branch
verify_result: pending
verification_report: null
branch_status: pending
archived: false
design_doc: docs/superpowers/specs/2026-06-16-payment-callback-design.md
plan: docs/superpowers/plans/2026-06-16-payment-callback.md
handoff_context: openspec/changes/add-payment-callback-idempotency/.comet/handoff/design-context.json
handoff_hash: <sha256>
```

**这是 Comet 与普通提示词最大的差别**：普通提示词只能说"你要记住现在是 build 阶段"；Comet 把这个事实**写进状态文件**。下次会话恢复时，`/comet` 不靠聊天记录猜，而是重新检测活跃 change、读取 `.comet.yaml`、再判断下一步。

### 1.6 单一入口与五阶段流水线

主入口只有一个：

```
/comet
```

可带描述：

```
/comet 给支付回调增加幂等控制，同一个 channel + payTradeNo 重复回调只能处理一次
```

也可在已有 active change 时直接输入 `/comet`，它会自动做阶段检测。

完整链路拆成五个阶段：

| 阶段 | 命令 | 归属 | 产出物 |
| --- | --- | --- | --- |
| **Open** | `/comet-open` | OpenSpec | `proposal.md`、`design.md`、`tasks.md` |
| **Deep Design** | `/comet-design` | Superpowers | Design Doc、delta spec |
| **Plan & Build** | `/comet-build` | Superpowers | 实现计划、代码提交 |
| **Verify & Finish** | `/comet-verify` | 双方 | 验证报告、分支处理 |
| **Archive** | `/comet-archive` | OpenSpec | delta spec 同步、归档 |

五阶段可以这样理解：

```
open      先把需求打开，形成 OpenSpec change
design    做深度设计，把模糊需求变成技术方案
build     生成计划，按 Superpowers 的纪律执行
verify    测试、验证、处理分支收尾
archive   把 delta spec 合并回主规格并归档
```

阶段自动检测策略（主 skill 内置）：

- 没有 active change → open；
- 有一个 active change → 自动推进或询问；
- 多于一个 active change → **列出来让人选，绝不让 Agent 自己猜**（两个 change 交叉实现是大型项目最难 review 的混乱）。

### 1.7 贯穿示例：支付回调幂等的五阶段落地

需求：

```
给支付回调增加幂等控制。
  - 同一个 channel + payTradeNo 重复回调只能业务处理一次。
  - 并发重复回调最多只能插入一条支付流水。
  - 只允许发布一次 OrderPaidEvent。
  - 已经处理成功的重复回调仍然返回 SUCCESS。
  - 不改三方支付协议。
  - 不重构支付网关。
  - 不改变订单状态机。
```

入口：

```
/comet 给支付回调增加幂等控制。
同一个 channel + payTradeNo 重复回调只能处理一次；
并发重复回调只能插入一条支付流水并发布一次 OrderPaidEvent；
已成功处理的重复回调仍返回 SUCCESS；
不改三方支付协议，不重构支付网关，不改变订单状态机。
```

#### 第一阶段：Open —— 不要让需求只活在一句话里

`/comet-open` 让 OpenSpec 接手。一个健康的 change 至少落出这些文件：

```
openspec/changes/add-payment-callback-idempotency/
  .openspec.yaml
  .comet.yaml
  proposal.md
  design.md
  tasks.md
  specs/
    payment-callback/spec.md
```

**`proposal.md` 必须有 Non-Goals**（否则 Agent 容易顺手改支付网关）：

```
## Non-Goals
- 不修改三方支付平台回调协议
- 不重构支付网关和支付渠道抽象
- 不改变订单主状态机定义
- 不处理历史支付流水迁移
```

**`spec.md` 必须写并发场景**（不能只写"重复回调返回成功"）：

```
### Requirement: Payment callback idempotency

The system SHALL process the same payment callback only once.

#### Scenario: same callback arrives concurrently

- GIVEN an order is in WAIT_PAY status
- AND two callbacks have the same channel and payTradeNo
- WHEN both callbacks are handled concurrently
- THEN only one payment record is inserted
- AND only one OrderPaidEvent is published
- AND both callbacks return SUCCESS to the payment channel
```

这不是文档好看——它后面会决定**测试怎么写、实现怎么验收、归档能不能过**。

#### 第二阶段：Design —— 别让方案选择被 AI 自己拍脑袋

支付回调幂等不是一个 `if`。常见方案至少四种：

| 方案 | 优点 | 风险 |
| --- | --- | --- |
| 判断订单状态 | 改动小 | 并发下两个线程都可能读到 `WAIT_PAY` |
| Redis 锁 | 能挡一部分并发 | 锁超时、释放时机和事务提交顺序都要处理 |
| 数据库唯一幂等表 | 约束硬、可审计 | 要设计幂等状态和异常分支 |
| 悲观锁订单行 | 直观 | 容易扩大锁范围，影响订单主流程 |

design 要明确写成**硬约束**（注意 `MUST` / `MUST NOT` / `forbidden`）：

```
## Idempotency design

- The system MUST use database unique constraint for idempotency.
- Unique key MUST be `(channel, pay_trade_no)`.
- Idempotency record and order payment update MUST be in one transaction.
- OrderPaidEvent MUST be published after transaction commit.
- In-memory idempotency cache is forbidden because service runs with multiple replicas.
- Redis lock MAY be used as optimization, but MUST NOT replace database unique constraint.
```

桥接层最需要读的就是这种硬约束。如果后面实现里出现：

```java
private final Set<String> processed = ConcurrentHashMap.newKeySet();
```

那不是"另一种实现方式"——这是**违反设计约束**。

#### 第三阶段：Build —— 把 OpenSpec tasks 变成 Superpowers plan

OpenSpec 的 `tasks.md` 往往是需求视角，粒度给需求评审够用，但给 Agent 执行还太粗：

```
- [ ] 新增 payment_callback_idempotency 表
- [ ] 新增幂等记录 repository
- [ ] 改造支付回调服务
- [ ] 补充重复回调测试
- [ ] 补充并发重复回调测试
- [ ] 归档前做规格合规检查
```

Superpowers 的 plan 要拆成更小的动作（TDD：先写失败测试，再最小实现）：

```
### Task 1: Add repository test for unique idempotency key

Files:
- src/test/java/com/acme/payment/PaymentCallbackIdempotencyRepositoryTest.java

Steps:
- Write a failing test that inserts two records with the same channel and payTradeNo
- Assert the second insert violates unique constraint
- Run targeted repository test and confirm it fails for missing table

Verification:
- ./mvnw -Dtest=PaymentCallbackIdempotencyRepositoryTest test
```

然后才是最小实现：

```
### Task 2: Add idempotency table and repository

Files:
- src/main/resources/db/migration/Vxxx__payment_callback_idempotency.sql
- src/main/java/com/acme/payment/PaymentCallbackIdempotencyRepository.java

Steps:
- Add table with unique key `(channel, pay_trade_no)`
- Add repository insert operation
- Run Task 1 test and confirm it passes
```

**这一步就是 Comet 真正"桥接"的地方**：不是把 `tasks.md` 原封不动丢给 Agent，而是把 OpenSpec 的需求任务交给 Superpowers 的计划和 TDD 纪律。

#### 第四阶段：Verify —— 别把"测试过了"当成"规格符合"

最容易出现一种假通过：单测都过、代码 review 也没大问题，但**实现没有数据库唯一约束**。这种代码可能长这样：

```java
@Transactional
public CallbackResult handle(PaymentCallbackCommand command) {
    Order order = orderRepository.findByOrderNo(command.orderNo())
        .orElseThrow(() -> new OrderNotFoundException(command.orderNo()));

    if (order.isPaid()) {
        return CallbackResult.success();
    }

    order.markPaid(command.payTradeNo(), command.paidAt());
    paymentRecordRepository.save(PaymentRecord.from(command));
    eventPublisher.publishEvent(new OrderPaidEvent(order.getOrderNo()));
    return CallbackResult.success();
}
```

从代码质量看不一定差，但从 OpenSpec 看至少有三个问题：

- 没有 `(channel, payTradeNo)` 唯一幂等记录；
- 并发重复回调可能重复插入支付流水；
- 事件发布时机没有满足"事务提交后发布"的设计约束。

所以 Verify 不能只看一个命令。**固定看四类结果**：

| 检查 | 回答的问题 |
| --- | --- |
| 目标测试 | 当前 task 对应行为是否跑通 |
| 全量测试 | 是否破坏已有功能 |
| 规格合规检查 | 是否满足 Scenario、Non-Goals、MUST / MUST NOT |
| OpenSpec verify | change 工件和规格生命周期是否一致 |

不是 Agent 说"我验证了"就算完。

#### 第五阶段：Archive —— 别把错误规格沉淀成项目真相

OpenSpec 的 archive 会把当前 change 的 delta spec 合并到主规格里。**正因为如此，archive 前必须谨慎**——错误的增量一旦归档，后续 AI 会把它当成系统事实。

`/comet-archive` 负责最后同步和归档。建议把 **archive gate** 写成团队固定要求：

```
Archive Gate:
- tasks.md 全部完成
- Design Doc 和 plan 已关联
- 目标测试通过
- 全量测试通过，或明确说明无法运行的原因
- Scenario 与测试映射完成
- Non-Goals 没有被违反
- MUST / MUST NOT 没有被违反
- verification_report 存在
- branch_status 已处理
- /comet-verify 已通过
```

最关键是最后两条：verify-pass 时要有验证报告，分支状态要处理完成。**归档不是"我觉得差不多了"，归档必须有证据。**

### 1.8 两个轻量入口：hotfix 与 tweak

- `/comet-hotfix`：单点 bug 修复；
- `/comet-tweak`：文案 / 配置 / 文档 / prompt 小调整。

**但它们不是免死金牌，有明确的升级红线**：

| 入口 | 触发升级到 full workflow 的条件 |
| --- | --- |
| hotfix | ≥ 3 个文件 / 涉及架构 / 新模块 / 新依赖 / DB schema / 新公共 API / 超出单函数单模块 |
| tweak | ≥ 5 个文件 / 跨模块协调 / 需要 ≥ 5 个测试 / 增删配置项 / 新能力 / 影响 delta spec |

文章特别点赞这套"升级条件"——它直接拦住了很多线上事故的源头：

> 一开始说是小修。修着修着变成重构。重构完大家还按小修验收。

### 1.9 落地时要盯的 6 个信号

Comet 能自动化很多步骤，但不是银弹。真正落地时盯这 6 个信号：

| 信号 | 正常状态 | 风险状态 |
| --- | --- | --- |
| active change | 只有一个明确 change，或用户已选择 | 多个 change 混在一起，Agent 自己选 |
| `.comet.yaml` | phase、plan、verify_result 可读 | 缺失、拼写错误、状态和文件不一致 |
| `proposal.md` | 有明确 Scope 和 Non-Goals | 只有一句"实现某功能" |
| `design.md` | 有 MUST / MUST NOT | 只有"尽量""建议""优化" |
| `tasks.md` | 能映射到 plan 和测试 | 任务全是大而空的 todo |
| archive gate | 有验证报告和分支处理 | 测试没跑、verify 没过就归档 |

多个 active change 时，正常做法是让 Agent 列出来让人选：

```
当前有多个 OpenSpec change：
1. add-payment-callback-idempotency
2. add-admin-audit-log
3. refactor-order-query-api
请选择要继续哪个。
```

### 1.10 推荐的团队接入流程

1. **安装并诊断**：`npm i -g @rpamis/comet` → `comet init` → `comet doctor` → `comet status`。
2. **开一个中等复杂度、小而真实的需求起步**（支付回调幂等 / 登录记住我 / API Key 管理 / 审计日志补齐 / 租户级配置项 / 老接口兼容改造）。
3. **设计阶段先问四个问题再进 build**：并发靠什么兜底？事务边界在哪？事件何时发？异常怎么返回三方？
4. **Build 前确认执行方式**：复杂业务优先 TDD；多模块但边界清楚才考虑 subagent；**第一次试点别追求并行**，先把单链路跑通。
5. **Verify 失败不要硬归档**：先回答失败的是测试 / 规格合规 / OpenSpec verify / 分支收尾哪一项；失败对应哪个 Scenario；需要回 build 修还是接受规格偏差（接受则 spec 要同步修改）。
6. **Archive 保留人工确认**（这一步代表系统规格进入长期上下文）。

### 1.11 什么时候不用 Comet

| 任务类型 | 建议 |
| --- | --- |
| 改文案、拼写、注释 | 不需要 Comet，直接改 |
| 小配置值调整 | `/comet-tweak` 或直接改 |
| 单点 bug 且不改架构 | `/comet-hotfix` |
| 跨模块需求 | full `/comet` |
| 支付、权限、认证、账务、审计 | full `/comet` |
| 需要长期沉淀规格的能力 | full `/comet` |

Comet 真正适合的场景：**需求影响长期规格 / 实现跨多模块 / 验证不能只靠"能跑" / 后续还希望 AI 读懂这段历史**。

### 1.12 与手写桥接 skill 怎么选

- **想理解原理** → 手写一个 `openspec-superpowers-bridge` 很有价值，能让你看懂桥接层到底在做什么（读 OpenSpec 工件 → 转 Superpowers plan → 执行 TDD → 规格合规检查 → 归档前卡闸）。可以当成"读懂 Comet 的前置课"。
- **要长期用、尤其是团队用** → 优先 Comet。原因：
  1. 状态恢复更稳——`.comet.yaml` 比聊天记录可靠；
  2. 阶段守护更稳——`comet-guard.sh` 比"请记得检查"可靠；
  3. 归档更稳——`comet-archive.sh` 把 delta spec 同步、设计文档标记、change 移动放进一个流程，少靠人脑记。

### 1.13 新手只记这 5 句话

1. Comet 不替代 OpenSpec 和 Superpowers，它是**桥接它们的状态机**。
2. OpenSpec 管 WHAT，Superpowers 管 HOW，Comet **管阶段 / 交接 / 守护 / 归档**。
3. 安装后先跑 `comet doctor`，确认你的 Agent 宿主真的能读取三组 skill。
4. 复杂需求从 `/comet <需求>` 开始，不要绕过 `/comet-open` 直接手搓 change。
5. **archive 前一定要看验证证据**——错误规格一旦归档，后续 AI 会把它当成项目真相。

---

## 第二部分　dst-task-* 现状梳理

### 2.1 实际研发链路：六段（比 Comet 五段多一条 PRD 前置线）

dst 的完整链路是**六段**，因为 dst 比 Comet 多了一条业务方案前置线（`dst-prd-plan`）：

```
dst-prd-plan        PRD → 研发落地计划.md          ← dst 独有（方案层）
   ↓
dst-plan-task       openspec new change            ≈ Comet · Open
   ↓
dst-task-continue   openspec status + instructions ≈ Comet · Design（仅 artifact 部分）
   ↓
dst-task-exec       openspec instructions apply    ≈ Comet · Build
   ↓
dst-task-verify     openspec validate --strict     ≈ Comet · Verify
                    + superpowers:code-reviewer
   ↓
dst-task-archive    openspec archive               ≈ Comet · Archive
                    + 研发计划文档清理
```

### 2.2 每个 skill 的本质（一句话定位）

| skill | 本质 | 对应 CLI 命令 | 与 Comet 的对应关系 |
| --- | --- | --- | --- |
| **dst-prd-plan** | PRD → 研发落地计划的方案拆解；强制 `superpowers:brainstorming` 反向校准、输入完整度评分、Team Lead + 原生 Agent Team | `dst prd-plan init` / `dst get-prd` | **dst 独有**，Comet 无对应 |
| **dst-plan-task** | OpenSpec CLI 创建变更的薄封装 | `openspec new change` + `openspec status --change --json` | ≈ Comet · Open |
| **dst-task-continue** | OpenSpec continue 工作流，一次只创建下一个 artifact | `openspec status` + `openspec instructions <artifact>` | ≈ Comet · Design 的 artifact 部分 |
| **dst-task-exec** | OpenSpec apply 指令的实现推进；严格跟随 CLI 输出，不发明另一套流程 | `openspec instructions --change --json apply` | ≈ Comet · Build（无 plan 中间层、无 build_mode） |
| **dst-task-verify** | OpenSpec 校验 + superpowers:code-reviewer 独立 CR | `openspec validate --type change --strict --json` | ≈ Comet · Verify |
| **dst-task-archive** | OpenSpec 归档 + 研发计划文档治理 | `openspec archive` | ≈ Comet · Archive（多业务交付物清理） |

**关键定位**：

- **dst-task-\* = OpenSpec CLI 的命令路由器**。每个 skill 严格映射一个 CLI 命令，且 skill 正文写明"不要发明另一套流程 / 不要退回手工流程"。
- 阶段衔接**完全依赖 OpenSpec 的 status 状态**（artifact 完成度 + tasks.md 的 checkbox）。
- dst 与 Superpowers 的桥接是"软"的（靠 skill 指令提醒，如 verify 调 code-reviewer）；Comet 的桥接是"硬"的（靠状态文件 + 脚本闸门）。

### 2.3 dst 现有闘门机制（已经做到的）

dst 并非完全没有闸门，它有基于 OpenSpec 状态的轻量 guard：

- **每个 skill 进入前先跑 `openspec status --change --json`**，artifact 不齐就停，并引导 `dst-task-continue` 补产物——这其实是用 OpenSpec 状态实现的"artifact 完整性闸门"，方向和 Comet 一致，只是粒度更粗（只覆盖 artifact 缺失这一类）。
- `dst-task-verify` 校验通过后，**必须先让用户对 CR 做显式选择**，用户做选择前不提示 archive、不自动归档。
- `dst-task-archive` 默认交互式归档，`--skip-specs` / `--yes` / `--no-validate` 都需用户明确要求才传。

---

## 第三部分　差距分析（逐维度）

> 对照 Comet 的设计支柱，逐维度评估 dst-task-* 的现状。结论分三档：**完全缺 / 部分有 / 已具备或更强**。

| # | 维度 | dst-task-\* 现状 | Comet | 差距判断 |
| --- | --- | --- | --- | --- |
| ① | **断点恢复粒度** | 靠 `openspec status` 的 artifact 完成度 + tasks.md checkbox 恢复 | `.comet.yaml` 记录工作流中间态：`phase` / `build_pause`（如 `plan-ready`，等用户选隔离方式）/ `branch_status` / `verify_result` | **缺**。dst 只能恢复到 OpenSpec 知道的粒度，恢复不到"刚生成 plan、正要决定执行方式"这种工作流中间态 |
| ② | **上下文交接完整性** | 各阶段靠 OpenSpec artifact 文件衔接，无校验 | `handoff_context` + `handoff_hash`（SHA256 校验交接内容未被篡改/截断） | **缺**。无交接完整性校验 |
| ③ | **Plan 中间层（tasks→TDD）** | `dst-task-exec` 直接 apply，tasks.md 即执行单元，顺序处理 + 勾 checkbox | Build 阶段把粗 task 转成小步 plan + TDD（先写失败测试 → 最小实现） | **缺**。需求视角的 task 不经细化为执行视角就 apply |
| ④ | **执行方式显式选择** | 顺序 apply，无 build_mode 概念 | `build_mode`：TDD / subagent-driven / direct，带权衡 | **缺**（实现期）。注：dst-prd-plan 的 Solo/Agent Team 是**方案阶段**的协作模式，不是执行期 |
| ⑤ | **阶段闘门强度** | 软提醒 + AskUserQuestion；前置跑 `openspec status` 查 artifact 完整性（不齐即停） | `comet-guard.sh` 阶段退出检查 + archive gate 10 条清单 | **部分有**。dst 的"artifact 完整性检查"≈ Comet guard 的子集，只防 artifact 缺失，不防"verify 没过就 archive"这类工作流跳步 |
| ⑥ | **hotfix / tweak 升级红线** | 无。`dst-plan-task` 所有变更一视同仁 `openspec new change` | `/comet-hotfix`、`/comet-tweak` + 升级条件（≥3 文件 / 涉架构 / 新依赖 / DB schema / 新公共 API → full） | **完全缺**。这正是 Comet 拦住"小修混进架构变更"的机制 |
| ⑦ | **Verify 规格合规维度** | `openspec validate --strict` + superpowers:code-reviewer 通用 CR | 固定四类：目标测试 / 全量测试 / **规格合规（Scenario·Non-Goals·MUST/MUST NOT）** / OpenSpec verify | **部分有**。有规格校验 + 通用 CR，但缺"Scenario↔测试映射""Non-Goals/MUST 是否被违反"的结构化逐条核对（CR 是 subAgent 自由审查，不对着 Scenario 打表） |
| ⑧ | **Archive gate** | `openspec archive`（CLI 内部 validate）+ 研发计划文档清理 | 显式 10 条：tasks 完成 / design&plan 关联 / 目标+全量测试通过 / Scenario 映射 / Non-Goals 未违反 / MUST 未违反 / verification_report 存在 / branch_status 处理 / verify 已过 | **缺**。无显式归档前置清单，靠"verify 先过 + archive 内部 validate"组合，但"验证报告存在 / 分支状态处理 / Scenario 映射"不强制 |
| ⑨ | **单一入口 / 阶段路由** | 用户需自行判断调哪个 skill，无总入口；多 change 时各自 `openspec list` 让用户选 | `/comet` 单入口自动检测 active change 数（0→open / 1→自动 / >1→列表让用户选） | **缺**。无"总指挥"入口做阶段检测和路由；不主动拦截"多 change 交叉实现" |

### dst 相对 Comet 的独有 / 优势点（客观补上）

差距分析不能只说 dst 缺什么，dst 有三处是 Comet 没有的：

1. **PRD → 研发计划前置线（dst-prd-plan）—— dst 最大优势**
   - Comet 的 Open 直接从需求一句话开始造 change；
   - dst 有独立方案层：强制 `superpowers:brainstorming` 反向校准、输入完整度评分（需求表达分 / 目标清晰度 / 期望产出 / 范围边界，不过线先澄清）、Team Lead + 原生 Agent Team、前后端契约对齐、Team Lead 三类审计（矛盾 / 漏项 / 证据不足），产出 `研发落地计划.md`。
   - 这恰恰补上了 Comet 文章里**需求侧理解深度不足**的短板。

2. **dst-task-verify 集成了 superpowers:code-reviewer**
   - 这是文章反复说的"OpenSpec + Superpowers 真正桥接"的落点，纯 OpenSpec 没有；
   - dst 在 verify 这步**强制启动独立 subAgent**，不能主线程口头 review，CR 范围默认 `HEAD~1..HEAD`。

3. **dst-task-archive 有业务交付物治理**
   - 归档后保留 `02-最终交付/研发落地计划.md`、清理冗余落地方案文档（`研发落地计划.md` / `研发落地方案.md` 同类主文档只留一份）；
   - Comet 只管 OpenSpec spec 归档，不管业务交付文档。

### 一句话定论

| 强项 | 短板 |
| --- | --- |
| dst 强在**需求侧**（PRD 方案理解、brainstorming 校准、Agent Team）和**归档侧**（交付文档治理） | dst 缺在**实现执行侧**：工作流状态化、tasks→TDD plan 细化、执行方式选择、规格合规结构化检查、小修升级红线、单一入口路由 |

> **dst 是一只"重头轻尾"的桥接**：需求 → 方案这半段做得比 Comet 重；方案 → 实现 → 归档这半段，靠 OpenSpec CLI 状态兜底，缺 Comet 那层独立工作流状态机和脚本闸门。

---

## 第四部分　dst 演进优先级建议

> 按「投入产出比 × 风险拦截价值」排序。以下均为**结论与方向**，若要落地任一项，需另行出具体改动方案并经确认。

### 🔴 P0｜小修升级红线（对应差距⑥）

- **价值**：投入最小、事故拦截价值最高。拦住"小修混进架构变更导致线上事故"——这是 Comet 文章反复强调的最高 ROI 机制。
- **方向**：给 `dst-plan-task` 加一个"变更规模预判"——≥3 文件 / 涉架构 / 新依赖 / DB schema / 新公共 API 时，提示用户升级到完整 change 流程，而非一视同仁 `openspec new change`。
- **落地成本**：**纯 skill 指令即可实现，无需状态文件、无需新基础设施**。

### 🟠 P1｜Verify 规格合规结构化（对应差距⑦）

- **价值**：dst 已有 `openspec validate` + code-reviewer，只差"对着规格打表"这一步，边际成本低、规格回归收益高。
- **方向**：让 code-reviewer 的 prompt **固定对着 Scenario / Non-Goals / MUST-MUST NOT 逐条核对**，输出结构化合规表，而非 subAgent 自由审查。同时补"Scenario↔测试映射"检查。
- **落地成本**：改动集中在 `dst-task-verify` 的 CR 模板与 `superpowers:code-reviewer` 调用上下文。

### 🟡 P2｜断点恢复工作流态（对应差距①②）

- **价值**：收益是跨会话恢复（Agent 断线后能续上"刚生成 plan、正要选执行方式"这种中间态）。
- **方向**：引入一个类似 `.comet.yaml` 的轻量状态文件，记录 `phase` / `build_pause` / `branch_status` / `handoff_hash`。
- **落地成本**：**唯一需要新增基础设施**的一项。当前 dst 靠 OpenSpec status 也能勉强恢复，可后置。

### 🟢 P3｜tasks→TDD plan 转换 + 单一入口（对应差距③⑨）

- **价值**：tasks→TDD 转换的价值依赖团队是否真用 TDD；单一入口 `/dst` 自动路由降低用户心智负担。
- **方向**：在 `dst-task-exec` 前增加"task 细化为 TDD 小步 plan"环节；新增一个总入口 skill 做 active change 检测与阶段路由。
- **落地成本**：改动面较大，建议观察 P0-P1 落地效果后再评估。

### 优先级矩阵

| 优先级 | 项 | 投入 | 拦截/收益价值 | 是否需新基础设施 |
| --- | --- | --- | --- | --- |
| P0 | 小修升级红线 | 低 | 高（事故拦截） | 否 |
| P1 | Verify 规格合规结构化 | 中 | 中高（规格回归） | 否 |
| P2 | 断点恢复工作流态 | 高 | 中（跨会话恢复） | **是** |
| P3 | tasks→TDD + 单一入口 | 高 | 视团队 TDD 采用度 | 部分 |

---

## 附录　参考资料与术语

### 参考资料

- **Comet GitHub README-zh**：https://github.com/rpamis/comet/blob/master/README-zh.md
- **Comet npm 包**：https://www.npmjs.com/package/@rpamis/comet
- **OpenSpec GitHub**：https://github.com/Fission-AI/OpenSpec
- **Superpowers GitHub**：https://github.com/obra/superpowers
- **CodeGraph GitHub**：https://github.com/colbymchenry/codegraph
- **原始文章**：https://mp.weixin.qq.com/s/Pl9gco7jXXKa7whi0vCuZw

### 术语对照

| 术语 | 含义 |
| --- | --- |
| **OpenSpec** | 需求规格化框架，管 WHAT（proposal / design / tasks / spec / archive） |
| **Superpowers** | 执行纪律 skill 集，管 HOW（brainstorming / writing-plans / TDD / code-reviewer / verification） |
| **Comet** | 桥接 OpenSpec + Superpowers 的工作流状态机，管阶段 / 交接 / 守护 / 归档 |
| **delta spec** | 一个 change 相对主规格的增量规格，归档时合并进主规格 |
| **archive gate** | 归档前置闸门，Comet 为 10 条硬性清单 |
| **build_mode** | Comet Build 阶段的执行方式：TDD / subagent-driven-development / direct |
| **build_pause** | Comet 工作流中间态标记，如 `plan-ready`（plan 已就绪，等用户选隔离方式） |
| **handoff_hash** | Comet 阶段交接内容的 SHA256 完整性校验 |
| **Non-Goals** | proposal 中"明确不做"的边界，防止 Agent 顺手改无关模块 |
| **Scenario** | spec 中 GIVEN/WHEN/THEN 形式的场景，决定测试怎么写、能否归档 |

### 本仓库相关 skill 索引

| skill | 文件 |
| --- | --- |
| dst-plan-task | `.claude/skills/dst-plan-task/SKILL.md` |
| dst-task-continue | `.claude/skills/dst-task-continue/SKILL.md` |
| dst-task-exec | `.claude/skills/dst-task-exec/SKILL.md` |
| dst-task-verify | `.claude/skills/dst-task-verify/SKILL.md` |
| dst-task-archive | `.claude/skills/dst-task-archive/SKILL.md` |
| dst-prd-plan | `.claude/skills/dst-prd-plan/SKILL.md` |

---

> **文档结论**：dst-task-* 已是一只"重头轻尾"的 OpenSpec + Superpowers 桥接。如果要向 Comet 看齐，**最高 ROI 的起点是小修升级红线（P0）与 Verify 规格合规结构化（P1）**——这两项不引入新基础设施，纯 skill 指令即可增强，且直接命中"小修混架构"和"假通过"两类最常见线上风险。
