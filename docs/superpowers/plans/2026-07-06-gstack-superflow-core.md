# gstack-superflow 核心引擎与最小闭环 实现计划（计划 1）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建 gstack-superflow 的核心引擎（状态加载/转移 guard/桥接转换层/CLI），并用最小 skills 跑通 `Gstack spec → handoff-contract → Superpowers plan` 的端到端闭环。

**Architecture:** 三段式 + 桥接转换。Gstack 规划段产物（spec/design doc/plan）由 `contract-builder` 解析为 `handoff-contract.md`（意图锁 + 任务切片 + 测试义务 + review gates），`guard.mjs` 拦截"无 handoff 或未批准则不许执行"，状态由 `state-loader` 持久化到 `.gstack-superflow.yaml`。`workflow-start` 做内容级状态路由。

**Tech Stack:** Node.js >=20（ESM / `.mjs`）、`node:test`（内置，零依赖）、npm、零运行时依赖。

**Scope:** MVP 第一部分。完整 vendor skills 库（Gstack 7 个 + SP 全套）、多平台 manifest、Conductor、浏览器 QA 留待计划 2。本计划的 Gstack/SP skill 用 minimal 版（自洽、可跑通闭环、无占位符），计划 2 替换为上游完整版。

## Global Constraints

- Node `>=20`，纯 ESM（`.mjs`），**零运行时依赖**（devDependencies 仅 `node:test` 已内置，无需安装）
- 包管理器：npm
- 所有代码位于 `coding-flow/gstack-superflow/`
- CLI 名 `gsf`，状态文件名 `.gstack-superflow.yaml`，handoff 文件名 `handoff-contract.md`
- 许可证 MIT；vendor 的上游内容（Gstack / Superpowers）须在文件头注明来源与上游 commit
- 测试一律用 `node --test`；每个引擎模块必须有单测
- 不引入 yaml/markdown 解析库——状态文件用 `.gstack-superflow.yaml` 但本计划内按"简单 KV 文本"解析（计划 2 视需要升级）

## File Structure

```
gstack-superflow/
├── package.json                    # npm manifest + gsf bin
├── plugin.json                     # Claude Code plugin 描述（Task 10）
├── LICENSE                         # MIT
├── README.md                       # 安装与用法（Task 12）
├── .gitignore
├── src/
│   ├── lib/
│   │   ├── state-loader.mjs        # 读写 .gstack-superflow.yaml（Task 2）
│   │   ├── schema.mjs              # handoff 字段定义 + 校验（Task 3）
│   │   ├── contract-builder.mjs    # Gstack 产物 → handoff（Task 4）
│   │   └── guard.mjs               # 转移矩阵 + handoff/批准门禁（Task 5）
│   └── cli/
│       └── gsf.mjs                 # validate/state/doctor（Task 6）
├── skills/
│   ├── workflow-start/SKILL.md     # 状态路由入口（Task 8）
│   ├── bridge-builder/SKILL.md     # 包装 contract-builder（Task 7）
│   ├── gstack-spec/SKILL.md        # minimal Gstack /spec（Task 9）
│   └── sp-writing-plans/SKILL.md   # minimal SP writing-plans（Task 9）
├── hooks/
│   └── session-start.mjs           # 注入 workflow-start（Task 10）
├── templates/
│   └── handoff-contract.md         # handoff 模板（Task 7）
├── fixtures/                       # 测试用 Gstack 产物样本
│   ├── sample-spec.md              #（Task 4）
│   └── sample-design-doc.md        #（Task 4）
└── tests/
    ├── state-loader.test.mjs
    ├── schema.test.mjs
    ├── contract-builder.test.mjs
    ├── guard.test.mjs
    ├── gsf.test.mjs
    └── e2e.test.mjs                #（Task 11）
```

---

## Task 1: 项目骨架与配置

**Files:**
- Create: `gstack-superflow/package.json`
- Create: `gstack-superflow/LICENSE`
- Create: `gstack-superflow/.gitignore`
- Create: `gstack-superflow/README.md`
- Create dirs: `src/lib`, `src/cli`, `skills`, `hooks`, `templates`, `fixtures`, `tests`

**Interfaces:** Produces 一个可 `npm test` 的空项目骨架（测试套件为空时报告"0 tests"即视为框架可用）。

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p gstack-superflow/{src/lib,src/cli,skills/{workflow-start,bridge-builder,gstack-spec,sp-writing-plans},hooks,templates,fixtures,tests}
```

- [ ] **Step 2: 创建 `package.json`**

```json
{
  "name": "gstack-superflow",
  "version": "0.1.0",
  "description": "融合 Gstack 规划 + Superpowers 执行的 spec-driven AI 编程工作流插件",
  "type": "module",
  "license": "MIT",
  "bin": {
    "gsf": "src/cli/gsf.mjs"
  },
  "scripts": {
    "test": "node --test"
  },
  "engines": {
    "node": ">=20"
  }
}
```

- [ ] **Step 3: 创建 `.gitignore`**

```
node_modules/
.DS_Store
*.log
```

- [ ] **Step 4: 创建 `LICENSE`（MIT，版权 `2026 lixu`）**

```
MIT License

Copyright (c) 2026 lixu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: 创建 `README.md`（stub，Task 12 补全）**

```markdown
# gstack-superflow

融合 Gstack（规划）+ Superpowers（执行）的 spec-driven AI 编程工作流插件。

> 状态：计划 1 实现中（核心引擎 + 最小闭环）。完整说明见 `docs/superpowers/specs/2026-07-06-gstack-superflow-design.md`。
```

- [ ] **Step 6: 验证骨架可用**

Run: `cd gstack-superflow && npm test`
Expected: 输出类似 `0 tests passed` / `# tests 0`，退出码 0（无测试文件时不报错）。

- [ ] **Step 7: Commit**

```bash
git add gstack-superflow/
git commit -m "feat(gstack-superflow): 项目骨架与配置"
```

---

## Task 2: state-loader.mjs（状态读写）

负责读写项目目录下的 `.gstack-superflow.yaml`。本期用简单 KV 文本格式（非真 YAML），格式：`key: value`，`phase: <name>`、`handoff_approved: true|false`、`handoff_path: <path>`、`handoff_hash: <sha256>`、`source_hashes:` 下缩进列表。

**Files:**
- Create: `gstack-superflow/src/lib/state-loader.mjs`
- Test: `gstack-superflow/tests/state-loader.test.mjs`

**Interfaces:**
- Produces: `defaultState()`、`loadState(projectDir)`、`saveState(projectDir, state)`、`stateFilePath(projectDir)`

State 对象形状（贯穿全计划，后续 task 据此消费）：
```js
{
  phase: 'thinking',            // 8 状态之一
  handoff_approved: false,
  handoff_path: null,           // string | null
  handoff_hash: null,           // string | null
  source_hashes: {}             // { spec?: string, design_doc?: string, plan?: string }
}
```

- [ ] **Step 1: 写失败测试 `tests/state-loader.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { defaultState, loadState, saveState, stateFilePath } from '../src/lib/state-loader.mjs';

test('defaultState 返回 thinking 初始态且 handoff 未批准', () => {
  const s = defaultState();
  assert.equal(s.phase, 'thinking');
  assert.equal(s.handoff_approved, false);
  assert.equal(s.handoff_path, null);
  assert.deepEqual(s.source_hashes, {});
});

test('loadState 在无状态文件时返回默认状态', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  const s = loadState(dir);
  assert.equal(s.phase, 'thinking');
  rmSync(dir, { recursive: true, force: true });
});

test('saveState 后 loadState 往返一致', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  const state = { phase: 'bridging', handoff_approved: false, handoff_path: 'handoff-contract.md', handoff_hash: 'abc123', source_hashes: { spec: 'sha1' } };
  saveState(dir, state);
  const loaded = loadState(dir);
  assert.equal(loaded.phase, 'bridging');
  assert.equal(loaded.handoff_path, 'handoff-contract.md');
  assert.equal(loaded.handoff_hash, 'abc123');
  assert.equal(loaded.handoff_approved, false);
  assert.equal(loaded.source_hashes.spec, 'sha1');
  rmSync(dir, { recursive: true, force: true });
});

test('stateFilePath 指向目录下的 .gstack-superflow.yaml', () => {
  assert.equal(stateFilePath('/proj'), '/proj/.gstack-superflow.yaml');
});
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `cd gstack-superflow && node --test tests/state-loader.test.mjs`
Expected: FAIL（模块不存在 / 导入失败）。

- [ ] **Step 3: 实现 `src/lib/state-loader.mjs`**

```js
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { posix as pathPosix } from 'node:path';

const STATE_FILE = '.gstack-superflow.yaml';

export function stateFilePath(projectDir) {
  return pathPosix.join(projectDir, STATE_FILE);
}

export function defaultState() {
  return {
    phase: 'thinking',
    handoff_approved: false,
    handoff_path: null,
    handoff_hash: null,
    source_hashes: {},
  };
}

export function loadState(projectDir) {
  const path = stateFilePath(projectDir);
  if (!existsSync(path)) return defaultState();
  const text = readFileSync(path, 'utf8');
  const state = defaultState();
  const sourceHashes = {};
  let inSourceHashes = false;
  for (const line of text.split('\n')) {
    if (line.startsWith('source_hashes:')) { inSourceHashes = true; continue; }
    if (inSourceHashes) {
      const m = line.match(/^\s+(\w+):\s*(.+)$/);
      if (m) { sourceHashes[m[1]] = m[2].trim(); continue; }
      inSourceHashes = false;
    }
    const m = line.match(/^(\w+):\s*(.*)$/);
    if (!m) continue;
    const [, k, v] = m;
    if (k === 'phase') state.phase = v.trim();
    else if (k === 'handoff_approved') state.handoff_approved = v.trim() === 'true';
    else if (k === 'handoff_path') state.handoff_path = v.trim() === 'null' ? null : v.trim();
    else if (k === 'handoff_hash') state.handoff_hash = v.trim() === 'null' ? null : v.trim();
  }
  state.source_hashes = sourceHashes;
  return state;
}

export function saveState(projectDir, state) {
  const lines = [
    `phase: ${state.phase}`,
    `handoff_approved: ${state.handoff_approved}`,
    `handoff_path: ${state.handoff_path ?? 'null'}`,
    `handoff_hash: ${state.handoff_hash ?? 'null'}`,
    `source_hashes:`,
    ...Object.entries(state.source_hashes || {}).map(([k, v]) => `  ${k}: ${v}`),
  ];
  writeFileSync(stateFilePath(projectDir), lines.join('\n') + '\n', 'utf8');
}
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `cd gstack-superflow && node --test tests/state-loader.test.mjs`
Expected: PASS（4 tests）。

- [ ] **Step 5: Commit**

```bash
git add gstack-superflow/src/lib/state-loader.mjs gstack-superflow/tests/state-loader.test.mjs
git commit -m "feat(state-loader): 状态文件读写与默认状态"
```

---

## Task 3: schema.mjs（handoff 字段校验）

定义 `handoff-contract` 的字段形状与校验规则。

**Files:**
- Create: `gstack-superflow/src/lib/schema.mjs`
- Test: `gstack-superflow/tests/schema.test.mjs`

**Interfaces:**
- Produces: `validateHandoff(handoff)` → `{ valid: boolean, errors: string[] }`
- Handoff 对象形状（contract-builder 产出、guard 消费）：
```js
{
  intent_lock: { in_scope: string[], out_scope: string[] },
  task_slices: [{ id: 'S1', files: string[], tdd: { red: string, green: string, refactor: string } }],
  test_obligations: string[],
  review_gates: string[],            // slice id 列表
  source_hashes: { spec?: string, design_doc?: string, plan?: string }
}
```

- [ ] **Step 1: 写失败测试 `tests/schema.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateHandoff } from '../src/lib/schema.mjs';

function validHandoff() {
  return {
    intent_lock: { in_scope: ['登录'], out_scope: ['OAuth'] },
    task_slices: [{ id: 'S1', files: ['src/auth/login.ts'], tdd: { red: '写失败测试', green: '实现', refactor: '重构' } }],
    test_obligations: ['tests/auth/login.test.ts'],
    review_gates: ['S1'],
    source_hashes: { spec: 'sha1' },
  };
}

test('合法 handoff 通过校验', () => {
  const r = validateHandoff(validHandoff());
  assert.equal(r.valid, true);
  assert.deepEqual(r.errors, []);
});

test('缺 intent_lock 报错', () => {
  const h = validHandoff(); delete h.intent_lock;
  const r = validateHandoff(h);
  assert.equal(r.valid, false);
  assert.ok(r.errors.some(e => e.includes('intent_lock')));
});

test('task_slices 缺 tdd 报错', () => {
  const h = validHandoff();
  h.task_slices[0] = { id: 'S1', files: ['a.ts'] };
  const r = validateHandoff(h);
  assert.equal(r.valid, false);
  assert.ok(r.errors.some(e => e.includes('tdd')));
});

test('空 task_slices 报错', () => {
  const h = validHandoff(); h.task_slices = [];
  const r = validateHandoff(h);
  assert.equal(r.valid, false);
  assert.ok(r.errors.some(e => e.includes('task_slices')));
});
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `cd gstack-superflow && node --test tests/schema.test.mjs`
Expected: FAIL（模块不存在）。

- [ ] **Step 3: 实现 `src/lib/schema.mjs`**

```js
export function validateHandoff(h) {
  const errors = [];
  if (!h || typeof h !== 'object') return { valid: false, errors: ['handoff 必须是对象'] };

  const il = h.intent_lock;
  if (!il || !Array.isArray(il.in_scope) || il.in_scope.length === 0) {
    errors.push('intent_lock.in_scope 必须是非空数组');
  }
  if (!il || !Array.isArray(il.out_scope)) {
    errors.push('intent_lock.out_scope 必须是数组');
  }

  if (!Array.isArray(h.task_slices) || h.task_slices.length === 0) {
    errors.push('task_slices 必须是非空数组');
  } else {
    h.task_slices.forEach((s, i) => {
      if (!s.id) errors.push(`task_slices[${i}].id 缺失`);
      if (!Array.isArray(s.files) || s.files.length === 0) errors.push(`task_slices[${i}].files 必须是非空数组`);
      if (!s.tdd || !s.tdd.red || !s.tdd.green || !s.tdd.refactor) errors.push(`task_slices[${i}].tdd 需含 red/green/refactor`);
    });
  }

  if (!Array.isArray(h.test_obligations)) errors.push('test_obligations 必须是数组');
  if (!Array.isArray(h.review_gates)) errors.push('review_gates 必须是数组');
  if (!h.source_hashes || typeof h.source_hashes !== 'object') errors.push('source_hashes 必须是对象');

  return { valid: errors.length === 0, errors };
}
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `cd gstack-superflow && node --test tests/schema.test.mjs`
Expected: PASS（4 tests）。

- [ ] **Step 5: Commit**

```bash
git add gstack-superflow/src/lib/schema.mjs gstack-superflow/tests/schema.test.mjs
git commit -m "feat(schema): handoff-contract 字段校验"
```

---

## Task 4: contract-builder.mjs（桥接转换层核心）

把 Gstack 产物（spec / design doc）解析为 handoff 对象、渲染为 markdown、计算 hash。这是项目核心创新。

**Files:**
- Create: `gstack-superflow/fixtures/sample-spec.md`
- Create: `gstack-superflow/fixtures/sample-design-doc.md`
- Create: `gstack-superflow/src/lib/contract-builder.mjs`
- Test: `gstack-superflow/tests/contract-builder.test.mjs`

**Interfaces:**
- Consumes: spec markdown 文本（含 `## Scope` / `## Files` / `## Technical` section）、design doc markdown 文本（可选）
- Produces:
  - `parseSpec(specText)` → `{ in_scope: string[], out_scope: string[], files: string[], technical: string[] }`
  - `buildHandoff({ spec, designDoc })` → handoff 对象（形状见 Task 3）
  - `handoffToMarkdown(handoff)` → string
  - `computeHandoffHash({ spec, designDoc, plan })` → sha256 hex（基于源文本）

spec markdown 解析约定（fixtures 遵循）：
- `## Scope` 下 `**In scope:**` 列表项 = in_scope；`**Out of scope:**` 列表项 = out_scope
- `## Files` 下列表项 = files
- `## Technical` 下列表项 = technical

- [ ] **Step 1: 创建 fixture `fixtures/sample-spec.md`**

```markdown
# Spec: 用户登录功能

## Why
用户需要登录才能访问个人数据。

## Scope
**In scope:**
- 邮箱+密码登录
- JWT token 签发

**Out of scope:**
- OAuth 第三方登录
- 密码找回

## Technical
- POST /api/login 接口
- bcrypt 密码校验

## Files
- src/auth/login.ts
- src/auth/jwt.ts
- tests/auth/login.test.ts
```

- [ ] **Step 2: 创建 fixture `fixtures/sample-design-doc.md`**

```markdown
# Design Doc: 用户登录

## Capabilities
- 登录端点签发 JWT
- 密码用 bcrypt 校验

## Approach
单一登录接口，返回 JWT。
```

- [ ] **Step 3: 写失败测试 `tests/contract-builder.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { parseSpec, buildHandoff, handoffToMarkdown, computeHandoffHash } from '../src/lib/contract-builder.mjs';
import { validateHandoff } from '../src/lib/schema.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const readFixture = (n) => readFileSync(join(here, '..', 'fixtures', n), 'utf8');
const sampleSpec = readFixture('sample-spec.md');
const sampleDesign = readFixture('sample-design-doc.md');

test('parseSpec 提取 in/out scope', () => {
  const p = parseSpec(sampleSpec);
  assert.ok(p.in_scope.includes('邮箱+密码登录'));
  assert.ok(p.out_scope.includes('OAuth 第三方登录'));
});

test('parseSpec 提取 files', () => {
  const p = parseSpec(sampleSpec);
  assert.ok(p.files.includes('src/auth/login.ts'));
  assert.equal(p.files.length, 3);
});

test('buildHandoff 产出合法 handoff 且 files 进入 task_slices', () => {
  const h = buildHandoff({ spec: sampleSpec, designDoc: sampleDesign });
  const r = validateHandoff(h);
  assert.equal(r.valid, true, JSON.stringify(r.errors));
  assert.ok(h.task_slices[0].files.includes('src/auth/login.ts'));
  assert.ok(h.intent_lock.in_scope.includes('邮箱+密码登录'));
  assert.ok(h.intent_lock.out_scope.includes('OAuth 第三方登录'));
});

test('handoffToMarkdown 输出含关键字段', () => {
  const h = buildHandoff({ spec: sampleSpec, designDoc: sampleDesign });
  const md = handoffToMarkdown(h);
  assert.match(md, /Intent Lock/);
  assert.match(md, /邮箱\+密码登录/);
  assert.match(md, /Task Slices/);
});

test('computeHandoffHash 对同输入稳定，输入变则变', () => {
  const h1 = computeHandoffHash({ spec: sampleSpec, designDoc: sampleDesign });
  const h2 = computeHandoffHash({ spec: sampleSpec, designDoc: sampleDesign });
  const h3 = computeHandoffHash({ spec: sampleSpec + 'x', designDoc: sampleDesign });
  assert.equal(h1, h2);
  assert.notEqual(h1, h3);
  assert.match(h1, /^[0-9a-f]{64}$/);
});
```

- [ ] **Step 4: 运行测试，确认失败**

Run: `cd gstack-superflow && node --test tests/contract-builder.test.mjs`
Expected: FAIL（模块不存在）。

- [ ] **Step 5: 实现 `src/lib/contract-builder.mjs`**

```js
import { createHash } from 'node:crypto';

function collectList(lines, startIdx) {
  // 从 startIdx 起收集 "- xxx" 列表项，直到空行或非列表
  const out = [];
  for (let i = startIdx; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*-\s+/.test(line)) {
      out.push(line.replace(/^\s*-\s+/, '').trim());
    } else if (line.trim() === '') {
      continue;
    } else {
      break;
    }
  }
  return out;
}

export function parseSpec(specText) {
  const lines = specText.split('\n');
  const result = { in_scope: [], out_scope: [], files: [], technical: [] };
  let section = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const h = line.match(/^##\s+(.+)$/);
    if (h) {
      const title = h[1].trim().toLowerCase();
      if (title === 'scope') section = 'scope';
      else if (title === 'files') section = 'files';
      else if (title === 'technical') section = 'technical';
      else section = null;
      continue;
    }
    if (line.match(/^\*\*In scope:\*\*/)) {
      result.in_scope = collectList(lines, i + 1);
      i += result.in_scope.length;
      continue;
    }
    if (line.match(/^\*\*Out of scope:\*\*/)) {
      result.out_scope = collectList(lines, i + 1);
      i += result.out_scope.length;
      continue;
    }
    if (section === 'files' && /^\s*-\s+/.test(line)) {
      result.files.push(line.replace(/^\s*-\s+/, '').trim());
    } else if (section === 'technical' && /^\s*-\s+/.test(line)) {
      result.technical.push(line.replace(/^\s*-\s+/, '').trim());
    }
  }
  return result;
}

export function buildHandoff({ spec, designDoc, plan }) {
  const p = parseSpec(spec || '');
  // files 列表里识别测试文件作为 test_obligations，其余作为实现文件
  const testFiles = p.files.filter(f => /test|spec/i.test(f));
  const implFiles = p.files.filter(f => !/test|spec/i.test(f));
  const task_slices = implFiles.length > 0
    ? [{ id: 'S1', files: implFiles, tdd: { red: `为 ${implFiles.join(', ')} 写失败测试`, green: '最小实现使测试通过', refactor: '重构并保持测试绿色' } }]
    : [];
  return {
    intent_lock: { in_scope: p.in_scope, out_scope: p.out_scope },
    task_slices,
    test_obligations: testFiles,
    review_gates: task_slices.map(s => s.id),
    source_hashes: computeHandoffHash({ spec, designDoc, plan }) ? { spec: computeHandoffHash({ spec, designDoc, plan }) } : {},
  };
}

export function handoffToMarkdown(handoff) {
  const il = handoff.intent_lock || { in_scope: [], out_scope: [] };
  const lines = [];
  lines.push('# Handoff Contract', '');
  lines.push('## Intent Lock');
  lines.push('**In scope:**');
  il.in_scope.forEach(x => lines.push(`- ${x}`));
  lines.push('**Out of scope:**');
  il.out_scope.forEach(x => lines.push(`- ${x}`));
  lines.push('', '## Task Slices');
  (handoff.task_slices || []).forEach(s => {
    lines.push(`### ${s.id}`);
    lines.push('Files:');
    s.files.forEach(f => lines.push(`- ${f}`));
    lines.push(`TDD: red=${s.tdd.red}; green=${s.tdd.green}; refactor=${s.tdd.refactor}`);
  });
  lines.push('', '## Test Obligations');
  (handoff.test_obligations || []).forEach(t => lines.push(`- ${t}`));
  lines.push('', '## Review Gates');
  (handoff.review_gates || []).forEach(g => lines.push(`- ${g}`));
  return lines.join('\n') + '\n';
}

export function computeHandoffHash({ spec, designDoc, plan }) {
  const payload = JSON.stringify({ spec: spec || '', designDoc: designDoc || '', plan: plan || '' });
  return createHash('sha256').update(payload).digest('hex');
}
```

- [ ] **Step 6: 运行测试，确认通过**

Run: `cd gstack-superflow && node --test tests/contract-builder.test.mjs`
Expected: PASS（5 tests）。

- [ ] **Step 7: Commit**

```bash
git add gstack-superflow/src/lib/contract-builder.mjs gstack-superflow/tests/contract-builder.test.mjs gstack-superflow/fixtures/
git commit -m "feat(contract-builder): Gstack 产物到 handoff 的桥接转换"
```

---

## Task 5: guard.mjs（转移矩阵 + 门禁）

状态转移合法性与"无 handoff / 未批准不许执行"的硬门禁。

**Files:**
- Create: `gstack-superflow/src/lib/guard.mjs`
- Test: `gstack-superflow/tests/guard.test.mjs`

**Interfaces:**
- Consumes: state 对象（Task 2 形状）、可选 handoff 对象（Task 3 形状）
- Produces:
  - `checkTransition(fromPhase, toPhase)` → `{ allowed: boolean, reason: string }`
  - `canExecute(state)` → `{ allowed: boolean, reason: string }`（进入 executing 的门禁）
  - `isStale(state, currentSourceHashes)` → `boolean`

合法转移表（一期）：
- `thinking → planning`
- `planning → specifying`
- `specifying → bridging`
- `bridging → executing`（额外要求 `state.handoff_approved === true`，由 `canExecute` 检查）
- `executing → reviewing`
- `reviewing → closing`
- `reviewing → debugging`
- `debugging → reviewing`

- [ ] **Step 1: 写失败测试 `tests/guard.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { checkTransition, canExecute, isStale } from '../src/lib/guard.mjs';

test('thinking→planning 合法', () => {
  assert.equal(checkTransition('thinking', 'planning').allowed, true);
});

test('thinking→executing 非法（跳过中间状态）', () => {
  const r = checkTransition('thinking', 'executing');
  assert.equal(r.allowed, false);
  assert.ok(r.reason);
});

test('reviewing→debugging 与 debugging→reviewing 合法', () => {
  assert.equal(checkTransition('reviewing', 'debugging').allowed, true);
  assert.equal(checkTransition('debugging', 'reviewing').allowed, true);
});

test('canExecute 在 handoff 未批准时拒绝', () => {
  const state = { phase: 'bridging', handoff_approved: false, handoff_path: 'handoff-contract.md', handoff_hash: 'abc' };
  const r = canExecute(state);
  assert.equal(r.allowed, false);
  assert.ok(r.reason.includes('批准') || r.reason.includes('approve'));
});

test('canExecute 在无 handoff_path 时拒绝', () => {
  const state = { phase: 'bridging', handoff_approved: false, handoff_path: null, handoff_hash: null };
  assert.equal(canExecute(state).allowed, false);
});

test('canExecute 在已批准且有 handoff 时通过', () => {
  const state = { phase: 'bridging', handoff_approved: true, handoff_path: 'handoff-contract.md', handoff_hash: 'abc' };
  assert.equal(canExecute(state).allowed, true);
});

test('isStale 在源 hash 变化时返回 true', () => {
  const state = { source_hashes: { spec: 'old' } };
  assert.equal(isStale(state, { spec: 'new' }), true);
  assert.equal(isStale(state, { spec: 'old' }), false);
});
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `cd gstack-superflow && node --test tests/guard.test.mjs`
Expected: FAIL（模块不存在）。

- [ ] **Step 3: 实现 `src/lib/guard.mjs`**

```js
const TRANSITIONS = new Map([
  ['thinking', ['planning']],
  ['planning', ['specifying']],
  ['specifying', ['bridging']],
  ['bridging', ['executing']],
  ['executing', ['reviewing']],
  ['reviewing', ['closing', 'debugging']],
  ['debugging', ['reviewing']],
  ['closing', []],
]);

export function checkTransition(fromPhase, toPhase) {
  if (fromPhase === toPhase) return { allowed: true, reason: '停留同状态' };
  const allowed = TRANSITIONS.get(fromPhase) || [];
  if (allowed.includes(toPhase)) return { allowed: true, reason: 'ok' };
  return { allowed: false, reason: `非法转移：${fromPhase} → ${toPhase}` };
}

export function canExecute(state) {
  if (!state.handoff_path) {
    return { allowed: false, reason: '无 handoff-contract，不允许执行（先走 bridging 生成）' };
  }
  if (!state.handoff_approved) {
    return { allowed: false, reason: 'handoff 未被用户批准，不允许执行' };
  }
  return { allowed: true, reason: 'ok' };
}

export function isStale(state, currentSourceHashes) {
  const stored = state.source_hashes || {};
  const current = currentSourceHashes || {};
  for (const k of Object.keys(stored)) {
    if (current[k] && current[k] !== stored[k]) return true;
  }
  return false;
}
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `cd gstack-superflow && node --test tests/guard.test.mjs`
Expected: PASS（7 tests）。

- [ ] **Step 5: Commit**

```bash
git add gstack-superflow/src/lib/guard.mjs gstack-superflow/tests/guard.test.mjs
git commit -m "feat(guard): 状态转移矩阵与 handoff 批准门禁"
```

---

## Task 6: gsf CLI（state / validate / build-handoff / doctor）

命令行入口，复用前几个模块。

**Files:**
- Create: `gstack-superflow/src/cli/gsf.mjs`
- Test: `gstack-superflow/tests/gsf.test.mjs`

**Interfaces:**
- Produces: CLI 子命令
  - `gsf validate [dir]` — 校验状态文件 + 若存在 handoff 则校验之；合法 exit 0，否则 exit 1
  - `gsf state [dir]` — 打印当前 phase；默认 dir 为 `process.cwd()`
  - `gsf doctor` — 打印版本/Node 版本/状态文件是否存在

实现约定：导出 `run(argv, { cwd, stdout })` 便于测试，不直接依赖 `process` 全局（入口 `bin` 才绑定 `process`）。

- [ ] **Step 1: 写失败测试 `tests/gsf.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync, existsSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { run } from '../src/cli/gsf.mjs';

test('gsf state 打印当前 phase', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  let out = '';
  const code = run(['state', dir], { cwd: dir, stdout: (s) => { out += s; } });
  assert.equal(code, 0);
  assert.match(out, /thinking/);
  rmSync(dir, { recursive: true, force: true });
});

test('gsf validate 无状态文件时仍合法（默认状态）', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  const code = run(['validate', dir], { cwd: dir, stdout: () => {} });
  assert.equal(code, 0);
  rmSync(dir, { recursive: true, force: true });
});

test('gsf validate 在 phase=executing 但未批准时退出 1', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  writeFileSync(join(dir, '.gstack-superflow.yaml'),
    'phase: executing\nhandoff_approved: false\nhandoff_path: null\nhandoff_hash: null\nsource_hashes:\n');
  const code = run(['validate', dir], { cwd: dir, stdout: () => {} });
  assert.equal(code, 1);
  rmSync(dir, { recursive: true, force: true });
});

test('gsf doctor 打印 Node 版本与版本号', () => {
  let out = '';
  const code = run(['doctor'], { cwd: process.cwd(), stdout: (s) => { out += s; } });
  assert.equal(code, 0);
  assert.match(out, /node/i);
  assert.match(out, /0\.1\.0/);
});

test('gsf build-handoff 读 spec 生成 handoff-contract.md', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  const specPath = join(dir, 'spec.md');
  writeFileSync(specPath, '# Spec: x\n\n## Scope\n**In scope:**\n- a\n\n**Out of scope:**\n- b\n\n## Technical\n- t\n\n## Files\n- src/x.ts\n- tests/x.test.ts\n');
  let out = '';
  const code = run(['build-handoff', specPath], { cwd: dir, stdout: (s) => { out += s; } });
  assert.equal(code, 0);
  assert.ok(existsSync(join(dir, 'handoff-contract.md')));
  assert.match(readFileSync(join(dir, 'handoff-contract.md'), 'utf8'), /In scope/);
  rmSync(dir, { recursive: true, force: true });
});
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `cd gstack-superflow && node --test tests/gsf.test.mjs`
Expected: FAIL（模块不存在）。

- [ ] **Step 3: 实现 `src/cli/gsf.mjs`**

```js
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadState } from '../lib/state-loader.mjs';
import { canExecute } from '../lib/guard.mjs';
import { buildHandoff, handoffToMarkdown } from '../lib/contract-builder.mjs';

const VERSION = '0.1.0';

export function run(argv, { cwd, stdout }) {
  const log = (s) => stdout((s ?? '') + '\n');
  const [sub, ...rest] = argv;

  if (sub === 'state') {
    const dir = rest[0] || cwd;
    const s = loadState(dir);
    log(`phase: ${s.phase}`);
    log(`handoff_approved: ${s.handoff_approved}`);
    return 0;
  }

  if (sub === 'validate') {
    const dir = rest[0] || cwd;
    const s = loadState(dir);
    if (s.phase === 'executing') {
      const r = canExecute(s);
      if (!r.allowed) { log(`✗ ${r.reason}`); return 1; }
    }
    log('✓ 状态合法');
    return 0;
  }

  if (sub === 'build-handoff') {
    const specPath = rest[0];
    if (!specPath) { log('用法: gsf build-handoff <specPath>'); return 1; }
    const spec = readFileSync(specPath, 'utf8');
    const handoff = buildHandoff({ spec });
    const outPath = join(cwd, 'handoff-contract.md');
    writeFileSync(outPath, handoffToMarkdown(handoff), 'utf8');
    log(`✓ 已生成 ${outPath}`);
    return 0;
  }

  if (sub === 'doctor') {
    log(`gstack-superflow v${VERSION}`);
    log(`node ${process.version}`);
    return 0;
  }

  log('用法: gsf <state|validate|build-handoff|doctor> [dir|specPath]');
  return 1;
}

// 作为 bin 入口时绑定 process
if (process.argv[1] && process.argv[1].endsWith('gsf.mjs')) {
  const code = run(process.argv.slice(2), { cwd: process.cwd(), stdout: (s) => process.stdout.write(s) });
  process.exit(code);
}
```

- [ ] **Step 4: 运行测试，确认通过**

Run: `cd gstack-superflow && node --test tests/gsf.test.mjs`
Expected: PASS（5 tests）。

- [ ] **Step 5: Commit**

```bash
git add gstack-superflow/src/cli/gsf.mjs gstack-superflow/tests/gsf.test.mjs
git commit -m "feat(gsf): validate/state/doctor 子命令"
```

---

## Task 7: handoff-contract 模板 + bridge-builder SKILL.md

把 contract-builder 引擎包装成 Claude Code skill，并提供模板。

**Files:**
- Create: `gstack-superflow/templates/handoff-contract.md`
- Create: `gstack-superflow/skills/bridge-builder/SKILL.md`

**Interfaces:**
- Consumes: contract-builder 引擎（Task 4）
- Produces: skill 文件（Claude Code 通过 frontmatter 发现）

- [ ] **Step 1: 创建模板 `templates/handoff-contract.md`**

```markdown
<!--
  本文件由 bridge-builder skill 生成，不要手编。
  生成器：src/lib/contract-builder.mjs#handoffToMarkdown
  字段定义：src/lib/schema.mjs
-->

# Handoff Contract

> 规划段（Gstack）→ 执行段（Superpowers）的唯一交接层。
> 必须由用户显式批准后，guard 才允许进入 executing。

## Intent Lock
**In scope:**
- （待 bridge-builder 填充）

**Out of scope:**
- （待 bridge-builder 填充）

## Task Slices
<!-- 每个 slice 含 id / files / tdd(red,green,refactor) -->

## Test Obligations
- （待填充）

## Review Gates
- （待填充）
```

- [ ] **Step 2: 创建 `skills/bridge-builder/SKILL.md`**

```markdown
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
```

- [ ] **Step 3: 验证 frontmatter 可被解析**

Run: `cd gstack-superflow && node -e "const t=require('fs').readFileSync('skills/bridge-builder/SKILL.md','utf8');const m=t.match(/---\n([\s\S]*?)\n---/);if(!m||!m[1].includes('name: bridge-builder')){process.exit(1)}console.log('frontmatter ok')"`
Expected: 输出 `frontmatter ok`，退出码 0。

- [ ] **Step 4: Commit**

```bash
git add gstack-superflow/templates/ gstack-superflow/skills/bridge-builder/
git commit -m "feat(bridge-builder): handoff 模板与桥接 skill"
```

---

## Task 8: workflow-start SKILL.md（状态路由入口）

单一入口，内容级状态检测，路由到正确状态。本期为 minimal 版（指令为主，路由逻辑由 AI 读 SKILL.md 执行；引擎化的状态检测留给计划 2 的 `ssf inject` 产物）。

**Files:**
- Create: `gstack-superflow/skills/workflow-start/SKILL.md`

**Interfaces:**
- Produces: 8 状态路由指令

- [ ] **Step 1: 创建 `skills/workflow-start/SKILL.md`**

```markdown
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
```

- [ ] **Step 2: 验证 frontmatter**

Run: `cd gstack-superflow && node -e "const t=require('fs').readFileSync('skills/workflow-start/SKILL.md','utf8');const m=t.match(/---\n([\s\S]*?)\n---/);if(!m||!m[1].includes('name: workflow-start'))process.exit(1);console.log('ok')"`
Expected: `ok`，退出码 0。

- [ ] **Step 3: Commit**

```bash
git add gstack-superflow/skills/workflow-start/
git commit -m "feat(workflow-start): 状态路由入口 skill"
```

---

## Task 9: minimal Gstack /spec + minimal SP writing-plans

闭环两端的最小 skill。本期自写 minimal 版以保证计划自洽；计划 2 替换为 vendor 的上游完整版（Gstack `/spec` 五阶段、Superpowers `writing-plans` 全文）。

**Files:**
- Create: `gstack-superflow/skills/gstack-spec/SKILL.md`
- Create: `gstack-superflow/skills/sp-writing-plans/SKILL.md`

**Interfaces:**
- Produces: spec 产出（`## Scope` / `## Files` / `## Technical` / `## Why` 结构，被 contract-builder 解析）、plan 消费 handoff

- [ ] **Step 1: 创建 `skills/gstack-spec/SKILL.md`（minimal）**

```markdown
---
name: gstack-spec
description: gstack-superflow 规划段（minimal 版）。把模糊意图转为结构化 spec，产出文件须含 ## Why / ## Scope（**In scope:**、**Out of scope:）/ ## Technical / ## Files 四个 section，供 bridge-builder 解析。计划 2 替换为 vendor 的 Gstack /spec 五阶段完整版。
---

# gstack-spec（minimal）

> 本期是自包含 minimal 版。上游来源：garrytan/gstack 的 /spec（MIT），计划 2 vendor 完整版并记录上游 commit。

## 步骤
1. 与用户澄清：为什么做（Why）、范围（Scope）、技术约束（Technical）。
2. **必读相关代码**后再列文件清单（Files）。
3. 产出 spec 文件，结构严格如下（bridge-builder 依赖此结构解析）：

\`\`\`markdown
# Spec: <功能名>

## Why
<动机>

## Scope
**In scope:**
- <要做的事>

**Out of scope:**
- <明确不做的事>

## Technical
- <技术决策>

## Files
- <将创建/修改的文件>
\`\`\`

## 铁律
- Files 列表里测试文件名须含 `test` 或 `spec`（contract-builder 据此识别测试义务）。
- 产出后进入 `bridging` 状态，调用 `bridge-builder`。
```

- [ ] **Step 2: 创建 `skills/sp-writing-plans/SKILL.md`（minimal）**

```markdown
---
name: sp-writing-plans
description: gstack-superflow 执行段（minimal 版）。读取已批准的 handoff-contract.md，把任务切片展开为实现计划 plan.md（每个 slice 含 TDD 三步），交由 executing-plans 执行。计划 2 替换为 vendor 的 Superpowers writing-plans 完整版。
---

# sp-writing-plans（minimal）

> 本期是自包含 minimal 版。上游来源：obra/superpowers 的 writing-plans（MIT），计划 2 vendor 完整版并记录上游 commit。

## 前置
- `handoff-contract.md` 存在且 `.gstack-superflow.yaml` 中 `handoff_approved: true`。
- 否则停止：`guard.canExecute` 会拒绝执行。

## 步骤
1. 读 `handoff-contract.md`，提取 task_slices、test_obligations、review_gates。
2. 为每个 slice 展开为 TDD 三步任务（红 → 绿 → 重构），写入 `plan.md`。
3. 把 test_obligations 标为必跑测试，review_gates 标为完成后须 review。
4. 交由 Superpowers `executing-plans` / `subagent-driven-development` 执行。

## 铁律
- 不得超出 intent_lock.in_scope 范围（guard 通过 handoff 监督）。
```

- [ ] **Step 3: 验证两个 frontmatter**

Run: `cd gstack-superflow && for f in skills/gstack-spec/SKILL.md skills/sp-writing-plans/SKILL.md; do node -e "const t=require('fs').readFileSync('$f','utf8');if(!/--\n[\s\S]*?\n---/.test(t))process.exit(1)"; done && echo ok`
Expected: `ok`，退出码 0。

- [ ] **Step 4: Commit**

```bash
git add gstack-superflow/skills/gstack-spec/ gstack-superflow/skills/sp-writing-plans/
git commit -m "feat(skills): minimal gstack-spec 与 sp-writing-plans（闭环两端）"
```

---

## Task 10: plugin.json + session-start hook

让 Claude Code 能发现并加载插件，新会话自动注入 workflow-start。

**Files:**
- Create: `gstack-superflow/plugin.json`
- Create: `gstack-superflow/hooks/session-start.mjs`

**Interfaces:**
- Produces: Claude Code plugin manifest（含 skills 目录与 session-start hook）

- [ ] **Step 1: 创建 `plugin.json`**

```json
{
  "name": "gstack-superflow",
  "version": "0.1.0",
  "description": "融合 Gstack 规划 + Superpowers 执行的 spec-driven AI 编程工作流插件",
  "license": "MIT",
  "skills": ["skills/workflow-start", "skills/bridge-builder", "skills/gstack-spec", "skills/sp-writing-plans"],
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "node hooks/session-start.mjs"
      }
    ]
  }
}
```

- [ ] **Step 2: 创建 `hooks/session-start.mjs`**

```js
// SessionStart hook：向新会话注入 workflow-start 提示。
// 输出到 stdout 的内容会作为上下文注入。
const cwd = process.cwd();
const { existsSync } = await import('node:fs');
const { join } = await import('node:path');

const hasState = existsSync(join(cwd, '.gstack-superflow.yaml'));
if (hasState) {
  process.stdout.write(
    'gstack-superflow：检测到本会话处于工作流中。不确定状态时，用 workflow-start 路由到正确阶段；进入 executing 前确认 handoff 已批准（gsf validate）。\n'
  );
} else {
  process.stdout.write(
    'gstack-superflow 已加载。新变更可用 workflow-start 开始（Think→Plan→Spec→Bridge→Execute→Review→Ship）。\n'
  );
}
```

- [ ] **Step 3: 验证 JSON 合法 + hook 可执行**

Run: `cd gstack-superflow && node -e "JSON.parse(require('fs').readFileSync('plugin.json','utf8'));console.log('json ok')" && node hooks/session-start.mjs`
Expected: `json ok` + 一行 gstack-superflow 注入提示，退出码 0。

- [ ] **Step 4: Commit**

```bash
git add gstack-superflow/plugin.json gstack-superflow/hooks/
git commit -m "feat(plugin): Claude Code plugin manifest 与 session-start hook"
```

---

## Task 11: e2e 测试（端到端闭环）

验证 spec → handoff → 批准 → 可执行 的全链路。

**Files:**
- Create: `gstack-superflow/tests/e2e.test.mjs`

**Interfaces:**
- Consumes: 所有引擎模块（Task 2-6）+ fixtures（Task 4）

- [ ] **Step 1: 写 e2e 测试 `tests/e2e.test.mjs`**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
import { saveState, loadState } from '../src/lib/state-loader.mjs';
import { buildHandoff, handoffToMarkdown, computeHandoffHash } from '../src/lib/contract-builder.mjs';
import { validateHandoff } from '../src/lib/schema.mjs';
import { checkTransition, canExecute } from '../src/lib/guard.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const sampleSpec = readFileSync(join(here, '..', 'fixtures', 'sample-spec.md'), 'utf8');

test('e2e: spec → handoff → 批准 → 可执行', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-e2e-'));
  try {
    // 1. 起始状态 thinking
    let state = loadState(dir);
    assert.equal(state.phase, 'thinking');

    // 2. 推进到 specifying（模拟 Gstack 段已完成 spec 产出）
    assert.equal(checkTransition('thinking', 'planning').allowed, true);
    assert.equal(checkTransition('planning', 'specifying').allowed, true);
    state.phase = 'specifying';
    saveState(dir, state);

    // 3. bridging：build handoff 并落盘
    state.phase = 'bridging';
    const handoff = buildHandoff({ spec: sampleSpec });
    const vr = validateHandoff(handoff);
    assert.equal(vr.valid, true, JSON.stringify(vr.errors));
    const md = handoffToMarkdown(handoff);
    const handoffPath = join(dir, 'handoff-contract.md');
    writeFileSync(handoffPath, md, 'utf8');

    // 4. 批准前：不能执行
    state.handoff_path = 'handoff-contract.md';
    state.handoff_hash = computeHandoffHash({ spec: sampleSpec });
    state.source_hashes = { spec: state.handoff_hash };
    saveState(dir, state);
    assert.equal(canExecute(state).allowed, false);

    // 5. 用户批准
    state.handoff_approved = true;
    saveState(dir, state);

    // 6. 批准后：可执行
    assert.equal(canExecute(state).allowed, true);

    // 7. handoff 文件确实存在且含字段
    assert.ok(existsSync(handoffPath));
    assert.match(readFileSync(handoffPath, 'utf8'), /邮箱\+密码登录/);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
```

- [ ] **Step 2: 运行 e2e，确认通过**

Run: `cd gstack-superflow && node --test tests/e2e.test.mjs`
Expected: PASS（1 test）。

- [ ] **Step 3: 运行全量测试**

Run: `cd gstack-superflow && npm test`
Expected: 全部 PASS（state-loader 4 + schema 4 + contract-builder 5 + guard 7 + gsf 5 + e2e 1 = 26 tests）。

- [ ] **Step 4: Commit**

```bash
git add gstack-superflow/tests/e2e.test.mjs
git commit -m "test(e2e): spec→handoff→批准→可执行 全链路"
```

---

## Task 12: README 与安装说明

**Files:**
- Modify: `gstack-superflow/README.md`（替换 Task 1 的 stub）

- [ ] **Step 1: 写 `README.md`**

````markdown
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
````

- [ ] **Step 2: 验证 README 存在且非 stub**

Run: `cd gstack-superflow && node -e "const t=require('fs').readFileSync('README.md','utf8');if(t.length<500||!t.includes('CLI'))process.exit(1);console.log('readme ok')"`
Expected: `readme ok`，退出码 0。

- [ ] **Step 3: 最终全量验证**

Run: `cd gstack-superflow && npm test`
Expected: 26 tests 全 PASS。

- [ ] **Step 4: Commit**

```bash
git add gstack-superflow/README.md
git commit -m "docs(gstack-superflow): README 与安装说明"
```

---

## 计划 2（后续，待立项）

- vendor Gstack 完整 skills（`/office-hours` `/autoplan` `/spec` 五阶段 `/plan-*-review`），记录上游 commit
- vendor Superpowers 完整 skills（`writing-plans` `executing-plans` `subagent-driven-development` `test-driven-development` `systematic-debugging` `verification-before-completion` `requesting/receiving-code-review`）
- 多平台 manifest（Cursor / Codex / OpenCode）
- `gsf inject` / `gsf list` / 状态机引擎化（`ssf` 风格）
- Conductor 并行编排、浏览器 QA（`/qa`）运行时集成
- 替换 minimal skills 为完整版后重跑 e2e
