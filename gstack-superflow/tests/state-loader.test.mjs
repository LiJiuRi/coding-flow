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
