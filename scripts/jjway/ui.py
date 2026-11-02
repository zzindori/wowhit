#!/usr/bin/env python3
"""jjWay 화면 확인: 출발 설정 → 🚗 서울에서 차(바다 막힘) → 김해공항 탑승 게이지(움직이면 줄어듦) → 탑승 취소(차로) → 다시 탑승 → 이륙
→ 직항 없는 곳 회색 → 다카마쓰 위 지나가기(안 내림) → 멈추면 착륙 → 걷기(도시 확대) · 착륙 취소 → 다시 착륙
→ 리쓰린 공원 도장 → 다카마쓰 도시 창 → ⌖ 버튼(자동차 비율·공항 화살표) → 마쓰야마에서 확대 → 도고 온천 도장 → 휠 확대·축소
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

def at(pg, js_obj, dx=0, dy=0):  # dx는 JS 식도 됨
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
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('far()'), '처음이 자동차 비율이 아님'
        x0 = pg.evaluate('P.x'); hold(pg, 'ArrowRight', 1); assert pg.evaluate('P.x') > x0 + 30
        pg.evaluate('(() => { P.x = -250; P.y = -110; })()'); hold(pg, 'ArrowRight', 2)
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '차가 바다로'
        # 김해: 탑승 게이지 → 움직이면 줄어듦 → 탑승 → 취소하면 차로
        at(pg, AIRJ('PUS'), 3); time.sleep(.8)
        g1 = pg.evaluate('P.g'); assert .3 < g1 < 1 and pg.evaluate('P.gKind') == 'board', g1
        hold(pg, 'ArrowUp', .2); at(pg, AIRJ('PUS'), 3)
        assert pg.evaluate('P.g') < g1
        wait(pg, 'S.mode === "ground"', 3)
        pg.click('#sheet .cbtn'); wait(pg, 'S.mode === "walk" && !S.from', 1)
        at(pg, AIRJ('PUS'), 40); time.sleep(.2); at(pg, AIRJ('PUS'), 3); wait(pg, 'S.mode === "ground"', 3)
        pg.screenshot(path=f'{OUT}/jj_{tag}_1ground.png')
        hold(pg, 'ArrowRight', .3); wait(pg, 'S.mode === "plane"', 4)
        # 직항 없는 곳(김해→고치 없음) 회색
        at(pg, '{x:' + str(0) + ',y:0}')
        at(pg, AIRJ('NGS')); time.sleep(.6)
        assert pg.evaluate('P.bad && P.bad.code') == 'NGS' and pg.evaluate('P.g') == 0
        at(pg, AIRJ('TAK'), -30); hold(pg, 'ArrowRight', .5); assert pg.evaluate('S.mode') == 'plane'
        # 실제로 날아서: 다카마쓰 서쪽 250km에서 오른쪽으로 날다가 공항 가까이(화면 약 30px)에서 손 떼면 끌려가 착륙
        pg.evaluate('S.span.plane = 1500'); time.sleep(.5)
        at(pg, AIRJ('TAK'), -250); time.sleep(.3)
        pg.keyboard.down('ArrowRight')
        for _ in range(80):
            if pg.evaluate('AIR.find(a => a.code === "TAK").x - P.x') < 70: break
            time.sleep(.04)
        pg.keyboard.up('ArrowRight')
        wait(pg, 'S.mode === "landing"', 4); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 4)
        # 착륙 취소 → 바로 비행 → 다시 착륙
        pg.click('#sheet .cbtn'); time.sleep(.15); assert pg.evaluate('S.mode') == 'plane' and '비행 중' in pg.inner_text('#loc')
        at(pg, AIRJ('TAK'), 150); time.sleep(.3); at(pg, AIRJ('TAK'), 8); wait(pg, 'S.mode === "walk" && S.country === "JPN"', 6)
        # 최대 확대로 공항 2km 옆에서 멈춰 있어도 탑승 게이지 안 참(공항 아이콘 바로 앞에서만)
        pg.evaluate('S.span.walk = 1.5'); time.sleep(1.2); at(pg, AIRJ('TAK'), 0, 2); pg.evaluate('P.quiet = null'); time.sleep(1.8)
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('P.g') == 0, '확대 걷기인데 공항 근처에서 탐'
        # 휠로 확대 → 사람 그림·명소 핀
        pg.mouse.move(w / 2, h / 3)
        for _ in range(6): pg.mouse.wheel(0, -500); time.sleep(.05)
        time.sleep(1.2)
        assert not pg.evaluate('far()') and pg.evaluate('Math.min(innerWidth, innerHeight) / CAM.z') < 120, '확대 안 됨'
        pg.screenshot(path=f'{OUT}/jj_{tag}_2walk.png')
        # 리쓰린 공원 도장 + 도시 창
        # 덜 확대하면 아이콘에 닿아도 반응 없음(안내만)
        pg.evaluate('S.span.walk = 30'); time.sleep(.6); at(pg, SPOTJ('리쓰린 공원')); time.sleep(.4)
        st = pg.evaluate('({seen: !!S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key], span: S.span.walk, toast: document.getElementById("toast").innerText, onT: P.onSpotT, far: far()})')
        assert not st['seen'] and '더 확대' in st['toast'], ('최대 확대 아닌데 반응', st)
        # 최대 확대: 근처(아이콘 밖)에선 반응 없음 → 아이콘에 닿으면 도장 + 아래 제목 띠 → 눌러야 창
        at(pg, SPOTJ('리쓰린 공원'), 5); time.sleep(.3); pg.evaluate('S.span.walk = 2'); time.sleep(1.2)
        at(pg, SPOTJ('리쓰린 공원'), 'Math.max(.2, 60 / CAM.z)'); time.sleep(.3)
        assert not pg.evaluate('S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key]'), '아이콘 밖인데 반응'
        at(pg, SPOTJ('리쓰린 공원')); wait(pg, 'S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key]', 2)
        assert pg.is_visible('#peek') and '리쓰린' in pg.inner_text('#peek') and not pg.is_visible('#sheet'), '제목 띠 대신 창이 뜸'
        pg.click('#peekBtn'); time.sleep(.2); assert '도장' in pg.inner_text('#sheet')
        pg.screenshot(path=f'{OUT}/jj_{tag}_3spot.png')
        at(pg, CITYJ('takamatsu'), -4, 4); time.sleep(.5)
        assert '다카마쓰' in pg.inner_text('#peek'); pg.click('#peekBtn'); time.sleep(.2)
        sh = pg.inner_text('#sheet'); assert '다카마쓰' in sh and '리쓰린 공원' in sh and '사누키 우동' in sh, sh[:200]
        pg.screenshot(path=f'{OUT}/jj_{tag}_4city.png')
        # ⌖ 버튼: 자동차 비율(260km)로 → 🚗 그림·공항 화살표, 마쓰야마에서 확대 → 도고 온천
        pg.click('#bTarget'); time.sleep(1.5)
        assert pg.evaluate('S.span.walk') == 260 and pg.evaluate('far()') and pg.evaluate('Math.min(innerWidth, innerHeight) / CAM.z') > 180, '⌖ 뒤 축소 안 됨'
        pg.screenshot(path=f'{OUT}/jj_{tag}_5car.png')
        at(pg, CITYJ('matsuyama'), 3, -3); time.sleep(.6)
        assert pg.evaluate('S.mode') == 'walk', '시내에서 저절로 탐'
        assert '마쓰야마' in pg.inner_text('#loc') and '🚗' in pg.inner_text('#loc')
        pg.evaluate('S.span.walk = 2'); time.sleep(1.2)
        at(pg, SPOTJ('도고 온천')); wait(pg, 'S.seen[SPOT.find(a=>a.ko==="도고 온천").key]', 2)
        # 🚩 깃발: 확대 상태에서만 버튼 → 이름 없으면 막힘 → 꽂기(+5) → 지나가면 +1 → 고치기
        assert pg.is_visible('#bFlag')
        pts0 = pg.evaluate('S.pts || 0')
        pg.evaluate('(() => { P.x += 3; P.y += 2; })()'); time.sleep(.3)
        pg.click('#bFlag'); time.sleep(.2); assert '깃발 꽂기' in pg.inner_text('#sheet')
        pg.click('#sheet .go'); time.sleep(.2); assert pg.evaluate('S.flags.length') == 0, '이름 없이 저장됨'
        pg.fill('#fName', '테스트 우동집'); pg.click('#sheet .cats button[data-c="cafe"]'); pg.click('#sheet .stars button[data-s="4"]'); pg.click('#sheet .seg button[data-v="been"]')
        pg.click('#sheet .go'); time.sleep(1.4)
        f = pg.evaluate('S.flags[0]'); assert f['name'] == '테스트 우동집' and f['cat'] == 'cafe' and f['star'] == 4 and f['status'] == 'been' and f['vis'] == 'private' and abs(f['lat'] - 33.8) < 1
        assert pg.evaluate('S.pts') == pts0 + 5, ('포인트', pg.evaluate('S.pts'), pts0)
        pg.screenshot(path=f'{OUT}/jj_{tag}_6flag.png')
        pg.evaluate('(() => { P.x += 4; })()'); time.sleep(.4); pg.evaluate('(() => { P.x -= 4; })()'); time.sleep(.6)
        assert pg.evaluate('S.pts') == pts0 + 6 and '테스트 우동집' in pg.inner_text('#peek'), '지나가도 동전·제목 띠 없음'
        pg.click('#peekBtn'); time.sleep(.2); pg.click('#sheet .cbtn'); time.sleep(.2); pg.fill('#fName', '고친 우동집'); pg.click('#sheet .go'); time.sleep(.3)
        assert pg.evaluate('S.flags[0].name') == '고친 우동집' and pg.evaluate('S.flags.length') == 1
        # 확대·축소
        s0 = pg.evaluate('S.span.walk'); pg.mouse.move(w / 2, h / 3); pg.mouse.wheel(0, 400); time.sleep(.1); assert pg.evaluate('S.span.walk') > s0, '휠 축소 안 됨'
        pg.mouse.wheel(0, -400); time.sleep(.1)
        # 쓸어내려 닫기 → 돋보기로 다시
        if not pg.is_visible('#sheet'): pg.click('#peekBtn'); time.sleep(.2)
        swipe_down(pg); assert not pg.is_visible('#sheet')
        pg.click('#pip'); time.sleep(.2); assert pg.is_visible('#sheet')
        # 설정·새로고침
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        pg.evaluate('save()'); pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('S.party.length') == 4 and len(pg.evaluate('Object.keys(S.seen)')) >= 2
        assert pg.evaluate('FLAGS.length') == 1 and pg.evaluate('S.pts') >= 26, '새로고침 뒤 깃발·포인트 없음'
        pg.once('dialog', lambda d: d.accept()); pg.evaluate('deleteFlag(S.flags[0].id)'); time.sleep(.2); assert pg.evaluate('S.flags.length') == 0
        # 마쓰야마공항에서 탑승 대기 중 새로고침
        pg.click('#bTarget')
        at(pg, AIRJ('MYJ'), 3); wait(pg, 'S.mode === "ground"', 3); pg.evaluate('save()')
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'ground' and '탑승 취소' in pg.inner_text('#sheet')
        print(tag, 'OK · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
