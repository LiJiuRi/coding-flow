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
