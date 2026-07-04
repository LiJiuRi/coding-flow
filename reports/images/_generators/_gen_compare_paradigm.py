# -*- coding: utf-8 -*-
"""对比报告 · 三方范式对比（手绘草稿风）."""
lines = []
W, H = 1200, 700
INK = '#2b2b2b'
PAPER = '#fbf7f0'
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Comic Sans MS', 'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif; }
    .t-title { font-size: 24px; font-weight: 700; fill: #2b2b2b; }
    .t-sub { font-size: 13px; fill: #6b6256; font-style: italic; }
    .t-name { font-size: 19px; font-weight: 700; fill: #2b2b2b; }
    .t-tag { font-size: 13px; font-weight: 600; }
    .t-box { font-size: 13px; font-weight: 600; fill: #2b2b2b; }
    .t-b { font-size: 11.5px; fill: #4a4438; }
    .t-cap { font-size: 12px; fill: #6b6256; font-style: italic; }
    .t-sticky { font-size: 11.5px; fill: #5a4a2a; }
    .t-axis { font-size: 13px; font-weight: 600; fill: #2b2b2b; }
  </style>""")
lines.append(f'  <rect width="{W}" height="{H}" fill="{PAPER}"/>')
# faint dot grid
lines.append('  <defs><pattern id="dots" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.7" fill="#e2d9c8"/></pattern></defs>')
lines.append(f'  <rect width="{W}" height="{H}" fill="url(#dots)"/>')
# sketch frame
lines.append(f'  <rect x="14" y="14" width="{W-28}" height="{H-28}" rx="6" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
lines.append(f'  <rect x="17" y="11" width="{W-34}" height="{H-22}" rx="6" fill="none" stroke="{INK}" stroke-width="1" opacity="0.35"/>')
lines.append("""  <defs>
    <marker id="h-ink" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#2b2b2b"/></marker>
    <marker id="h-blue" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#3b6ea5"/></marker>
    <marker id="h-green" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#4a7c59"/></marker>
    <marker id="h-orange" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#c97b3a"/></marker>
  </defs>""")

def squiggle(x, y, w, color=INK):
    d = f'M {x},{y} '
    n = max(4, int(w/14))
    step = w/n
    for i in range(n):
        dy = -3 if i % 2 == 0 else 3
        d += f'q {step/2},{dy} {step},0 '
    lines.append(f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')

def sketch_rect(x, y, w, h, rot=0, fill='#ffffff', stroke=INK, sw=2, dash=''):
    cx, cy = x+w/2, y+h/2
    tr = f'rotate({rot} {cx} {cy})'
    d = f' stroke-dasharray="{dash}"' if dash else ''
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" transform="{tr}"{d}/>')
    lines.append(f'  <rect x="{x+2.5}" y="{y-1.8}" width="{w}" height="{h}" rx="7" fill="none" stroke="{stroke}" stroke-width="1" opacity="0.3" transform="{tr}"/>')

def sticky(x, y, w, h, text_lines, rot=-2.5, color='#fff4c2', border='#d9c27a'):
    cx, cy = x+w/2, y+h/2
    tr = f'rotate({rot} {cx} {cy})'
    lines.append(f'  <path d="M {x},{y} L {x+w-10},{y} L {x+w},{y+10} L {x+w},{y+h} L {x},{y+h} Z" fill="{color}" stroke="{border}" stroke-width="1.4" transform="{tr}"/>')
    # folded corner
    lines.append(f'  <path d="M {x+w-10},{y} L {x+w-10},{y+10} L {x+w},{y+10}" fill="none" stroke="{border}" stroke-width="1.2" transform="{tr}"/>')
    for i, t in enumerate(text_lines):
        lines.append(f'  <text x="{cx}" y="{y+22+i*16}" text-anchor="middle" class="t-sticky" transform="{tr}">{t}</text>')

# Title
lines.append(f'  <text x="600" y="52" text-anchor="middle" class="t-title">三种范式：编排器 / 融合器 / 平台</text>')
squiggle(430, 62, 340)
lines.append(f'  <text x="600" y="82" text-anchor="middle" class="t-sub">同源三种策略 —— 从轻到重：松耦合编排 → 高内聚融合 → 平台化全功能</text>')

# ===== Column 1: openflow (编排器) =====
lines.append('  <g transform="rotate(-0.6 200 380)">')
lines.append('  <text x="200" y="118" text-anchor="middle" class="t-name">openflow</text>')
lines.append('  <text x="200" y="138" text-anchor="middle" class="t-tag" fill="#3b6ea5">编排器 Orchestrator</text>')
squiggle(140, 144, 120, '#3b6ea5')
# sketch: thin me in center, external deps around
sketch_rect(150, 180, 100, 46, rot=-1, fill='#ffffff')
lines.append('  <text x="200" y="200" text-anchor="middle" class="t-box">openflow</text>')
lines.append('  <text x="200" y="215" text-anchor="middle" class="t-b">（极薄胶水层）</text>')
# external OpenSpec
sketch_rect(80, 270, 110, 44, rot=2, fill='#eaf1f8')
lines.append('  <text x="135" y="289" text-anchor="middle" class="t-box">OpenSpec</text>')
lines.append('  <text x="135" y="304" text-anchor="middle" class="t-b">外部·PATH</text>')
sketch_rect(210, 270, 110, 44, rot=-2, fill='#eaf1f8')
lines.append('  <text x="265" y="289" text-anchor="middle" class="t-box">Superpowers</text>')
lines.append('  <text x="265" y="304" text-anchor="middle" class="t-b">外部·文件</text>')
lines.append('  <path d="M 180 226 Q 160 248 150 268" fill="none" stroke="#3b6ea5" stroke-width="1.8" stroke-linecap="round" marker-end="url(#h-blue)"/>')
lines.append('  <path d="M 220 226 Q 240 248 250 268" fill="none" stroke="#3b6ea5" stroke-width="1.8" stroke-linecap="round" marker-end="url(#h-blue)"/>')
lines.append('  <text x="200" y="350" text-anchor="middle" class="t-cap">自己不演奏 · 只指挥</text>')
# sticky notes
sticky(60, 380, 150, 50, ['纯 markdown 约束（软）', '无运行时强制'], rot=-3)
sticky(180, 445, 150, 50, ['无独有能力', '平台支持：4'], rot=2.5)
lines.append('  <text x="200" y="552" text-anchor="middle" class="t-b" font-weight="600">不嵌入 · 不分叉</text>')
lines.append('  </g>')

# ===== Column 2: spec-superflow (融合器) =====
lines.append('  <g transform="rotate(0.5 600 380)">')
lines.append('  <text x="600" y="118" text-anchor="middle" class="t-name">spec-superflow</text>')
lines.append('  <text x="600" y="138" text-anchor="middle" class="t-tag" fill="#6b5b95">融合器 Fusion</text>')
squiggle(540, 144, 120, '#6b5b95')
# big self-contained container absorbing internals
sketch_rect(450, 175, 300, 150, rot=-0.5, fill='#f1eef7', sw=2.2)
lines.append('  <text x="600" y="196" text-anchor="middle" class="t-b" font-style="italic">自包含单一 owner</text>')
sketch_rect(468, 210, 124, 46, rot=1, fill='#ffffff')
lines.append('  <text x="530" y="230" text-anchor="middle" class="t-box">OpenSpec 引擎</text>')
lines.append('  <text x="530" y="244" text-anchor="middle" class="t-b">schema/解析/验证</text>')
sketch_rect(608, 210, 124, 46, rot=-1, fill='#ffffff')
lines.append('  <text x="670" y="230" text-anchor="middle" class="t-box">SP 铁律</text>')
lines.append('  <text x="670" y="244" text-anchor="middle" class="t-b">TDD/debug/review</text>')
sketch_rect(500, 270, 200, 38, rot=0.5, fill='#fbe9d6', stroke='#c97b3a')
lines.append('  <text x="600" y="293" text-anchor="middle" class="t-box" fill="#7a4a1a">execution-contract 桥接</text>')
lines.append('  <text x="600" y="352" text-anchor="middle" class="t-cap">全能乐队 · 全内化</text>')
sticky(455, 380, 145, 50, ['软 + 硬门禁', 'guard.mjs exit 拦截'], rot=2.5)
sticky(610, 445, 145, 50, ['桥接层独创', '平台支持：7+'], rot=-3)
lines.append('  <text x="600" y="552" text-anchor="middle" class="t-b" font-weight="600">吸收源码 · 自包含</text>')
lines.append('  </g>')

# ===== Column 3: comet (平台) =====
lines.append('  <g transform="rotate(-0.4 1000 380)">')
lines.append('  <text x="1000" y="118" text-anchor="middle" class="t-name">comet</text>')
lines.append('  <text x="1000" y="138" text-anchor="middle" class="t-tag" fill="#4a7c59">平台 Platform</text>')
squiggle(940, 144, 120, '#4a7c59')
# big platform box
sketch_rect(850, 175, 250, 150, rot=0.5, fill='#eaf3ec', sw=2.2)
lines.append('  <text x="975" y="196" text-anchor="middle" class="t-b" font-style="italic">Node-only runtime 平台</text>')
sketch_rect(866, 210, 150, 46, rot=-1, fill='#ffffff')
lines.append('  <text x="941" y="230" text-anchor="middle" class="t-box">确定性状态机</text>')
lines.append('  <text x="941" y="244" text-anchor="middle" class="t-b">自带引擎（无 LLM）</text>')
sketch_rect(1024, 210, 64, 46, rot=1.5, fill='#fbe9d6', stroke='#c97b3a')
lines.append('  <text x="1056" y="230" text-anchor="middle" class="t-box">Skill</text>')
lines.append('  <text x="1056" y="244" text-anchor="middle" class="t-box">工厂</text>')
sketch_rect(900, 270, 150, 38, rot=0.5, fill='#ffffff')
lines.append('  <text x="975" y="293" text-anchor="middle" class="t-b">hook-guard 物理拦截</text>')
# external OpenSpec call (arrow out right) + 33 platforms down
lines.append('  <text x="975" y="352" text-anchor="middle" class="t-cap">唱片公司 + 发行渠道</text>')
sticky(850, 380, 150, 50, ['软 + 硬 + 物理门禁', 'Node-only · 33 平台'], rot=-3)
sticky(1010, 445, 150, 50, ['独有：Skill 创作分发', '可恢复 · 可校验'], rot=2.5)
lines.append('  <text x="1000" y="552" text-anchor="middle" class="t-b" font-weight="600">调用 + 自带 · 平台化</text>')
lines.append('  </g>')

# ===== Bottom progressive axis =====
lines.append(f'  <line x1="120" y1="600" x2="1080" y2="600" stroke="{INK}" stroke-width="2" stroke-linecap="round" marker-end="url(#h-ink)"/>')
lines.append('  <circle cx="200" cy="600" r="5" fill="#3b6ea5"/>')
lines.append('  <circle cx="600" cy="600" r="5" fill="#6b5b95"/>')
lines.append('  <circle cx="1000" cy="600" r="5" fill="#4a7c59"/>')
lines.append('  <text x="200" y="628" text-anchor="middle" class="t-axis" fill="#3b6ea5">松耦合编排</text>')
lines.append('  <text x="600" y="628" text-anchor="middle" class="t-axis" fill="#6b5b95">高内聚融合</text>')
lines.append('  <text x="1000" y="628" text-anchor="middle" class="t-axis" fill="#4a7c59">平台化全功能</text>')
lines.append('  <text x="600" y="658" text-anchor="middle" class="t-sub">整合程度递进 · 复杂度递增 · 可控性递增</text>')
lines.append('  <text x="120" y="678" class="t-cap">轻</text>')
lines.append('  <text x="1060" y="678" class="t-cap">重</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\compare-三方范式.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
