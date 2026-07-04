# -*- coding: utf-8 -*-
"""openflow 整体架构图 — Style 1 Flat Icon."""
lines = []
W, H = 1000, 540
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-box { font-size: 13.5px; font-weight: 600; fill: #111827; }
    .t-box-sub { font-size: 11.5px; fill: #475569; }
    .t-layer { font-size: 11px; font-weight: 600; fill: #9ca3af; letter-spacing: 1px; }
    .t-cont { font-size: 12px; font-weight: 600; fill: #6b7280; }
    .t-edge { font-size: 11.5px; fill: #374151; }
    .t-edge-em { font-size: 11.5px; font-weight: 600; fill: #065f46; }
    .t-leg { font-size: 11.5px; fill: #475569; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))

# arrow markers
lines.append("""  <defs>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#9333ea"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
  </defs>""")

# Title
lines.append('  <text x="500" y="30" text-anchor="middle" class="t-title">openflow 整体架构：四层职责划分 + 外部编排</text>')
lines.append('  <text x="500" y="50" text-anchor="middle" class="t-sub">本质：极薄的「markdown 指令分发器 + 文件系统状态读取器」—— 不实现业务逻辑，业务逻辑全住 markdown 模板里</text>')

# Zone A container (openflow npm 包)
lines.append('  <rect x="30" y="70" width="470" height="400" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6,4"/>')
lines.append('  <text x="46" y="89" class="t-cont">openflow npm 包 · 不嵌入上游代码（仅 chalk/commander/inquirer/ora/yaml）</text>')

# L1 bin
lines.append('  <rect x="55" y="108" width="420" height="42" rx="8" fill="#ffffff" stroke="#d1d5db" stroke-width="1.5"/>')
lines.append('  <text x="68" y="125" class="t-layer">L1 · 入口</text>')
lines.append('  <text x="265" y="140" text-anchor="middle" class="t-box">bin/openflow.js</text>')
lines.append('  <text x="468" y="140" text-anchor="end" class="t-box-sub">5 行 shim · import dist 调 run()</text>')

# L2 cli
lines.append('  <rect x="55" y="164" width="420" height="52" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>')
lines.append('  <text x="68" y="181" class="t-layer">L2 · CLI</text>')
lines.append('  <text x="265" y="199" text-anchor="middle" class="t-box">src/cli/ · commander 注册</text>')
lines.append('  <text x="265" y="213" text-anchor="middle" class="t-box-sub">三命令：init · status · update</text>')

# L3a core
lines.append('  <rect x="55" y="232" width="250" height="120" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.5"/>')
lines.append('  <text x="68" y="249" class="t-layer">L3 · 核心域</text>')
lines.append('  <text x="180" y="266" text-anchor="middle" class="t-box">src/core/</text>')
for i, m in enumerate(['constants.ts · 路径表/阶段表', 'dependency-check.ts · 依赖检测', 'skill-generator.ts · 模板拷贝/别名', 'workflow-status.ts · 状态读取/推断']):
    lines.append(f'  <text x="70" y="{286 + i*16}" class="t-box-sub">• {m}</text>')

# L3b utils
lines.append('  <rect x="320" y="232" width="155" height="120" rx="8" fill="#f8fafc" stroke="#d1d5db" stroke-width="1.5"/>')
lines.append('  <text x="332" y="249" class="t-layer">L3 · 基础设施</text>')
lines.append('  <text x="397" y="266" text-anchor="middle" class="t-box">src/utils/</text>')
for i, m in enumerate(['logger.ts · chalk 日志', 'shell.ts · execSync', '         + cmdExists']):
    lines.append(f'  <text x="333" y="{286 + i*16}" class="t-box-sub">• {m}</text>')

# L4 templates
lines.append('  <rect x="55" y="372" width="420" height="84" rx="8" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.5"/>')
lines.append('  <text x="68" y="389" class="t-layer">L4 · 产品逻辑（真正注入 AI 的指令）</text>')
lines.append('  <text x="265" y="408" text-anchor="middle" class="t-box">templates/*.md（9 个）· init/proposal/grill/spec/build/close/SKILL…</text>')
lines.append('  <text x="265" y="424" text-anchor="middle" class="t-box-sub">不编译进 dist · package.json files:["templates"] 随包发布</text>')
lines.append('  <text x="265" y="440" text-anchor="middle" class="t-box-sub">→ 每阶段该做什么/产出什么/禁止什么 全写在这里</text>')

# Internal gray arrows (call hierarchy)
lines.append('  <line x1="265" y1="150" x2="265" y2="161" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')
lines.append('  <line x1="180" y1="216" x2="180" y2="229" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')
lines.append('  <line x1="397" y1="216" x2="397" y2="229" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')

# ---- Right side: runtime ecosystem ----
# OpenSpec CLI (top-right)
lines.append('  <rect x="540" y="150" width="200" height="66" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>')
lines.append('  <text x="640" y="173" text-anchor="middle" class="t-box">OpenSpec CLI（外部进程）</text>')
lines.append('  <text x="640" y="191" text-anchor="middle" class="t-box-sub">规划引擎 · 经 PATH 调用</text>')
lines.append('  <text x="640" y="206" text-anchor="middle" class="t-box-sub">openspec validate --strict</text>')

# AI tools runtime (center-right)
lines.append('  <rect x="540" y="250" width="300" height="110" rx="10" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>')
lines.append('  <text x="690" y="273" text-anchor="middle" class="t-box">AI 工具运行时（执行 skill 指令）</text>')
lines.append('  <text x="690" y="292" text-anchor="middle" class="t-box-sub">Claude Code · Codex · Cursor · OpenCode</text>')
lines.append('  <text x="690" y="312" text-anchor="middle" class="t-box-sub">按 templates 指令：何时调 OpenSpec、</text>')
lines.append('  <text x="690" y="328" text-anchor="middle" class="t-box-sub">何时委托 Superpowers、写边界在哪</text>')
lines.append('  <text x="690" y="347" text-anchor="middle" class="t-box-sub">（自觉执行，无运行时强制）</text>')

# Superpowers (right)
lines.append('  <rect x="860" y="250" width="120" height="110" rx="8" fill="#f0fdf4" stroke="#bbf7d0" stroke-width="1.5"/>')
lines.append('  <text x="920" y="278" text-anchor="middle" class="t-box">Superpowers</text>')
lines.append('  <text x="920" y="296" text-anchor="middle" class="t-box-sub">（文件系统 skill）</text>')
lines.append('  <text x="920" y="316" text-anchor="middle" class="t-box-sub">writing-plans</text>')
lines.append('  <text x="920" y="334" text-anchor="middle" class="t-box-sub">+ TDD 节奏</text>')

# Green: templates -> AI tools (skill distribution)
lines.append('  <path d="M 475 400 L 510 400 L 510 305 L 535 305" fill="none" stroke="#16a34a" stroke-width="2" marker-end="url(#a-green)"/>')
lines.append('  <text x="517" y="350" class="t-edge-em">skill-generator</text>')
lines.append('  <text x="517" y="365" class="t-edge-em">分发为各平台 skill</text>')

# Blue: AI -> OpenSpec (PATH call)
lines.append('  <line x1="640" y1="250" x2="640" y2="219" stroke="#2563eb" stroke-width="1.8" marker-end="url(#a-blue)"/>')
lines.append('  <text x="648" y="238" class="t-edge">PATH 调用 · 生成规格</text>')

# Purple: AI -> Superpowers
lines.append('  <line x1="840" y1="305" x2="857" y2="305" stroke="#9333ea" stroke-width="1.8" marker-end="url(#a-purple)"/>')
lines.append('  <text x="849" y="297" text-anchor="middle" class="t-edge">委托</text>')

# Orange dashed: dependency-check -> OpenSpec & Superpowers (route along top y=125)
lines.append('  <path d="M 305 295 L 525 295 L 525 125 L 640 125 L 640 147" fill="none" stroke="#ea580c" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#a-orange)"/>')
lines.append('  <path d="M 525 125 L 900 125 L 900 247" fill="none" stroke="#ea580c" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#a-orange)"/>')
lines.append('  <rect x="555" y="111" width="240" height="18" rx="4" fill="#fff7ed" stroke="none"/>')
lines.append('  <text x="675" y="124" text-anchor="middle" class="t-edge" fill="#c2410c">init/运行时依赖检测 · 缺失→手动降级</text>')
# small note pointing dependency-check as source
lines.append('  <text x="312" y="288" class="t-edge" fill="#c2410c">dependency-check</text>')

# ---- Legend ----
ly = 495
lines.append(f'  <rect x="30" y="{ly-12}" width="940" height="38" rx="6" fill="#f9fafb" stroke="#e5e7eb"/>')
items = [('#94a3b8', '包内调用', 'gray'),
         ('#16a34a', 'skill 分发（openflow→AI）', 'green'),
         ('#2563eb', 'PATH 调用外部 OpenSpec', 'blue'),
         ('#9333ea', '委托 Superpowers', 'purple'),
         ('#ea580c', '依赖检测·缺失降级（虚线）', 'orange')]
x = 46
for color, label, mk in items:
    dash = ' stroke-dasharray="5,3"' if mk == 'orange' else ''
    lines.append(f'  <line x1="{x}" y1="{ly+6}" x2="{x+26}" y2="{ly+6}" stroke="{color}" stroke-width="1.8"{dash} marker-end="url(#a-{mk})"/>')
    lines.append(f'  <text x="{x+33}" y="{ly+10}" class="t-leg">{label}</text>')
    x += 188

lines.append('</svg>')

with open(r'D:\developTools\Idea_project\coding-flow\reports\images\openflow-架构图.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
