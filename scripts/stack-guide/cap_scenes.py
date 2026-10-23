import json, time, sys
from playwright.sync_api import sync_playwright
src='/home/zzindori/dev/workspace/portfolio/wowhit/public/games/stack/index.html'
html=open(src).read().replace('(() => {', '(() => { window.__t = s => eval(s);', 1)
VW,VH=760,1240
def zone(w=2):
    return {"sp":[{"on":True,"items":7,"t":0} for _ in range(3)],"wrkLv":w,"sellLv":1,"prodLv":1,"bagLv":1,"shelfLv":0,"cash":0,"bills":0,"queue":[],"auto":False}
def page(p, zones, z, stack):
    st={"v":2,"money":1500000,"capLv":6,"spdLv":3,"walLv":12,"warp":True,"zones":zones,"paid":{},"stack":stack,"px":380,"py":-980*z+560,
     "tut":{k:True for k in "sold collected upgraded zone angry cashFull wallet autoInfo moved direct goldOnly".split()},
     "stats":{"sell":50,"collect":30,"tip":5,"upgrade":10,"golden":1},"mission":None,"seen":int(time.time()*1000)}
    pg=p.chromium.launch().new_page(viewport={'width':VW,'height':VH},device_scale_factor=2)
    pg.route('https://wowhit.org/games/stack/',lambda r,q=None:r.fulfill(body=html,content_type='text/html'))
    pg.add_init_script(f"localStorage.setItem('stack-sell-v2', {json.dumps(json.dumps(st))})")
    pg.goto('https://wowhit.org/games/stack/'); pg.wait_for_timeout(900)
    pg.add_style_tag(content='#toast,#hint,.hud,#zones,#mission,#orders,#elev{display:none!important}')
    pg.evaluate("__t('scale = 1; CFG.events.first = 1e9; evT = 1e9; thiefCd = 1e9')")
    return pg
def crop(pg, out, x, y, w, h, z):
    sx, sy = pg.evaluate(f"__t('toS({x}, gy({z}, {y}))')")
    pg.screenshot(path=out, clip={'x':sx-w/2,'y':sy-h/2,'width':w,'height':h})
with sync_playwright() as p:
    Z=2
    # 배달
    pg=page(p,[zone(0),zone(0),zone(0)],Z,[0]*4)
    pg.evaluate("__t('P.x = 330; P.y = gy(2, 420); P.fx = -1; P.fy = 0; for (let i = 0; i < 50 && !rt(2).deliv; i++) { [0,1,2].forEach(z => rt(z).deliv = null); startDeliv(); } rt(2).deliv.src = 0; rt(2).deliv.want = 4')")
    pg.wait_for_timeout(3600); crop(pg,'g/ev_deliv.png',255,360,280,240,Z)
    # 건물주
    pg.evaluate("__t('rt(2).deliv = null; const [lo] = CFG.vip.want; rt(2).vip = { x:-30, y:gy(2, VIP_SPOT.y), want:4, got:0, sum:0, t:CFG.vip.time, state:\"come\", fx:1, fy:0, svx:0, svy:0, serveT:0 }; P.x = 360; P.y = gy(2, 560)')")
    pg.wait_for_timeout(3800); crop(pg,'g/ev_vip.png',225,285,280,240,Z)
    # 고장 + 황금
    pg.evaluate("__t('rt(2).vip = null; Object.assign(S.zones[2].sp[0], { broken:true, fix:0, brokenT:30 }); Object.assign(S.zones[2].sp[2], { items:9, golden:2, goldLife:[50, 55] })')")
    pg.wait_for_timeout(1500); crop(pg,'g/ev_broken.png',145,630,300,300,Z); crop(pg,'g/ev_gold.png',565,690,280,280,Z)
    # 도둑
    pg.evaluate("__t('S.zones[2].cash = 500000; S.zones[2].bills = 12; const side = THIEF_SIDES[0], path = thiefPath(side, 2); thief = { tp:\"bag\", z:2, x:path[0][0], y:path[0][1], path, wp:1, out:thiefPath(THIEF_SIDES[1], 2).reverse(), owp:0, state:\"come\", loot:0, t:0, fx:-1, fy:0, svx:0, svy:0 }; P.x = 150; P.y = gy(2, 560)')")
    for i in range(80):
        d=pg.evaluate("__t('thief ? Math.hypot(thief.x - CASH.x, thief.y - gy(2, CASH.y)) : -1')")
        if 0 <= d < 75: break
        pg.wait_for_timeout(100)
    crop(pg,'g/ev_thief.png',490,250,300,240,Z)
    # 층별 가게 (PREVIEW)
    pg.evaluate("__t('thief = null; S.zones[2].cash = 0; S.zones[2].sp.forEach(s => Object.assign(s, { broken:false, golden:0, goldLife:[], items:5 })); P.x = 380; P.y = gy(2, 470); CFG.cust.every = 1e9; rt(2).custs = []; workers.length = 0')")
    for f in list(range(10))+[-1]:
        pg.evaluate(f"__t('PREVIEW = {f}; S.zones[2].sp.forEach(s => s.items = 5)')"); pg.wait_for_timeout(1300)   # 층마다 물건 수 다시(쌓여서 '가득 참' 안 뜨게)
        crop(pg,f'g/floor{f+1 if f>=0 else 11}.png',355,750-82,600,290,Z)
    print('ok')
