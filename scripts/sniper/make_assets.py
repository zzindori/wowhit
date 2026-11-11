# 홈페이지 카드용 그림(헤드리스): 아이콘(512px png, SVG 코드) + 화면 캡처 4장(1280×720 webp: 처음 화면·조준경 명중·사거리 카드·총알 카메라)
# public을 http://127.0.0.1:8777 로 띄워 둔 상태에서: python3 scripts/sniper/make_assets.py
# 헤드리스엔 GPU가 없어 그리기가 아주 느림(초당 1~2장) — 기다리는 시간을 넉넉히, 소리는 끔(오디오 장치 없으면 막힘)
from pathlib import Path
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/apps/sniper'; OUT.mkdir(parents=True, exist_ok=True)
URL = 'http://127.0.0.1:8777/games/sniper/'

ticks = ''.join(f'<line x1="{256-L}" y1="{256+m*15}" x2="{256+L}" y2="{256+m*15}"/><line x1="{256+m*15}" y1="{256-L}" x2="{256+m*15}" y2="{256+L}"/><line x1="{256-L}" y1="{256-m*15}" x2="{256+L}" y2="{256-m*15}"/><line x1="{256-m*15}" y1="{256-L}" x2="{256-m*15}" y2="{256+L}"/>'
                for m in range(1, 9) for L in [6 if m % 2 == 0 else 4])
ICON = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f78a8"/><stop offset=".55" stop-color="#e9a86d"/><stop offset=".62" stop-color="#f6c48c"/></linearGradient>
 <radialGradient id="vig" cx=".5" cy=".5" r=".5"><stop offset=".72" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>
 <clipPath id="c"><circle cx="256" cy="256" r="214"/></clipPath>
</defs>
<rect width="512" height="512" rx="0" fill="#0b0f14"/>
<g clip-path="url(#c)">
 <rect width="512" height="512" fill="url(#sky)"/>
 <path d="M0 330 L70 250 L130 300 L200 230 L262 296 L330 222 L400 288 L460 246 L512 290 L512 512 L0 512Z" fill="#7a8796"/>
 <path d="M0 360 C120 330 200 345 256 338 S 420 330 512 352 L512 512 L0 512Z" fill="#8e9a4a"/>
 <path d="M0 400 C150 380 330 392 512 384 L512 512 L0 512Z" fill="#b79a5c"/>
 <g fill="#3f5a2a"><path d="M40 360 l14 -48 l14 48z"/><path d="M80 356 l11 -38 l11 38z"/><path d="M420 352 l14 -50 l14 50z"/><path d="M455 356 l10 -36 l10 36z"/></g>
 <rect x="250" y="262" width="12" height="48" fill="#6b5a44"/><rect x="226" y="262" width="60" height="7" fill="#6b5a44"/>
 <circle cx="256" cy="286" r="20" fill="#f2f0ea"/><circle cx="256" cy="286" r="7" fill="#ff6a1a"/>
 <circle cx="256" cy="256" r="214" fill="url(#vig)"/>
 <g stroke="#0a0a0a" stroke-width="3"><line x1="0" y1="256" x2="512" y2="256"/><line x1="256" y1="0" x2="256" y2="512"/></g>
 <g stroke="#0a0a0a" stroke-width="2.4">{ticks}</g>
 <g stroke="#0a0a0a" stroke-width="10"><line x1="0" y1="256" x2="106" y2="256"/><line x1="406" y1="256" x2="512" y2="256"/><line x1="256" y1="406" x2="256" y2="512"/><line x1="256" y1="0" x2="256" y2="106"/></g>
 <circle cx="256" cy="256" r="4.5" fill="#ff2a1e"/>
</g>
<circle cx="256" cy="256" r="216" fill="none" stroke="#1b1f24" stroke-width="10"/>
<circle cx="256" cy="256" r="230" fill="none" stroke="#ffb547" stroke-width="5" stroke-dasharray="70 26" opacity=".85"/>
</svg>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 512, 'height': 512})
    pg.set_content(f'<html><body style="margin:0">{ICON}</body></html>')
    Image.open(BytesIO(pg.screenshot())).save(OUT / 'icon.png')
    pg.close()

    ctx = b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True, is_mobile=True, device_scale_factor=1)
    pg = ctx.new_page(); pg.add_init_script('window.AudioContext=undefined; window.webkitAudioContext=undefined;')
    def shot(name, wait=6000):
        pg.wait_for_timeout(wait)
        Image.open(BytesIO(pg.screenshot())).convert('RGB').save(OUT / f'{name}.webp', quality=82)
    solve = """(si, ti)=>{const L=LS; const t=L.TG[ti];
      const c=L.tgPos(t,L.S.t); const yaw=Math.atan2(-(c.x-L.EYE.x),-(c.z-L.EYE.z)),pit=Math.atan2(c.y-L.EYE.y,Math.hypot(c.x-L.EYE.x,c.z-L.EYE.z));
      const D=L.DOPE.reduce((a,b)=>Math.abs(b.R-t.dist)<Math.abs(a.R-t.dist)?b:a); const hits=[];
      for(let e=D.drop-2;e<=D.drop+2;e+=0.1) for(let w=-4;w<=4;w+=0.1){const s=L.dryShot(yaw,pit,Math.round(e*10)/10,Math.round(w*10)/10,L.S.t+0.1); if(s.hit&&s.hit.tg===t) hits.push([e,w]);}
      const me=hits.reduce((a,b)=>a+b[0],0)/hits.length, mw=hits.reduce((a,b)=>a+b[1],0)/hits.length;
      L.S.elev=Math.round(me*10)/10; L.S.windT=Math.round(mw*10)/10; L.S.yaw=yaw; L.S.pitch=pit; L.S.recoil=0; L.S.recoilY=0; }"""
    pg.goto(URL); shot('screen1', 7000)                                   # 처음 화면
    pg.evaluate("LS.startStage(4); LS.S.test=true; LS.S.scoped=true; LS.S.zoom=16")
    pg.evaluate(f"({solve})(4,1)")
    pg.evaluate("LS.fire()")                                              # 가운데 풍선 — 명중 뒤 스포터
    pg.wait_for_function("document.getElementById('spot').classList.contains('on')", timeout=300000)
    pg.evaluate("LS.S.bolt=0; LS.S.recoil=0"); shot('screen2', 2500)
    pg.evaluate("LS.startStage(5); LS.S.test=true; LS.S.scoped=true; LS.S.zoom=12; LS.aimAt(LS.TG[0], 0, 0); document.getElementById('menuB').dispatchEvent(new PointerEvent('pointerdown', {bubbles:true}))")
    pg.click('#pCard'); shot('screen3', 4000)                             # 사거리 카드
    pg.click('#card [data-back]')
    pg.evaluate("LS.startStage(9); LS.S.test=true; LS.S.scoped=true; LS.S.zoom=25")
    pg.evaluate(f"({solve})(9,0)")
    pg.evaluate("LS.fire()")
    pg.wait_for_function("LS.S.bcam && LS.S.t - LS.S.bcam.shot.t0 > 0.55", timeout=600000)
    pg.evaluate("LS.S.timeScale = 0"); shot('screen4', 3000)              # 총알 카메라(멈춰 찍음)
    b.close()
print('ok', sorted(x.name for x in OUT.iterdir()))
