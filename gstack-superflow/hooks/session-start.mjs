// SessionStart hook：向新会话注入 workflow-start 提示。
// 输出 JSON（hookSpecificOutput.additionalContext），符合 Claude Code SessionStart 事件契约。
const cwd = process.cwd();
const { existsSync } = await import('node:fs');
const { join } = await import('node:path');

const hasState = existsSync(join(cwd, '.gstack-superflow.yaml'));
const additionalContext = hasState
  ? 'gstack-superflow：检测到本会话处于工作流中。不确定状态时，用 workflow-start 路由到正确阶段；进入 executing 前确认 handoff 已批准（gsf validate）。\n'
  : 'gstack-superflow 已加载。新变更可用 workflow-start 开始（Think→Plan→Spec→Bridge→Execute→Review→Ship）。\n';

process.stdout.write(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: 'SessionStart',
    additionalContext,
  },
}) + '\n');
