# -*- coding: utf-8 -*-
"""openflow 8 阶段工作流流程图 — Style 1 Flat Icon."""
lines = []
W, H = 1000, 820
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-phase { font-size: 14px; font-weight: 600; fill: #111827; }
    .t-phase-sub { font-size: 11.5px; fill: #475569; }
    .t-tag { font-size: 11px; font-weight: 600; }
    .t-gate { font-size: 11.5px; font-weight: 600; fill: #92400e; }
    .t-edge { font-size: 11.5px; fill: #374151; }
    .t-edge-y { font-size: 11.5px; font-weight: 600; fill: #15803d; }
    .t-edge-n { font-size: 11.5px; font-weight: 600; fill: #b91c1c; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#64748b"/></marker>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#9333ea"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
  </defs>""")

lines.append('  <text x="500" y="30" text-anchor="middle" class="t-title">openflow 工作流：8 阶段 + 硬编码门禁（DEFAULT_GATES）</text>')
lines.append('  <text x="500" y="50" text-anchor="middle" class="t-sub">阶段见 src/core/skill-generator.ts PHASES · 门禁见 workflow-status.ts · 状态来源优先级：workflow-status.md &gt; 文件扫描 &gt; 会话记忆</text>')

def box(x, y, w, h, fill, stroke, title, subs, tag=None, tag_color=None):
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    cx = x + w/2
    ty = y + 22
    lines.append(f'  <text x="{cx}" y="{ty}" text-anchor="middle" class="t-phase">{title}</text>')
    for i, s in enumerate(subs):
        lines.append(f'  <text x="{cx}" y="{ty + 18 + i*16}" text-anchor="middle" class="t-phase-sub">{s}</text>')
    if tag:
        lines.append(f'  <rect x="{x+w-92}" y="{y+6}" width="84" height="17" rx="4" fill="{tag_color}" opacity="0.16"/>')
        lines.append(f'  <text x="{x+w-50}" y="{y+18}" text-anchor="middle" class="t-tag" fill="{tag_color}">{tag}</text>')

def diamond(cx, cy, hw, hh, label, sub=None, font_main='11.5'):
    lines.append(f'  <polygon points="{cx-hw},{cy} {cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh}" fill="#fefce8" stroke="#eab308" stroke-width="1.5"/>')
    lines.append(f'  <text x="{cx}" y="{cy-1}" text-anchor="middle" class="t-gate" font-size="{font_main}">{label}</text>')
    if sub:
        lines.append(f'  <text x="{cx}" y="{cy+13}" text-anchor="middle" class="t-gate" font-size="10.5">{sub}</text>')

# ① init
box(350, 72, 300, 56, '#eff6ff', '#bfdbfe', '① init', ['扫码 package.json/README/AGENTS.md → openspec/config.yaml', '只写 config.yaml + state；禁写代码/change'])
lines.append('  <line x1="500" y1="128" x2="500" y2="146" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
diamond(500, 172, 130, 26, '门禁：config.yaml 存在？', '(init 产出)')
lines.append('  <text x="640" y="168" class="t-edge-n">否 → 强制 init</text>')
lines.append('  <line x1="500" y1="198" x2="500" y2="214" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
lines.append('  <text x="510" y="211" class="t-edge-y">是</text>')

# ② capture (single container, two inner cells)
lines.append('  <rect x="300" y="218" width="380" height="76" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>')
lines.append('  <text x="490" y="236" text-anchor="middle" class="t-phase">② capture（提案捕获 · Step0 先查 config.yaml）</text>')
lines.append('  <line x1="490" y1="242" x2="490" y2="290" stroke="#bfdbfe" stroke-width="1.2"/>')
lines.append('  <text x="395" y="262" text-anchor="middle" class="t-phase-sub" font-weight="600">proposal</text>')
lines.append('  <text x="395" y="278" text-anchor="middle" class="t-phase-sub">3-5 问快速收敛</text>')
lines.append('  <text x="585" y="262" text-anchor="middle" class="t-phase-sub" font-weight="600">brainstorming</text>')
lines.append('  <text x="585" y="278" text-anchor="middle" class="t-phase-sub">一问一答+方案权衡</text>')

# ③ grill optional side branch
lines.append('  <rect x="730" y="226" width="180" height="60" rx="8" fill="#fefce8" stroke="#fde68a" stroke-width="1.5" stroke-dasharray="5,3"/>')
lines.append('  <text x="820" y="248" text-anchor="middle" class="t-phase" fill="#92400e">③ grill（可选）</text>')
lines.append('  <text x="820" y="264" text-anchor="middle" class="t-phase-sub">对抗性提问·每问附推荐答案</text>')
lines.append('  <text x="820" y="278" text-anchor="middle" class="t-phase-sub">非门禁 · 追加 grill-me 决策记录</text>')
lines.append('  <path d="M 680 256 L 730 256" fill="none" stroke="#eab308" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#a-orange)"/>')
lines.append('  <text x="705" y="250" text-anchor="middle" class="t-edge" fill="#92400e">可选</text>')

# capture -> spec
lines.append('  <line x1="490" y1="294" x2="490" y2="312" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
lines.append('  <path d="M 820 286 L 820 302 L 490 302" fill="none" stroke="#eab308" stroke-width="1.5" stroke-dasharray="5,3"/>')

# ④ spec
box(330, 314, 340, 70, '#fff7ed', '#fed7aa', '④ spec（翻译层·产品核心）',
    ['调 OpenSpec CLI 生成规格 → 翻译 7 规则 → plan-ready.md（强制 12 段）', '产出 proposal/design/specs/tasks + plan-ready · 翻译后 5 项自检'],
    tag='NO CODE', tag_color='#dc2626')
lines.append('  <line x1="500" y1="384" x2="500" y2="402" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
diamond(500, 428, 155, 28, '门禁：plan-ready 完整 + 用户确认？', '(DP · 5 项自检全过)')
lines.append('  <text x="665" y="424" class="t-edge-n">否 → 回 spec 修订</text>')
lines.append('  <line x1="500" y1="456" x2="500" y2="472" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
lines.append('  <text x="510" y="469" class="t-edge-y">是</text>')

# ⑥ build
box(330, 474, 340, 70, '#f0fdf4', '#bbf7d0', '⑥ build（委托 Superpowers）',
    ['plan-ready → writing-plans + TDD（先失败测试→实现→每 task 一 commit）', '前置 3 检查；slice 展开 2-5 分钟 checkbox · 唯一默认可写代码'],
    tag='可写代码', tag_color='#16a34a')
# ⑤ amend loop
lines.append('  <rect x="730" y="480" width="180" height="58" rx="8" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>')
lines.append('  <text x="820" y="502" text-anchor="middle" class="t-phase" fill="#6b21a8">⑤ amend（受控修订）</text>')
lines.append('  <text x="820" y="518" text-anchor="middle" class="t-phase-sub">活跃 change/plan-ready 受控改</text>')
lines.append('  <text x="820" y="532" text-anchor="middle" class="t-phase-sub">已归档不可 amend · 回 build</text>')
lines.append('  <path d="M 670 502 L 730 502" fill="none" stroke="#9333ea" stroke-width="1.5" marker-end="url(#a-purple)"/>')
lines.append('  <path d="M 730 516 L 670 516" fill="none" stroke="#9333ea" stroke-width="1.5" marker-end="url(#a-purple)"/>')
lines.append('  <text x="700" y="472" text-anchor="middle" class="t-edge" fill="#6b21a8">修订/回环</text>')

lines.append('  <line x1="500" y1="544" x2="500" y2="562" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
diamond(500, 588, 165, 28, '门禁：全 task 勾选 + OpenSpec task 同步？', '(build 完成条件)')
lines.append('  <text x="675" y="584" class="t-edge-n">否 → 回 build</text>')
lines.append('  <line x1="500" y1="616" x2="500" y2="632" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
lines.append('  <text x="510" y="629" class="t-edge-y">是</text>')

# ⑦ close
box(330, 634, 340, 62, '#fef2f2', '#fecaca', '⑦ close（最严门禁）',
    ['验证一致性 + 归档 · 不改代码', 'MODIFIED/REMOVED capability 必须先有 spec.md 才能归档'],
    tag='NO CODE', tag_color='#dc2626')
lines.append('  <line x1="500" y1="696" x2="500" y2="714" stroke="#64748b" stroke-width="1.6" marker-end="url(#a-gray)"/>')
diamond(500, 740, 150, 26, '门禁：归档依赖检查（最严）', '否则禁止 openspec archive')
lines.append('  <text x="660" y="736" class="t-edge-n">否 → 阻塞</text>')
lines.append('  <line x1="500" y1="766" x2="500" y2="788" stroke="#16a34a" stroke-width="1.9" marker-end="url(#a-green)"/>')
lines.append('  <text x="510" y="783" class="t-edge-y">是</text>')
lines.append('  <text x="500" y="808" text-anchor="middle" class="t-phase" fill="#15803d">✓ archived（归档完成）</text>')

# left-side artifact rail
lines.append('  <text x="40" y="100" class="t-sub" font-weight="600">产物主线</text>')
lines.append('  <text x="40" y="118" class="t-sub">openspec/config.yaml</text>')
lines.append('  <line x1="178" y1="114" x2="298" y2="114" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>')
lines.append('  <text x="40" y="262" class="t-sub">proposal.md</text>')
lines.append('  <line x1="120" y1="258" x2="298" y2="258" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>')
lines.append('  <text x="40" y="345" class="t-sub" font-weight="600" fill="#9a3412">plan-ready.md ★</text>')
lines.append('  <line x1="150" y1="341" x2="328" y2="341" stroke="#fed7aa" stroke-width="1" stroke-dasharray="3,3"/>')
lines.append('  <text x="40" y="513" class="t-sub">superpowers/plans</text>')
lines.append('  <text x="40" y="529" class="t-sub">+ 代码 + tasks 勾选</text>')
lines.append('  <line x1="160" y1="525" x2="328" y2="525" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>')
lines.append('  <text x="40" y="668" class="t-sub">archive/ +</text>')
lines.append('  <text x="40" y="684" class="t-sub">close-issues.md</text>')
lines.append('  <line x1="140" y1="680" x2="328" y2="680" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\openflow-工作流8阶段.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
