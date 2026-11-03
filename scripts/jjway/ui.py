#!/usr/bin/env python3
"""jjWay 화면 확인: 출발 설정 → 🚗 서울에서 차(바다 막힘) → 김해공항 탑승 게이지(움직이면 줄어듦) → 탑승 취소(차로) → 다시 탑승 → 이륙
→ 직항 없는 곳 회색 → 다카마쓰 위 지나가기(안 내림) → 멈추면 착륙 → 걷기(도시 확대) · 착륙 취소 → 다시 착륙
→ 리쓰린 공원 카드 버튼(가고 싶어요·다녀왔어요) → 다카마쓰 도시 창 → ⌖ 버튼(자동차 비율·공항 화살표) → 마쓰야마에서 확대 → 도고 온천 다녀왔어요 → 휠 확대·축소
→ 쓸어내려 닫기·돋보기로 다시 열기 → 설정 → 새로고침 이어짐 → 탑승 대기 중 새로고침.
python3 scripts/jjway/ui.py [캡처 폴더]"""
import sys, os, time, threading, http.server, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
PORT = 8771
GKEY = ''
try:
    GKEY = [l.split('=',1)[1].strip() for l in open(os.path.expanduser('~/.secrets/jjway.env')) if l.startswith('GMAPS_KEY=')][0]
except Exception: pass
GK_OK = []
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
        pg.on('response', lambda r: r.status >= 500 and print(tag, '서버 오류', r.status, r.url.split('?')[0][:90]))
        pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html')
        pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0 && SPOT.length > 0')
        pg.fill('#mems .mem:nth-child(3) input', '첫째'); pg.click('#goBtn'); time.sleep(.3)
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('far()'), '처음이 자동차 비율이 아님'
        x0 = pg.evaluate('P.x'); hold(pg, 'ArrowRight', 1); assert pg.evaluate('P.x') > x0 + 30
        pg.evaluate('(() => { P.x = -250; P.y = -110; })()'); hold(pg, 'ArrowRight', 2)
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '차가 바다로'
        # 김해: 탑승 게이지 → 움직이면 줄어듦 → 탑승 → 취소하면 차로
        # 멀리 볼 땐(260km) 공항 아이콘에 닿아도 안 탐 → '더 확대하면' 안내, 확대(40km)하면 게이지
        at(pg, AIRJ('PUS')); time.sleep(.8)
        assert pg.evaluate('P.g') == 0 and pg.evaluate('P.onAirT') == 'PUS' and '확대' in pg.inner_text('#toast'), '멀리서 탑승됨'
        at(pg, AIRJ('PUS'), 40); pg.evaluate('S.span.walk = 40'); time.sleep(1.2)
        at(pg, AIRJ('PUS'), 1); time.sleep(.8)
        g1 = pg.evaluate('P.g'); assert .3 < g1 < 1 and pg.evaluate('P.gKind') == 'board', g1
        hold(pg, 'ArrowUp', .2); at(pg, AIRJ('PUS'), 1)
        assert pg.evaluate('P.g') < g1
        wait(pg, 'S.mode === "ground"', 3)
        pg.click('#sheet .cbtn'); wait(pg, 'S.mode === "walk" && !S.from', 1)
        at(pg, AIRJ('PUS'), 40); time.sleep(.2); at(pg, AIRJ('PUS'), 1); wait(pg, 'S.mode === "ground"', 3)
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
        # 리쓰린 공원 채움·다녀왔어요 + 도시 창
        # 덜 확대하면 아이콘에 닿아도 반응 없음(안내만)
        pg.evaluate('S.span.walk = 30'); time.sleep(.6); at(pg, SPOTJ('리쓰린 공원')); time.sleep(.4)
        st = pg.evaluate('({seen: !!S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key], span: S.span.walk, toast: document.getElementById("toast").innerText, onT: P.onSpotT, far: far()})')
        assert not st['seen'] and '더 확대' in st['toast'], ('최대 확대 아닌데 반응', st)
        # 최대 확대: 근처(아이콘 밖)에선 반응 없음 → 아이콘에 닿으면 채움 + 아래 제목 띠 → 눌러야 창
        at(pg, SPOTJ('리쓰린 공원'), 5); time.sleep(.3); pg.evaluate('S.span.walk = 2'); time.sleep(1.2)
        at(pg, SPOTJ('리쓰린 공원'), 'Math.max(.2, 60 / CAM.z)'); time.sleep(.3)
        assert not pg.evaluate('S.seen[SPOT.find(a=>a.ko==="리쓰린 공원").key]'), '아이콘 밖인데 반응'
        # 마커 위에 서면 머리 위 고리가 차오름 → 꽉 차면 자동 '가고 싶어요'(+2) → 카드 아래 버튼 둘로 손으로 바꿈(상세엔 상태 버튼 없음)
        k = 'SPOT.find(a=>a.ko==="리쓰린 공원").key'
        on = lambda: pg.evaluate("[...document.querySelectorAll('#card .cbtns .on')].map(b=>b.className)")
        at(pg, SPOTJ('리쓰린 공원')); time.sleep(.5)
        assert pg.is_visible('#card .cdt') and on() == [] and 0 < pg.evaluate('P.ring') < 1, ('고리', pg.evaluate('P.ring'), on())
        p0 = pg.evaluate('S.pts||0'); wait(pg, f'!!S.wish[{k}]', 3); time.sleep(.1)
        assert on() == ['wi on'] and pg.evaluate('S.pts') == p0 + 2, on()
        pg.click('#card .cbtns button.ok'); time.sleep(.2)
        assert pg.evaluate(f'S.seen[{k}]') and not pg.evaluate(f'S.wish[{k}]') and pg.evaluate('S.pts') == p0 + 12 and on() == ['ok on'], '카드에서 다녀왔어요'
        pg.click('#card .cbtns button.wi'); time.sleep(.2); assert pg.evaluate(f'S.wish[{k}]') and not pg.evaluate(f'S.seen[{k}]') and on() == ['wi on'], '가고 싶어요로 바꾸기'
        pg.click('#card .cbtns button.wi'); time.sleep(.2); assert not pg.evaluate(f'S.wish[{k}]') and on() == [], '해제'
        time.sleep(2.5)
        assert not pg.evaluate(f'S.wish[{k}]') and not pg.evaluate(f'S.seen[{k}]'), '손으로 되돌린 곳이 다시 자동으로 바뀜'
        pg.click('#card .cbtns button.ok'); time.sleep(.2); assert pg.evaluate(f'S.seen[{k}]') and pg.evaluate('S.pts') == p0 + 12, '포인트 두 번'
        pg.click('#card .cdt'); time.sleep(.2)
        assert pg.is_visible('#sheet') and '리쓰린' in pg.inner_text('#sheet') and pg.locator('#sheet .seg, #sheet .cbtns').count() == 0, '상세에 상태 버튼이 남음'
        pg.evaluate('xClose()')
        # 멀리서 핀 톡 → 카드 → 💭 가고 싶어요
        k3 = 'SPOT.find(a=>a.ko==="야시마지").key'
        at(pg, SPOTJ('야시마지'), 1); time.sleep(1)
        pos = pg.evaluate('(()=>{const s=SPOT.find(a=>a.ko==="야시마지");return [W/2+(s.x-CAM.x)*CAM.z, H*CY+(s.y-CAM.y)*CAM.z-12*1.55]})()')
        if 0 < pos[0] < w and 60 < pos[1] < h - 60:
            pg.mouse.click(pos[0], pos[1]); time.sleep(.3)
            assert pg.is_visible('#card') and '야시마지' in pg.inner_text('#card') and '여기서' in pg.inner_text('#card'), '핀 톡 카드 없음'
            pg.click('#card .cbtns button.wi'); time.sleep(.2); assert pg.evaluate(f'S.wish[{k3}]'), '멀리서 가고 싶어요 안 됨'
            pg.evaluate('xClose()')
        else: print(tag, '핀이 화면 밖이라 톡 건너뜀', pos)
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
        at(pg, SPOTJ('도고 온천')); time.sleep(.6); pg.click('#card .cbtns button.ok'); time.sleep(.2); assert pg.evaluate('S.seen[SPOT.find(a=>a.ko==="도고 온천").key]')
        # 🚩 깃발: 확대 상태에서만 버튼 → 이름 없으면 막힘 → 꽂기(+5) → 지나가면 +1 → 고치기
        assert pg.is_visible('#bFlag')
        pts0 = pg.evaluate('S.pts || 0')
        pg.evaluate('(() => { P.x += 3; P.y += 2; })()'); time.sleep(.3)
        pg.click('#bFlag'); time.sleep(.2); pg.click('#sheet .qbs button:nth-child(2)'); time.sleep(.2); assert '깃발 꽂기' in pg.inner_text('#sheet')
        pg.click('#sheet .go'); time.sleep(.2); assert pg.evaluate('S.flags.length') == 0, '이름 없이 저장됨'
        pg.fill('#fName', '테스트 우동집'); pg.click('#sheet .cats button[data-c="cafe"]'); pg.click('#sheet .stars button[data-s="4"]'); pg.click('#sheet .seg button[data-v="been"]')
        pg.click('#sheet .go'); time.sleep(1.4)
        f = pg.evaluate('S.flags[0]'); assert f['name'] == '테스트 우동집' and f['cat'] == 'cafe' and f['star'] == 4 and f['status'] == 'been' and f['vis'] == 'private' and abs(f['lat'] - 33.8) < 1
        assert pg.evaluate('S.pts') == pts0 + 5, ('포인트', pg.evaluate('S.pts'), pts0)
        pg.screenshot(path=f'{OUT}/jj_{tag}_6flag.png')
        pg.evaluate('(() => { P.x += 4; })()'); time.sleep(.4); pg.evaluate('(() => { P.x -= 4; })()'); time.sleep(.6)
        assert pg.evaluate('S.pts') == pts0 + 6 and '테스트 우동집' in pg.inner_text('#peek'), '지나가도 동전·제목 띠 없음'
        assert pg.locator('#card .cbtns button.ok.on').count() == 1, '깃발 카드 다녀왔어요 표시'
        pg.click('#card .cbtns button.ok'); time.sleep(.2); assert pg.evaluate('S.flags[0].status') == '', '깃발 해제'
        pg.click('#card .cbtns button.wi'); time.sleep(.2); assert pg.evaluate('S.flags[0].status') == 'want', '깃발 가고 싶어요'
        pg.click('#card .cbtns button.ok'); time.sleep(.2); assert pg.evaluate('S.flags[0].status') == 'been' and pg.evaluate('S.pts') == pts0 + 9, '깃발 다녀왔어요 +3'
        pg.click('#card .cbtns button.ok'); pg.click('#card .cbtns button.ok'); time.sleep(.2); assert pg.evaluate('S.flags[0].status') == 'been' and pg.evaluate('S.pts') == pts0 + 9, '깃발 포인트 두 번'
        pg.click('#card .cdt'); time.sleep(.2); pg.click('#sheet .cbtn'); time.sleep(.2); pg.fill('#fName', '고친 우동집'); pg.click('#sheet .go'); time.sleep(.3)
        assert pg.evaluate('S.flags[0].name') == '고친 우동집' and pg.evaluate('S.flags.length') == 1
        # 🔎 장소 찾기: 좌표 → 십자선 → 지도 끌어 조정 → 꽂기 / 구글 지도 긴 링크 → 이름까지 / 이름 검색(네트워크)
        pg.click('#bFlag'); time.sleep(.2); assert '장소 찾기' in pg.inner_text('#sheet')
        pg.fill('#qIn', '34.3295, 134.0439'); pg.click('#sheet .qgo'); time.sleep(.4)
        assert pg.evaluate('!!P.pick') and '자리 고르기' in pg.inner_text('#sheet'), '좌표로 십자선 안 됨'
        px0 = pg.evaluate('P.x'); hold(pg, 'ArrowRight', .3)
        assert pg.evaluate('P.x') == px0, '십자선 모드인데 사람이 움직임'
        pg.click('#sheet .go'); time.sleep(.3); assert '깃발 꽂기' in pg.inner_text('#sheet')
        pg.fill('#fName', '리쓰린 근처 카페'); pg.click('#sheet .go'); time.sleep(.5)
        nf = pg.evaluate('S.flags.find(f => f.name === "리쓰린 근처 카페")'); assert nf and abs(nf['lat'] - 34.3295) < .02 and abs(nf['lon'] - 134.0439) < .02, nf
        pg.click('#bFlag'); time.sleep(.2)
        pg.fill('#qIn', 'https://www.google.com/maps/place/Ritsurin+Garden/@34.3299,134.0442,17z/data=!3m1!4b1!4m6!3m5!1s0x0:0x0!8m2!3d34.329497!4d134.043926')
        pg.click('#sheet .qgo'); time.sleep(.4)
        assert pg.evaluate('!!P.pick') and 'Ritsurin Garden' in pg.inner_text('#pkInfo') and '34.3295' in pg.inner_text('#pkInfo'), pg.inner_text('#sheet')[:200]
        pg.click('#sheet .cbtn'); time.sleep(.2); assert not pg.evaluate('!!P.pick')
        # 구글 지도 '공유 → 복사'처럼 이름·주소·링크가 함께 붙어도 링크만 골라 정확한 좌표로, 첫 줄은 이름
        pg.click('#bFlag'); time.sleep(.2)
        pg.fill('#qIn', '栗林公園\n日本、〒760-0073 香川県高松市栗林町1-20-16\nhttps://www.google.com/maps/place/@34.3299,134.0442,17z/data=!3m1!4b1!8m2!3d34.329497!4d134.043926')
        pg.click('#sheet .qgo'); time.sleep(.4)
        assert pg.evaluate('!!P.pick') and '栗林公園' in pg.inner_text('#pkInfo') and '34.3295' in pg.inner_text('#pkInfo'), pg.inner_text('#sheet')[:200]
        pg.click('#sheet .cbtn'); time.sleep(.2)
        # 이름 검색: 키 없으면 안내만 → ⚙️ 설정에 키(~/.secrets/jjway.env GMAPS_KEY, wowhit.org 제한이라 Referer를 붙여 보냄) → 구글 검색 → 고르면 십자선 → 꽂으면 장소 ID(gid) 저장
        pg.click('#bFlag'); time.sleep(.2); pg.fill('#qIn', '다카마쓰 우동'); pg.click('#sheet .qgo'); time.sleep(.3)
        assert '설정에 구글 지도 키' in pg.inner_text('#qRes'), pg.inner_text('#qRes')
        pg.evaluate('closeSheet()')
        if GKEY:
            def gfwd(r):   # 테스트는 127.0.0.1에서 돌아서: 구글엔 wowhit.org에서 온 것처럼, 브라우저엔 CORS 허용으로
                resp = r.fetch(headers={**r.request.headers, 'referer': 'https://wowhit.org/games/jjway/', 'origin': 'https://wowhit.org'})
                r.fulfill(response=resp, headers={**resp.headers, 'access-control-allow-origin': '*'})
            pg.route('https://places.googleapis.com/**', gfwd); pg.route('https://tile.googleapis.com/**', gfwd)   # 키를 넣으면 배경도 구글 지도
            pg.click('#bSet'); time.sleep(.2); pg.fill('#gkIn', GKEY); pg.click('#gkGo')
            pg.wait_for_function('document.getElementById("gkMsg").innerText.includes("✅") || document.getElementById("gkMsg").innerText.includes("⚠️")', timeout=10000)
            assert '✅' in pg.inner_text('#gkMsg'), pg.inner_text('#gkMsg')
            pg.click('#setClose'); time.sleep(.2)
            pg.click('#bFlag'); time.sleep(.2); pg.fill('#qIn', '다카마쓰 우동'); pg.click('#sheet .qgo')
            pg.wait_for_selector('#qRes .mr', timeout=10000); n = pg.locator('#qRes .mr').count()
            print(tag, '구글 검색 다카마쓰 우동', n, '개:', ' / '.join(pg.locator('#qRes .mr b').all_inner_texts()[:3]).replace('\n', ' '))
            assert n >= 3
            pg.click('#qRes .mr >> nth=0'); time.sleep(.3); assert pg.evaluate('!!(P.pick && P.pick.gid)')
            pg.click('#sheet button.go'); time.sleep(.3); assert pg.evaluate('!!FORM.gid'), '장소 ID 안 넘어감'
            pg.evaluate('cancelFlag()'); GK_OK.append(tag)
        pg.evaluate('closeSheet()')
        # 확대·축소
        s0 = pg.evaluate('S.span.walk'); pg.mouse.move(w / 2, h / 3); pg.mouse.wheel(0, 400); time.sleep(.1); assert pg.evaluate('S.span.walk') > s0, '휠 축소 안 됨'
        pg.mouse.wheel(0, -400); time.sleep(.1)
        # 쓸어내려 닫기 → 돋보기로 다시
        if not pg.is_visible('#sheet'): pg.click('#card .cdt') if pg.is_visible('#card') else pg.click('#peekBtn'); time.sleep(.2)
        swipe_down(pg); assert not pg.is_visible('#sheet')
        pg.click('#pip'); time.sleep(.2); assert pg.is_visible('#sheet')
        # 설정·새로고침
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        pg.evaluate('save()'); pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('S.party.length') == 4 and len(pg.evaluate('Object.keys(S.seen)')) >= 2
        assert pg.evaluate('FLAGS.length') == 2 and pg.evaluate('S.pts') >= 26, '새로고침 뒤 깃발·포인트 없음'
        # 🏅 기록 창: 명소(현·도시 묶음·진행도) · 공항 · 깃발 탭, 항목 누르면 창
        pg.click('#pts'); time.sleep(.2); assert pg.is_visible('#medals')
        ml = pg.inner_text('#mList'); assert '가가와현' in ml and '리쓰린 공원' in ml and '에히메현' in ml and '도고 온천' in ml, ml[:200]
        assert '/34' in pg.inner_text('#mSum')
        hb = pg.locator('#mList .hb').first; kk = hb.get_attribute('data-wish'); was = pg.evaluate(f'!!S.wish["{kk}"]')
        hb.click(); time.sleep(.1); assert pg.evaluate(f'!!S.wish["{kk}"]') != was and pg.is_visible('#medals'), '목록 ♥ 안 됨'
        pg.click('.mtabs button[data-t="air"]'); assert '다카마쓰공항' in pg.inner_text('#mList')
        pg.click('.mtabs button[data-t="flag"]'); assert '고친 우동집' in pg.inner_text('#mList')
        pg.click('.mr[data-flag]:has-text("고친 우동집")'); time.sleep(.3); assert not pg.is_visible('#medals') and '고친 우동집' in pg.inner_text('#sheet')
        time.sleep(.6); assert pg.is_visible('#sheet'), '목록에서 연 창이 바로 닫힘'
        # 탭 지우기(공항) → 전체 초기화
        pg.click('#pts'); time.sleep(.2); pg.click('.mtabs button[data-t="air"]')
        pg.once('dialog', lambda d: d.accept()); pg.click('#mResetTab'); time.sleep(.2)
        assert pg.evaluate('Object.keys(S.stamps).length') == 0 and pg.evaluate('S.flags.length') == 2 and pg.evaluate('S.pts') > 0
        pg.once('dialog', lambda d: d.accept()); pg.click('#mResetAll'); time.sleep(.2)
        assert pg.evaluate('S.flags.length + Object.keys(S.seen).length + S.pts') == 0 and pg.inner_text('#ptsN') == '0' and pg.evaluate('S.party.length') == 4
        pg.click('#mClose')
        # 확대하면 지리원 물 면적(1:25,000)으로 바다 막힘 — 다카마쓰역에서 북쪽(항구 → 바다)으로 3초(막히지 않으면 약 3km 감)
        pg.evaluate('S.country = "JPN"; S.span.walk = 4'); at(pg, 'proj(134.0465, 34.3505)'); time.sleep(.3); at(pg, 'proj(134.0465, 34.3505)')
        wait(pg, 'fineWater(P.x, P.y) === 0', 8)
        hold(pg, 'ArrowUp', 3)
        # 물이어도 화면 4px(SHORE_PX) 안에 땅이 보이면 걸음 → 끝 자리는 땅이거나 땅에서 tol 안
        st = pg.evaluate('''(() => { const tol = Math.max(.012, SHORE_PX / CAM.z); let near = fineWater(P.x, P.y) === 0;
          for (let r = .1; r <= 1.01 && !near; r += .1) for (let a = 0; a < 32 && !near; a++) near = fineWater(P.x + Math.cos(a * .196) * tol * r, P.y + Math.sin(a * .196) * tol * r) === 0;
          return {lat: unproj(P.x, P.y).lat, near, tolM: Math.round(tol * 1000)}; })()''')
        assert st['lat'] < 34.36 and st['near'], f'바다로 걸어감 {st}'
        # 확대 막대: 점 누르면 그 확대(2km = 3번째 점), ＋/－ 한 단계, 지금 확대에 가장 가까운 점이 큼, 점 색 = 되는 것(분홍 3km 이하·파랑 60km 이하·회색)
        on = lambda: pg.evaluate("[...document.querySelectorAll('#zbar .zd')].findIndex(d => d.classList.contains('on'))")
        pg.click('#zbar .zd[data-i="3"]'); time.sleep(1.6); assert pg.evaluate('S.span.walk') == 2 and on() == 3, ('점 2km', pg.evaluate('S.span.walk'), on())
        mn = pg.evaluate("spanMin('walk')")   # 구글 키가 있으면 0.25km, 없으면 지리원 1.2km
        pg.click('#zIn'); time.sleep(1.6); assert pg.evaluate('S.span.walk') == (1 if mn < 1 else 1.2) and on() == 2, ('＋', mn, pg.evaluate('S.span.walk'), on())
        assert pg.locator('#zbar .zd.off').count() == (0 if mn < .5 else 2), '지리원 지도면 0.25·0.5km 점은 막힘'
        pg.click('#zOut'); time.sleep(.3); pg.click('#zOut'); time.sleep(1.6); assert pg.evaluate('S.span.walk') == 5 and on() == 4, ('－ 두 번', pg.evaluate('S.span.walk'))
        cols = pg.evaluate("[...document.querySelectorAll('#zbar .zd')].map(d => d.style.getPropertyValue('--zc'))")
        assert cols[3] == '#e05a8a' and cols[6] == '#2f6fd0' and cols[9] == '#8d8a96', cols
        pg.evaluate('S.span.walk = 4'); time.sleep(1.2); assert on() == 4, '손으로 4km면 5km 점'
        # 멀리 볼 땐(260km) 예전처럼 넉넉하게(해협 건너기)
        pg.evaluate('S.span.walk = 260'); time.sleep(1.2); hold(pg, 'ArrowUp', .6)
        assert pg.evaluate('unproj(P.x, P.y).lat') > 34.37, '멀리 볼 때도 막힘'
        # 마쓰야마공항에서 탑승 대기 중 새로고침
        pg.click('#bTarget'); time.sleep(.3)
        at(pg, AIRJ('MYJ'), 1); time.sleep(.6); assert pg.evaluate('S.mode') == 'walk' and pg.evaluate('P.g') == 0, '⌖(260km)에서 탑승됨'
        pg.evaluate('S.span.walk = 40'); time.sleep(.2)
        at(pg, AIRJ('MYJ'), 1); wait(pg, 'S.mode === "ground"', 3); pg.evaluate('save()')
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && SPOT.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'ground' and '탑승 취소' in pg.inner_text('#sheet')
        print(tag, 'OK · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
