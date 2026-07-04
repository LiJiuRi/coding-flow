# -*- coding: utf-8 -*-
"""comet Classic 确定性状态机图 — Style 1 Flat Icon."""
lines = []
W, H = 1200, 600
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-st { font-size: 13.5px; font-weight: 600; fill: #111827; }
    .t-st-sub { font-size: 10.5px; fill: #475569; }
    .t-edge { font-size: 10.5px; fill: #1e3a8a; }
    .t-edge-em { font-size: 11px; font-weight: 600; }
    .t-note { font-size: 11px; fill: #6b7280; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#dc2626"/></marker>
    <marker id="a-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#9333ea"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
  </defs>""")

lines.append('  <text x="600" y="30" text-anchor="middle" class="t-title">comet Classic 运行时：8 事件驱动的确定性状态机（纯函数 · 无 LLM · 无网络）</text>')
lines.append('  <text x="600" y="50" text-anchor="middle" class="t-sub">domains/comet-classic/classic-transitions.ts · 5 phase + archived · 每个事件有前置 guard · effects 经 setField 记录到 state-events.jsonl</text>')

def state(cx, cy, w, h, name, sub, fill, stroke, term=False):
    sw = 2.2 if term else 1.6
    lines.append(f'  <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    lines.append(f'  <text x="{cx}" y="{cy-4}" text-anchor="middle" class="t-st">{name}</text>')
    lines.append(f'  <text x="{cx}" y="{cy+12}" text-anchor="middle" class="t-st-sub">{sub}</text>')

cy = 220
# main phases
state(110, cy, 130, 60, 'open', '提案·建 .comet.yaml', '#eff6ff', '#93c5fd')
state(320, cy, 130, 60, 'design', '设计·evidence', '#eff6ff', '#93c5fd')
state(540, cy, 130, 60, 'build', '实现·TDD/隔离', '#eff6ff', '#93c5fd')
state(760, cy, 130, 60, 'verify', '验证·4 维度', '#eff6ff', '#93c5fd')
state(970, cy, 130, 60, 'archive', '归档·sync', '#eff6ff', '#93c5fd')
state(1130, cy, 120, 60, 'archived', '终态', '#dcfce7', '#86efac', term=True)

# main event arrows
def ev(x1, x2, lbl, sub, y=220):
    lines.append(f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#2563eb" stroke-width="1.7" marker-end="url(#a-blue)"/>')
    lines.append(f'  <text x="{(x1+x2)/2}" y="{y-20}" text-anchor="middle" class="t-edge" font-weight="600">{lbl}</text>')
    lines.append(f'  <text x="{(x1+x2)/2}" y="{y-7}" text-anchor="middle" class="t-edge" fill="#475569">[{sub}]</text>')

ev(177, 253, 'open-complete', 'open-artifacts-present')
ev(387, 473, 'design-complete', 'design-evidence-present')
ev(607, 693, 'build-complete', 'build-decisions-selected')
ev(827, 903, 'verify-pass', 'verification-passed')
lines.append(f'  <line x1="1037" y1="{cy}" x2="1069" y2="{cy}" stroke="#16a34a" stroke-width="1.9" marker-end="url(#a-green)"/>')
lines.append(f'  <text x="1053" y="{cy-7}" text-anchor="middle" class="t-edge-em" fill="#15803d">archived</text>')

# rollback: verify-fail (arc below)
lines.append('  <path d="M 760 251 C 760 305, 540 305, 540 251" fill="none" stroke="#dc2626" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#a-red)"/>')
lines.append('  <text x="650" y="312" text-anchor="middle" class="t-edge-em" fill="#b91c1c">verify-fail [verification-failed] → verify_result=fail</text>')

# preset-escalate: build -> design (arc above, y=130)
lines.append('  <path d="M 540 189 C 540 140, 320 140, 320 189" fill="none" stroke="#9333ea" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#a-purple)"/>')
lines.append('  <text x="430" y="132" text-anchor="middle" class="t-edge-em" fill="#6b21a8">preset-escalate [preset-workflow] hotfix/tweak→full</text>')

# archive-reopen: archive -> design (long arc above, y=85)
lines.append('  <path d="M 970 189 C 970 80, 320 80, 320 189" fill="none" stroke="#9333ea" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#a-purple)"/>')
lines.append('  <text x="645" y="74" text-anchor="middle" class="t-edge-em" fill="#6b21a8">archive-reopen（重新打开修订）</text>')

# preset shortcut paths (below, y=380)
lines.append('  <rect x="60" y="370" width="1080" height="74" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.5" stroke-dasharray="5,3"/>')
lines.append('  <text x="74" y="390" class="t-st" fill="#15803d">2 个预设路径（preset）· intent-frame 路由</text>')
lines.append('  <text x="74" y="411" class="t-note" font-weight="600">hotfix：</text>')
lines.append('  <text x="124" y="411" class="t-note">open → build（跳过 design）→ verify → archive　　</text>')
lines.append('  <text x="430" y="411" class="t-note" font-weight="600">tweak：</text>')
lines.append('  <text x="478" y="411" class="t-note">open → OpenSpec apply（delta spec 一等公民）→ verify → archive</text>')
lines.append('  <text x="74" y="430" class="t-note" fill="#6b21a8">preset-escalate 是唯一合法升级通道：原子置 workflow/classic_profile=full、回退 phase=design、清 design_doc（直接 set phase 被 state machine 硬拦截）</text>')

# bottom: three-layer enforcement + determinism
lines.append('  <rect x="60" y="466" width="1080" height="118" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>')
lines.append('  <text x="76" y="488" class="t-st" fill="#1e3a8a">三层冗余强制（build 的 6 决策字段在三处独立校验）</text>')
lines.append('  <text x="76" y="510" class="t-note" font-weight="600">① transition 入口</text>')
lines.append('  <text x="180" y="510" class="t-note">requireBuildDecisions —— 查转换表 + guard + 应用 effects</text>')
lines.append('  <text x="76" y="528" class="t-note" font-weight="600">② guard --apply</text>')
lines.append('  <text x="180" y="528" class="t-note">CLASSIC_GUARD_TRANSITION_EVENT 复用同一转换表（source=comet-guard）</text>')
lines.append('  <text x="76" y="546" class="t-note" font-weight="600">③ hook-guard PreToolUse</text>')
lines.append('  <text x="180" y="546" class="t-note">物理拦截文件写入 —— open/design/archive 阶段写源码直接 BLOCK（唯一不依赖 agent 主动调用的硬门禁）</text>')
lines.append('  <line x1="76" y1="558" x2="1124" y2="558" stroke="#e5e7eb"/>')
lines.append('  <text x="76" y="576" class="t-note" fill="#15803d">确定性收益：</text>')
lines.append('  <text x="160" y="576" class="t-note">effects 经 setField 只在值变化时记录 {field,from,to} → state-events.jsonl 审计 · 三文件解耦支持精确恢复（trajectory/checkpoint）· 7 个 runtime eval 做差分兼容测试</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\comet-Classic状态机.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
