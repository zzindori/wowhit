# 홈페이지 카드용 그림 만들기(헤드리스): 오목·층층이 아이콘(512px png), 오목 화면 캡처(390×844 webp)
# 아이콘은 SVG 코드로 그림 — 고치면 이 스크립트를 다시 돌릴 것
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
PUB = ROOT / 'public'

def stones():
    # 대각선 흑 5개(5목) + 백 몇 개, 9×9 줄
    c, m = 56, 32
    P = lambda x, y: (m + x * c, m + y * c)
    out = []
    for x, y in [(2, 1), (6, 3), (1, 5), (3, 7)]:
        X, Y = P(x, y); out.append(f'<circle cx="{X + 4}" cy="{Y + 6}" r="25" fill="rgba(60,30,0,.35)"/><circle cx="{X}" cy="{Y}" r="25" fill="url(#w)"/>')
    pts = [P(i + 2, i + 2) for i in range(5)]
    for X, Y in pts:
        out.append(f'<circle cx="{X + 4}" cy="{Y + 6}" r="25" fill="rgba(60,30,0,.35)"/><circle cx="{X}" cy="{Y}" r="25" fill="url(#b)"/>')
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    line = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#ffd65a" stroke-opacity=".45" stroke-width="40" stroke-linecap="round"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#ffd65a" stroke-width="6" stroke-linecap="round"/>')
    grid = ''.join(f'<path d="M{m} {m + i * c}H{m + 8 * c}M{m + i * c} {m}V{m + 8 * c}"/>' for i in range(9))
    return grid, ''.join(out), line

g, st, line = stones()
OMOK = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
 <linearGradient id="wd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ecc278"/><stop offset=".55" stop-color="#dcaa5c"/><stop offset="1" stop-color="#c58d42"/></linearGradient>
 <radialGradient id="b" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#7a7a7a"/><stop offset=".3" stop-color="#2a2a2a"/><stop offset="1" stop-color="#050505"/></radialGradient>
 <radialGradient id="w" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#ecece6"/><stop offset="1" stop-color="#a9a9a0"/></radialGradient>
</defs>
<rect width="512" height="512" fill="url(#wd)"/>
<g stroke="#a26b2a" stroke-opacity=".18" stroke-width="3" fill="none">
 <path d="M0 70 Q130 50 260 78 T512 64"/><path d="M0 190 Q160 170 300 196 T512 180"/><path d="M0 330 Q140 312 270 340 T512 322"/><path d="M0 450 Q150 432 290 458 T512 440"/>
</g>
<g stroke="#3b2a14" stroke-width="2.4" stroke-opacity=".85" transform="translate(16 16)">{g}</g>
<g transform="translate(16 16)">{line}{st}</g>
</svg>'''

# 층층이: 하늘 + 층마다 다른 가게가 쌓인 상가 건물, 맨 위는 공사 중(크레인), 앞엔 둥실이
FLOORS = [  # (차양 색, 벽 색, 간판 글자)
    ('#d8402f', '#fff4e6', '분식'),
    ('#e8742a', '#fff4e6', '붕어빵'),
    ('#f2b705', '#fffaf0', '치킨'),
    ('#2fae9a', '#f2fbf8', '편의점'),
]
def building():
    x0, w, fh, base = 116, 280, 78, 468
    out = [f'<rect x="{x0 - 14}" y="{base}" width="{w + 28}" height="14" rx="4" fill="#6c7a8a"/>']
    for i, (awn, wall, name) in enumerate(FLOORS):
        y = base - (i + 1) * fh
        out.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{fh}" fill="{wall}" stroke="#38445a" stroke-width="5"/>')
        # 간판
        out.append(f'<rect x="{x0 + 16}" y="{y + 9}" width="{w - 32}" height="24" rx="5" fill="{awn}"/>')
        out.append(f'<text x="{x0 + w / 2}" y="{y + 28.5}" text-anchor="middle" font-family="Jua" font-size="21" fill="#fff">{name}</text>')
        # 줄무늬 차양
        n = 8; sw = (w - 24) / n
        for k in range(n):
            out.append(f'<path d="M{x0 + 12 + k * sw} {y + 38}h{sw}v12a{sw / 2} {sw / 2} 0 0 1 -{sw} 0z" fill="{awn if k % 2 == 0 else "#fff"}" stroke="#38445a" stroke-width="2"/>')
        # 창문 불빛
        for k in range(4):
            out.append(f'<rect x="{x0 + 26 + k * 62}" y="{y + 56}" width="44" height="16" rx="3" fill="#ffe08a" stroke="#38445a" stroke-width="2.5"/>')
    top = base - len(FLOORS) * fh
    # 공사 중 층: 철골 + 줄무늬 띠
    out.append(f'<path d="M{x0} {top}V{top - 58}M{x0 + w} {top}V{top - 58}M{x0 + w / 2} {top}V{top - 58}M{x0} {top - 58}H{x0 + w}M{x0} {top}L{x0 + w / 2} {top - 58}L{x0 + w} {top}" stroke="#f2b705" stroke-width="8" fill="none" stroke-linejoin="round"/>')
    out.append(f'<rect x="{x0 - 6}" y="{top - 8}" width="{w + 12}" height="14" fill="url(#hz)" stroke="#38445a" stroke-width="3"/>')
    # 크레인
    cx = x0 + w - 40
    out.append(f'<path d="M{cx} {top - 58}V40M{cx - 150} 52H{cx + 46}" stroke="#e8742a" stroke-width="12" stroke-linecap="round"/>')
    out.append(f'<path d="M{cx - 120} 52V{top - 92}" stroke="#38445a" stroke-width="3"/>')
    out.append(f'<rect x="{cx - 140}" y="{top - 92}" width="40" height="30" rx="4" fill="#c99a5b" stroke="#38445a" stroke-width="3.5"/>')
    out.append(f'<text x="{cx - 120}" y="{top - 70}" text-anchor="middle" font-family="Jua" font-size="20" fill="#5a3410">층</text>')
    return ''.join(out)

def robot(x, y, s=1):
    # 둥실이: 흰 달걀 몸 + 파란 띠 + 까만 얼굴 화면 속 ^^ 눈
    return f'''<g transform="translate({x} {y}) scale({s})">
 <ellipse cx="0" cy="58" rx="30" ry="7" fill="rgba(30,50,90,.25)"/>
 <ellipse cx="0" cy="44" rx="18" ry="5" fill="#9fe4ff" opacity=".7"/>
 <path d="M0 -46C26 -46 36 -12 36 6C36 30 20 40 0 40C-20 40 -36 30 -36 6C-36 -12 -26 -46 0 -46Z" fill="#fff" stroke="#38445a" stroke-width="5"/>
 <path d="M-35 14C-20 22 20 22 35 14" stroke="#2f7de1" stroke-width="9" fill="none"/>
 <rect x="-24" y="-30" width="48" height="30" rx="13" fill="#1d2433"/>
 <path d="M-15 -12q5 -8 10 0M5 -12q5 -8 10 0" stroke="#7ff3ff" stroke-width="4" fill="none" stroke-linecap="round"/>
 <path d="M-36 0q-14 -4 -16 -18M36 0q14 -4 16 -18" stroke="#38445a" stroke-width="6" fill="none" stroke-linecap="round"/>
</g>'''

STACK = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc8ff"/><stop offset="1" stop-color="#d9f0ff"/></linearGradient>
 <pattern id="hz" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="20" height="20" fill="#f2b705"/><rect width="10" height="20" fill="#2a2a2a"/></pattern>
</defs>
<rect width="512" height="512" fill="url(#sky)"/>
<g fill="#fff" opacity=".85"><ellipse cx="80" cy="96" rx="44" ry="16"/><ellipse cx="112" cy="84" rx="30" ry="16"/><ellipse cx="420" cy="160" rx="38" ry="13"/></g>
<rect x="0" y="476" width="512" height="36" fill="#9aa7b3"/>
{building()}
{robot(84, 410, 1.15)}
</svg>'''

def render(pg, svg, out, size=512):
    pg.set_content(f'<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jua&display=swap">'
                   f'<style>body{{margin:0}}</style></head><body>{svg}</body></html>')
    pg.wait_for_timeout(1200)
    png = pg.locator('svg').screenshot()
    Image.open(BytesIO(png)).convert('RGB').resize((size, size), Image.LANCZOS).save(out)
    print('saved', out)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 600, 'height': 600})
    (PUB / 'apps/omok').mkdir(parents=True, exist_ok=True); (PUB / 'apps/stack').mkdir(parents=True, exist_ok=True)
    render(pg, OMOK, PUB / 'apps/omok/icon.png')
    render(pg, STACK, PUB / 'apps/stack/icon.png')
    # 오목 화면 캡처: 중반 판 + 수 읽기 도움(컴퓨터 열린 3 → 주황 막을 자리)
    sp = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    sp.goto((PUB / 'games/omok/index.html').as_uri()); sp.evaluate('localStorage.clear()')
    moves = [(7, 7), (8, 6), (8, 8), (6, 6), (6, 8), (9, 5), (9, 9), (10, 10), (5, 7), (7, 5), (4, 6), (9, 7), (6, 9), (8, 7)]
    sp.evaluate(f"localStorage.setItem('omok-v1', JSON.stringify({{moves: {[y * 15 + x for x, y in moves]}, me: 1, hint: true}}))")
    sp.reload(); sp.wait_for_timeout(1200)
    print('msg', sp.inner_text('#msg'))
    Image.open(BytesIO(sp.screenshot())).save(PUB / 'apps/omok/screen1.webp', quality=86)
    b.close()
