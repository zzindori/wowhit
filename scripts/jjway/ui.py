#!/usr/bin/env python3
"""jjWay 화면 확인: public을 띄우고 출발 설정 → 걷기 → 청주공항 변신 → 직항 없는 곳 안내 → 간사이 착륙 → 일본에서 걷기 → 돌아오기.
python3 scripts/jjway/ui.py [캡처 폴더]"""
import sys, os, subprocess, time, threading, http.server, functools
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../public')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
PORT = 8771

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(Q, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()

def run(w, h, tag):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{PORT}/games/jjway/index.html')
        pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0')
        assert pg.is_visible('#setup'), '출발 설정 창 안 뜸'
        pg.click('#nPlus'); pg.click('#nMinus')
        pg.fill('#mems .mem:nth-child(3) input', '첫째')
        pg.click('#goBtn'); time.sleep(.3)
        pg.screenshot(path=f'{OUT}/jj_{tag}_1start.png')
        # 걷기: 오른쪽 키 1초 → 육지에 남아 있어야
        x0 = pg.evaluate('P.x'); pg.keyboard.down('ArrowRight'); time.sleep(1); pg.keyboard.up('ArrowRight'); time.sleep(.3)
        st = pg.evaluate('({x:P.x, land: landAt(P.x,P.y), loc: document.getElementById("loc").textContent})')
        assert st['x'] > x0 + 30, f'안 움직임 {st}'
        # 서해로 계속 가도 바다에 못 들어감
        pg.evaluate('(() => { P.x = -250; P.y = -110; P.trail = []; })()')
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '포항 근처가 땅이 아님'
        pg.keyboard.down('ArrowRight'); time.sleep(3); pg.keyboard.up('ArrowRight')
        assert pg.evaluate('S.mode') == 'walk'
        # 공항 다리 구역을 지나 서해로 가도 바다 한가운데로 못 나감 (김포 근처에서 출발, 인천공항 변신 막으려고 armAt)
        pg.evaluate('(() => { P.x = -470; P.y = -300; P.armAt = "ICN"; })()')
        pg.keyboard.down('ArrowLeft'); time.sleep(3); pg.keyboard.up('ArrowLeft')
        far = pg.evaluate('canStand(P.x,P.y,"KOR") || AIR.some(a => Math.hypot(a.x-P.x,a.y-P.y) < 22) || S.mode === "plane"')
        assert far, '서해 한가운데로 나감'
        pg.evaluate('(() => { P.armAt = null; })()')
        assert pg.evaluate('canStand(P.x,P.y,"KOR")'), '바다로 나감'
        # 청주공항에 서기 → 정보 창 → 변신
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "CJJ"); P.x = a.x + 3; P.y = a.y; P.trail = []; })()')
        time.sleep(.5)
        sheet = pg.inner_text('#sheet')
        assert '청주국제공항' in sheet and '일본 직항' in sheet, sheet[:200]
        time.sleep(1.2)
        assert pg.evaluate('S.mode') == 'plane', '변신 안 함'
        time.sleep(1.2)
        pg.screenshot(path=f'{OUT}/jj_{tag}_2plane.png')
        assert pg.evaluate('S.mode') == 'plane', '출발 공항에 바로 다시 내림'
        # 직항 없는 마쓰야마 위 → 안내, 착륙 안 함
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "MYJ"); P.x = a.x; P.y = a.y; })()'); time.sleep(1)
        toast = pg.inner_text('#toast')
        assert pg.evaluate('S.mode') == 'plane' and '직항이 없어요' in toast, toast
        # 간사이 → 착륙
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "KIX"); P.x = a.x + 5; P.y = a.y; })()'); time.sleep(1.2)
        st = pg.evaluate('({m:S.mode, c:S.country, st:Object.keys(S.stamps)})')
        assert st['m'] == 'walk' and st['c'] == 'JPN' and 'KIX' in st['st'], st
        sheet = pg.inner_text('#sheet')
        assert '간사이국제공항' in sheet and '청주' in sheet, sheet[:300]
        pg.screenshot(path=f'{OUT}/jj_{tag}_3land.png')
        # 바로 다시 안 탐 → 벗어났다 오면 탐
        time.sleep(1.5); assert pg.evaluate('S.mode') == 'walk', '내린 공항에서 바로 다시 탐'
        pg.keyboard.down('ArrowUp'); time.sleep(.8); pg.keyboard.up('ArrowUp'); time.sleep(.2)
        assert pg.evaluate('canStand(P.x,P.y,"JPN")')
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "KIX"); P.x = a.x; P.y = a.y; })()'); time.sleep(1.6)
        assert pg.evaluate('S.mode') == 'plane' and pg.evaluate('S.from') == 'KIX'
        n = pg.evaluate('Object.keys(destsFrom("KIX")).length')
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "PUS"); P.x = a.x; P.y = a.y; })()'); time.sleep(1.2)
        assert pg.evaluate('S.mode + S.country') == 'walkKOR', '김해 착륙 실패'
        # 설정 창
        pg.click('#bSet'); time.sleep(.2); pg.click('#ints .int:nth-child(4) .sw'); pg.click('#setClose')
        assert pg.evaluate('S.ints[3].on') is True
        # 새로고침해도 이어짐
        pg.reload(); pg.wait_for_function('typeof AIR !== "undefined" && AIR.length > 0'); time.sleep(.5)
        assert not pg.is_visible('#setup') and pg.evaluate('S.party.length') == 4 and pg.evaluate('S.country') == 'KOR'
        # 제주는 걸어서 못 감, 비행기(국내선)로
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "PUS"); P.x = a.x; P.y = a.y; P.armAt=null; })()'); time.sleep(1.5)
        assert pg.evaluate('destsFrom("PUS").CJU') and pg.evaluate('S.mode') == 'plane'
        pg.evaluate('(() => { const a = AIR.find(a => a.code === "CJU"); P.x = a.x; P.y = a.y; })()'); time.sleep(1.2)
        assert pg.evaluate('S.mode + S.country') == 'walkKOR'
        print(tag, 'OK · KIX에서 한국으로', n, '곳 · 오류', len(errs), errs[:3])
        b.close()
    return errs

e = run(390, 800, 'port') + run(1280, 720, 'land')
srv.shutdown()
sys.exit(1 if e else 0)
