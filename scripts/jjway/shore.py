#!/usr/bin/env python3
"""호수·바다 한가운데 좌표(위키데이터의 호수 중심 등)는 최대 확대에서 걸어서 못 닿음 → 게임의 물 판정(fineWater, 국토지리원)으로 가장 가까운 물가 땅으로 옮김.
결과 cache_shore.json('도시id:일본어' → lat, lon, km) → build_places.py write가 씀. 기존 시코쿠 명소는 건드리지 않음."""
import json, os, http.server, functools, threading
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '../../public'); OUT = os.path.join(HERE, 'cache_shore.json'); PORT = 8773
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Q, directory=ROOT)); threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = r"""async (limit) => {
  const fw = async (x, y) => { for (let i = 0; i < 200; i++) { const w = fineWater(x, y); if (w !== null) return w; await new Promise(r => setTimeout(r, 60)); } return null; };
  const out = [];
  for (const c of PL.cities) { if (c.region === 'shikoku' && !window.__all) { if (c.id !== 'shodoshima' && c.id !== 'ozu' && c.id !== 'shimanto' && c.id !== 'muroto') continue; }
    for (const s of c.spots) {
      const p = proj(s.lon, s.lat), w = await fw(p.x, p.y);
      if (w === null) { out.push({ k: c.id + ':' + s.ja, fail: 1 }); continue; }
      if (!w) continue;
      let hit = null;
      for (let r = .04; r < 30 && !hit; r *= 1.2) for (let a = 0; a < 16 && !hit; a++) { const x = p.x + Math.cos(a * .3927) * r, y = p.y + Math.sin(a * .3927) * r; if (await fw(x, y) === 0) hit = { x, y, r }; }
      if (hit) { const u = unproj(hit.x, hit.y); out.push({ k: c.id + ':' + s.ja, ko: s.ko, lat: u.lat, lon: u.lon, km: +hit.r.toFixed(2) }); }
      else out.push({ k: c.id + ':' + s.ja, ko: s.ko, none: 1 });
    }
  }
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.set_default_timeout(0)
    pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html'); pg.wait_for_function('typeof SPOT !== "undefined" && SPOT.length > 0')
    r = pg.evaluate(JS, 0); b.close()
json.dump({x['k']: x for x in r if 'lat' in x}, open(OUT, 'w'), ensure_ascii=False, indent=0)
print('옮김', sum('lat' in x for x in r), '· 실패', [x['k'] for x in r if x.get('fail')], '· 못 찾음', [x['k'] for x in r if x.get('none')])
for x in sorted((x for x in r if 'lat' in x), key=lambda x: -x['km']): print(x['ko'], x['km'], 'km')
