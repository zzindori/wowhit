# 홈페이지 카드용 그림(헤드리스): 아이콘(512px png, SVG 코드) + 화면 캡처 4장(390×844 webp)
# python3 scripts/jjway/make_assets.py  (public을 직접 띄움, 지리원 타일은 인터넷에서)
import os, time, threading, http.server, functools
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/apps/jjway'; OUT.mkdir(parents=True, exist_ok=True)
PORT = 8772
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Q, directory=str(ROOT / 'public')))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{PORT}/games/jjway/index.html'

# 아이콘: 바다 위 초록 섬 + 점선 비행 길 + 작은 비행기 + 게임과 같은 동그란 마커 핀(분홍 테두리·♥)
ICON = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc8e8"/><stop offset="1" stop-color="#3a8fc4"/></linearGradient></defs>
<rect width="512" height="512" fill="url(#sea)"/>
<g fill="#ffffff" opacity=".18"><path d="M40 120 q20 -10 40 0 t40 0" stroke="#fff" stroke-width="5" fill="none"/><path d="M380 440 q20 -10 40 0 t40 0" stroke="#fff" stroke-width="5" fill="none"/></g>
<path d="M120 400 C 150 330, 230 300, 300 318 C 360 332, 420 300, 450 340 C 470 380, 430 440, 360 450 C 280 462, 200 470, 150 450 C 120 438, 108 420, 120 400 Z" fill="#9fd37a" stroke="#5f9e45" stroke-width="8"/>
<path d="M200 420 C 230 400, 270 395, 300 410" stroke="#5f9e45" stroke-width="5" fill="none" stroke-dasharray="2 12" stroke-linecap="round"/>
<path d="M70 300 C 120 160, 250 90, 360 110" stroke="#fff" stroke-width="8" fill="none" stroke-dasharray="4 18" stroke-linecap="round"/>
<g transform="translate(392 112) rotate(12) scale(3.1)">
 <path d="M14 0 L4 -2 L-2 -12 L-6 -12 L-3 -2 L-10 -1.5 L-13 -6 L-15 -6 L-14 0 L-15 6 L-13 6 L-10 1.5 L-3 2 L-6 12 L-2 12 L4 2 Z" fill="#eef3f8" stroke="#4a6378" stroke-width="1.2" stroke-linejoin="round"/>
</g>
<g transform="translate(300 300)">
 <ellipse cx="0" cy="62" rx="26" ry="8" fill="#000" opacity=".22"/>
 <path d="M-30 -40 L0 60 L30 -40 Z" fill="#e05a8a" stroke="#fff" stroke-width="7" stroke-linejoin="round"/>
 <circle cx="0" cy="-70" r="66" fill="#fff" stroke="#e05a8a" stroke-width="12"/>
 <text x="0" y="-46" text-anchor="middle" font-size="68">🏯</text>
 <circle cx="46" cy="-118" r="26" fill="#e05a8a" stroke="#fff" stroke-width="6"/>
 <text x="46" y="-107" text-anchor="middle" font-size="30" fill="#fff" font-family="sans-serif" font-weight="bold">♥</text>
</g>
</svg>'''

def at(pg, js, dx=0, dy=0):
    pg.evaluate(f'(() => {{ const a = {js}; P.x = a.x + {dx}; P.y = a.y + {dy}; P.vx = P.vy = 0; P.trail = []; }})()')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 600, 'height': 600})
    pg.set_content(f'<html><body style="margin:0">{ICON}</body></html>'); pg.wait_for_timeout(600)
    Image.open(BytesIO(pg.locator('svg').screenshot())).convert('RGB').resize((512, 512), Image.LANCZOS).save(OUT / 'icon.png')
    sp = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    errs = []; sp.on('pageerror', lambda e: errs.append(str(e)))
    sp.goto(URL); sp.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0 && SPOT.length > 0')
    # 1 출발 설정
    sp.fill('#mems .mem:nth-child(1) input', '아빠'); sp.fill('#mems .mem:nth-child(2) input', '엄마')
    sp.fill('#mems .mem:nth-child(3) input', '첫째'); sp.fill('#mems .mem:nth-child(4) input', '둘째')
    sp.wait_for_timeout(300); sp.screenshot(path=str(OUT / 'screen1.png'))
    sp.click('#goBtn'); sp.wait_for_timeout(400)
    # 2 비행 중(인천 → 다카마쓰 방향, 직항 점선)
    at(sp, 'AIR.find(a => a.code === "ICN")', 30); sp.evaluate('S.span.walk = 40'); sp.wait_for_timeout(900)
    at(sp, 'AIR.find(a => a.code === "ICN")', 1); sp.wait_for_function('S.mode === "ground"', timeout=5000)
    sp.keyboard.down('ArrowDown'); sp.keyboard.down('ArrowRight'); sp.wait_for_timeout(2600)
    sp.keyboard.up('ArrowDown'); sp.keyboard.up('ArrowRight')
    sp.evaluate('(() => { const t = AIR.find(a => a.code === "TAK"); P.x = t.x - 260; P.y = t.y - 120; })()')
    sp.keyboard.down('ArrowRight'); sp.wait_for_timeout(700); sp.screenshot(path=str(OUT / 'screen2.png')); sp.keyboard.up('ArrowRight')
    # 3 다카마쓰 리쓰린 공원 위에 서서 최대 확대(지리원 타일 + 고리 차서 가고 싶어요 + 카드)
    sp.evaluate('(() => { S.mode = "walk"; S.country = "JPN"; S.from = null; S.span.walk = 2.5; })()')
    at(sp, 'SPOT.find(a => a.ko.includes("리쓰린"))', 0, 0); sp.wait_for_timeout(5000)
    sp.screenshot(path=str(OUT / 'screen3.png'))
    # 4 나의 여행 기록
    sp.click('#pts'); sp.wait_for_timeout(600); sp.screenshot(path=str(OUT / 'screen4.png'))
    print('errors', errs, sp.evaluate('S.mode'))
    b.close()
for n in (1, 2, 3, 4):
    f = OUT / f'screen{n}.png'; Image.open(f).save(OUT / f'screen{n}.webp', quality=84); f.unlink()
print('done', sorted(x.name for x in OUT.iterdir()))
