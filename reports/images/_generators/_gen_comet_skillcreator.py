# -*- coding: utf-8 -*-
"""comet Skill Creator + Bundle 控制平面 — Style 1 Flat Icon."""
lines = []
W, H = 900, 840
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-st { font-size: 14px; font-weight: 600; fill: #111827; }
    .t-b { font-size: 11.5px; fill: #475569; }
    .t-edge { font-size: 11.5px; fill: #1e3a8a; }
    .t-grp { font-size: 12px; font-weight: 600; letter-spacing: 1px; }
    .t-note { font-size: 11px; fill: #6b7280; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
  </defs>""")

lines.append('  <text x="450" y="30" text-anchor="middle" class="t-title">comet 独有创新：Skill Creator + Bundle 控制平面</text>')
lines.append('  <text x="450" y="50" text-anchor="middle" class="t-sub">把「工作流想法」变成可分发、可校验、可发行的 Skill Package（openflow/spec-superflow 均无此能力）</text>')

# group bands (left rail)
lines.append('  <rect x="30" y="72" width="840" height="296" rx="10" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" stroke-dasharray="5,4"/>')
lines.append('  <text x="46" y="91" class="t-grp" fill="#1e40af">① 创作阶段</text>')
lines.append('  <rect x="30" y="372" width="840" height="240" rx="10" fill="#fff7ed" stroke="#fed7aa" stroke-width="1" stroke-dasharray="5,4"/>')
lines.append('  <text x="46" y="391" class="t-grp" fill="#9a3412">② 编译 · 评估 · 审查</text>')
lines.append('  <rect x="30" y="616" width="840" height="170" rx="10" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1" stroke-dasharray="5,4"/>')
lines.append('  <text x="46" y="635" class="t-grp" fill="#166534">③ 发行 · 分发</text>')

def stage(cy, title, sub, fill, stroke, w=380, cx=380):
    lines.append(f'  <rect x="{cx-w/2}" y="{cy-30}" width="{w}" height="60" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
    lines.append(f'  <text x="{cx}" y="{cy-7}" text-anchor="middle" class="t-st">{title}</text>')
    lines.append(f'  <text x="{cx}" y="{cy+12}" text-anchor="middle" class="t-b">{sub}</text>')

def varrow(y1, y2):
    lines.append(f'  <line x1="380" y1="{y1}" x2="380" y2="{y2}" stroke="#2563eb" stroke-width="1.8" marker-end="url(#a-blue)"/>')

# Stage 1-4 (creation)
stage(120, '工作流想法（自然语言 spec 描述）', '用户用自然语言描述想要的工作流 / Skill', '#ffffff', '#cbd5e1')
varrow(150, 185)
stage(205, '/comet-any（Skill Creator 入口）', 'assets/skills/comet-any · reference/authoring-protocol.json', '#eff6ff', '#93c5fd')
varrow(235, 270)
stage(290, 'workflow-contract（单一事实源深模块 · 6ts）', '规范化 contract / phase / step · 是后续所有阶段的契约源', '#dbeafe', '#3b82f6')
varrow(320, 355)
stage(375, 'draft（Bundle 草稿）', 'domains/bundle · 按 contract 生成草稿结构', '#eff6ff', '#93c5fd')
varrow(405, 440)

# Stage 5-7 (compile/eval/review)
stage(460, 'compile（编译）', 'esbuild 打包 · 生成跨平台可执行 skill 包（Node-only .mjs）', '#fff7ed', '#fb923c')
varrow(490, 525)
# eval + engine side-by-side
lines.append('  <rect x="190" y="515" width="240" height="60" rx="8" fill="#fff7ed" stroke="#fb923c" stroke-width="1.6"/>')
lines.append('  <text x="310" y="538" text-anchor="middle" class="t-st">eval（评估）</text>')
lines.append('  <text x="310" y="557" text-anchor="middle" class="t-b">实际运行 skill · 采证</text>')
# engine box (right of eval)
lines.append('  <rect x="470" y="515" width="220" height="60" rx="8" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.6"/>')
lines.append('  <text x="580" y="538" text-anchor="middle" class="t-st">engine（执行引擎）</text>')
lines.append('  <text x="580" y="557" text-anchor="middle" class="t-b">loop/run-store/resolver/guardrails/evals</text>')
lines.append('  <line x1="430" y1="545" x2="466" y2="545" stroke="#ea580c" stroke-width="1.7" marker-end="url(#a-orange)"/>')
lines.append('  <line x1="466" y1="535" x2="430" y2="535" stroke="#ea580c" stroke-width="1.7" marker-end="url(#a-orange)"/>')
lines.append('  <text x="448" y="528" text-anchor="middle" class="t-edge" fill="#9a3412">跑</text>')
varrow(575, 610)
stage(630, 'review（审查）', '三级问题分级 · 禁表演式同意 · 不通过回 compile', '#fff7ed', '#fb923c')
varrow(660, 695)

# Stage 8-9 (publish/distribute)
stage(715, 'publish（发布）', 'app/commands/publish.ts · 版本化 + 注册', '#f0fdf4', '#86efac')
varrow(745, 780)
stage(800, 'distribute → 33 平台 skill 产物', 'copy/symlink 安装到 33 个 AI 编码平台', '#dcfce7', '#4ade80')

# side note: lifecycle command set
lines.append('  <rect x="660" y="120" width="200" height="100" rx="8" fill="#f9fafb" stroke="#e5e7eb"/>')
lines.append('  <text x="760" y="142" text-anchor="middle" class="t-st" font-size="12">控制平面命令</text>')
lines.append('  <text x="672" y="162" class="t-b">comet creator · comet bundle</text>')
lines.append('  <text x="672" y="178" class="t-b">comet publish · comet skill</text>')
lines.append('  <text x="672" y="196" class="t-b">comet eval · comet update</text>')
lines.append('  <text x="672" y="214" class="t-b" fill="#6b21a8">/comet-any 统一入口</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\comet-SkillCreator控制平面.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
