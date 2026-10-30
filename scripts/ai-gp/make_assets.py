# 홈페이지 카드용 그림(헤드리스): 아이콘(512px png, SVG 코드로 그림) + 화면 캡처 3장(390×844 webp: 학습·서킷 만들기·대결)
# public을 http://127.0.0.1:8766 으로 띄워 둔 상태에서: python3 scripts/ai-gp/make_assets.py
import math
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/apps/ai-gp'; OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8766/games/ai-gp/'

# 아이콘: 어두운 밤 서킷 커브(연석) + 보라 레이싱 라인 + 빨간 차 + 오른쪽 위 작은 신경망
def kerb(path_id):
    return f'<use href="#{path_id}" stroke="#e8e8e8" stroke-width="150" fill="none"/><use href="#{path_id}" stroke="#d8342c" stroke-width="150" stroke-dasharray="22 22" fill="none"/>'
nodes = [(330, 86), (330, 138), (330, 190), (392, 112), (392, 164), (450, 138)]
links = [(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (4, 5)]
net = ''.join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="#c48bff" stroke-opacity=".55" stroke-width="4"/>' for a, b in links)
net += ''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="#1d1430" stroke="#c48bff" stroke-width="5"/>' for x, y in nodes)
ICON = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3c7f34"/><stop offset="1" stop-color="#25521f"/></linearGradient>
 <path id="trk" d="M-40 470 C 120 470, 170 300, 250 300 S 400 420, 560 250"/>
</defs>
<rect width="512" height="512" fill="url(#bg)"/>
<g fill="#ffffff" opacity=".05"><rect x="0" width="64" height="512"/><rect x="128" width="64" height="512"/><rect x="256" width="64" height="512"/><rect x="384" width="64" height="512"/></g>
{kerb('trk')}
<use href="#trk" stroke="#f4f4f4" stroke-width="136" fill="none"/>
<use href="#trk" stroke="#3a3e46" stroke-width="128" fill="none"/>
<path d="M-40 500 C 120 500, 150 290, 250 282 S 410 400, 560 228" stroke="#b46cff" stroke-opacity=".35" stroke-width="22" fill="none"/>
<path d="M-40 500 C 120 500, 150 290, 250 282 S 410 400, 560 228" stroke="#d2a6ff" stroke-width="7" fill="none"/>
<g transform="translate(262 286) rotate(4) scale(5.2)">
 <rect x="-10" y="-5" width="20" height="10" rx="4" fill="#000" opacity=".35" transform="translate(2 3)"/>
 <g fill="#111"><rect x="-8.4" y="-7.3" width="4.8" height="3.4"/><rect x="-8.4" y="3.9" width="4.8" height="3.4"/><rect x="3.1" y="-6.7" width="4.8" height="3.4"/><rect x="3.1" y="3.3" width="4.8" height="3.4"/></g>
 <path d="M11 0 L5 -2.6 L-4 -3.6 L-9 -3 L-9 3 L-4 3.6 L5 2.6 Z" fill="#ff3b3b"/>
 <rect x="8.5" y="-5" width="2.4" height="10" fill="#ff3b3b"/><rect x="-11" y="-4.6" width="2.6" height="9.2" fill="#ff3b3b"/>
 <ellipse cx="-1.5" cy="0" rx="2.6" ry="1.7" fill="#16181d"/>
</g>
<rect x="296" y="56" width="190" height="164" rx="26" fill="#120d1d" opacity=".82"/>
{net}
<text x="391" y="210" text-anchor="middle" font-family="Jua" font-size="0" fill="#fff"></text>
</svg>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 600, 'height': 600})
    pg.set_content(f'<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&display=swap"><style>body{{margin:0}}</style></head><body>{ICON}</body></html>')
    pg.wait_for_timeout(800)
    Image.open(BytesIO(pg.locator('svg').screenshot())).convert('RGB').resize((512, 512), Image.LANCZOS).save(OUT / 'icon.png')
    print('icon')
    sp = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    sp.goto(URL); sp.evaluate('localStorage.clear()'); sp.reload(); sp.wait_for_timeout(1200)
    sp.click('#iGo'); sp.wait_for_timeout(60000)
    sp.click('[data-sp="1"]'); sp.wait_for_timeout(2500)
    print('train', sp.evaluate('({laps: GP.ST.laps, best: GP.ST.best})'))
    sp.screenshot(path=str(OUT / 'screen1.png'))
    sp.click('#bEdit'); sp.wait_for_timeout(300)
    for t, (wx, wy) in [('sand', (480, 580)), ('water', (100, 240)), ('cone', (640, 572)), ('cone', (420, 86)), ('hill', (650, 180))]:
        sp.click(f'[data-tool="{t}"]')
        x, y = sp.evaluate(f"""(() => {{ const [sx, sy] = GP.toStage({wx}, {wy}), r = document.getElementById('cv').getBoundingClientRect(), L = r.width / 420; return [r.left + sx * L, r.top + sy * L]; }})()""")
        sp.mouse.click(x, y); sp.wait_for_timeout(120)
    sp.click('[data-tool="cone"]'); sp.wait_for_timeout(200)
    sp.screenshot(path=str(OUT / 'screen2.png'))
    sp.click('#eCancel'); sp.wait_for_timeout(500)
    sp.click('#bRace'); sp.wait_for_timeout(4800)
    sp.keyboard.down('ArrowUp'); sp.wait_for_timeout(2600)
    sp.screenshot(path=str(OUT / 'screen3.png'))
    sp.keyboard.up('ArrowUp')
    b.close()
for n in (1, 2, 3):
    f = OUT / f'screen{n}.png'; Image.open(f).save(OUT / f'screen{n}.webp', quality=84); f.unlink()
print('done', sorted(x.name for x in OUT.iterdir()))
