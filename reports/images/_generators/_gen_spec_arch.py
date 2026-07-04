# -*- coding: utf-8 -*-
"""spec-superflow 整体架构图（五层 + 源码级融合）— Style 1 Flat Icon."""
lines = []
W, H = 1000, 660
lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
lines.append("""  <style>
    text { font-family: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', 'Microsoft JhengHei', 'SimHei', sans-serif; }
    .t-title { font-size: 19px; font-weight: 600; fill: #111827; }
    .t-sub { font-size: 12.5px; fill: #6b7280; }
    .t-h { font-size: 13.5px; font-weight: 600; fill: #111827; }
    .t-b { font-size: 11.5px; fill: #475569; }
    .t-layer { font-size: 11px; font-weight: 600; fill: #9ca3af; letter-spacing: 1px; }
    .t-chip { font-size: 10.5px; fill: #1e3a8a; }
    .t-edge { font-size: 11.5px; fill: #374151; }
    .t-edge-em { font-size: 11.5px; font-weight: 600; }
  </style>""")
lines.append('  <rect width="%d" height="%d" fill="#ffffff"/>' % (W, H))
lines.append("""  <defs>
    <marker id="a-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#2563eb"/></marker>
    <marker id="a-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ea580c"/></marker>
    <marker id="a-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#16a34a"/></marker>
    <marker id="a-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#94a3b8"/></marker>
    <marker id="a-purple" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#9333ea"/></marker>
  </defs>""")

lines.append('  <text x="500" y="30" text-anchor="middle" class="t-title">spec-superflow 整体架构：五层 + 源码级融合（自包含）</text>')
lines.append('  <text x="500" y="50" text-anchor="middle" class="t-sub">把 OpenSpec 规划引擎 + Superpowers 执行纪律「吸收」进单一工作流 owner · dist 入库 · 零运行时依赖</text>')

# ---- Left: two source streams being absorbed ----
lines.append('  <rect x="30" y="84" width="160" height="80" rx="8" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>')
lines.append('  <text x="110" y="106" text-anchor="middle" class="t-h">OpenSpec</text>')
lines.append('  <text x="110" y="123" text-anchor="middle" class="t-b">规划引擎（源码）</text>')
lines.append('  <text x="110" y="140" text-anchor="middle" class="t-b">schema/requirement</text>')
lines.append('  <text x="110" y="155" text-anchor="middle" class="t-b">delta/spec-syncer</text>')

lines.append('  <rect x="30" y="184" width="160" height="80" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>')
lines.append('  <text x="110" y="206" text-anchor="middle" class="t-h">Superpowers</text>')
lines.append('  <text x="110" y="223" text-anchor="middle" class="t-b">执行纪律（源码）</text>')
lines.append('  <text x="110" y="240" text-anchor="middle" class="t-b">TDD/debugger/</text>')
lines.append('  <text x="110" y="255" text-anchor="middle" class="t-b">code-reviewer</text>')

# absorb arrows (merge into the right stack)
lines.append('  <path d="M 190 124 C 230 124, 230 470, 258 470" fill="none" stroke="#2563eb" stroke-width="1.8" marker-end="url(#a-blue)"/>')
lines.append('  <path d="M 190 224 C 235 224, 235 200, 258 200" fill="none" stroke="#16a34a" stroke-width="1.8" marker-end="url(#a-green)"/>')
lines.append('  <text x="200" y="160" class="t-edge-em" fill="#2563eb">吸收→引擎层</text>')
lines.append('  <text x="200" y="252" class="t-edge-em" fill="#16a34a">吸收→skill 层</text>')

# ---- Center: 5 layers stack (container) ----
lines.append('  <rect x="250" y="74" width="510" height="430" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6,4"/>')
lines.append('  <text x="266" y="93" class="t-layer">spec-superflow 自包含工作流 owner（dist 入库）</text>')

# L1 hooks
lines.append('  <rect x="266" y="102" width="478" height="44" rx="8" fill="#fefce8" stroke="#fde68a" stroke-width="1.5"/>')
lines.append('  <text x="278" y="119" class="t-layer">L1 · hooks 层</text>')
lines.append('  <text x="505" y="119" text-anchor="middle" class="t-h">session-start hook</text>')
lines.append('  <text x="505" y="136" text-anchor="middle" class="t-b">平台检测 + 注入 workflow-orchestrator SKILL.md（包裹 &lt;EXTREMELY_IMPORTANT&gt;）</text>')
lines.append('  <line x1="505" y1="146" x2="505" y2="158" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')

# L2 skill (9 SKILL.md)
lines.append('  <rect x="266" y="160" width="478" height="100" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1.5"/>')
lines.append('  <text x="278" y="177" class="t-layer">L2 · skill 层（9 个 SKILL.md · Agent 指令集）</text>')
skills = [
    ('workflow-\norchestrator', '#dc2626', '入口·独创'),
    ('spec-\nexplorer', '#2563eb', '探索'),
    ('spec-\nforger', '#2563eb', '规格'),
    ('bridge-\ncontract', '#dc2626', '桥接·独创'),
    ('execution-\ngovernor', '#2563eb', '执行'),
    ('systematic-\ndebugger', '#16a34a', '←SP'),
    ('code-\nreviewer', '#16a34a', '←SP'),
    ('closure-\narchivist', '#2563eb', '收口'),
    ('spec-\nsyncer', '#2563eb', '←OS'),
]
sx = 276
for i, (name, col, role) in enumerate(skills):
    fill = '#fee2e2' if col == '#dc2626' else ('#dcfce7' if col == '#16a34a' else '#dbeafe')
    lines.append(f'  <rect x="{sx}" y="186" width="50" height="46" rx="6" fill="{fill}" stroke="{col}" stroke-width="1.2"/>')
    n1, n2 = name.split('\n')
    lines.append(f'  <text x="{sx+25}" y="201" text-anchor="middle" class="t-chip" font-weight="600">{n1}</text>')
    lines.append(f'  <text x="{sx+25}" y="214" text-anchor="middle" class="t-chip" font-weight="600">{n2}</text>')
    lines.append(f'  <text x="{sx+25}" y="227" text-anchor="middle" class="t-chip" font-size="9" fill="{col}">{role}</text>')
    sx += 52
lines.append('  <text x="505" y="250" text-anchor="middle" class="t-b">红=独创  蓝=融合增强  绿=←Superpowers  由 orchestrator 路由，每路由前先跑 guard.mjs</text>')
lines.append('  <line x1="505" y1="260" x2="505" y2="272" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')

# L3 rules
lines.append('  <rect x="266" y="274" width="478" height="44" rx="8" fill="#fff7ed" stroke="#fed7aa" stroke-width="1.5"/>')
lines.append('  <text x="278" y="291" class="t-layer">L3 · rules 层</text>')
lines.append('  <text x="505" y="291" text-anchor="middle" class="t-h">phase-guard.md（ssf inject 生成的「允许/禁止」软门禁）</text>')
lines.append('  <text x="505" y="308" text-anchor="middle" class="t-b">每轮注入上下文 · 7 个标准决策点（DP-3 用户批准门禁等）</text>')
lines.append('  <line x1="505" y1="318" x2="505" y2="330" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')

# L4 CLI
lines.append('  <rect x="266" y="332" width="478" height="78" rx="8" fill="#faf5ff" stroke="#d8b4fe" stroke-width="1.5"/>')
lines.append('  <text x="278" y="349" class="t-layer">L4 · CLI 层（scripts/ · ssf · 零依赖路由器）</text>')
lines.append('  <text x="505" y="367" text-anchor="middle" class="t-h">ssf 8 子命令：state · guard · sync · inject · version · config · doctor · build</text>')
lines.append('  <text x="505" y="385" text-anchor="middle" class="t-b">状态机读写 · SHA256 哈希校验 · 工件存在性验证 · 版本/配置/健康检查</text>')
lines.append('  <text x="505" y="401" text-anchor="middle" class="t-b">guard.mjs 五维度硬门禁（exit≠0 即 BLOCK）</text>')
lines.append('  <line x1="505" y1="410" x2="505" y2="422" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#a-gray)"/>')

# L5 engine
lines.append('  <rect x="266" y="424" width="478" height="70" rx="8" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>')
lines.append('  <text x="278" y="441" class="t-layer">L5 · 引擎层（src/ → dist/ · 被 CLI 与 skill 共同 import）</text>')
lines.append('  <text x="505" y="459" text-anchor="middle" class="t-h">schema/ · parsing/ · validation/</text>')
lines.append('  <text x="505" y="476" text-anchor="middle" class="t-b">Requirement/Scenario/Delta/Spec 类型 · markdown→结构化正则解析 · Validator + 中英文双语 tokenizer</text>')

# ---- Right: state file + chain ----
lines.append('  <rect x="790" y="160" width="185" height="120" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>')
lines.append('  <text x="882" y="182" text-anchor="middle" class="t-h">.spec-superflow.yaml</text>')
lines.append('  <text x="882" y="199" text-anchor="middle" class="t-b">状态文件</text>')
lines.append('  <text x="882" y="219" text-anchor="middle" class="t-b">• 26 个状态字段</text>')
lines.append('  <text x="882" y="237" text-anchor="middle" class="t-b">• SHA256 哈希（防篡改）</text>')
lines.append('  <text x="882" y="255" text-anchor="middle" class="t-b">• 当前 state + contract hash</text>')
lines.append('  <text x="882" y="273" text-anchor="middle" class="t-b">• 双层过时检测</text>')
# orchestrator reads state
lines.append('  <path d="M 744 210 L 786 210" fill="none" stroke="#ea580c" stroke-width="1.6" marker-end="url(#a-orange)"/>')
lines.append('  <path d="M 786 226 L 744 226" fill="none" stroke="#ea580c" stroke-width="1.6" marker-end="url(#a-orange)"/>')
lines.append('  <text x="765" y="202" text-anchor="middle" class="t-edge" fill="#c2410c">读/写</text>')

# execution-contract.md (bridge artifact) right-mid
lines.append('  <rect x="790" y="300" width="185" height="86" rx="8" fill="#fff7ed" stroke="#fb923c" stroke-width="1.6"/>')
lines.append('  <text x="882" y="322" text-anchor="middle" class="t-h" fill="#9a3412">execution-contract.md</text>')
lines.append('  <text x="882" y="340" text-anchor="middle" class="t-b">桥接工件（独创核心）</text>')
lines.append('  <text x="882" y="358" text-anchor="middle" class="t-b">4 规划工件 → 意图锁契约</text>')
lines.append('  <text x="882" y="376" text-anchor="middle" class="t-b">Intent Lock + Test Obligations</text>')
# bridge-contract skill -> contract artifact
lines.append('  <path d="M 530 248 C 700 290, 720 320, 786 340" fill="none" stroke="#dc2626" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#a-orange)"/>')
lines.append('  <text x="690" y="288" class="t-edge" fill="#991b1b">bridge-contract 生成</text>')

# ---- Bottom: collaboration chain ----
lines.append('  <rect x="30" y="540" width="945" height="100" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>')
lines.append('  <text x="48" y="562" class="t-h">运行时协作链路（5 步）</text>')
chain = [
    ('① 会话启动', 'hooks 注入 orchestrator 全文'),
    ('② orchestrator', '读工件 + ssf state get / guard.mjs check 决定路由'),
    ('③ guard.mjs', '调 dist/ Validator 做 schema-valid 维度检查'),
    ('④ skill 产/消工件', 'bridge-contract 生成 contract → ssf state init 写哈希'),
    ('⑤ closure', 'ssf state transition closing → ssf sync'),
]
cx = 48
for h, d in chain:
    lines.append(f'  <text x="{cx}" y="586" class="t-h" fill="#1e3a8a">{h}</text>')
    lines.append(f'  <text x="{cx}" y="603" class="t-b">{d}</text>')
    cx += 188

lines.append('  <text x="48" y="628" class="t-b" fill="#6b21a8">⚠ 铁律直引：NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST ｜ NO FIXES WITHOUT ROOT CAUSE FIRST ｜ NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE</text>')

lines.append('</svg>')
with open(r'D:\developTools\Idea_project\coding-flow\reports\images\spec-架构图.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('SVG written:', len(lines), 'lines')
