import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync, existsSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { run } from '../src/cli/gsf.mjs';
import { loadState } from '../src/lib/state-loader.mjs';

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

test('gsf validate 在 phase=executing 已批准但 handoff 文件缺失时退出 1', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  writeFileSync(join(dir, '.gstack-superflow.yaml'),
    'phase: executing\nhandoff_approved: true\nhandoff_path: handoff-contract.md\nhandoff_hash: abc\nsource_hashes:\n  spec: abc\n');
  // 故意不创建 handoff-contract.md
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

test('gsf build-handoff 同步写入状态文件（phase=bridging, handoff_path 已设）', () => {
  const dir = mkdtempSync(join(tmpdir(), 'gsf-'));
  const specPath = join(dir, 'spec.md');
  writeFileSync(specPath, '# Spec: x\n\n## Scope\n**In scope:**\n- a\n\n## Out of scope:**\n- b\n\n## Technical\n- t\n\n## Files\n- src/x.ts\n- tests/x.test.ts\n');
  const code = run(['build-handoff', specPath], { cwd: dir, stdout: () => {} });
  assert.equal(code, 0);
  assert.ok(existsSync(join(dir, '.gstack-superflow.yaml')));
  const state = loadState(dir);
  assert.equal(state.phase, 'bridging');
  assert.equal(state.handoff_path, 'handoff-contract.md');
  assert.ok(state.handoff_hash, 'handoff_hash 应非空');
  assert.equal(state.source_hashes.spec, state.handoff_hash);
  rmSync(dir, { recursive: true, force: true });
});
