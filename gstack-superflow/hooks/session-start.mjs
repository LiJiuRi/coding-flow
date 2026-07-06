// SessionStart hook：向新会话注入 workflow-start 提示。
// 输出到 stdout 的内容会作为上下文注入。
const cwd = process.cwd();
const { existsSync } = await import('node:fs');
const { join } = await import('node:path');

const hasState = existsSync(join(cwd, '.gstack-superflow.yaml'));
if (hasState) {
  process.stdout.write(
    'gstack-superflow：检测到本会话处于工作流中。不确定状态时，用 workflow-start 路由到正确阶段；进入 executing 前确认 handoff 已批准（gsf validate）。\n'
  );
} else {
  process.stdout.write(
    'gstack-superflow 已加载。新变更可用 workflow-start 开始（Think→Plan→Spec→Bridge→Execute→Review→Ship）。\n'
  );
}
