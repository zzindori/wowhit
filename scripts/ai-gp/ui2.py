# 2단계 화면 확인(헤드리스): 학습 → 마우스로 서킷 그리기·언덕·모래·콘 → 지금 뇌로 이어서 → 나 vs AI 경주 끝까지.
# public을 http://127.0.0.1:8766 으로 띄워 둔 상태에서: python3 scripts/ai-gp/ui2.py
import math
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent / 'out'; OUT.mkdir(exist_ok=True)
URL = 'http://127.0.0.1:8766/games/ai-gp/'

def world_to_client(pg, x, y):
    return pg.evaluate(f"""(() => {{ const [sx, sy] = GP.toStage({x}, {y}), r = document.getElementById('cv').getBoundingClientRect();
      const L = r.width / (document.getElementById('stage').className === 'land' ? 1280 : 420); return [r.left + sx * L, r.top + sy * L]; }})()""")

def run(pg, tag):
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(URL); pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(1200)
    pg.click('#iGo'); pg.wait_for_timeout(25000)
    print(tag, 'train', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best})'))
    # 서킷 그리기: 콩 모양을 마우스로
    pg.click('#bEdit'); pg.wait_for_timeout(300)
    pts = []
    for k in range(121):
        a = 2 * math.pi * k / 120
        r = 1 + .18 * math.sin(3 * a)
        pts.append((500 + 360 * r * math.cos(a), 320 + 210 * r * math.sin(a)))
    x, y = world_to_client(pg, *pts[0]); pg.mouse.move(x, y); pg.mouse.down()
    for p in pts[1:]:
        x, y = world_to_client(pg, *p); pg.mouse.move(x, y)
    pg.mouse.up(); pg.wait_for_timeout(500)
    print(tag, 'draw', pg.evaluate('({bad: GP.draftBad, n: GP.draft.pts.length, L: Math.round(GP.TR.L)})'), pg.inner_text('#eMsg')[:60])
    for t, (wx, wy) in [('hill', (860, 320)), ('valley', (500, 110)), ('sand', (500, 530)), ('water', (150, 320)), ('cone', (300, 470)), ('cone', (720, 170))]:
        pg.click(f'[data-tool="{t}"]'); x, y = world_to_client(pg, wx, wy); pg.mouse.click(x, y); pg.wait_for_timeout(150)
    print(tag, 'items', pg.evaluate('({h: GP.draft.hills.length, p: GP.draft.patches.length, c: GP.draft.cones.length, bad: GP.draftBad})'))
    pg.screenshot(path=str(OUT / f'{tag}_edit.png'))
    pg.click('#eDone'); pg.wait_for_timeout(300); pg.click('#kKeep'); pg.wait_for_timeout(20000)
    print(tag, 'new circuit (kept brain)', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best, far: GP.ST.far, mode: GP.mode})'))
    if not pg.evaluate('GP.ST.laps'): pg.wait_for_timeout(20000); print(tag, 'later', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best})'))
    pg.screenshot(path=str(OUT / f'{tag}_newtrack.png'))
    # 경주: 출발 신호 뒤 자동 운전(중심선 따라 방향키) — AI가 먼저 3바퀴 돌면 결과 창
    pg.click('#bRace'); pg.wait_for_timeout(300)
    if pg.evaluate('GP.mode') != 'race':
        print(tag, 'race blocked', pg.inner_text('#toast')); return errs
    pg.wait_for_timeout(4500)
    pg.evaluate("""window._ap = setInterval(() => {
      const RC = GP.RC; if (!RC || !RC.me) return; const T = GP.TR, [x, y, th, v] = RC.me;
      let bi = 0, bd = 1e9; for (let i = 0; i < T.N; i++) { const d = (x - T.cx[i]) ** 2 + (y - T.cy[i]) ** 2; if (d < bd) { bd = d; bi = i; } }
      const j = (bi + 12) % T.N, want = Math.atan2(T.cy[j] - y, T.cx[j] - x); let e = want - th; while (e > Math.PI) e -= 2 * Math.PI; while (e < -Math.PI) e += 2 * Math.PI;
      GP.keys.R = e > .05 ? 1 : 0; GP.keys.L = e < -.05 ? 1 : 0; GP.keys.G = v < 150 ? 1 : 0; GP.keys.B = v > 200 ? 1 : 0; }, 33)""")
    pg.wait_for_timeout(6000); pg.screenshot(path=str(OUT / f'{tag}_race.png'))
    print(tag, 'race', pg.evaluate('({laps: GP.RC && GP.RC.laps, go: GP.RC && GP.RC.go})'), pg.inner_text('#rInfo').replace('\n', ' / ')[:120])
    pg.wait_for_function("!document.getElementById('result').hidden", timeout=120000)
    print(tag, 'result', pg.inner_text('#resT'), '|', pg.inner_text('#resB').replace('\n', ' ')[:160])
    pg.screenshot(path=str(OUT / f'{tag}_result.png'))
    pg.evaluate('clearInterval(window._ap)')
    pg.click('#resBack'); pg.wait_for_timeout(3000)
    print(tag, 'back', pg.evaluate('({mode: GP.mode, q: GP.queue.length, laps: GP.ST.laps})'))
    pg.wait_for_timeout(21000)
    print(tag, 'saved circuit pts', pg.evaluate("(JSON.parse(localStorage.getItem('aigp-v2')||'{}').circuit||{pts:[]}).pts.length"))
    return errs

with sync_playwright() as p:
    b = p.chromium.launch()
    e1 = run(b.new_page(viewport={'width': 1366, 'height': 768}), 'land')
    e2 = run(b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2), 'port')
    print('errors', (e1 + e2)[:5])
    b.close()
