# -*- coding: utf-8 -*-
"""spec-superflow 8 状态机图 — Style 1 Flat Icon."""
lines = []
W, H = 1200, 600
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-st { font-size: 13px; font-weight: 600; fill: #111827; }
    .t-st-sub { font-size: 10.5px; fill: #475569; }
    .t-edge { font-size: 11.5px; fill: #1e3a8a; }
    .t-edge-em { font-size: 11.5px; font-weight: 600; }
    .t-note { font-size: 11px; fill: #6b7280; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#9333ea"/></marker>
    <marker id="a-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#dc2626"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
  </defs>""")

lines.append('  <text x="600" y="30" text-anchor="middle" class="t-title">spec-superflow 状态机：8 状态 + 转移规则（含 abandoned 终态）</text>')
lines.append('  <text x="600" y="50" text-anchor="middle" class="t-sub">workflow-orchestrator/SKILL.md:33-40 · 每条路由前先跑 guard.mjs（exit≠0 即 BLOCK）· 内容级状态检测（proposal scope vs contract intent lock）</text>')

def state(cx, cy, w, h, name, role, fill, stroke, double=False):
    sw = 2.4 if double else 1.6
    lines.append(f'  <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    lines.append(f'  <text x="{cx}" y="{cy-4}" text-anchor="middle" class="t-st">{name}</text>')
    lines.append(f'  <text x="{cx}" y="{cy+12}" text-anchor="middle" class="t-st-sub">{role}</text>')

# main chain states (cy = 250)
cy = 250
states = [
    (95, 'exploring', '探索·一问一问', '#eff6ff', '#93c5fd'),
    (255, 'specifying', '规格·产出4工件', '#eff6ff', '#93c5fd'),
    (415, 'bridging', '桥接·生成契约', '#eff6ff', '#93c5fd'),
    (600, 'approved-for-build', '已批准·DP-3', '#dbeafe', '#3b82f6'),
    (780, 'executing', '执行·TDD/SDD', '#eff6ff', '#93c5fd'),
    (945, 'closing', '收口·验证归档', '#eff6ff', '#93c5fd'),
]
for cx, name, role, fill, stroke in states:
    w = 150 if name == 'approved-for-build' else 130
    state(cx, cy, w, 58, name, role, fill, stroke)

# done terminal (right of closing)
state(1100, cy, 120, 58, '✓ done', '归档完成·sync', '#dcfce7', '#86efac')

# main flow arrows (blue) — between states, with event labels
pairs = [
    (95, 255, '探索收敛'),
    (255, 415, '规格就绪'),
    (415, 600, 'contract 生成'),
    (600, 780, 'DP-3 用户批准'),
    (780, 945, '任务全绿'),
    (945, 1100, '验证通过'),
]
# compute arrow start/end from box edges
widths = {95:130, 255:130, 415:130, 600:150, 780:130, 945:130, 1100:120}
for a, b, lbl in pairs:
    x1 = a + widths[a]/2
    x2 = b - widths[b]/2
    lines.append(f'  <line x1="{x1+2}" y1="{cy}" x2="{x2-2}" y2="{cy}" stroke="#2563eb" stroke-width="1.8" marker-end="url(#a-blue)"/>')
    lines.append(f'  <text x="{(x1+x2)/2}" y="{cy-8}" text-anchor="middle" class="t-edge">{lbl}</text>')

# DP-3 gate emphasis (above approved-for-build arrow)
lines.append('  <text x="690" y="265" text-anchor="middle" class="t-edge-em" fill="#b91c1c">⚠ 用户显式批准门禁</text>')

# ---- debugging bypass (below executing) ----
state(780, 380, 140, 52, 'debugging', '调试·4阶段根因', '#fff7ed', '#fb923c')
# executing <-> debugging (bidirectional orange)
lines.append('  <line x1="765" y1="280" x2="765" y2="353" stroke="#ea580c" stroke-width="1.7" marker-end="url(#a-orange)"/>')
lines.append('  <text x="722" y="320" class="t-edge" fill="#9a3412">遇 bug</text>')
lines.append('  <line x1="795" y1="353" x2="795" y2="280" stroke="#ea580c" stroke-width="1.7" marker-end="url(#a-orange)"/>')
lines.append('  <text x="838" y="320" class="t-edge" fill="#9a3412">修复后回</text>')

# escalation (3+ fails -> question architecture -> user)
lines.append('  <path d="M 780 407 C 780 450, 780 460, 780 472" fill="none" stroke="#9333ea" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#a-purple)"/>')
lines.append('  <rect x="690" y="475" width="180" height="50" rx="8" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>')
lines.append('  <text x="780" y="495" text-anchor="middle" class="t-st" fill="#6b21a8">升级用户（质疑架构）</text>')
lines.append('  <text x="780" y="512" text-anchor="middle" class="t-st-sub">≥3 次修复失败 → each fix reveals new problem</text>')
lines.append('  <text x="780" y="525" text-anchor="middle" class="t-st-sub">→ 与用户讨论，不打补丁</text>')

# ---- rollback arcs (above main chain) ----
# contract drift: executing -> bridging (re-bridge), higher arc y=150
lines.append('  <path d="M 780 221 C 780 150, 415 150, 415 221" fill="none" stroke="#dc2626" stroke-width="1.6" stroke-dasharray="6,3" marker-end="url(#a-red)"/>')
lines.append('  <text x="597" y="145" text-anchor="middle" class="t-edge-em" fill="#b91c1c">contract drift → re-bridge（重新桥接）</text>')

# scope change: bridging -> specifying (re-specify), lower arc y=180
lines.append('  <path d="M 380 221 C 380 185, 290 185, 290 221" fill="none" stroke="#dc2626" stroke-width="1.6" stroke-dasharray="6,3" marker-end="url(#a-red)"/>')
lines.append('  <text x="335" y="180" text-anchor="middle" class="t-edge-em" fill="#b91c1c">scope change → re-specify</text>')

# hotfix quick path (exploring -> approved-for-build shortcut, dashed)
lines.append('  <path d="M 95 221 C 95 100, 600 100, 600 221" fill="none" stroke="#16a34a" stroke-width="1.4" stroke-dasharray="4,3" marker-end="url(#a-green)"/>')
lines.append('  <text x="347" y="98" text-anchor="middle" class="t-edge-em" fill="#15803d">hotfix 快速路径（最小契约 · 跳过 specifying/bridging 细节）</text>')

# ---- abandoned terminal (bottom-right) ----
state(1090, 410, 150, 64, 'abandoned', '终态·禁止出向', '#f1f5f9', '#94a3b8', double=True)
# funnel from "any non-terminal" — dashed gray from main chain area
lines.append('  <path d="M 945 280 C 945 350, 1000 380, 1050 392" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#a-gray)"/>')
lines.append('  <text x="1015" y="350" class="t-edge" fill="#475569">任意非终态</text>')
lines.append('  <text x="1015" y="366" class="t-note">（需用户确认 · 不自动放弃）</text>')
lines.append('  <text x="1090" y="500" text-anchor="middle" class="t-note" fill="#475569">不合并 abandoned 变更的 delta spec</text>')

# legend
lines.append('  <rect x="30" y="540" width="1140" height="48" rx="6" fill="#f9fafb" stroke="#e5e7eb"/>')
leg = [('#2563eb','主转移（每路由前 guard.mjs 校验）','blue',''),
       ('#ea580c','debugging 旁路（双向）','orange',''),
       ('#9333ea','升级用户（虚线）','purple','dashed'),
       ('#dc2626','回退：drift/scope（虚线）','red','dashed'),
       ('#16a34a','hotfix 快速路径（虚线）','green','dashed'),
       ('#94a3b8','放弃 → 终态（虚线）','gray','dashed')]
lx = 46
for c, lbl, mk, dash in leg:
    d = ' stroke-dasharray="5,4"' if dash == 'dashed' else ''
    lines.append(f'  <line x1="{lx}" y1="566" x2="{lx+24}" y2="566" stroke="{c}" stroke-width="1.8"{d} marker-end="url(#a-{mk})"/>')
    lines.append(f'  <text x="{lx+30}" y="570" class="t-note">{lbl}</text>')
    lx += 192

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\spec-8状态机.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
