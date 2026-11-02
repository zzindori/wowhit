#!/usr/bin/env python3
"""jjWay 화면 확인: 출발 설정 → 걷기·바다 막힘 → 청주공항 탑승하기 → 내리기(취소) → 다시 탑승 → 이륙(직접 조종)
→ 직항 없는 곳 안내 → 간사이 착륙 확인 '계속 날기' → 다시 와서 착륙 → 공항 밖으로 → 다시 탑승 → 목적지 눌러 자동 비행 → 김해 도착
→ 돌아가기 버튼 → 설정 → 새로고침 이어짐 → 탑승 대기 중 새로고침.
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
    pg.evaluate(f'(() => {{ const a = AIR.find(a => a.code === "{code}"); P.x = a.x + {dx}; P.y = a.y; P.trail = []; }})()')

def wait(pg, js, sec=6):
    t = time.time()
    while time.time() - t < sec:
        if pg.evaluate(js): return True
        time.sleep(.1)
    raise AssertionError(f'시간 초과: {js} / mode={pg.evaluate("S.mode")} loc={pg.inner_text("#loc")}')

def run(w, h, tag):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html')
        pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0')
        assert pg.is_visible('#setup')
        pg.fill('#mems .mem:nth-child(3) input', '첫째'); pg.click('#goBtn'); time.sleep(.3)
        # 걷기
        x0 = pg.evaluate('P.x'); pg.keyboard.down('ArrowRight'); time.sleep(1); pg.keyboard.up('ArrowRight')
        assert pg.evaluate('P.x') > x0 + 30
        pg.evaluate('(() => { P.x = -250; P.y = -110; })()'); pg.keyboard.down('ArrowRight'); time.sleep(3); pg.keyboard.up('ArrowRight')
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '동해로 나감'
        # 청주공항: 저절로 안 탐
        at(pg, 'CJJ', 3); time.sleep(2)
        assert pg.evaluate('S.mode') == 'walk', '저절로 탐'
        assert '탑승하기' in pg.inner_text('#sheet')
        pg.click('#sheet .pbtn'); wait(pg, 'S.mode === "ground"')
        assert '탑승 완료' in pg.inner_text('#sheet')
        pg.screenshot(path=f'{OUT}/jj_{tag}_1ground.png')
        pg.click('#sheet .sbtn'); wait(pg, 'S.mode === "walk"')            # 내리기(취소)
        assert '탑승하기' in pg.inner_text('#sheet')
        pg.click('#sheet .pbtn'); wait(pg, 'S.mode === "ground"')
        pg.click('#sheet .pbtn'); wait(pg, 'S.mode === "takeoff"', 2)          # 이륙(직접 조종)
        time.sleep(.9); pg.screenshot(path=f'{OUT}/jj_{tag}_2takeoff.png')
        wait(pg, 'S.mode === "plane"', 4)
        time.sleep(.5); assert not pg.evaluate('P.ask'), '출발 공항에서 바로 착륙 물어봄'
        assert pg.is_visible('#flyBar')
        # 직항 없는 마쓰야마
        at(pg, 'MYJ'); time.sleep(.6)
        assert '직항이 없어요' in pg.inner_text('#toast') and not pg.evaluate('P.ask')
        # 간사이 → 물어봄 → 계속 날기 → 안 내림
        at(pg, 'KIX', 10); wait(pg, 'P.ask && P.ask.code === "KIX"', 2)
        assert '착륙할까요' in pg.inner_text('#sheet')
        pg.screenshot(path=f'{OUT}/jj_{tag}_3ask.png')
        pg.click('#sheet .sbtn'); time.sleep(.8)
        assert pg.evaluate('S.mode') == 'plane' and not pg.evaluate('P.ask'), '계속 날기 안 됨'
        # 멀리 갔다 다시 오면 다시 물어봄 → 착륙
        at(pg, 'KIX', 200); time.sleep(.4); at(pg, 'KIX', 10)
        wait(pg, 'P.ask && P.ask.code === "KIX"', 2); pg.click('#sheet .pbtn')
        wait(pg, 'S.mode === "landing"', 1); time.sleep(1); pg.screenshot(path=f'{OUT}/jj_{tag}_4landing.png')
        wait(pg, 'S.mode === "walk" && S.country === "JPN"', 4)
        assert 'KIX' in pg.evaluate('Object.keys(S.stamps)')
        sh = pg.inner_text('#sheet'); assert '공항 밖으로' in sh and '다시 탑승' in sh and '청주' in sh
        pg.screenshot(path=f'{OUT}/jj_{tag}_5arrive.png')
        pg.click('#sheet .pbtn'); time.sleep(.5)                                # 공항 밖으로
        assert not pg.is_visible('#sheet'), '창이 다시 열림'
        pg.keyboard.down('ArrowUp'); time.sleep(.8); pg.keyboard.up('ArrowUp')   # 섬에서 걸어 나옴
        assert pg.evaluate('Math.hypot(P.x - AIR.find(a=>a.code==="KIX").x, P.y - AIR.find(a=>a.code==="KIX").y)') > 30, '간사이 섬에 갇힘'
        # 다시 와서 탑승 → 목적지 '부산' 눌러 자동 비행
        at(pg, 'KIX'); wait(pg, '!document.getElementById("sheet").hidden', 2)
        pg.click('#sheet .pbtn'); wait(pg, 'S.mode === "ground"')
        pg.click('#sheet .dst:has(b:text-is("부산"))'); wait(pg, 'P.auto === "PUS"', 2)
        wait(pg, 'S.mode === "walk" && S.country === "KOR"', 12)
        assert abs(pg.evaluate('P.x') - pg.evaluate('AIR.find(a=>a.code==="PUS").x')) < 1
        # 돌아가기 버튼: 김해 → 이륙 → 돌아가기 누르면 자동으로 김해
        pg.click('#sheet .sbtn:has-text("다시 탑승")') if pg.is_visible('#sheet .sbtn:has-text("다시 탑승")') else None
        wait(pg, 'S.mode === "ground"'); pg.click('#sheet .pbtn'); wait(pg, 'S.mode === "plane"', 4)
        pg.keyboard.down('ArrowRight'); time.sleep(.6); pg.keyboard.up('ArrowRight')
        pg.click('#bRet'); wait(pg, 'P.auto === "PUS"', 1); wait(pg, 'S.mode === "walk"', 10)
        # 설정·새로고침
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0'); time.sleep(.4)
        assert not pg.is_visible('#setup') and pg.evaluate('S.party.length') == 4 and pg.evaluate('S.mode') == 'walk'
        # 탑승 대기 중 새로고침 → 대기 창 그대로
        at(pg, 'PUS'); wait(pg, '!document.getElementById("sheet").hidden', 2)
        if pg.is_visible('#sheet .pbtn:has-text("탑승하기")'): pg.click('#sheet .pbtn')
        else: pg.click('#sheet .sbtn:has-text("다시 탑승")')
        wait(pg, 'S.mode === "ground"'); pg.evaluate('save()')
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0'); time.sleep(.4)
        assert pg.evaluate('S.mode') == 'ground' and '탑승 완료' in pg.inner_text('#sheet')
        # 제주 국내선(자동)
        pg.click('#sheet .dst:has(b:text-is("제주"))'); wait(pg, 'S.mode === "walk" && Math.hypot(P.x-AIR.find(a=>a.code==="CJU").x, P.y-AIR.find(a=>a.code==="CJU").y) < 1', 10)
        print(tag, 'OK · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
