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
import { run } from '../src/cli/gsf.mjs';

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

test('e2e CLI: gsf build-handoff → validate 走真实 CLI 边界', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-cli-e2e-'));
  try {
    // 写入示例 spec
    const specPath = join(dir, 'spec.md');
    writeFileSync(specPath, sampleSpec);

    // 通过 CLI 边界 build-handoff
    const code1 = run(['build-handoff', specPath], { cwd: dir, stdout: () => {} });
    assert.equal(code1, 0);
    assert.ok(existsSync(join(dir, 'handoff-contract.md')), 'handoff-contract.md 应生成');

    // 状态文件应被写入：phase=bridging, handoff_path 已设
    const state = loadState(dir);
    assert.equal(state.phase, 'bridging');
    assert.equal(state.handoff_path, 'handoff-contract.md');

    // 通过 CLI 边界 validate（bridging 合法）
    const code2 = run(['validate', dir], { cwd: dir, stdout: () => {} });
    assert.equal(code2, 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
