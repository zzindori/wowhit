# 헤드리스로 오목 확인: 금지 수·5목 판정, 컴퓨터끼리 N판(난이도별 승률·한 수 생각 시간), 화면 눌러 두기·무르기.
# 캡처는 scripts/omok/out/
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[2] / 'public/games/omok/index.html'
OUT = Path(__file__).resolve().parent / 'out'; OUT.mkdir(exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
RULES = """(() => {
  const O = OM, bad = [];
  const P = s => s.map(([x, y]) => O.at(x, y));
  const board = (bl, wh = []) => { O.B.fill(0); P(bl).forEach(p => O.B[p] = 1); P(wh).forEach(p => O.B[p] = 2); };
  const t = (name, got, want) => { if (got !== want) bad.push(name + ' got ' + got); };
  // 쌍삼: 가로 (5,7)(6,7) + 세로 (7,5)(7,6) → (7,7)
  O.setRule('kr'); board([[5,7],[6,7],[7,5],[7,6]]);
  t('kr 33', O.forbidden(O.B, O.at(7,7), 1), true);
  t('kr 33 white too', O.forbidden(O.B, O.at(7,7), 2), false);   // 흰 돌 자리가 아님(흑 모양) → 백이 두면 3 아님
  board([], [[5,7],[6,7],[7,5],[7,6]]); t('kr 33 white', O.forbidden(O.B, O.at(7,7), 2), true);
  // 한쪽이 막힌 3은 열린 3 아님 → 쌍삼 아님
  board([[5,7],[6,7],[7,5],[7,6]], [[4,7]]); t('kr blocked3', O.forbidden(O.B, O.at(7,7), 1), false);
  // 띈 3(●●_● 모양)도 열린 3: 가로 (4,7)(5,7) + (7,7) 빈칸 (6,7)…  → (7,7)에 둬서 ●●_● + 세로 3
  board([[4,7],[5,7],[7,5],[7,6]]); t('kr split3', O.forbidden(O.B, O.at(7,7), 1), true);
  // 4-4는 쌍삼 금지 규칙에선 허용, 렌주 흑은 금지
  board([[4,7],[5,7],[6,7],[7,4],[7,5],[7,6]], [[3,7],[7,3]]);
  t('kr 44 ok', O.forbidden(O.B, O.at(7,7), 1), false);
  O.setRule('renju'); t('renju 44', O.forbidden(O.B, O.at(7,7), 1), true);
  t('renju white 44 ok', (board([], [[4,7],[5,7],[6,7],[7,4],[7,5],[7,6]]), O.forbidden(O.B, O.at(7,7), 2)), false);
  // 장목: 흑 6 → 렌주 금지, 쌍삼 금지 규칙에선 5 이상 이김
  board([[2,7],[3,7],[4,7],[6,7],[7,7]]);
  t('renju overline', O.forbidden(O.B, O.at(5,7), 1), true);
  O.B[O.at(5,7)] = 1; t('renju six no win', O.isFive(O.B, 5, 7, 1), false);
  O.setRule('kr'); t('kr six win', O.isFive(O.B, 5, 7, 1), true);
  // 5가 되면 쌍삼이어도 금지 아님
  board([[3,7],[4,7],[5,7],[6,7],[8,5],[9,4]]); O.setRule('kr');
  t('five beats 33', O.forbidden(O.B, O.at(7,7), 1), false);
  // 자유 규칙은 금지 없음
  O.setRule('free'); board([[5,7],[6,7],[7,5],[7,6]]); t('free', O.forbidden(O.B, O.at(7,7), 1), false);
  // 컴퓨터: 내 4는 꼭 막고, 자기 5는 꼭 둠
  O.setRule('kr'); board([[3,3],[4,3],[5,3],[6,3]], [[9,9],[10,10]]);
  const m1 = O.think(O.B, 2, 'easy'); t('block four', m1.p === O.at(7,3) || m1.p === O.at(2,3), true);
  board([[3,3],[4,3],[5,3]], [[9,9],[10,9],[11,9],[12,9]]);
  t('take five', [O.at(8,9), O.at(13,9)].includes(O.think(O.B, 2, 'easy').p), true);
  // 열린 3은 보통부터 꼭 막음
  board([[5,5],[6,5],[7,5]], [[9,9]]);
  t('block open3', [O.at(4,5), O.at(8,5), O.at(3,5), O.at(9,5)].includes(O.think(O.B, 2, 'normal').p), true);
  // 연속 4(VCF): 흑이 4-4로 이기는 길
  board([[5,7],[6,7],[7,7],[8,4],[8,5],[8,6]], [[4,7],[8,3],[1,1],[13,13],[1,13],[13,1]]);
  const v = O.vcf(O.B, 1); t('vcf 44', v, O.at(8,7));
  O.B.fill(0); O.setRule(O.store.grule);
  return bad;
})()"""
GAME = """((bl, wl, rule) => {
  OM.setRule(rule); const B = OM.B; B.fill(0);
  let c = 1, n = 0, maxT = 0, win = 0;
  while (n < 225) {
    const t0 = performance.now(); const m = OM.think(B, c, c === 1 ? bl : wl); const dt = performance.now() - t0; maxT = Math.max(maxT, dt);
    if (!m) break;
    if (B[m.p] || OM.forbidden(B, m.p, c)) return {err: 'bad move ' + m.p + ' c' + c};
    B[m.p] = c; n++;
    const [x, y] = OM.XY(m.p);
    if (OM.isFive(B, x, y, c)) { win = c; break; }
    c = 3 - c;
  }
  B.fill(0);
  return {win, n, maxT: Math.round(maxT)};
})"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(ROOT.as_uri()); pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(600)
    print('rules bad', pg.evaluate(RULES))
    for rule in ['kr', 'renju']:
        for bl, wl in [('hard', 'easy'), ('easy', 'hard'), ('hard', 'normal'), ('normal', 'hard'), ('normal', 'easy'), ('hard', 'hard')]:
            rs = [pg.evaluate(GAME + f"('{bl}','{wl}','{rule}')") for _ in range(N)]
            bad = [r for r in rs if 'err' in r]
            print(rule, f'흑 {bl} vs 백 {wl}', '흑승', sum(r.get('win') == 1 for r in rs), '백승', sum(r.get('win') == 2 for r in rs),
                  '무', sum(r.get('win') == 0 for r in rs), '평균수', round(sum(r.get('n', 0) for r in rs) / N), '최대ms', max(r.get('maxT', 0) for r in rs), bad[:2])
    # 화면 눌러 두기: 판 가운데부터 몇 수, 무르기, 캡처
    pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(500)
    box = pg.evaluate("(() => { const r = document.getElementById('cv').getBoundingClientRect(); return [r.left, r.top, r.width / OM.LY.W]; })()")
    def tap(x, y):
        X, Y = pg.evaluate(f'OM.px(OM.at({x},{y}))')
        pg.mouse.move(box[0] + X * box[2], box[1] + Y * box[2]); pg.mouse.down(); pg.mouse.up()
        pg.wait_for_function('!OM.thinking && (OM.turn === OM.store.me || OM.store.over)', timeout=20000)
    for x, y in [(7, 7), (8, 8), (6, 8), (8, 6), (9, 9)]:
        if pg.evaluate('OM.store.over'): break
        if pg.evaluate(f'OM.B[OM.at({x},{y})]'): continue
        tap(x, y)
    n0 = pg.evaluate('OM.store.moves.length'); pg.screenshot(path=str(OUT / 'port_play.png'))
    pg.click('#bUndo'); pg.wait_for_timeout(300); n1 = pg.evaluate('OM.store.moves.length')
    print('ui moves', n0, 'after undo', n1, 'turn me', pg.evaluate('OM.turn === OM.store.me'))
    pg.click('#bTip'); pg.wait_for_timeout(300); pg.screenshot(path=str(OUT / 'port_tip.png'))
    print('msg', pg.inner_text('#msg'))
    # 백으로 시작 → 컴퓨터가 먼저 둠
    pg.evaluate("OM.store.side = 'white'; OM.store.moves = []; OM.newGame()"); pg.wait_for_function('OM.store.moves.length === 1', timeout=5000)
    print('white start ai first', pg.evaluate('OM.store.moves'), 'me', pg.evaluate('OM.store.me'))
    lp = b.new_page(viewport={'width': 1366, 'height': 768})
    lp.on('pageerror', lambda e: errs.append(str(e)))
    lp.goto(ROOT.as_uri()); lp.wait_for_timeout(500); lp.screenshot(path=str(OUT / 'land.png'))
    print('errors', errs[:3])
    b.close()
