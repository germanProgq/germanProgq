"""Render repository-owned profile art. Refresh activity with:
gh api graphql -f query='{ user(login:"germanProgq") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }' > assets/activity.json
python3 scripts/render_profile.py
"""
import json
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
def svg(name, height, body):
    (A/name).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img">
<style>text{{font-family:Inter,Arial,sans-serif}}.mono{{font-family:ui-monospace,Menlo,monospace}}.muted{{fill:#9ea9b8}}.light{{fill:#f1f4f8}}</style>
<defs><linearGradient id="panel" x2="1" y2="1"><stop stop-color="#27121c"/><stop offset=".55" stop-color="#151521"/><stop offset="1" stop-color="#27111a"/></linearGradient></defs><rect x="1.5" y="1.5" width="957" height="{height-3}" rx="16" fill="url(#panel)" stroke="#ef4444" stroke-width="2.5"/>{body}</svg>''')
svg('header.svg', 290, '''
<defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#252e3e" stroke-width=".5"/></pattern></defs>
<rect x="620" width="340" height="290" fill="url(#grid)"/>
<rect x="36" y="36" width="36" height="4" rx="2" fill="#ef4444"/>
<text x="84" y="43" class="mono muted" font-size="12" letter-spacing="2">GERMANPROGQ / ENGINEERING</text>
<text x="36" y="113" class="light" font-size="44" font-weight="750">German Vinokurov</text>
<text x="38" y="151" fill="#ed7979" font-size="21">Full-stack interfaces. Backend services. Systems code.</text>
<text x="38" y="202" class="mono muted" font-size="15">TypeScript / React · Rust · Python · C++</text>
<text x="38" y="252" class="muted" font-size="13">Senior Full-Stack Developer @ Positron  /  Co-founder @ Veltos.tech</text>
<path d="M700 80H750V140H840V210H905" fill="none" stroke="#ef4444" stroke-width="2"/>
<path d="M700 210H750V140H840V80H905" fill="none" stroke="#f2bb54" stroke-width="2"/>
<g fill="#10151e" stroke="#ef4444" stroke-width="2"><circle cx="700" cy="80" r="8"/><circle cx="750" cy="140" r="10"/><circle cx="840" cy="210" r="8"/><circle cx="905" cy="210" r="5"/></g>
<g fill="#f2bb54"><circle cx="700" cy="210" r="5"/><circle cx="840" cy="80" r="5"/><circle cx="905" cy="80" r="5"/></g>
<circle cx="750" cy="140" r="18" fill="none" stroke="#ef4444" opacity=".5"><animate attributeName="r" values="14;26;14" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0;.6" dur="4s" repeatCount="indefinite"/></circle>
''')
for filename,label,width in [('portfolio','PORTFOLIO',180),('linkedin','LINKEDIN',160),('email','EMAIL ME',160),('x','X / TWITTER',170)]:
    (A/f'{filename}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="38"><rect x=".5" y=".5" width="{width-1}" height="37" rx="7" fill="#36151e" stroke="#f05261" stroke-width="1.5"/><rect x="13" y="16" width="6" height="6" rx="2" fill="#ef4444"/><text x="30" y="24" font-family="Arial,sans-serif" font-size="12" letter-spacing="1.4" fill="#f1f4f8">{label}</text></svg>')
rows=[('INTERFACES','TypeScript · React · React Native / Expo · Next.js'),('SERVICES','Rust / Axum · Python / FastAPI · Node.js / Express'),('SYSTEMS','C++17 · WebAssembly · CMake · CTest · Rust / C++ FFI'),('DATA & TOOLS','PostgreSQL · MongoDB · SQLite · Git · Docker')]
b='<text x="32" y="39" class="mono muted" font-size="12" letter-spacing="2">REACT TO RUST. INTERFACE TO CORE.</text>'
for i,(label,value) in enumerate(rows):
 y=78+i*47
 b+=f'<path d="M32 {y+22}H928" stroke="#68313e"/><text x="32" y="{y}" class="mono" fill="#ef7979" font-size="12">{escape(label)}</text><text x="230" y="{y}" class="light" font-size="16">{escape(value)}</text>'
svg('stack.svg',270,b)
c=json.loads((A/'activity.json').read_text())['data']['user']['contributionsCollection']['contributionCalendar']
days=[d for w in c['weeks'] for d in w['contributionDays']]
active=sum(d['contributionCount']>0 for d in days)
end=days[-1]['date']
b=f'<text x="32" y="39" class="mono muted" font-size="12" letter-spacing="2">GITHUB ACTIVITY / SNAPSHOT {end}</text><text x="32" y="93" class="light" font-size="38" font-weight="700">{c["totalContributions"]:,}</text><text x="170" y="91" class="muted" font-size="14">contributions</text><text x="400" y="93" class="light" font-size="38" font-weight="700">{active}</text><text x="484" y="91" class="muted" font-size="14">active days</text><text x="700" y="87" class="mono muted" font-size="12">{days[0]["date"]} — {end}</text>'
colors=['#30212c','#782238','#c12b4b','#f04b65','#ffc16b']
for wi,w in enumerate(c['weeks']):
 for di,d in enumerate(w['contributionDays']):
  n=d['contributionCount']; col=colors[0 if n==0 else 1 if n<4 else 2 if n<10 else 3 if n<20 else 4]
  b+=f'<rect x="{32+wi*17}" y="{126+di*17}" width="13" height="13" rx="3" fill="{col}"><title>{d["date"]}: {n} contributions</title></rect>'
b+='<text x="32" y="272" class="muted" font-size="12">Source: GitHub contribution calendar · Includes activity visible through the GitHub API.</text>'
svg('activity.svg',298,b)
svg('footer.svg',74,'<path d="M32 1H928" stroke="#ef4444"/><text x="32" y="43" class="mono muted" font-size="13">LET’S BUILD SOMETHING USEFUL.</text><text x="642" y="43" class="mono" fill="#f18b8b" font-size="13">gvinok@duck.com  /  germanProgq</text>')

projects = [
('p2p','P2P Chat',['Messaging core, SQLite storage and OpenSSL.','C FFI bridge to Rust/Tauri; CTest unit and','integration tests.'],'C++17 / RUST / SQLITE','#fb7185'),
('saas','B2B SaaS templates',['Authentication, permissions and organization','APIs across three reusable backend stacks.','Rust/Axum, Python/FastAPI and Node.js.'],'RUST / PYTHON / TYPESCRIPT','#f6bd60'),
('resident','Resident services',['Document downloads, service requests,','status tracking and user authentication.','C++17 backend with PostgreSQL.'],'C++17 / POSTGRESQL','#c49bff'),
('tacs','TACS',['Kalman-filter tracking, actor-critic learning,','training fixes and a traffic simulator.','A C++ traffic-control project.'],'C++17 / REINFORCEMENT LEARNING','#ff906e')]
for name,title,lines,stack,accent in projects:
 body=f'<svg xmlns="http://www.w3.org/2000/svg" width="460" height="210" viewBox="0 0 460 210"><rect x="1.5" y="1.5" width="457" height="207" rx="13" fill="#21141f" stroke="#ed4055" stroke-width="2.5"/><path d="M25 27H57" stroke="{accent}" stroke-width="4"/><text x="25" y="65" font-family="Arial,sans-serif" font-size="25" font-weight="700" fill="{accent}">{title} ↗</text>'
 for i,line in enumerate(lines): body+=f'<text x="25" y="{96+i*22}" font-family="Arial,sans-serif" font-size="15" fill="#e3dce5">{escape(line)}</text>'
 body+=f'<text x="25" y="183" font-family="monospace" font-size="11" fill="{accent}">{stack}</text></svg>'
 (A/f'{name}.svg').write_text(body)
