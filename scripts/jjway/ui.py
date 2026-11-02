#!/usr/bin/env python3
"""jjWay 화면 확인: 출발 설정 → 🚗 서울에서 차(바다 막힘) → 김해공항 탑승 게이지(움직이면 줄어듦) → 탑승 취소(차로) → 다시 탑승 → 이륙
→ 직항 없는 곳 회색 → 다카마쓰 위 지나가기(안 내림) → 멈추면 착륙 → 걷기(도시 확대) · 착륙 취소 → 다시 착륙
→ 리쓰린 공원 도장 → 다카마쓰 도시 창 → 🚗 버튼(축소·명소 숨김·공항 화살표) → 마쓰야마에서 🚶 버튼(확대) → 도고 온천 도장 → 휠 확대·축소
→ 쓸어내려 닫기·돋보기로 다시 열기 → 설정 → 새로고침 이어짐 → 탑승 대기 중 새로고침.
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

def at(pg, js_obj, dx=0, dy=0):
    pg.evaluate(f'(() => {{ const a = {js_obj}; P.x = a.x + {dx}; P.y = a.y + {dy}; P.vx = P.vy = 0; P.trail = []; }})()')
AIRJ = lambda c: f'AIR.find(a => a.code === "{c}")'
CITYJ = lambda c: f'CITY.find(a => a.id === "{c}")'
SPOTJ = lambda k: f'SPOT.find(a => a.ko === "{k}")'

def wait(pg, js, sec=6):
    t = time.time()
    while time.time() - t < sec:
        if pg.evaluate(js): return True
        time.sleep(.08)
    raise AssertionError(f'시간 초과: {js} / mode={pg.evaluate("S.mode")} g={pg.evaluate("P.g")} kind={pg.evaluate("P.gKind")} loc={pg.inner_text("#loc")}')

def hold(pg, key, sec):
    pg.keyboard.down(key); time.sleep(sec); pg.keyboard.up(key)

def swipe_down(pg):
    bx = pg.locator('#sheet .grab').bounding_box(); x, y = bx['x'] + bx['width'] / 2, bx['y'] + 2
    pg.mouse.move(x, y); pg.mouse.down(); pg.mouse.move(x, y + 50, steps=4); pg.mouse.move(x, y + 110, steps=4); pg.mouse.up(); time.sleep(.4)

def run(w, h, tag):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html')
        pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0 && SPOT.length > 0')
        pg.fill('#mems .mem:nth-child(3) input', '첫째'); pg.click('#goBtn'); time.sleep(.3)
        assert pg.evaluate('S.mode') == 'car', '처음이 차가 아님'
        x0 = pg.evaluate('P.x'); hold(pg, 'ArrowRight', 1); assert pg.evaluate('P.x') > x0 + 30
        pg.evaluate('(() => { P.x = -250; P.y = -110; })()'); hold(pg, 'ArrowRight', 2)
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '차가 바다로'
        # 김해: 탑승 게이지 → 움직이면 줄어듦 → 탑승 → 취소하면 차로
        at(pg, AIRJ('PUS'), 3); time.sleep(.8)
        g1 = pg.evaluate('P.g'); assert .3 < g1 < 1 and pg.evaluate('P.gKind') == 'board', g1
        hold(pg, 'ArrowUp', .2); at(pg, AIRJ('PUS'), 3)
        assert pg.evaluate('P.g') < g1
        wait(pg, 'S.mode === "ground"', 3)
        pg.click('#sheet .cbtn'); wait(pg, 'S.mode === "car"', 1)
        at(pg, AIRJ('PUS'), 40); time.sleep(.2); at(pg, AIRJ('PUS'), 3); wait(pg, 'S.mode === "ground"', 3)
        pg.screenshot(path=f'{OUT}/jj_{tag}_1ground.png')
        hold(pg, 'ArrowRight', .3); wait(pg, 'S.mode === "plane"', 4)
        # 직항 없는 곳(김해→고치 없음) 회색
        at(pg, '{x:' + str(0) + ',y:0}')
        at(pg, AIRJ('NGS')); time.sleep(.6)
        assert pg.evaluate('P.bad && P.bad.code') == 'NGS' and pg.evaluate('P.g') == 0
        at(pg, AIRJ('TAK'), -30); hold(pg, 'ArrowRight', .5); assert pg.evaluate('S.mode') == 'plane'
        at(pg, AIRJ('TAK'), 8); wait(pg, 'S.mode === "landing"', 3); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 4)
        # 착륙 취소 → 바로 비행 → 다시 착륙
        pg.click('#sheet .cbtn'); time.sleep(.15); assert pg.evaluate('S.mode') == 'plane' and '비행 중' in pg.inner_text('#loc')
        at(pg, AIRJ('TAK'), 150); time.sleep(.3); at(pg, AIRJ('TAK'), 8); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 6)
        time.sleep(1.2)
        assert pg.evaluate('S.span.walk') <= 80 and pg.evaluate('Math.min(innerWidth, innerHeight) / CAM.z') < 120, '걷기 지도가 확대 안 됨'
        pg.screenshot(path=f'{OUT}/jj_{tag}_2walk.png')
        # 리쓰린 공원 도장 + 도시 창
        at(pg, SPOTJ('리쓰린 공원'), .3); wait(pg, 'S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key]', 2)
        assert '도장' in pg.inner_text('#sheet')
        pg.screenshot(path=f'{OUT}/jj_{tag}_3spot.png')
        at(pg, CITYJ('takamatsu'), -4, 4); time.sleep(.5)
        sh = pg.inner_text('#sheet'); assert '다카마쓰' in sh and '리쓰린 공원' in sh and '사누키 우동' in sh, sh[:200]
        pg.screenshot(path=f'{OUT}/jj_{tag}_4city.png')
        # 🚗 버튼: 지도 축소, 마쓰야마로 → 🚶 버튼: 확대 → 도고 온천
        pg.click('#mCar'); assert pg.evaluate('S.mode') == 'car'; time.sleep(1.5)
        assert pg.evaluate('Math.min(innerWidth, innerHeight) / CAM.z') > 180, '차인데 축소 안 됨'
        pg.screenshot(path=f'{OUT}/jj_{tag}_5car.png')
        at(pg, CITYJ('matsuyama'), -3, 3); time.sleep(.6)
        assert pg.evaluate('S.mode') == 'car', '시내에서 저절로 탐/바뀜'
        assert '마쓰야마' in pg.inner_text('#loc')
        pg.click('#mWalk'); assert pg.evaluate('S.mode') == 'walk'
        at(pg, SPOTJ('도고 온천'), .2); wait(pg, 'S.seen[SPOT.find(a=>a.ko==="도고 온천").key]', 2)
        # 확대·축소
        s0 = pg.evaluate('S.span.walk'); pg.mouse.move(w / 2, h / 3); pg.mouse.wheel(0, 400); time.sleep(.1); assert pg.evaluate('S.span.walk') > s0
        pg.mouse.wheel(0, -400); time.sleep(.1)
        # 쓸어내려 닫기 → 돋보기로 다시
        swipe_down(pg); assert not pg.is_visible('#sheet')
        pg.click('#pip'); time.sleep(.2); assert pg.is_visible('#sheet')
        # 설정·새로고침
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        pg.evaluate('save()'); pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('S.party.length') == 4 and len(pg.evaluate('Object.keys(S.seen)')) >= 2
        # 마쓰야마공항에서 탑승 대기 중 새로고침
        pg.click('#mCar')
        at(pg, AIRJ('MYJ'), 3); wait(pg, 'S.mode === "ground"', 3); pg.evaluate('save()')
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'ground' and '탑승 취소' in pg.inner_text('#sheet')
        print(tag, 'OK · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
