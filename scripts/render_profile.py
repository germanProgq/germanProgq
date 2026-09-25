"""Generate the profile banner: python3 scripts/render_profile.py."""
from pathlib import Path

banner = Path(__file__).resolve().parents[1] / "assets" / "header.svg"
banner.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
<title id="title">German Vinokurov</title>
<desc id="desc">Full-Stack Developer. Red and black custom profile banner.</desc>
<rect width="1200" height="260" fill="#11090b"/>
<rect x="2" y="2" width="1196" height="256" fill="none" stroke="#ff233d" stroke-width="4"/>
<rect x="0" y="0" width="12" height="260" fill="#ff233d"/>
<path d="M1010 0H1200V260H900Z" fill="#ec1835"/>
<path d="M1060 0L950 260M1110 0L1000 260M1160 0L1050 260" stroke="#11090b" stroke-width="3" opacity=".35"/>
<text x="48" y="58" font-family="monospace" font-size="16" letter-spacing="4" fill="#ff4056">GERMANPROGQ</text>
<text x="44" y="139" font-family="Arial,Helvetica,sans-serif" font-size="67" font-weight="900" letter-spacing="-2" fill="#fff1f3">GERMAN VINOKUROV</text>
<text x="48" y="198" font-family="monospace" font-size="23" letter-spacing="3" fill="#ff4056">FULL-STACK DEVELOPER</text>
<path d="M48 230H310" stroke="#ff233d" stroke-width="4"/>
</svg>''')


# Wrap locally stored logos in a small, staggered animation.
import json
from xml.etree import ElementTree as ET
ET.register_namespace('', 'http://www.w3.org/2000/svg')
assets = banner.parent
technologies = json.loads((assets / 'technologies.json').read_text())
for i, (name, label) in enumerate(technologies):
    icon = ET.fromstring((assets / 'logos' / f'{name}.svg').read_text())
    icon.set('x', '8'); icon.set('y', '8')
    icon.set('width', '36'); icon.set('height', '36')
    if name in ('rust', 'expo'):
        for node in icon.iter():
            color = node.get('fill', '').lower()
            if color in ('#000', '#000000', 'black'):
                node.set('fill', '#f4edef')
        icon.set('fill', '#f4edef')
    art = ET.tostring(icon, encoding='unicode')
    (assets / f'{name}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="52" height="58" viewBox="0 0 52 58" role="img" aria-label="{label}">
<style>
.logo {{ animation: float 6s ease-in-out infinite; animation-delay: -{i * .19:.2f}s; }}
.line {{ animation: pulse 6s ease-in-out infinite; animation-delay: -{i * .19:.2f}s; }}
@keyframes float {{ 0%, 65%, 100% {{ transform: translateY(0); }} 32% {{ transform: translateY(-3px); }} }}
@keyframes pulse {{ 0%, 65%, 100% {{ opacity: .18; }} 32% {{ opacity: .85; }} }}
@media (prefers-reduced-motion: reduce) {{ .logo, .line {{ animation: none; }} }}
</style>
<title>{label}</title><g class="logo">{art}</g>
<path class="line" d="M18 52H34" stroke="#ff233d" stroke-width="2" stroke-linecap="round" opacity=".3"/>
</svg>''')

# Keep the stack aligned without README tables or individual card containers.
groups = [
    ('LANGUAGES', ['typescript', 'javascript', 'python', 'rust', 'cplusplus', 'c', 'go', 'kotlin', 'dart']),
    ('WEB & MOBILE', ['react', 'nextjs', 'expo', 'flutter', 'html5', 'css3']),
    ('APIS & DATA', ['nodejs', 'fastapi', 'postgresql', 'mongodb', 'sqlite']),
    ('SYSTEMS & TOOLS', ['wasm', 'docker', 'git', 'cmake']),
]
from html import escape
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="248" viewBox="0 0 800 248" role="img" aria-labelledby="stack-title"><title id="stack-title">Technology stack grouped by languages, web and mobile, APIs and data, systems and tools</title>']
for row, (label, names) in enumerate(groups):
    y = row * 62
    parts.append(f'<text x="0" y="{y + 31}" font-family="Arial,Helvetica,sans-serif" font-size="10" letter-spacing="1" fill="#ba969d">{escape(label)}</text>')
    for col, name in enumerate(names):
        icon = ET.fromstring((assets / f'{name}.svg').read_text())
        icon.set('x', str(145 + col * 68)); icon.set('y', str(y))
        art = ET.tostring(icon, encoding='unicode')
        # Scope animation selectors to preserve each logo's phase.
        art = art.replace('.logo', f'.logo-{name}').replace('.line', f'.line-{name}')
        art = art.replace('class="logo"', f'class="logo-{name}"').replace('class="line"', f'class="line-{name}"')
        parts.append(art)
parts.append('</svg>')
(assets / 'stack.svg').write_text(''.join(parts))
