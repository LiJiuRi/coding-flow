import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { loadState, saveState, stateFilePath } from '../lib/state-loader.mjs';
import { canExecute } from '../lib/guard.mjs';
import { buildHandoff, handoffToMarkdown, computeHandoffHash } from '../lib/contract-builder.mjs';

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
      if (s.handoff_path && !existsSync(join(dir, s.handoff_path))) {
        log('✗ handoff-contract.md 不存在');
        return 1;
      }
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
    const hash = computeHandoffHash({ spec });
    const state = loadState(cwd);
    state.phase = 'bridging';
    state.handoff_path = 'handoff-contract.md';
    state.handoff_hash = hash;
    state.source_hashes = { spec: hash };
    saveState(cwd, state);
    log(`✓ 已生成 ${outPath}`);
    return 0;
  }

  if (sub === 'doctor') {
    log(`gstack-superflow v${VERSION}`);
    log(`node ${process.version}`);
    log(`state file: ${existsSync(stateFilePath(cwd)) ? 'present' : 'absent'}`);
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
