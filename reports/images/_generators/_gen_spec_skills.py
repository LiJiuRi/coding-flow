# -*- coding: utf-8 -*-
"""spec-superflow 9 skill 协作关系图 — Style 1 Flat Icon."""
lines = []
W, H = 1100, 600
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-h { font-size: 13px; font-weight: 600; fill: #111827; }
    .t-b { font-size: 11px; fill: #475569; }
    .t-edge { font-size: 11px; fill: #1e3a8a; }
    .t-art { font-size: 10.5px; fill: #374151; }
    .t-note { font-size: 11px; fill: #6b7280; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
  </defs>""")

lines.append('  <text x="550" y="30" text-anchor="middle" class="t-title">spec-superflow 9 个 Skill 协作关系（运行时交接）</text>')
lines.append('  <text x="550" y="50" text-anchor="middle" class="t-sub">workflow-orchestrator 按当前 state 路由 · 每条路由前先跑 guard.mjs（exit≠0 即 BLOCK）· 工件在各 skill 间流转</text>')

# orchestrator (top center)
lines.append('  <rect x="430" y="74" width="240" height="64" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>')
lines.append('  <text x="550" y="96" text-anchor="middle" class="t-h" fill="#991b1b">workflow-orchestrator（入口·独创）</text>')
lines.append('  <text x="550" y="113" text-anchor="middle" class="t-b">检测内容级状态 + 路由 + 拦截非法跳转</text>')
lines.append('  <text x="550" y="128" text-anchor="middle" class="t-b">不直接实现任何东西，只决定下一个 skill</text>')

# guard.mjs + .yaml consulted by orchestrator
lines.append('  <rect x="40" y="80" width="180" height="54" rx="8" fill="#fff7ed" stroke="#fb923c"/>')
lines.append('  <text x="130" y="102" text-anchor="middle" class="t-h" fill="#9a3412">guard.mjs</text>')
lines.append('  <text x="130" y="118" text-anchor="middle" class="t-b">五维度硬门禁</text>')
lines.append('  <text x="130" y="130" text-anchor="middle" class="t-b">exit code 拦截</text>')
lines.append('  <rect x="880" y="80" width="180" height="54" rx="8" fill="#ffffff" stroke="#cbd5e1"/>')
lines.append('  <text x="970" y="102" text-anchor="middle" class="t-h">.spec-superflow.yaml</text>')
lines.append('  <text x="970" y="118" text-anchor="middle" class="t-b">state + SHA256 hash</text>')
lines.append('  <text x="970" y="130" text-anchor="middle" class="t-b">26 字段 · 双层过时检测</text>')
lines.append('  <line x1="220" y1="107" x2="428" y2="107" stroke="#ea580c" stroke-width="1.6" marker-end="url(#a-orange)" stroke-dasharray="4,3"/>')
lines.append('  <line x1="670" y1="107" x2="878" y2="107" stroke="#ea580c" stroke-width="1.6" marker-end="url(#a-orange)" stroke-dasharray="4,3"/>')
lines.append('  <text x="324" y="100" text-anchor="middle" class="t-edge" fill="#9a3412">每路由前校验</text>')
lines.append('  <text x="774" y="100" text-anchor="middle" class="t-edge" fill="#9a3412">读/写状态</text>')

# routing bus
lines.append('  <line x1="550" y1="138" x2="550" y2="170" stroke="#94a3b8" stroke-width="1.5"/>')
lines.append('  <line x1="92" y1="170" x2="982" y2="170" stroke="#94a3b8" stroke-width="1.5"/>')
lines.append('  <text x="560" y="166" class="t-note">按 state 路由（dashed = orchestrator 派发）</text>')

# pipeline 6 skills (cy=330), drop arrows from bus
PIPE = [
    (92, 'spec-explorer', '探索·一次一问', '#eff6ff', '#93c5fd'),
    (270, 'spec-forger', '规格·4工件+schema', '#eff6ff', '#93c5fd'),
    (448, 'bridge-contract', '桥接·独创', '#fee2e2', '#fca5a5'),
    (626, 'execution-governor', '执行·TDD+SDD', '#eff6ff', '#93c5fd'),
    (804, 'closure-archivist', '收口·验证归档', '#eff6ff', '#93c5fd'),
    (982, 'spec-syncer', '同步·←OpenSpec', '#eff6ff', '#93c5fd'),
]
w, h = 124, 64
for cx, name, role, fill, stroke in PIPE:
    lines.append(f'  <line x1="{cx}" y1="170" x2="{cx}" y2="296" stroke="#94a3b8" stroke-width="1.3" stroke-dasharray="3,3" marker-end="url(#a-gray)"/>')
    lines.append(f'  <rect x="{cx-w/2}" y="300" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>')
    lines.append(f'  <text x="{cx}" y="324" text-anchor="middle" class="t-h">{name}</text>')
    lines.append(f'  <text x="{cx}" y="342" text-anchor="middle" class="t-b">{role}</text>')
    lines.append(f'  <text x="{cx}" y="356" text-anchor="middle" class="t-b" font-size="9.5" fill="#94a3b8">{"独创" if stroke=="#fca5a5" else ""}</text>')

# pipeline flow arrows + artifacts (on arrows at y=330)
ART = [
    (181, 'proposal'),
    (359, '4 工件 ✓schema'),
    (537, 'execution-contract'),
    (715, '代码+验证证据'),
    (893, 'delta spec'),
]
rights = [92+w/2, 270+w/2, 448+w/2, 626+w/2, 804+w/2]
lefts = [270-w/2, 448-w/2, 626-w/2, 804-w/2, 982-w/2]
for (mx, label), x1, x2 in zip(ART, rights, lefts):
    lines.append(f'  <line x1="{x1+3}" y1="330" x2="{x2-3}" y2="330" stroke="#2563eb" stroke-width="1.7" marker-end="url(#a-blue)"/>')
    lines.append(f'  <rect x="{mx-58}" y="321" width="116" height="17" rx="3" fill="#ffffff" stroke="none"/>')
    lines.append(f'  <text x="{mx}" y="333" text-anchor="middle" class="t-art">{label}</text>')

# branches: systematic-debugger + code-reviewer (below governor)
lines.append('  <rect x="374" y="450" width="148" height="56" rx="8" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>')
lines.append('  <text x="448" y="472" text-anchor="middle" class="t-h">systematic-debugger</text>')
lines.append('  <text x="448" y="488" text-anchor="middle" class="t-b">调试（←Superpowers）</text>')
lines.append('  <text x="448" y="500" text-anchor="middle" class="t-b">4 阶段根因 · 3+失败质疑架构</text>')

lines.append('  <rect x="730" y="450" width="148" height="56" rx="8" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>')
lines.append('  <text x="804" y="472" text-anchor="middle" class="t-h">code-reviewer</text>')
lines.append('  <text x="804" y="488" text-anchor="middle" class="t-b">审查（←Superpowers）</text>')
lines.append('  <text x="804" y="500" text-anchor="middle" class="t-b">三级分级 · 禁表演式同意</text>')

# branch arrows from governor (626,364)
lines.append('  <path d="M 588 364 L 470 450" fill="none" stroke="#16a34a" stroke-width="1.6" marker-end="url(#a-green)"/>')
lines.append('  <path d="M 470 470 L 590 372" fill="none" stroke="#16a34a" stroke-width="1.6" marker-end="url(#a-green)" stroke-dasharray="4,3"/>')
lines.append('  <text x="498" y="418" class="t-edge" fill="#15803d">遇bug</text>')
lines.append('  <text x="478" y="438" class="t-edge" fill="#15803d">修复回</text>')
lines.append('  <path d="M 664 364 L 780 450" fill="none" stroke="#16a34a" stroke-width="1.6" marker-end="url(#a-green)"/>')
lines.append('  <text x="734" y="418" class="t-edge" fill="#15803d">Review Gate</text>')

# footer
lines.append('  <rect x="40" y="540" width="1020" height="46" rx="8" fill="#f9fafb" stroke="#e5e7eb"/>')
lines.append('  <text x="56" y="560" class="t-note" font-weight="600">决策点：</text>')
lines.append('  <text x="110" y="560" class="t-note">DP-3 用户批准（approved-for-build）· DP-4/5/7 路由确认（orchestrator 输出附决策点编号）</text>')
lines.append('  <text x="56" y="578" class="t-note" font-weight="600" fill="#6b21a8">铁律：</text>')
lines.append('  <text x="110" y="578" class="t-note">NO PRODUCTION CODE WITHOUT FAILING TEST ｜ NO FIXES WITHOUT ROOT CAUSE ｜ NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\spec-9skill协作.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
