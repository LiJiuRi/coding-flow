# openflow 与 spec-superflow CLI 实现与发布机制分析报告

> 分析对象：`@lininn/openflow` v0.4.5-beta.0 ｜ `spec-superflow` v0.6.0
> 主题：两者如何通过 `npm install -g` 变成全局可用命令、CLI 入口如何实现、如何发布到 npm registry
> 分析粒度：实现级（已读取 bin 入口、CLI 源码、构建配置、CI workflow、.gitignore）
> 生成日期：2026-06-30
> 配套文档：[openflow 详细分析报告](./openflow-详细分析报告.md) ｜ [spec-superflow 详细分析报告](./spec-superflow-详细分析报告.md) ｜ [工作流对比分析报告](./工作流对比分析报告.md)

---

## 目录

1. [结论速览](#1-结论速览)
2. [核心机制：`npm install -g` 做了什么](#2-核心机制npm-install--g-做了什么)
3. [openflow 的 CLI 实现链路](#3-openflow-的-cli-实现链路)
4. [spec-superflow 的 CLI 实现链路](#4-spec-superflow-的-cli-实现链路)
5. [并排对比](#5-并排对比)
6. [发布自动化差异：手动 vs CI](#6-发布自动化差异手动-vs-ci)
7. [Windows shim 与 cmdExists 隐患的呼应](#7-windows-shim-与-cmdexists-隐患的呼应)
8. [通用公式：自己做一个 npm CLI 的最小要素](#8-通用公式自己做一个-npm-cli-的最小要素)
9. [结论](#9-结论)

---

## 1. 结论速览

**两个项目都支持通过 `npm install -g` 安装为全局 CLI**，且命令分别是：

```bash
npm install -g @lininn/openflow      # → 全局命令 openflow
npm install -g spec-superflow        # → 全局命令 ssf 和 spec-superflow
```

两者都遵循 npm CLI 包的通用公式（`bin` 字段 + shebang + 入口进包 + 发到 registry），但在**入口设计、依赖策略、构建产物处理、发布自动化**四个方面给出了几乎对立的实现选择：

| | openflow | spec-superflow |
|---|---|---|
| 入口设计 | 薄 shim → TS 编译的 dist | 自包含 `.mjs` 路由器 |
| CLI 框架 | `commander` | 零依赖手写（`node:util.parseArgs`） |
| 运行时依赖 | 5 个 | **0 个** |
| dist 处理 | 不入库，发布时现场编译 | 入库，clone 即用 |
| 发布方式 | 手动 `npm publish` | CI 自动发布（tag 触发） |

---

## 2. 核心机制：`npm install -g` 做了什么

无论哪个项目，能被全局安装成命令，靠的都是 npm 的同一套机制，核心只有一个字段：**`bin`**。

当执行 `npm install -g @lininn/openflow` 时，npm 会：

1. 从 npm registry 下载 tarball，解压到全局 `node_modules`。
2. 读取 `package.json` 的 **`bin` 字段**（命令名 → 入口文件路径的映射）。
3. 在系统的全局 bin 目录创建可执行的 **shim（垫片）**：
   - **Unix**：在 `/usr/local/bin`（或 `~/.npm-global/bin`）创建符号链接或脚本，指向包内的入口文件。
   - **Windows**：在 `%AppData%\npm\` 生成 `openflow.cmd`、`ssf.cmd` 这样的 shim（因为 Windows 不认 shebang，必须靠 `.cmd` 包装）。
4. shim 内部调用 `node` 去执行真正的 `.js`/`.mjs` 入口文件。
5. 入口文件首行的 **shebang** `#!/usr/bin/env node` 确保直接执行时由 node 解释。

所以"做成全局 CLI"的必要条件只有 4 个：

> **`bin` 字段 + shebang + 入口文件进了发布包 + 包发到了 registry**

下面看两者各自的实现细节。

---

## 3. openflow 的 CLI 实现链路

### 3.1 bin 字段（证据：`package.json:5-7`）

```json
"bin": { "openflow": "bin/openflow.js" }
```

注册一个命令 `openflow`，指向 `bin/openflow.js`。

### 3.2 入口是"薄 shim"（证据：`bin/openflow.js` 全文 5 行）

```js
#!/usr/bin/env node
import { run } from '../dist/cli/index.js';
run();
```

入口**自身不含业务逻辑**，只负责加载 `dist/cli/index.js` 并调用 `run()`。shebang 在第 1 行。这是一种典型的"入口极薄、逻辑分层"的做法——入口只做引导，便于维护和跨平台。

### 3.3 真正的 CLI 逻辑在 TypeScript 源码（证据：`src/cli/index.ts`）

```ts
import { Command } from 'commander';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const pkg = require('../../package.json') as { version: string };

export function run(): void {
  const program = new Command();
  program.name('openflow').description('...').version(pkg.version);
  program.addCommand(initCommand);     // openflow init
  program.addCommand(statusCommand);   // openflow status
  program.addCommand(updateCommand);   // openflow update
  program.parse();
}
```

- 用 **`commander`** 框架注册 `init / status / update` 三个子命令。
- 版本号用 `createRequire(import.meta.url)` 在编译期从 `package.json` 读取（运行时单源，避免版本号漂移）。

### 3.4 构建链：TS 源码必须编译成 dist（证据：`package.json` scripts + `.gitignore`）

```
src/cli/*.ts  ──tsc (npm run build)──▶  dist/cli/index.js  ◀── bin/openflow.js 引用
```

- `.gitignore` 里写着 `dist/` —— **dist 不入库**。
- 所以发布前必须现场编译：`"prepublishOnly": "npm run build"`（`package.json:16`）保证 `npm publish` 时 dist 是最新的。

> ⚠️ 关键：因为 `bin/openflow.js` 引用的是 `../dist/cli/index.js`，如果发布时 dist 缺失或过期，全局安装后 `openflow` 命令会直接报模块找不到。`prepublishOnly` 是防止这个事故的保险。

### 3.5 发布清单（证据：`package.json:35-44` `files` 字段）

```json
"files": ["bin", "dist", "openflow-architecture.png", "openflow-architecture.svg",
          "openflow-workflow.png", "openflow-workflow.svg", "templates", "scripts"]
```

明确告诉 npm 只发布这些目录。其中：

- `bin/` —— CLI 入口。
- `dist/` —— 编译产物（现场编译后进包）。
- `templates/` —— **关键**：`openflow init` 的工作就是把 templates 拷贝到各工具的 skills 目录，所以 templates 必须进包。
- 4 张架构图 —— README 引用，随包发布便于离线查看。

### 3.6 发布方式：手动（证据：`.github/workflows/ci.yml`）

openflow 的 CI 只有 `lint → build → test`，**没有 release/publish job**。结合 `prepublishOnly` 脚本判断，openflow 是**作者在本地手动执行 `npm publish`** 发布的，不是 CI 自动发布。

### 3.7 postinstall 脚本（证据：`scripts/postinstall.js`）

```js
console.log(`
openflow — OpenSpec + Superpowers workflow orchestrator

Initialize a project:
  openflow init --tools claude
...`);
```

- `package.json:17` 配置 `"postinstall": "node ./scripts/postinstall.js"`。
- 内容**只打印使用说明 banner，不做任何文件操作**——安装时不会自动改你的项目，必须手动跑 `openflow init`。
- 这是一种"非变异 postinstall"的安全设计，不会在用户项目里留下意外改动。

---

## 4. spec-superflow 的 CLI 实现链路

### 4.1 bin 字段：双命令名同入口（证据：`package.json:7-10`）

```json
"bin": {
  "ssf": "./scripts/spec-superflow.mjs",
  "spec-superflow": "./scripts/spec-superflow.mjs"
}
```

注册**两个命令**（短命令 `ssf` + 全名 `spec-superflow`），都指向同一个 `.mjs` 文件。这是常见的"短别名"做法——用户敲 `ssf` 更省事，`ssf` 即 "spec-superflow" 的缩写。

### 4.2 入口是"自包含的零依赖路由器"（证据：`scripts/spec-superflow.mjs` 全文）

```js
#!/usr/bin/env node
// spec-superflow CLI — zero-dependency CLI for spec management
import { parseArgs } from 'node:util';

const COMMANDS = {
  list:     () => import('./lib/cmd-list.mjs'),
  validate: () => import('./lib/cmd-validate.mjs'),
  doctor:   () => import('./lib/cmd-doctor.mjs'),
  version:  () => import('./lib/cmd-version.mjs'),
  sync:     () => import('./lib/cmd-sync.mjs'),
  config:   () => import('./lib/cmd-config.mjs'),
  state:    () => import('./lib/cmd-state.mjs'),
  inject:   () => import('./lib/cmd-inject.mjs'),
};

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(HELP); process.exit(0);
  }
  if (args.includes('--version') || args.includes('-v')) {
    const pkg = JSON.parse(
      (await import('node:fs')).readFileSync(
        new URL('../package.json', import.meta.url), 'utf-8'
      )
    );
    console.log(pkg.version); process.exit(0);
  }
  const command = args[0];
  if (!COMMANDS[command]) {
    console.error(`Unknown command: ${command}`);
    console.error(`Run "ssf --help" for available commands.`);
    process.exit(2);
  }
  const mod = await COMMANDS[command]();   // 动态 import，按需加载
  await mod.run(args.slice(1));
}

main().catch(err => { console.error(`Error: ${err.message}`); process.exit(1); });
```

这是与 openflow 完全不同的设计选择：

- **不用 commander**，纯手写路由（`process.argv` 切片 + `COMMANDS` 映射表 + 退出码）。
- **懒加载**：每个子命令是 `() => import(...)` 闭包，只有被调用时才动态 import 对应模块——启动快、省内存（跑 `ssf list` 不会加载 `ssf sync` 的代码）。
- **版本号运行期读取**：用 `node:fs` 现读 `package.json`（而 openflow 是编译期固化）。
- **零运行时依赖**：连 CLI 框架都不用，只靠 Node 内置的 `node:util.parseArgs`（Node 18+ 内置）。
- **退出码语义清晰**：0 正常、1 运行时错误、2 未知命令。

### 4.3 入口直接是源码，无需"编译成可执行入口"

`.mjs` 文件本身就能被 Node 直接执行（ESM 原生支持），所以 `ssf` 入口**不需要先编译**。但 CLI 子命令（如 `cmd-validate.mjs`）会 import 内嵌引擎，引擎是 TS 写的、需要编译成 `dist/` 才能被子命令调用。

### 4.4 构建产物 dist 是入库的（证据：`.gitignore`）

```
# Build output (rebuild with: npm run build)
# dist/ is committed so the plugin works out-of-the-box after clone.
# Uncomment the next line if you prefer to not track compiled output:
# dist/
```

注释明确：**dist 提交进 git**，为的是 clone 后无需 build 即可用（`ssf doctor` 的健康检查也把 dist 存在性列为检查项）。这与 openflow（dist 不入库、靠 prepublishOnly 现场编译）正好相反。

### 4.5 发布清单：无 `files` 字段、无 `.npmignore`

spec-superflow 的 `package.json` 没有 `files` 字段，也没有 `.npmignore`。npm 默认行为是"发布 git 里所有未忽略文件"——而 dist 未被 `.gitignore` 忽略，所以 dist 随包发布。CLI 子命令运行时 `import('../dist/index.js')` 才能拿到引擎。

> ⚠️ 这种"无 files 字段"做法的潜在风险：会把仓库里所有未忽略文件都发包（如 `docs/`、`specs/`、`examples/`、`.github/` 等），包体积通常比 openflow 的精准清单大。好处是简单、不会漏发依赖文件。

### 4.6 发布方式：CI 自动发布（证据：`.github/workflows/ci.yml` release job）

```yaml
release:
  name: Release
  if: startsWith(github.ref, 'refs/tags/v')   # 打 tag 触发
  permissions:
    contents: write
    id-token: write
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 22
        registry-url: https://registry.npmjs.org
        cache: npm
    - run: npm ci
    - run: npm run build                        # 确保最新 dist
    - run: npm test
    - name: Create GitHub Release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: gh release create "$GITHUB_REF_NAME" --generate-notes
    - name: Publish to npm
      run: npm publish --provenance --access public   # 自动发 npm
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

打一个 `v*` tag → CI 自动跑测试 → 创建 GitHub Release → 自动 `npm publish`（带 `--provenance` SLSA 来源证明）。这是比 openflow 更工业化的发布流水线。

---

## 5. 并排对比

| 维度 | openflow | spec-superflow |
|---|---|---|
| **bin 命令数** | 1（`openflow`） | 2（`ssf` + `spec-superflow`，同入口） |
| **bin 路径** | `bin/openflow.js` | `scripts/spec-superflow.mjs` |
| **CLI 框架** | `commander` | 零依赖手写（`node:util.parseArgs`） |
| **入口形态** | 薄 shim（5 行）→ 调 TS 编译的 dist | 自包含 `.mjs` 路由器，Node 直接执行 |
| **子命令加载** | commander 静态注册 3 个 | 动态 `import()` 懒加载 8 个 |
| **运行时依赖** | 5 个（chalk/commander/inquirer/ora/yaml） | **0 个** |
| **版本号读取** | 编译期 `createRequire` 读 package.json | 运行期 `node:fs` 现读 package.json |
| **dist 处理** | 不入库，`prepublishOnly` 现场编译 | **入库**，clone 即用 |
| **发布清单** | `files` 字段明确列出（精准） | 无 `files`/无 `.npmignore`（默认全发） |
| **postinstall** | 打印 banner（非变异） | 无 |
| **发布方式** | ⚠️ 手动 `npm publish`（CI 无 publish） | ✅ CI 自动发布（tag 触发，带 provenance） |

### 5.1 两种 CLI 设计哲学

- **openflow 的"薄入口 + 框架 + 编译期"模式**：入口只引导，靠 commander 处理命令解析，TS 编译保证类型安全。优点是规范、可读、借助成熟框架；缺点是依赖多、需要构建步骤。

- **spec-superflow 的"自包含 + 手写 + 零依赖"模式**：入口即路由器，手写参数解析，懒加载子命令。优点是零依赖、启动快、Node 22 原生跑 .ts/.mjs；缺点是命令解析逻辑要自己维护（帮助文本、参数校验都得手写）。

两者各有取舍，都是合理选择。spec-superflow 的零依赖哲学与其"自包含插件"定位一致；openflow 的框架依赖与其"编排器"定位也不冲突（毕竟它运行时本来就要交互式引导，inquirer/ora 这些 UI 库是必需的）。

---

## 6. 发布自动化差异：手动 vs CI

两者最大的工程化差距其实不在 CLI 本身，而在**怎么把包送到 npm registry**：

### 6.1 openflow：手动发布

- CI 只跑测试，发布是作者本地手动 `npm publish`。
- 由 `prepublishOnly: npm run build` 保证发布前现场编译最新 dist。
- 简单直接，但依赖人工纪律，没有 provenance（供应链来源证明）。

### 6.2 spec-superflow：CI 自动发布

- `git tag v0.6.0 && git push --tags` 即触发完整发布流水线。
- 流程：test → GitHub Release（自动生成 notes）→ `npm publish --provenance --access public`。
- 更可靠、可追溯、防篡改。`--provenance` 是 npm 较新的供应链安全特性，会在 registry 上公示构建来源。
- 需要配置两个 secret：`GITHUB_TOKEN`（内置）和 `NPM_TOKEN`（手动配置），以及 `id-token: write` 权限（用于 provenance）。

> **建议**：openflow 若要提升工程化水平，可以借鉴 spec-superflow 的 CI 发布流水线——把手动 `npm publish` 改成 tag 触发的自动化发布，减少人工操作风险。

---

## 7. Windows shim 与 cmdExists 隐患的呼应

这里有一个值得指出的"对称性"细节：

- **自己被装**：openflow 和 spec-superflow 被 `npm install -g` 时，npm 在 Windows 上会**正确生成** `openflow.cmd` / `ssf.cmd` shim，所以用户敲 `openflow`、`ssf` 都能正常工作。
- **检测别人装没装**：openflow 在 `init` 时要检测上游 `openspec` 是否安装，用的是自写的 `cmdExists`（`src/utils/shell.ts:44-59`）——它遍历 `PATH` 时**只匹配裸名，不尝试 `.cmd`/`.bat`/`.ps1` 扩展名**。而 npm 在 Windows 上装的全局包通常是 `openspec.cmd`，所以这个检测在 win32 上**可能误判 openspec 未安装**。

也就是说：npm 自己处理 shim 是完备的，但 openflow 自己实现的检测逻辑不完备。本项目正运行在 win32，这是现实风险（详见 [openflow 详细分析报告 §7.2](./openflow-详细分析报告.md)）。

修复方法：`cmdExists` 应在遍历 PATH 时，对每个目录尝试附加 `process.env.PATHEXT` 列出的扩展名（Windows 上 `PATHEXT=.COM;.EXE;.BAT;.CMD;...`）。

---

## 8. 通用公式：自己做一个 npm CLI 的最小要素

从这两个项目提炼出的通用公式，任何人要做 npm CLI 都适用：

### 8.1 必须具备的 4 个要素

1. **`package.json` 加 `bin` 字段**：`{ "命令名": "./入口文件" }`。可注册多个别名指向同一入口。
2. **入口文件首行写 shebang**：`#!/usr/bin/env node`。
3. **入口文件及其依赖必须进得了发布包**：
   - 方式 A（推荐）：用 `files` 字段明确列出（像 openflow）。
   - 方式 B：确保产物不被 `.gitignore`（像 spec-superflow 的 dist）。
4. **发布到 registry**：`npm publish`（手动）或 CI（tag 触发）。

### 8.2 TypeScript 项目的额外步骤

5. **加 `prepublishOnly`**：`"prepublishOnly": "npm run build"`，确保发布前现场编译最新 dist。
6. **入口指向 dist**：`bin` 指向的入口要么是编译产物，要么是引用 `../dist/...` 的薄 shim（像 openflow）。

### 8.3 工业化发布（可选但推荐）

7. **CI 自动发布**：tag 触发，`npm publish --provenance --access public`，配置 `NPM_TOKEN` 和 `id-token: write`（像 spec-superflow）。
8. **版本号单源**：运行时从 `package.json` 读，避免多处硬编码漂移（openflow 编译期读、spec-superflow 运行期读，都是单源）。

### 8.4 可选：postinstall

9. **postinstall**：只在需要在安装时执行副作用时才加。openflow 示范了"只打印提示、不动文件"的安全做法——**绝不建议在 postinstall 里偷偷改用户项目**，这会引发信任问题和卸载困难。

---

## 9. 结论

**openflow 和 spec-superflow 都支持 `npm install -g` 全局安装 CLI**，命令分别是 `openflow` 和 `ssf`（+ `spec-superflow` 别名）。两者都遵循 npm CLI 包的通用公式，但实现风格对立：

- **openflow** 走"**薄入口 + commander 框架 + TS 编译 + 精准 files 清单 + 手动发布**"路线——规范、可读、依赖成熟工具，但需要构建步骤、依赖较多、发布靠人工。
- **spec-superflow** 走"**自包含 .mjs + 零依赖手写 + dist 入库 + CI 自动发布**"路线——轻量、启动快、发布可靠可追溯，但命令解析要自己维护、发包清单不够精准。

两者的共同点是都正确使用了 npm 的 `bin` + shebang + registry 三件套，差异点集中在**入口设计哲学、依赖策略、构建产物处理、发布自动化**四个维度——这恰好是两个项目"编排器 vs 融合器"总体定位在 CLI 层面的具体投射：openflow 借力外部（commander、预装上游），spec-superflow 一切自包含（零依赖、dist 入库）。

> **一句话**：能被 `npm install -g` 装成命令，靠的是 `bin` 字段 + shebang + 入口进包 + 发到 registry 这四件套；至于入口怎么写、靠不靠框架、dist 怎么处理、发布用不用 CI，两个项目给出了"借力外部"与"一切自包含"两种都成立的范式。

---

> **附**：本报告与三份主报告配套，专门聚焦 CLI 实现与 npm 发布的横切主题。完整证据见各主报告。
