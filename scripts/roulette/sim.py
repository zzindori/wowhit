# 헤드리스로 룰렛 확인: 베팅 자리 판정(세로·가로), 배당 기댓값, 난수 균등, 공이 정해진 칸에 멈추는지,
# 실제 화면을 눌러 N판 돌려 칩 계산이 맞는지. 캡처는 scripts/roulette/out/
import sys, random, json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2] / 'public/games/roulette/index.html'
OUT = Path(__file__).resolve().parent / 'out'; OUT.mkdir(exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
CHECK = """(() => {
  const R = RT, bad = [];
  // 1) 모든 베팅 자리를 화면 좌표로 바꿨다가 다시 판정 → 같은 베팅
  for (const k in R.DEFS) { const d = R.DEFS[k], [x, y] = R.toXY(d.L, d.A), [L, A] = R.toLA(x, y), h = R.hitKey(L, A); if (h !== k) bad.push(k + '->' + h); }
  // 2) 기댓값: 탑라인 -3/38, 나머지 -2/38
  const ev = {};
  for (const k in R.DEFS) { let s = 0; for (let n = 0; n < 38; n++) s += R.payout({[k]: 1}, n).paid; const e = s / 38 - 1;
    const want = R.DEFS[k].type === 'topline' ? -3/38 : -2/38; if (Math.abs(e - want) > 1e-9) bad.push('ev ' + k + ' ' + e); ev[R.DEFS[k].type] = e; }
  // 3) 공이 정해진 칸에 멈춤
  for (let i = 0; i < 400; i++) { const n = i % 38; R.W.rot = Math.random() * 7; const P = R.planSpin(n), b = R.ballAt(P, P.T3);
    const rel = ((b.th - (P.rot0 - 1.15 * P.T3)) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI); const p = Math.round(rel / R.SEG) % 38;
    if (R.ORDER[p] !== n) bad.push('land ' + n + ' got ' + R.ORDER[p]); }
  return {bad: bad.slice(0, 10), nbad: bad.length, defs: Object.keys(R.DEFS).length, ev};
})()"""
RNG = """(() => { const c = new Array(38).fill(0), M = 380000; for (let i = 0; i < M; i++) c[RT.rand38()]++;
  const e = M / 38; return c.reduce((a, x) => a + (x - e) ** 2 / e, 0); })()"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [('port', {'width': 390, 'height': 844}), ('land', {'width': 1366, 'height': 768})]:
        pg = b.new_page(viewport=vp, device_scale_factor=2 if name == 'port' else 1)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(ROOT.as_uri() + '?ts=12'); pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(800)
        print(name, 'check', json.dumps(pg.evaluate(CHECK), ensure_ascii=False))
        if name == 'port': print('rng chi2(df37, 95%<52.2)', round(pg.evaluate(RNG), 1))
        pg.screenshot(path=str(OUT / f'{name}_idle.png'))
        box = pg.evaluate("(() => { const r = document.getElementById('cv').getBoundingClientRect(); return [r.left, r.top, r.width / RT.LY.W]; })()")
        keys = pg.evaluate('Object.keys(RT.DEFS)')
        bad = []
        for i in range(N if name == 'port' else 8):
            pg.wait_for_function('RT.state !== "spin"')
            pg.evaluate("document.querySelectorAll('.chip')[%d].click()" % random.choice([0, 1, 2]))
            for k in random.sample(keys, random.randint(1, 6)):
                x, y = pg.evaluate(f"RT.toXY(RT.DEFS['{k}'].L, RT.DEFS['{k}'].A)")
                pg.mouse.click(box[0] + x * box[2], box[1] + y * box[2])
            spins0 = pg.evaluate("RT.store.spins"); before = pg.evaluate("RT.store.bal"); bets = pg.evaluate('JSON.stringify(RT.bets)')
            stake = pg.evaluate('Object.values(RT.bets).reduce((a,x)=>a+x,0)')
            if not stake: continue
            if i == 1: pg.mouse.move(box[0] + 200 * box[2], box[1] + 500 * box[2])
            pg.click('#spin')
            if i == 0: pg.wait_for_timeout(250); pg.screenshot(path=str(OUT / f'{name}_spin.png'))
            pg.wait_for_function(f"RT.store.spins > {spins0}", timeout=60000)
            if i == 0: pg.wait_for_timeout(120); pg.screenshot(path=str(OUT / f'{name}_pay.png'))
            r = pg.evaluate("""(() => { const n = RT.store.hist[0], b = RT.W.ball;
              const rel = ((b.th - RT.W.rot) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI);
              return {n, vis: RT.lastVis, bal: RT.store.bal}; })()""")
            exp = pg.evaluate(f"RT.payout({bets}, {r['n']}).paid")
            if r['vis'] != r['n'] or r['bal'] != before + exp: bad.append((r, before, exp))
        pg.wait_for_timeout(3000); pg.screenshot(path=str(OUT / f'{name}_after.png'))
        print(name, 'spins bad', bad[:3], 'errors', errs[:3], 'store', pg.evaluate("JSON.stringify({b:RT.store.bal,s:RT.store.spins,h:RT.store.hist.slice(0,10)})"))
    b.close()
