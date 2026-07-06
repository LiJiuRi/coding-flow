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
