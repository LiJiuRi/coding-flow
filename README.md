# coding-flow

本仓库是一个**总仓（meta repository）**，通过 Git submodule 汇聚并引用三个开源工作流（workflow）项目，便于统一拉取、对比研究与本地开发；同时收录了对这三个项目的分析报告（见 [`reports/`](./reports)）。

> 总仓本身**不包含**三个子项目的源码，只在 `.gitmodules` 中记录它们的远程地址与固定 commit 指针。源码仍保留在各自的 GitHub 仓库中。

## 包含的子项目

| 子项目 | 来源仓库 | 当前指向 | 分支 | 分析报告 |
|---|---|---|---|---|
| comet | [rpamis/comet](https://github.com/rpamis/comet) | `f43cf7b` | master | [comet-详细分析报告](./reports/comet-详细分析报告.md) |
| openflow | [lininn/openflow](https://github.com/lininn/openflow) | `698fbfe9` | main | [openflow-详细分析报告](./reports/openflow-详细分析报告.md) |
| spec-superflow | [MageByte-Zero/spec-superflow](https://github.com/MageByte-Zero/spec-superflow) | `a764f2b2` | main | [spec-superflow-详细分析报告](./reports/spec-superflow-详细分析报告.md) |

横向对比见 [`reports/工作流对比分析报告.md`](./reports/工作流对比分析报告.md)。

## 目录结构

```
coding-flow/
├── .gitmodules           # submodule 配置（自动生成）
├── comet/                # submodule → rpamis/comet
├── openflow/             # submodule → lininn/openflow
├── spec-superflow/       # submodule → MageByte-Zero/spec-superflow
└── reports/              # 本仓自有内容：项目分析报告
    ├── images/
    ├── comet-详细分析报告.md
    ├── openflow-分析报告.md
    ├── openflow-详细分析报告.md
    ├── spec-superflow-详细分析报告.md
    ├── 工作流对比分析报告.md
    └── CLI实现与发布分析报告.md
```

## 克隆

由于使用了 submodule，克隆时需带上 `--recursive` 以一并拉取三个子项目：

```bash
git clone --recursive <本仓地址>
```

若已克隆但未带 `--recursive`，可补拉子项目：

```bash
git submodule update --init --recursive
```

## 更新子项目到上游最新

```bash
git -C <子项目目录> pull          # 拉取该子项目的上游更新
git add <子项目目录>              # 总仓记录新的 commit 指针
git commit -m "bump <子项目>"
```

## 备注

- 三个子项目分属不同 GitHub 账号（`rpamis` / `lininn` / `MageByte-Zero`），均为第三方开源项目，本仓仅作引用与整合。
- submodule 远程地址采用 SSH（`git@github.com:…`）。如需切换为 HTTPS，修改 `.gitmodules` 中对应 `url` 即可。
