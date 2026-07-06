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
