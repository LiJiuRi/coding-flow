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
