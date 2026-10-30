# 3단계 화면 확인(헤드리스): 2단계 뇌(보는 것 24) 불러와 이어 달리기 → 🎓시험(결과표·다시 보기) → 서킷에 점프대·다리·눈 → 학습 → 경주.
# public을 http://127.0.0.1:8766 으로 띄워 둔 상태에서: python3 scripts/ai-gp/ui3.py  (out/brain.json = train.cjs가 남긴 뇌)
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = Path(__file__).resolve().parent / 'out'; OUT.mkdir(exist_ok=True)
URL = 'http://127.0.0.1:8766/games/ai-gp/'
BRAIN = json.loads((OUT / 'brain.json').read_text())

def w2c(pg, x, y):
    return pg.evaluate(f"""(() => {{ const [sx, sy] = GP.toStage({x}, {y}), r = document.getElementById('cv').getBoundingClientRect();
      const L = r.width / (document.getElementById('stage').className === 'land' ? 1280 : 420); return [r.left + sx * L, r.top + sy * L]; }})()""")

def fits(pg):   # 판 밖으로 넘치는 것
    return pg.evaluate("""(() => { const P = document.getElementById('panel').getBoundingClientRect(), C = document.getElementById('ctl').getBoundingClientRect(), S = document.getElementById('stage').getBoundingClientRect();
      const kids = [...document.querySelectorAll('#panel > .card')].filter(e => e.offsetParent).map(e => e.getBoundingClientRect());
      return { panelOver: Math.round(Math.max(0, ...kids.map(k => k.bottom - P.bottom))), ctlRight: Math.round(C.right - S.right) }; })()""")

def run(pg, tag):
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(URL); pg.evaluate('localStorage.clear()')
    pg.evaluate(f"localStorage.setItem('aigp-v2', JSON.stringify({{ circuit: GPCORE.CIRCUITS.main, brain: {json.dumps(BRAIN)}, st: {{ laps: 1, best: 12 }} }}))")
    pg.reload(); pg.wait_for_timeout(1000)
    pg.click('#iGo'); pg.wait_for_timeout(8000)
    print(tag, 'old brain', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best, upd: GP.ST.updates})'), fits(pg))
    pg.click('#bExam'); pg.wait_for_function('GP.EX && GP.EX.res', timeout=20000)
    print(tag, 'exam', pg.evaluate("GP.EX.res.map(r => r.name + ':' + (r.laps >= 2 ? '완주' : Math.round(r.pct * 100) + '%') + ' 사고' + r.crashes).join(' | ')"), pg.inner_text('#xSum').replace('\n', ' / ')[:140], fits(pg))
    pg.wait_for_timeout(3500); pg.screenshot(path=str(OUT / f'{tag}_exam1.png'))
    for i in (3, 4):
        pg.click(f'[data-x="{i}"]'); pg.wait_for_timeout(4500 if i == 4 else 2500); pg.screenshot(path=str(OUT / f'{tag}_exam{i}.png'))
    pg.click('#xExit'); pg.wait_for_timeout(1500)
    print(tag, 'back', pg.evaluate('({mode: GP.mode, track: GP.TR.name, q: GP.queue.length})'))
    # 점프대·다리·눈
    pg.click('#bEdit'); pg.wait_for_timeout(300)
    for t, (x, y) in [('ramp', (420, 580)), ('bridge', (250, 92))]:
        pg.click(f'[data-tool="{t}"]'); cx, cy = w2c(pg, x, y); pg.mouse.click(cx, cy); pg.wait_for_timeout(200)
        print(tag, t, pg.inner_text('#eMsg')[:70])
    pg.click('[data-th="snow"]'); pg.wait_for_timeout(200)
    print(tag, 'edit', pg.evaluate('({r: GP.draft.ramps, b: GP.draft.bridges, th: GP.draft.theme, bad: GP.draftBad, jumps: GP.TR.jumps.length})'), fits(pg))
    pg.screenshot(path=str(OUT / f'{tag}_edit3.png'))
    pg.click('#eDone'); pg.wait_for_timeout(300); pg.click('#kKeep'); pg.wait_for_timeout(25000)
    print(tag, 'snow+jump train', pg.evaluate('({laps: GP.ST.laps, best: GP.ST.best, crashes: GP.ST.crashes, theme: GP.TR.theme})'))
    pg.click('[data-sp="1"]'); pg.wait_for_timeout(2500); pg.screenshot(path=str(OUT / f'{tag}_snow.png')); pg.click('[data-sp="0"]')
    pg.click('#bRace'); pg.wait_for_timeout(300)
    if pg.evaluate('GP.mode') != 'race': print(tag, 'race blocked (AI 완주 없음)'); return errs
    pg.wait_for_timeout(4900)
    pg.keyboard.down('ArrowUp'); pg.wait_for_timeout(3000); pg.screenshot(path=str(OUT / f'{tag}_race3.png')); pg.keyboard.up('ArrowUp')
    print(tag, 'race', pg.evaluate('GP.mode'), pg.inner_text('#rInfo').replace('\n', ' / ')[:80])
    pg.click('#rExit'); pg.wait_for_timeout(500)
    return errs

with sync_playwright() as p:
    b = p.chromium.launch()
    e1 = run(b.new_page(viewport={'width': 1366, 'height': 768}), 'land')
    e2 = run(b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2), 'port')
    print('errors', (e1 + e2)[:5])
    b.close()
