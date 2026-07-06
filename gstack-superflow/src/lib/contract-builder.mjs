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
