# 헤드리스로 맞고를 자동으로 여러 판 돌려서 오류·카드 수(48장)·바닥 자리 겹침 확인.
# 사람 차례는 무작위 손패, 고/흔들기 대화창은 무작위 버튼. 기다리는 시간은 1/25로.
import sys, random
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2] / 'public/games/gostop'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
html = (ROOT / 'index.html').read_text().replace(
    'const sleep = ms => new Promise(r => setTimeout(r, ms));',
    'const sleep = ms => new Promise(r => setTimeout(r, ms / 25));')
tmp = ROOT / '_sim.html'; tmp.write_text(html)
CHECK = """(() => { if (!G) return null;
  const all = [...G.deck, ...G.hand[0], ...G.hand[1], ...G.floor, ...G.cap[0], ...G.cap[1]];
  const bad = [];
  if (all.length !== 48 || new Set(all).size !== 48) bad.push('cards ' + all.length + '/' + new Set(all).size);
  const ms = [...new Set(G.floor.map(id => C[id].m))], sl = ms.map(m => G.slot[m]);
  if (new Set(sl).size !== sl.length || sl.some(s => s == null)) bad.push('slot ' + JSON.stringify(G.slot));
  return bad.join(';'); })()"""
try:
  with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("window.__ban={}; addEventListener('DOMContentLoaded',()=>{const b=document.getElementById('banner');new MutationObserver(()=>{const t=b.textContent;window.__ban[t]=(window.__ban[t]||0)+1}).observe(b,{childList:true,characterData:true,subtree:true})})")
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(300)
    rounds, bads, ev = 0, set(), {}
    for step in range(20000):
        r = pg.evaluate(CHECK)
        if r: bads.add(r)
        st = pg.evaluate("""(() => {
          const vis = id => !document.getElementById(id).hidden;
          if (vis('result')) return 'result';
          if (vis('ask')) return 'ask';
          if (G && G.wait) return G.wait.kind; return 'busy'; })()""")
        if st == 'result':
            rounds += 1
            t = pg.evaluate("document.getElementById('resT').textContent")
            ev[t.split(' ')[0]] = ev.get(t.split(' ')[0], 0) + 1
            if rounds >= N: break
            pg.click('#bNext')
        elif st == 'ask':
            bs = pg.query_selector_all('#askB button'); random.choice(bs).click()
        elif st == 'hand':
            pg.evaluate("(() => { const h = G.hand[0]; onCard(G.bombFlip[0] && Math.random() < .5 ? G.deck[G.deck.length-1] : h[Math.random()*h.length|0]); })()")
        elif st == 'floor':
            pg.evaluate("onCard(G.wait.opts[Math.random()*2|0])")
        pg.wait_for_timeout(15)
    print('rounds', rounds, ev); print('errors', errs[:5]); print('invariant', list(bads)[:5])
    print('banners', pg.evaluate('JSON.stringify(window.__ban)')); print('store', pg.evaluate("JSON.stringify(store)"))
    b.close()
finally:
    tmp.unlink()
