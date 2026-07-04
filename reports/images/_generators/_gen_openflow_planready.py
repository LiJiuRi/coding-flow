# -*- coding: utf-8 -*-
"""openflow plan-ready.md 翻译层数据流图 — Style 1 Flat Icon."""
lines = []
W, H = 1000, 600
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-h { font-size: 13.5px; font-weight: 600; fill: #111827; }
    .t-b { font-size: 11.5px; fill: #475569; }
    .t-sec { font-size: 11px; fill: #1e3a8a; }
    .t-tag { font-size: 11px; font-weight: 600; }
    .t-edge { font-size: 11.5px; fill: #374151; }
    .t-edge-em { font-size: 11.5px; font-weight: 600; fill: #065f46; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#dc2626"/></marker>
  </defs>""")

lines.append('  <text x="500" y="30" text-anchor="middle" class="t-title">openflow 核心机制：plan-ready.md 翻译层（唯一上下文桥梁）</text>')
lines.append('  <text x="500" y="50" text-anchor="middle" class="t-sub">OpenSpec 规格语言 → 翻译 7 规则 → Superpowers 可消费的实现交接文档（templates/spec.md:82-185）</text>')

# ---- Left: OpenSpec inputs ----
lines.append('  <rect x="30" y="80" width="220" height="320" rx="10" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>')
lines.append('  <text x="140" y="102" text-anchor="middle" class="t-h">OpenSpec 规格产出</text>')
lines.append('  <text x="140" y="118" text-anchor="middle" class="t-b">（spec 阶段调 openspec CLI 生成）</text>')
items_l = [
    ('openspec/config.yaml', '项目规则/编码约束/架构边界'),
    ('proposal.md', '需求范围 · What Changes'),
    ('design.md', '方案设计'),
    ('specs/&lt;cap&gt;/spec.md', 'Requirements + Scenarios'),
    ('tasks.md', '验收任务清单'),
    ('delta（变更）', 'ADDED/MODIFIED/REMOVED'),
]
yy = 142
for name, desc in items_l:
    lines.append(f'  <rect x="44" y="{yy}" width="192" height="36" rx="6" fill="#ffffff" stroke="#dbeafe" stroke-width="1.2"/>')
    lines.append(f'  <text x="52" y="{yy+15}" class="t-sec" font-weight="600">{name}</text>')
    lines.append(f'  <text x="52" y="{yy+29}" class="t-b">{desc}</text>')
    yy += 42

# ---- Center: translation engine ----
lines.append('  <rect x="290" y="80" width="240" height="320" rx="10" fill="#fff7ed" stroke="#fb923c" stroke-width="1.8"/>')
lines.append('  <text x="410" y="102" text-anchor="middle" class="t-h" fill="#9a3412">spec 阶段 · 翻译层</text>')
lines.append('  <text x="410" y="118" text-anchor="middle" class="t-b" fill="#9a3412">templates/spec.md</text>')
lines.append('  <rect x="306" y="132" width="208" height="44" rx="6" fill="#ffffff" stroke="#fed7aa"/>')
lines.append('  <text x="410" y="150" text-anchor="middle" class="t-sec" font-weight="600">翻译 7 规则（spec.md:86-93）</text>')
lines.append('  <text x="410" y="166" text-anchor="middle" class="t-b">规格语言 → 实现交接语言</text>')
lines.append('  <text x="410" y="196" text-anchor="middle" class="t-b" fill="#9a3412">↓ 强制 12 段结构 ↓</text>')
# 12-section structure (key sections shown)
secs = [
    '## Project Context',
    '## Applicable OpenSpec Rules',
    '## Goal / Non-Goals',
    '## Source Coverage（源→验收→切片）',
    '## File Responsibility Map',
    '## Implementation Slices（TDD 3 步）',
    '## Verification Plan',
    '## Superpowers Handoff',
]
yy = 210
for s in secs:
    lines.append(f'  <rect x="306" y="{yy}" width="208" height="20" rx="4" fill="#fffbeb" stroke="#fde68a" stroke-width="1"/>')
    lines.append(f'  <text x="314" y="{yy+14}" class="t-sec">{s}</text>')
    yy += 23

# ---- Right: plan-ready output + Superpowers ----
# plan-ready document (folded corner)
lines.append('  <rect x="570" y="120" width="170" height="100" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.8"/>')
lines.append('  <path d="M 720 120 L 740 120 L 740 140 Z" fill="#bbf7d0"/>')
lines.append('  <path d="M 720 120 L 720 140 L 740 140" fill="none" stroke="#86efac" stroke-width="1.5"/>')
lines.append('  <text x="655" y="142" text-anchor="middle" class="t-h" fill="#15803d">plan-ready.md</text>')
lines.append('  <text x="655" y="160" text-anchor="middle" class="t-b">强制 12 段实现交接</text>')
lines.append('  <text x="655" y="178" text-anchor="middle" class="t-b">→ 唯一上下文桥梁</text>')
lines.append('  <text x="655" y="198" text-anchor="middle" class="t-b">翻译后跑 5 项自检</text>')

# 5 checks badge
lines.append('  <rect x="570" y="232" width="170" height="56" rx="6" fill="#fefce8" stroke="#eab308"/>')
lines.append('  <text x="655" y="252" text-anchor="middle" class="t-h" fill="#92400e">5 项自检（spec.md:181）</text>')
lines.append('  <text x="655" y="270" text-anchor="middle" class="t-b">Source Coverage 完整</text>')
lines.append('  <text x="655" y="283" text-anchor="middle" class="t-b">Slices 含 TDD/验证/风险 · Handoff 非 TODO</text>')

# Superpowers consumption
lines.append('  <rect x="780" y="120" width="195" height="280" rx="10" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>')
lines.append('  <text x="877" y="142" text-anchor="middle" class="t-h" fill="#6b21a8">Superpowers 消费</text>')
lines.append('  <text x="877" y="158" text-anchor="middle" class="t-b">writing-plans + TDD</text>')
sp = [
    ('build 前置 3 检查', 'Project Context / Rules /', 'Handoff 必须 非 TODO'),
    ('slice 展开', '每 slice → 2-5 分钟', 'checkbox 步骤'),
    ('TDD 节奏', '先写失败测试 → 实现', '→ 每 task 一 commit'),
    ('产出', 'docs/superpowers/plans/', 'YYYY-MM-DD-&lt;变更&gt;.md'),
]
yy = 174
for h, s1, s2 in sp:
    lines.append(f'  <rect x="794" y="{yy}" width="167" height="48" rx="6" fill="#ffffff" stroke="#e9d5ff"/>')
    lines.append(f'  <text x="802" y="{yy+16}" class="t-sec" font-weight="600">{h}</text>')
    lines.append(f'  <text x="802" y="{yy+31}" class="t-b">{s1}</text>')
    lines.append(f'  <text x="802" y="{yy+43}" class="t-b">{s2}</text>')
    yy += 54

# ---- Arrows ----
# OpenSpec -> translation
lines.append('  <line x1="250" y1="200" x2="286" y2="200" stroke="#ea580c" stroke-width="2" marker-end="url(#a-orange)"/>')
lines.append('  <text x="268" y="192" text-anchor="middle" class="t-edge-em">输入</text>')
# translation -> plan-ready
lines.append('  <line x1="530" y1="170" x2="566" y2="170" stroke="#16a34a" stroke-width="2" marker-end="url(#a-green)"/>')
lines.append('  <text x="548" y="162" text-anchor="middle" class="t-edge-em">产出</text>')
# plan-ready -> Superpowers
lines.append('  <line x1="740" y1="170" x2="776" y2="170" stroke="#9333ea" stroke-width="2" marker-end="url(#a-orange)"/>')
lines.append('  <text x="758" y="162" text-anchor="middle" class="t-edge-em">消费</text>')

# ---- Bottom: root reason callout ----
lines.append('  <rect x="30" y="440" width="945" height="138" rx="10" fill="#fef2f2" stroke="#fecaca" stroke-width="1.5"/>')
lines.append('  <text x="48" y="464" class="t-h" fill="#991b1b">⚠ 为什么必须翻译？——编排器模式的根本代价</text>')
lines.append('  <text x="48" y="488" class="t-b">templates/spec.md:82 与 build.md 反复强调：「Superpowers 本身不会自动读取 openspec/config.yaml；上下文必须通过 plan-ready.md 传递给 writing-plans」。</text>')
lines.append('  <text x="48" y="508" class="t-b">→ 即：若不显式把 OpenSpec 的项目规则复制进 plan-ready，这些规则就会在 Superpowers 执行时丢失。这是「两个独立系统拼接」必须付出的代价。</text>')
lines.append('  <text x="48" y="536" class="t-b" font-weight="600" fill="#991b1b">格式漂移发现（实现不一致）：</text>')
lines.append('  <text x="48" y="554" class="t-b">真实存档 openspec/changes/archive/.../plan-ready.md 是旧版 amendment 驱动格式（## 来源 / ## Amendments / ## 追加实现步骤），缺 Source Coverage / File Responsibility Map / Implementation Slices(TDD) /</text>')
lines.append('  <text x="48" y="570" class="t-b">Verification Plan / Superpowers Handoff 段 —— 说明 12 段硬化格式是 0.4.x 引入的，比该存档新（实现与历史产物的漂移）。</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\openflow-plan-ready翻译层.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
