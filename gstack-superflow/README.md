# gstack-superflow

融合 **Gstack**（规划）+ **Superpowers**（执行）的 spec-driven AI 编程工作流插件。用桥接转换层把 Gstack 的 spec/plan 产物转换为 Superpowers 可执行任务。

> **状态：计划 1（核心引擎 + 最小闭环）。** 完整 vendor skills 库、多平台、Conductor 在计划 2。
> 设计文档：`../docs/superpowers/specs/2026-07-06-gstack-superflow-design.md`

## 安装（开发期，本地）

```bash
cd gstack-superflow
npm install   # 目前零运行时依赖，仅初始化
```

在 Claude Code 中加载本插件目录的 skills（符号链接或复制 `skills/*` 到 `~/.claude/skills/`）。

## CLI

```bash
node src/cli/gsf.mjs state [dir]      # 查看当前工作流状态
node src/cli/gsf.mjs validate [dir]   # 校验状态与 handoff 门禁
node src/cli/gsf.mjs build-handoff <specPath>  # 读 spec 生成 handoff-contract.md
node src/cli/gsf.mjs doctor           # 版本与健康检查
```

## 工作流

```
thinking → planning → specifying → bridging → executing → reviewing → closing
                                                       ↘ debugging ↗
```

- 规划段（Gstack）：`/office-hours` → `/autoplan` → `/spec`
- 桥接：`bridge-builder` 生成 `handoff-contract.md`（须用户批准）
- 执行段（Superpowers）：`writing-plans` → `executing-plans` + TDD → `verification`

铁律：无 `handoff-contract.md` 或未被用户批准 → `guard` 拦截执行。

## 测试

```bash
npm test
```

## 上游与许可

- Gstack（MIT）：https://github.com/garrytan/gstack —— 计划 2 vendor 完整 skills
- Superpowers（MIT）：https://github.com/obra/superpowers —— 计划 2 vendor 完整 skills
- 本项目 MIT，版权归上游各自的作者所有。
