export function validateHandoff(h) {
  const errors = [];
  if (!h || typeof h !== 'object') return { valid: false, errors: ['handoff 必须是对象'] };

  const il = h.intent_lock;
  if (!il || !Array.isArray(il.in_scope) || il.in_scope.length === 0) {
    errors.push('intent_lock.in_scope 必须是非空数组');
  }
  if (!il || !Array.isArray(il.out_scope)) {
    errors.push('intent_lock.out_scope 必须是数组');
  }

  if (!Array.isArray(h.task_slices) || h.task_slices.length === 0) {
    errors.push('task_slices 必须是非空数组');
  } else {
    h.task_slices.forEach((s, i) => {
      if (!s.id) errors.push(`task_slices[${i}].id 缺失`);
      if (!Array.isArray(s.files) || s.files.length === 0) errors.push(`task_slices[${i}].files 必须是非空数组`);
      if (!s.tdd || !s.tdd.red || !s.tdd.green || !s.tdd.refactor) errors.push(`task_slices[${i}].tdd 需含 red/green/refactor`);
    });
  }

  if (!Array.isArray(h.test_obligations)) errors.push('test_obligations 必须是数组');
  if (!Array.isArray(h.review_gates)) errors.push('review_gates 必须是数组');
  if (!h.source_hashes || typeof h.source_hashes !== 'object') errors.push('source_hashes 必须是对象');

  return { valid: errors.length === 0, errors };
}
