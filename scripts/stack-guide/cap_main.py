import json, time
from playwright.sync_api import sync_playwright
src='/home/zzindori/dev/workspace/portfolio/wowhit/public/games/stack/index.html'
html=open(src).read().replace('(() => {', '(() => { window.__t = s => eval(s);', 1)
VW,VH=760,1240
def zone(w=2):
    return {"sp":[{"on":True,"items":7,"t":0} for _ in range(3)],"wrkLv":w,"sellLv":1,"prodLv":1,"bagLv":1,"shelfLv":0,"cash":0,"bills":0,"queue":[],"auto":False}
z=[zone(3),zone(3),zone(2)]
st={"v":2,"money":1500000,"capLv":6,"spdLv":3,"walLv":12,"warp":True,"zones":z,"paid":{},"stack":[2]*9,"px":380,"py":-1960+560,
 "tut":{k:True for k in "sold collected upgraded zone angry cashFull wallet autoInfo moved direct goldOnly".split()},
 "stats":{"sell":50,"collect":30,"tip":5,"upgrade":10,"golden":1},"mission":None,"seen":int(time.time()*1000)}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':VW,'height':VH},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://wowhit.org/games/stack/',lambda r,q=None:r.fulfill(body=html,content_type='text/html'))
    pg.add_init_script(f"localStorage.setItem('stack-sell-v2', {json.dumps(json.dumps(st))})")
    pg.goto('https://wowhit.org/games/stack/'); pg.wait_for_timeout(900)
    pg.add_style_tag(content='#toast,#hint{display:none!important}')
    pg.evaluate("__t('scale = 1; CFG.events.first = 1e9; evT = 1e9; thiefCd = 1e9; P.x = 300; P.y = gy(2, 560); S.zones[2].cash = 900000; S.zones[2].bills = 14')")
    pg.wait_for_timeout(9000)
    pg.evaluate("__t('P.x = 300; P.y = gy(2, 470); P.fx = 0; P.fy = 1; S.stack = Array(9).fill(2); P.still = 0')")
    pg.wait_for_timeout(1200)
    pg.screenshot(path='g/main.png')
    # hotspot points (world -> screen)
    pts=pg.evaluate("""__t(`(() => { const z = 2, f = (x, y, h=0) => toS(x, gy(z, y), h);
      return { machine: f(SP[1].x, SP[1].y - 60), pickup: f(SP[0].x, SP[0].y + 10), sell: f(SELL.x, SELL.y), cust: f(LINE.x - 40, LINE.y - 20),
        cash: f(CASH.x, CASH.y), worker: workers.filter(w => w.z === z).map(w => toS(w.x, w.y, 30))[0] || null, hero: toS(P.x, P.y, 40),
        padsL: f(PAD_L, PAD_Y[1]), padsR: f(PAD_R, PAD_Y[1]), padsLow: f(PAD_R - 84, PAD_LOW), stair: f(STAIR_UP.x, STAIR_UP.y), elev: f(ELEV.x, ELEV.y - 30), safe: f(SAFE.x, SAFE.y) }; })()`)""")
    hud=pg.evaluate("""(() => { const r = id => { const e = document.getElementById(id); if (!e || e.hidden) return null; const b = e.getBoundingClientRect(); return [b.x + b.width/2, b.y + b.height/2]; };
      return { money: r('money'), zones: r('zones'), mission: r('mission'), menu: r('menuBtn') }; })()""")
    print(json.dumps({'w':VW,'h':VH,'pts':pts,'hud':hud}))
    print('errors',errs); b.close()
