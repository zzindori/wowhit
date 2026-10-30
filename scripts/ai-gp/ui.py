# 헤드리스로 화면 확인: python3 scripts/ai-gp/ui.py [초]  (public을 http://127.0.0.1:8766 으로 띄워 둔 상태에서)
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent / 'out'; OUT.mkdir(exist_ok=True)
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 40
URL = 'http://127.0.0.1:8766/games/ai-gp/'
with sync_playwright() as p:
    b = p.chromium.launch()
    errs = []
    pg = b.new_page(viewport={'width': 1366, 'height': 768})
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(URL); pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(1500)
    pg.screenshot(path=str(OUT / 'intro.png'))
    pg.click('#iGo')
    for t in range(SEC // 10):
        pg.wait_for_timeout(10000)
        print(t * 10 + 10, 's', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best, upd: GP.ST.updates, samples: GP.ST.samples, crashes: GP.ST.crashes, far: GP.ST.far})'))
    pg.screenshot(path=str(OUT / 'land.png'))
    pg.click('[data-sp="1"]'); pg.wait_for_timeout(3000)
    print('x1 queue', pg.evaluate('GP.queue.length'))
    pg.screenshot(path=str(OUT / 'land_x1.png'))
    pg.evaluate("document.getElementById('bHelp').click()"); pg.wait_for_timeout(300); pg.screenshot(path=str(OUT / 'help.png'))
    pg.evaluate("document.getElementById('bHelpClose').click()")
    pg.wait_for_timeout(21000)   # 저장 주기
    saved = pg.evaluate("(localStorage.getItem('aigp-v1')||'').length")
    print('saved bytes', saved)
    pp = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pp.on('pageerror', lambda e: errs.append(str(e)))
    pp.goto(URL); pp.wait_for_timeout(1200); pp.click('#iGo'); pp.wait_for_timeout(8000)
    print('port resumed', pp.evaluate('({laps: GP.ST.laps, best: GP.ST.best, upd: GP.ST.updates})'))
    pp.screenshot(path=str(OUT / 'port.png'))
    print('errors', errs[:5])
    b.close()
