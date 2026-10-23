# 게임 파일 → 자료실 '생산기만 보는' 테스트 페이지
import sys
src='/home/zzindori/dev/workspace/portfolio/wowhit/public/games/stack/index.html'
out='/home/zzindori/dev/workspace/tgbot/uploads/web/층층이_생산기테스트.html'
s=open(src).read()
s=s.replace('(() => {','(() => { window.__t = s => eval(s);',1)
a="const k = Math.min(1, dt*6); cam.x += (tx-cam.x)*k; cam.y += (ty-cam.y)*k;"
assert s.count(a)==1
s=s.replace(a, a+" if (window.VIEW) { const v = window.VIEW(); cam.x = v.x; cam.y = v.y; scale = v.s; }")
seed=r'''<script>
(() => { try {   // 테스트 전용: 저장을 9층·엘리베이터로 새로 만듦(진짜 게임과 주소가 달라 서로 영향 없음)
  const zone = () => ({ sp:[0, 1, 2].map(() => ({ on:true, items:3, t:0 })), wrkLv:0, sellLv:1, prodLv:0, bagLv:0, shelfLv:0, cash:0, bills:0, queue:[], auto:false });
  localStorage.setItem('stack-sell-v2', JSON.stringify({ v:2, money:1e9, capLv:1, spdLv:1, walLv:20, warp:true, zones:Array.from({ length:11 }, zone), paid:{}, stack:[], px:700, py:300,
    tut:Object.fromEntries('sold collected upgraded zone angry cashFull wallet autoInfo moved direct goldOnly'.split(' ').map(k => [k, true])), stats:{ sell:0, collect:0, tip:0, upgrade:0, golden:0 }, mission:null, seen:Date.now() }));
} catch (e) {} })();
</script>
<style>
.hud,#zones,#mission,#orders,#toast,#hint,#elev,#menu,#settings,#slowChip{display:none!important}
#tv{position:fixed;left:0;right:0;top:0;z-index:99;background:rgba(30,24,20,.92);color:#fff;font:14px/1.2 system-ui,sans-serif;padding:8px 8px 10px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#tv button{border:0;border-radius:8px;padding:7px 9px;background:#5a4636;color:#fff;font-weight:700;font-size:14px}
#tv button.on{background:#f2b630;color:#3b2418}
#tv .row{display:flex;gap:5px;flex-wrap:wrap;width:100%;align-items:center}
#tv input{flex:1;min-width:120px}
#tv b{color:#ffd84a}
</style>
'''
s=s.replace('<head>','<head>\n'+seed,1).replace('<title>층층이 · 쌓고 팔고, 빨리빨리!</title>','<title>[테스트] 층층이 생산기</title>',1)
ui=r'''<div id="tv"><div class="row" id="tvF"></div><div class="row"><button id="tvAuto" class="on">자동</button><input id="tvP" type="range" min="0" max="100" value="50"><b id="tvPv">자동</b><button id="tvB">고장</button><button id="tvR">🔄 다시 읽기</button></div><div class="row" id="tvM"></div></div>
<script>
(() => {
  let F = 0, AUTO = true, P = 0.5, BROKEN = false, M = 1, ZOOM = false;
  try { const h = JSON.parse(decodeURIComponent(location.hash.slice(1)) || '{}'); ({ F = F, M = M, ZOOM = ZOOM, AUTO = AUTO, P = P } = h); } catch (e) {}   // 다시 읽기 뒤에도 보던 층·자리 그대로
  const T = s => window.__t && window.__t(s), $ = id => document.getElementById(id);
  const names = ['1F 분식', '2F 붕어빵', '3F 치킨', '4F 편의점', '5F 라면', '6F 찜질방', '7F 뷰티', '8F 한복', '9F 박물관', '10F 야구장', '11F 공장'];
  names.forEach((n, i) => { const b = document.createElement('button'); b.textContent = n; b.onclick = () => { F = i; paint(); }; $('tvF').appendChild(b); });
  ['왼쪽', '가운데', '오른쪽', '셋 다', '확대'].forEach((n, i) => { const b = document.createElement('button'); b.textContent = n; b.onclick = () => { if (i < 4) M = i; else ZOOM = !ZOOM; paint(); }; $('tvM').appendChild(b); });
  const paint = () => { [...$('tvM').children].forEach((b, i) => b.classList.toggle('on', i < 4 ? i === M : ZOOM)); [...$('tvF').children].forEach((b, i) => b.classList.toggle('on', i === F)); $('tvAuto').classList.toggle('on', AUTO); $('tvB').classList.toggle('on', BROKEN); $('tvPv').textContent = AUTO ? '자동' : Math.round(P*100) + '%'; };
  $('tvAuto').onclick = () => { AUTO = !AUTO; paint(); };
  $('tvP').oninput = e => { AUTO = false; P = e.target.value/100; paint(); };
  $('tvB').onclick = () => { BROKEN = !BROKEN; paint(); };
  $('tvR').onclick = () => { location.href = location.pathname + '?v=' + Date.now() + '#' + encodeURIComponent(JSON.stringify({ F, M, ZOOM, AUTO, P })); };   // 새 그림 받아오기(캐시 무시)
  window.VIEW = () => T(`(() => { const z = ${F}, all = ${M} === 3, m = all ? 1 : ${M}, y = prnBase(z, m), top = document.getElementById('tv').offsetHeight, b = PU*bigOf(z);
    const g = Math.max(0.55, Math.min(1.6, Math.min(VW/430, VH/660))), s = ${ZOOM} ? (all ? Math.min(VW/770, (VH - top)/(230*b)) : Math.min(VW/(250*b), (VH - top)/(230*b))) : g;   // 셋 다 = 세 대 나란히(원근 비교)   // 기본 = 실제 게임 화면 배율
    return { x: all ? SP[1].x : Math.max(VW/s/2, Math.min(760 - VW/s/2, SP[m].x)), y: y - 95*b - top/2/s, s }; })()`);
  setInterval(() => { if (!window.__t) return;
    T(`CFG.events.first = 1e9; evT = 1e9; thiefCd = 1e9; thief = null; CFG.cust.every = 1e9; workers.length = 0;
      for (let z = 0; z < S.zones.length; z++) { rt(z).custs = []; rt(z).vip = null; rt(z).deliv = null; }
      P.x = 700; P.y = gy(${F}, 300); P.svx = 0; P.svy = 0; curZone = ${F};
      S.zones[${F}].sp.forEach(s => { s.on = true; s.ruined = false; s.broken = ${BROKEN}; s.fix = 0; s.brokenT = 0; s.items = Math.min(s.items, 3); if (!${AUTO}) s.t = prodIv(${F})*${P}; });`); }, 30);
  paint();
})();
</script>
'''
s=s.replace('</body>', ui+'</body>',1)
open(out,'w').write(s); print('ok', len(s)//1024, 'KB')
