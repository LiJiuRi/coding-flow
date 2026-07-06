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
