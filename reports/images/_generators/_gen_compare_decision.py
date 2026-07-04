# -*- coding: utf-8 -*-
"""对比报告 · 选型决策树（手绘草稿风）."""
lines = []
W, H = 1200, 860
INK = '#2b2b2b'
PAPER = '#fbf7f0'
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Comic Sans MS', 'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif; }
    .t-title { font-size: 24px; font-weight: 700; fill: #2b2b2b; }
    .t-sub { font-size: 13px; fill: #6b6256; font-style: italic; }
    .t-root { font-size: 14px; font-weight: 700; fill: #2b2b2b; }
    .t-q { font-size: 12.5px; font-weight: 600; fill: #2b2b2b; }
    .t-out { font-size: 17px; font-weight: 700; }
    .t-why { font-size: 11px; fill: #4a4438; }
    .t-yn { font-size: 12px; font-weight: 700; }
    .t-cap { font-size: 12px; fill: #6b6256; font-style: italic; }
    .t-sticky { font-size: 10.5px; fill: #5a4a2a; }
  </style>""")
lines.append(f'  <rect width="{W}" height="{H}" fill="{PAPER}"/>')
lines.append('  <defs><pattern id="dots3" x="0" y="0" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="0.7" fill="#e2d9c8"/></pattern></defs>')
lines.append(f'  <rect width="{W}" height="{H}" fill="url(#dots3)"/>')
lines.append(f'  <rect x="14" y="14" width="{W-28}" height="{H-28}" rx="6" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
lines.append(f'  <rect x="17" y="11" width="{W-34}" height="{H-22}" rx="6" fill="none" stroke="{INK}" stroke-width="1" opacity="0.35"/>')
lines.append("""  <defs>
    <marker id="hd-ink" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#2b2b2b"/></marker>
    <marker id="hd-green" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,10 4.5,0 9" fill="#4a7c59"/></marker>
  </defs>""")

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

def sketch_diamond(cx, cy, hw, hh, rot=0):
    tr = f'rotate({rot} {cx} {cy})'
    pts = f'{cx-hw},{cy} {cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh}'
    lines.append(f'  <polygon points="{pts}" fill="#fff8e1" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round" transform="{tr}"/>')
    pts2 = f'{cx-hw+2.2},{cy-1.6} {cx+2.2},{cy-hh-1.6} {cx+hw+2.2},{cy-1.6} {cx+2.2},{cy+hh-1.6}'
    lines.append(f'  <polygon points="{pts2}" fill="none" stroke="{INK}" stroke-width="1" opacity="0.3" transform="{tr}"/>')

def sticky(x, y, w, h, lines_t, rot=-2.5):
    cx, cy = x+w/2, y+h/2
    tr = f'rotate({rot} {cx} {cy})'
    lines.append(f'  <path d="M {x},{y} L {x+w-9},{y} L {x+w},{y+9} L {x+w},{y+h} L {x},{y+h} Z" fill="#fff4c2" stroke="#d9c27a" stroke-width="1.3" transform="{tr}"/>')
    lines.append(f'  <path d="M {x+w-9},{y} L {x+w-9},{y+9} L {x+w},{y+9}" fill="none" stroke="#d9c27a" stroke-width="1.1" transform="{tr}"/>')
    for i, t in enumerate(lines_t):
        lines.append(f'  <text x="{cx}" y="{y+18+i*14}" text-anchor="middle" class="t-sticky" transform="{tr}">{t}</text>')

# Title
lines.append(f'  <text x="600" y="50" text-anchor="middle" class="t-title">选型决策树</title>')
squiggle(500, 60, 200)
lines.append(f'  <text x="600" y="80" text-anchor="middle" class="t-sub">按需求画像逐步判断 · 四个出口 · 复杂度与能力递增</text>')

# Root
sketch_rect(320, 100, 560, 50, rot=-0.4, fill='#ffffff')
lines.append('  <text x="600" y="130" text-anchor="middle" class="t-root">开始：要把 OpenSpec 规划纪律 + Superpowers 执行纪律 统一进 AI 编程工作流？</text>')
# root 否 → 都不选 (far right small), root 是 → down
lines.append('  <path d="M 880 125 Q 980 125 980 95" fill="none" stroke="#2b2b2b" stroke-width="1.6" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="908" y="118" class="t-yn" fill="#b85450">否</text>')
sticky(950, 70, 200, 42, ['都不需要 → 维持现状'], rot=2)
# root 是 down to Q1
lines.append('  <line x1="600" y1="150" x2="300" y2="178" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="455" y="170" class="t-yn" fill="#4a7c59">是</text>')

# Q1
sketch_diamond(300, 235, 175, 50, rot=-0.6)
lines.append('  <text x="300" y="228" text-anchor="middle" class="t-q">追求极简·可组合·跟随上游？</text>')
lines.append('  <text x="300" y="247" text-anchor="middle" class="t-q">4 大平台够用？</text>')
# Q1 是 → openflow
lines.append('  <line x1="475" y1="235" x2="548" y2="235" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="510" y="228" text-anchor="middle" class="t-yn" fill="#4a7c59">是</text>')
sketch_rect(550, 200, 230, 70, rot=0.8, fill='#eaf1f8', stroke='#3b6ea5', sw=2)
lines.append('  <text x="665" y="228" text-anchor="middle" class="t-out" fill="#3b6ea5">✓ openflow</text>')
lines.append('  <text x="665" y="250" text-anchor="middle" class="t-why">极薄编排器 · 零嵌入 · 平台 4</text>')
sticky(820, 205, 180, 60, ['适合：小团队/开源项目', '不在意手动降级', '想跟随上游演进'], rot=3)
# Q1 否 down
lines.append('  <line x1="300" y1="285" x2="300" y2="318" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="312" y="305" class="t-yn" fill="#b85450">否</text>')

# Q2
sketch_diamond(300, 370, 180, 52, rot=0.5)
lines.append('  <text x="300" y="362" text-anchor="middle" class="t-q">要自包含·强约束·内容级</text>')
lines.append('  <text x="300" y="380" text-anchor="middle" class="t-q">状态检测？能维护内嵌引擎？</text>')
# Q2 是 → spec-superflow
lines.append('  <line x1="480" y1="370" x2="548" y2="370" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="514" y="363" text-anchor="middle" class="t-yn" fill="#4a7c59">是</text>')
sketch_rect(550, 335, 230, 70, rot=-0.8, fill='#f1eef7', stroke='#6b5b95', sw=2)
lines.append('  <text x="665" y="363" text-anchor="middle" class="t-out" fill="#6b5b95">✓ spec-superflow</text>')
lines.append('  <text x="665" y="385" text-anchor="middle" class="t-why">源码融合 · 软+硬门禁 · 平台 7+</text>')
sticky(820, 340, 180, 60, ['适合：中型团队/严肃工程', '要可检查的意图契约', '能承担引擎维护'], rot=-3)
# Q2 否 down
lines.append('  <line x1="300" y1="422" x2="300" y2="458" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="312" y="445" class="t-yn" fill="#b85450">否</text>')

# Q3
sketch_diamond(300, 515, 185, 56, rot=-0.5)
lines.append('  <text x="300" y="505" text-anchor="middle" class="t-q">需 Skill 创作/分发 + 确定性</text>')
lines.append('  <text x="300" y="523" text-anchor="middle" class="t-q">可恢复 + Windows 原生？</text>')
lines.append('  <text x="300" y="540" text-anchor="middle" class="t-q">（需 33 平台？）</text>')
# Q3 否 → 都不选 (right)
lines.append('  <line x1="485" y1="515" x2="548" y2="515" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="516" y="508" text-anchor="middle" class="t-yn" fill="#b85450">否</text>')
sketch_rect(550, 480, 230, 70, rot=0.8, fill='#f5f5f5', stroke='#888888', sw=2)
lines.append('  <text x="665" y="508" text-anchor="middle" class="t-out" fill="#555555">✗ 三者都不选</text>')
lines.append('  <text x="665" y="530" text-anchor="middle" class="t-why">不需要 spec-driven 纪律</text>')
sticky(820, 485, 180, 60, ['项目过小 / 已有成熟流程', '团队不适应铁律约束', '或直接用 OpenSpec+SP'], rot=3)
# Q3 是 down to Q4
lines.append('  <line x1="300" y1="571" x2="300" y2="608" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="312" y="595" class="t-yn" fill="#4a7c59">是</text>')

# Q4
sketch_diamond(300, 665, 175, 52, rot=0.5)
lines.append('  <text x="300" y="657" text-anchor="middle" class="t-q">能接受高复杂度？</text>')
lines.append('  <text x="300" y="675" text-anchor="middle" class="t-q">（9 领域 ~110 .ts）</text>')
# Q4 是 → comet
lines.append('  <line x1="475" y1="665" x2="548" y2="665" stroke="#2b2b2b" stroke-width="1.8" stroke-linecap="round" marker-end="url(#hd-green)"/>')
lines.append('  <text x="510" y="658" text-anchor="middle" class="t-yn" fill="#4a7c59">是</text>')
sketch_rect(550, 630, 230, 70, rot=-0.8, fill='#eaf3ec', stroke='#4a7c59', sw=2)
lines.append('  <text x="665" y="658" text-anchor="middle" class="t-out" fill="#4a7c59">✓ comet</text>')
lines.append('  <text x="665" y="680" text-anchor="middle" class="t-why">Node-only 平台 · 独有 Skill 创作 · 33 平台</text>')
sticky(820, 635, 180, 60, ['适合：平台团队/工具建设', '要可恢复·可校验·可发行', 'Windows 原生刚需'], rot=-3)
# Q4 否 → spec-superflow 降级 (far right)
lines.append('  <path d="M 300 717 Q 300 760 540 760 L 866 760 L 866 705" fill="none" stroke="#2b2b2b" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="5,4" marker-end="url(#hd-ink)"/>')
lines.append('  <text x="312" y="740" class="t-yn" fill="#b85450">否</text>')
sketch_rect(866, 670, 200, 60, rot=0.8, fill='#f1eef7', stroke='#6b5b95', sw=1.6)
lines.append('  <text x="966" y="695" text-anchor="middle" class="t-out" fill="#6b5b95" font-size="14">↩ spec-superflow</text>')
lines.append('  <text x="966" y="714" text-anchor="middle" class="t-why">（降级选择）</text>')

# Bottom note
lines.append(f'  <rect x="60" y="790" width="1080" height="46" rx="8" fill="#fff8e1" stroke="#d9c27a"/>')
lines.append('  <text x="78" y="812" class="t-cap" font-weight="700" fill="#5a4a2a">核心推荐：</text>')
lines.append('  <text x="160" y="812" class="t-cap">三者不互斥 —— 理想形态是 contract 锁意图 + plan 给细节 + handoff 防漂移；comet 的 build 仍依赖 Superpowers plan，故可与 SP 并存</text>')
lines.append('  <text x="78" y="828" class="t-cap" fill="#6b6256">组合建议：openflow 做轻量编排入门 → spec-superflow 做工程主力 → comet 做平台化/发行；按团队规模与复杂度耐受度递进采用</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\compare-选型决策树.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
