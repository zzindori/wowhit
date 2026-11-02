#!/usr/bin/env python3
"""jjWay 화면 확인(게이지 방식): 출발 설정 → 걷기·바다 막힘 → 청주공항에 서 있기(돋보기 테두리 차오름) → 움직이면 취소
→ 꽉 차면 탑승 → 끌어서 이륙 → 직항 없는 곳(회색) → 간사이 위를 지나가기(안 내림) → 멈추면 착륙 → 도착 공항에서 다시 안 탐
→ 벗어났다 오면 탑승 → 김해 착륙 → 이륙 후 김해에 다시 내리기(취소) → ✕ 닫으면 다시 안 열림 → 탑승 중 새로고침 → 제주 국내선.
python3 scripts/jjway/ui.py [캡처 폴더]"""
import sys, os, time, threading, http.server, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
PORT = 8771
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()

def at(pg, code, dx=0):
    pg.evaluate(f'(() => {{ const a = AIR.find(a => a.code === "{code}"); P.x = a.x + {dx}; P.y = a.y; P.vx = P.vy = 0; P.trail = []; }})()')

def wait(pg, js, sec=6):
    t = time.time()
    while time.time() - t < sec:
        if pg.evaluate(js): return True
        time.sleep(.08)
    raise AssertionError(f'시간 초과: {js} / mode={pg.evaluate("S.mode")} g={pg.evaluate("P.g")} loc={pg.inner_text("#loc")}')

def swipe_down(pg):
    bx = pg.locator('#sheet .grab').bounding_box(); x, y = bx['x'] + bx['width'] / 2, bx['y'] + 2
    pg.mouse.move(x, y); pg.mouse.down(); pg.mouse.move(x, y + 50, steps=4); pg.mouse.move(x, y + 110, steps=4); pg.mouse.up(); time.sleep(.4)

def hold(pg, key, sec):
    pg.keyboard.down(key); time.sleep(sec); pg.keyboard.up(key)

def run(w, h, tag):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html')
        pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0')
        pg.fill('#mems .mem:nth-child(3) input', '첫째'); pg.click('#goBtn'); time.sleep(.3)
        x0 = pg.evaluate('P.x'); hold(pg, 'ArrowRight', 1); assert pg.evaluate('P.x') > x0 + 30
        pg.evaluate('(() => { P.x = -250; P.y = -110; })()'); hold(pg, 'ArrowRight', 3)
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '동해로 나감'
        at(pg, 'CJJ', 3); time.sleep(.8)
        g1 = pg.evaluate('P.g'); assert .3 < g1 < 1 and pg.evaluate('S.mode') == 'walk', g1
        assert '탑승까지' in pg.inner_text('#pipTxt')
        pg.screenshot(path=f'{OUT}/jj_{tag}_1gauge.png')
        hold(pg, 'ArrowUp', .25); at(pg, 'CJJ', 3)
        assert pg.evaluate('P.g') < g1 and pg.evaluate('S.mode') == 'walk', '움직여도 안 줄어듦'
        wait(pg, 'S.mode === "ground"', 3)
        assert '탑승 취소' in pg.inner_text('#sheet')
        swipe_down(pg); assert not pg.is_visible('#sheet') and pg.evaluate('S.mode') == 'ground'
        pg.click('#pip'); time.sleep(.2); assert pg.is_visible('#sheet .cbtn'), '탑승 창 다시 안 열림'
        # 탑승 취소 → 걷기, 바로 다시 안 참 → 벗어났다 와서 다시 탑승
        pg.click('#sheet .cbtn'); wait(pg, 'S.mode === "walk"', 1)
        time.sleep(2); assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('P.g') == 0, '취소 뒤 바로 다시 탐'
        at(pg, 'CJJ', 40); time.sleep(.2); at(pg, 'CJJ', 3); wait(pg, 'S.mode === "ground"', 3)
        time.sleep(1.5); assert pg.evaluate('S.mode') == 'ground', '가만히 있는데 이륙함'
        hold(pg, 'ArrowRight', .3); wait(pg, 'S.mode === "takeoff"', 1)
        wait(pg, 'S.mode === "plane"', 4)
        time.sleep(.4); assert pg.evaluate('P.g') == 0, '출발 공항 착륙 게이지가 바로 참'
        at(pg, 'MYJ'); time.sleep(.6)
        assert pg.evaluate('P.bad && P.bad.code') == 'MYJ' and pg.evaluate('P.g') == 0 and '직항이 없어요' in pg.inner_text('#toast')
        at(pg, 'KIX', -30); hold(pg, 'ArrowRight', .5)
        assert pg.evaluate('S.mode') == 'plane', '지나가다 내림'
        at(pg, 'KIX', 8); wait(pg, 'P.g > .3 && P.gKind === "land"', 2)
        assert '착륙' in pg.inner_text('#pipTxt')
        pg.screenshot(path=f'{OUT}/jj_{tag}_2land_gauge.png')
        wait(pg, 'S.mode === "landing"', 2); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 4)
        assert 'KIX' in pg.evaluate('Object.keys(S.stamps)')
        time.sleep(2.2); assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('P.g') == 0, '내린 공항에서 바로 탐'
        # 착륙 취소 → 다시 이륙(도장도 되돌림, 출발지 청주 그대로) → 간사이 다시 물어보지 않다가 멀어졌다 오면 착륙
        assert '착륙 취소' in pg.inner_text('#sheet')
        pg.click('#sheet .cbtn'); wait(pg, 'S.mode === "plane"', 4)
        assert pg.evaluate('S.from') == 'CJJ' and 'KIX' not in pg.evaluate('Object.keys(S.stamps)')
        time.sleep(.3); assert pg.evaluate('P.g') == 0, '취소한 공항 게이지가 바로 참'
        at(pg, 'KIX', 150); time.sleep(.3); at(pg, 'KIX', 8); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 6)
        # 걸어서 벗어나면 착륙 취소 사라짐
        hold(pg, 'ArrowUp', .8)
        assert not pg.evaluate('P.lastFrom'), '벗어났는데 착륙 취소 남음'
        assert pg.evaluate('Math.hypot(P.x - AIR.find(a=>a.code==="KIX").x, P.y - AIR.find(a=>a.code==="KIX").y)') > 30
        at(pg, 'KIX'); wait(pg, 'S.mode === "ground"', 3)
        hold(pg, 'ArrowLeft', .3); wait(pg, 'S.mode === "plane"', 4)
        at(pg, 'PUS', 5); wait(pg, 'S.mode === "walk" && S.country === "KOR"', 5)
        at(pg, 'PUS', 30); time.sleep(.2); at(pg, 'PUS', 3)
        wait(pg, 'S.mode === "ground"', 3); hold(pg, 'ArrowRight', .3); wait(pg, 'S.mode === "plane"', 4)
        at(pg, 'PUS', 120); time.sleep(.3); at(pg, 'PUS', 6)
        wait(pg, 'S.mode === "walk" && S.country === "KOR"', 5)
        swipe_down(pg); time.sleep(.4); assert not pg.is_visible('#sheet'), '쓸어내려도 안 닫힘 / 다시 열림'
        pg.click('#pip'); time.sleep(.2); assert pg.is_visible('#sheet') and '김해' in pg.inner_text('#sheet'), '돋보기로 다시 안 열림'
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        at(pg, 'PUS', 30); time.sleep(.2); at(pg, 'PUS'); wait(pg, 'S.mode === "ground"', 3); pg.evaluate('save()')
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'ground' and '탑승 취소' in pg.inner_text('#sheet') and not pg.is_visible('#setup')
        hold(pg, 'ArrowLeft', .3); wait(pg, 'S.mode === "plane"', 4)
        at(pg, 'CJU', 5); wait(pg, 'S.mode === "walk" && Math.hypot(P.x-AIR.find(a=>a.code==="CJU").x, P.y-AIR.find(a=>a.code==="CJU").y) < 1', 6)
        print(tag, 'OK · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
