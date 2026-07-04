# -*- coding: utf-8 -*-
"""对比报告 · 核心维度差异（手绘草稿风 · 3 行 × 3 列）."""
lines = []
W, H = 1200, 800
INK = '#2b2b2b'
PAPER = '#fbf7f0'
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Comic Sans MS', 'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif; }
    .t-title { font-size: 24px; font-weight: 700; fill: #2b2b2b; }
    .t-sub { font-size: 13px; fill: #6b6256; font-style: italic; }
    .t-col { font-size: 17px; font-weight: 700; fill: #2b2b2b; }
    .t-coltag { font-size: 12px; font-weight: 600; }
    .t-cell { font-size: 14px; font-weight: 700; fill: #2b2b2b; }
    .t-b { font-size: 11.5px; fill: #4a4438; }
    .t-row { font-size: 14px; font-weight: 700; fill: #5a4a2a; }
    .t-axis { font-size: 13px; font-weight: 600; fill: #2b2b2b; }
    .t-cap { font-size: 12px; fill: #6b6256; font-style: italic; }
  </style>""")
lines.append(f'  <rect width="{W}" height="{H}" fill="{PAPER}"/>')
lines.append('  <defs><pattern id="dots2" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.7" fill="#e2d9c8"/></pattern></defs>')
lines.append(f'  <rect width="{W}" height="{H}" fill="url(#dots2)"/>')
lines.append(f'  <rect x="14" y="14" width="{W-28}" height="{H-28}" rx="6" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
lines.append(f'  <rect x="17" y="11" width="{W-34}" height="{H-22}" rx="6" fill="none" stroke="{INK}" stroke-width="1" opacity="0.35"/>')

def squiggle(x, y, w, color=INK):
    d = f'M {x},{y} '
    n = max(4, int(w/14)); step = w/n
    for i in range(n):
        dy = -3 if i % 2 == 0 else 3
        d += f'q {step/2},{dy} {step},0 '
    lines.append(f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')

def sketch_rect(x, y, w, h, rot=0, fill='#ffffff', stroke=INK, sw=1.8):
    cx, cy = x+w/2, y+h/2
    tr = f'rotate({rot} {cx} {cy})'
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" transform="{tr}"/>')
    lines.append(f'  <rect x="{x+2.2}" y="{y-1.6}" width="{w}" height="{h}" rx="7" fill="none" stroke="{stroke}" stroke-width="1" opacity="0.3" transform="{tr}"/>')

def cell(x, y, w, h, title, title_color, subs, rot=0, fill='#ffffff'):
    sketch_rect(x, y, w, h, rot=rot, fill=fill)
    cx = x+w/2
    lines.append(f'  <text x="{cx}" y="{y+26}" text-anchor="middle" class="t-cell" fill="{title_color}">{title}</text>')
    lines.append(f'  <line x1="{x+18}" y1="{y+34}" x2="{x+w-18}" y2="{y+34}" stroke="{title_color}" stroke-width="1" opacity="0.4"/>')
    for i, s in enumerate(subs):
        lines.append(f'  <text x="{cx}" y="{y+54+i*20}" text-anchor="middle" class="t-b">{s}</text>')

def rowtag(y, label):
    lines.append(f'  <path d="M 30,{y-18} L 108,{y-26} L 112,{y+30} L 26,{y+24} Z" fill="#fff4c2" stroke="#d9c27a" stroke-width="1.4"/>')
    lines.append(f'  <text x="69" y="{y-2}" text-anchor="middle" class="t-row">{label[0]}</text>')
    lines.append(f'  <text x="69" y="{y+18}" text-anchor="middle" class="t-row" font-size="11">{label[1]}</text>')

# Title
lines.append(f'  <text x="600" y="50" text-anchor="middle" class="t-title">核心维度差异速写</text>')
squiggle(470, 60, 260)
lines.append(f'  <text x="600" y="80" text-anchor="middle" class="t-sub">三个关键维度 × 三种范式 · 约束力递进 · 本质各不相同</text>')

# Column headers
cols = [(270, 'openflow', '#3b6ea5', '编排器'), (600, 'spec-superflow', '#6b5b95', '融合器'), (930, 'comet', '#4a7c59', '平台')]
for cx, name, col, tag in cols:
    lines.append(f'  <text x="{cx}" y="118" text-anchor="middle" class="t-col">{name}</text>')
    lines.append(f'  <text x="{cx}" y="136" text-anchor="middle" class="t-coltag" fill="{col}">{tag}</text>')
    squiggle(cx-55, 143, 110, col)

# sketch column divider lines (vertical, dashed rough)
for dx in [437, 767]:
    lines.append(f'  <line x1="{dx}" y1="155" x2="{dx}" y2="690" stroke="{INK}" stroke-width="1" stroke-dasharray="2,6" opacity="0.4"/>')

# ===== Row 1: 状态机 =====
rowtag(230, ('①', '状态机'))
cell(125, 158, 290, 150, '扁平推断', '#3b6ea5',
     ['5 phase + capture mode', '状态来源：status.md > 文件扫描', '> 会话记忆', '无非法转移拦截（靠 AI 自觉）', '文件推断回退 5 级 · 脆弱'],
     rot=-0.6, fill='#eaf1f8')
cell(455, 158, 290, 150, '严格转移', '#6b5b95',
     ['8 状态 + 9 条合法转移矩阵', 'guard.mjs TRANSITION_CHECKS', '非法转移 → exit=1 拦截', '（可机器执行的硬门禁）', 'SHA256 + 内容语义双层过时'],
     rot=0.5, fill='#f1eef7')
cell(785, 158, 290, 150, '确定性引擎', '#4a7c59',
     ['8 事件纯函数转换表', '三层冗余强制（transition/guard/', 'hook-guard）· 无 LLM 无网络', 'Classic Resolver + 12 step evidence', '可精确恢复（trajectory/checkpoint）'],
     rot=-0.4, fill='#eaf3ec')

# ===== Row 2: 规划→执行桥梁 =====
rowtag(415, ('②', '规划→执行桥梁'))
cell(125, 343, 290, 150, 'plan-ready.md', '#3b6ea5',
     ['实现计划 brief · 强制 12 段', 'Source Coverage（源→验收→切片）', 'Implementation Slices（TDD 3 步）', '解决「SP 不读 config.yaml」', '本质：足够详细的计划'],
     rot=0.6, fill='#eaf1f8')
cell(455, 343, 290, 150, 'execution-contract.md', '#6b5b95',
     ['可检查的意图契约 · 7 大节', 'Intent Lock（锁死 in/out scope）', 'Test Obligations + Review Gates', '解析引擎从 4 工件自动提取', '需用户显式批准（DP-3）'],
     rot=-0.5, fill='#f1eef7')
cell(785, 343, 290, 150, 'design-context.json', '#4a7c59',
     ['design→build 上下文交接包', 'SHA256 追踪（handoff_hash）', 'stale 检测 · 改动则强制重生', 'context compression（-25~30% token）', 'build 仍委托 SP writing-plans'],
     rot=0.4, fill='#eaf3ec')

# ===== Row 3: 约束力 =====
rowtag(600, ('③', '约束力'))
cell(125, 528, 290, 160, '纯软', '#3b6ea5',
     ['全部约束写在 markdown', '无任何运行时强制', '仅 detectWorkflowConflicts', '事后冲突告警', '（且告警本身依赖 AI 读取）', '本质：君子协定'],
     rot=-0.6, fill='#eaf1f8')
cell(455, 528, 290, 160, '软 + 硬', '#6b5b95',
     ['① 铁律（SKILL.md 大写直引）', '② guard.mjs 五维度 exit code', '③ phase-guard.md 软门禁', '+ DP-3 批准门禁', '⚠ 硬门禁依赖 orchestrator 主动调', '本质：法律 + 君子协定'],
     rot=0.5, fill='#f1eef7')
cell(785, 528, 290, 160, '软 + 硬 + 物理', '#4a7c59',
     ['① phase-guard rule（每轮注入）', '② guard.mjs（phase 退出 + --apply）', '③ hook-guard.mjs PreToolUse', '   物理拦截文件写入（open/design/', '   archive 阶段写源码直接 BLOCK）', '④ intent-frame（conf&lt;0.7 强制 ask）'],
     rot=-0.4, fill='#eaf3ec')

# Bottom progressive axis
lines.append(f'  <line x1="125" y1="725" x2="1075" y2="725" stroke="{INK}" stroke-width="2" stroke-linecap="round" marker-end="url(#h-ink2)"/>')
lines.append(f'  <circle cx="270" cy="725" r="5" fill="#3b6ea5"/><circle cx="600" cy="725" r="5" fill="#6b5b95"/><circle cx="930" cy="725" r="5" fill="#4a7c59"/>')
lines.append('  <text x="270" y="752" text-anchor="middle" class="t-axis" fill="#3b6ea5">描述性</text>')
lines.append('  <text x="600" y="752" text-anchor="middle" class="t-axis" fill="#6b5b95">强制性（exit 拦截）</text>')
lines.append('  <text x="930" y="752" text-anchor="middle" class="t-axis" fill="#4a7c59">确定性 + 物理性</text>')
lines.append('  <text x="600" y="778" text-anchor="middle" class="t-cap">约束力递进 · comet 的 hook-guard 是唯一由平台在写入前强制触发的硬门禁</text>')
lines.append("""  <defs>
    <marker id="h-ink2" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#2b2b2b"/></marker>
  </defs>""")

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\compare-核心维度差异.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
