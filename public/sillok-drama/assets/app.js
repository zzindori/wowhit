// 실록과 드라마 — 테마 전환, 연표·장면 거르기, 결말 가림 풀기, 검색어 복사, 공유
(() => {
  const $ = s => document.querySelector(s);
  const store = (k, v) => { try { v === undefined ? 0 : localStorage.setItem('sillok-' + k, v); return localStorage.getItem('sillok-' + k); } catch { return null; } };

  const toastEl = $('#toast'); let toastT;
  const toast = t => { toastEl.textContent = t; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('on'), 1800); };

  $('#bTheme').addEventListener('click', () => {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark'; store('theme', root.dataset.theme);
  });

  // 거르기 칩: 같은 그룹에서 하나만 눌림
  function chips(group, attr, apply) {
    const g = $(group); if (!g) return;
    g.addEventListener('click', ev => {
      const b = ev.target.closest('.chip'); if (!b) return;
      g.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', c === b));
      apply(b.dataset[attr]);
    });
  }
  // 왕 연표: 고른 드라마에 나오는 사건만, 빈 해 제목은 숨김
  // 왕별 연표: 고른 드라마에 나오는 사건만 — 빈 해 제목·사건 없는 왕 띠는 숨김
  function filterKings(f) {
    let shown = 0;
    document.querySelectorAll('#kings .king').forEach(sec => {
      const items = [...sec.querySelectorAll('.tl li')];
      items.forEach(li => { if (li.classList.contains('ev')) li.classList.toggle('hide', f !== 'all' && !li.dataset.d.split(' ').includes(f)); });
      items.forEach((li, i) => {
        if (!li.classList.contains('year')) return;
        let any = false;
        for (let j = i + 1; j < items.length && !items[j].classList.contains('year'); j++) if (!items[j].classList.contains('hide')) any = true;
        li.classList.toggle('hide', !any);
      });
      const n = items.filter(li => li.classList.contains('ev') && !li.classList.contains('hide')).length;
      shown += n;
      sec.classList.toggle('hide', f !== 'all' && n === 0);
    });
    const msg = $('#fmsg');
    if (msg) {
      const b = document.querySelector(`#filter [data-f="${f}"]`);
      msg.hidden = f === 'all';
      msg.textContent = f === 'all' ? '' : `${b.textContent.replace('🎬 ', '')}에 나오는 실록 사건 ${shown}개`;
    }
  }
  chips('#filter', 'f', filterKings);

  // 탭(왕별 / 드라마별) — 주소 ?tab=drama 로 남김
  const tabs = [...document.querySelectorAll('.tab')];
  function showTab(name, push) {
    if (!tabs.length) return;
    tabs.forEach(t => {
      const on = t.dataset.tab === name;
      t.setAttribute('aria-selected', on);
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (push) { try { history.replaceState(null, '', name === 'drama' ? '?tab=drama' : location.pathname); } catch {} }
  }
  tabs.forEach(t => t.addEventListener('click', () => showTab(t.dataset.tab, true)));
  if (tabs.length) {
    // #왕 으로 들어오면 왕별 탭, ?tab=drama 면 드라마별
    showTab(new URLSearchParams(location.search).get('tab') === 'drama' && !location.hash ? 'drama' : 'kings', false);
  }

  // 왕 목록 창: 고르면 그 왕 띠로(거르기 중이라 숨어 있으면 전체로 되돌림)
  const sheet = $('#jump');
  if (sheet) {
    document.addEventListener('click', ev => {
      if (ev.target.closest('[data-jump]')) { sheet.showModal(); return; }
      if (ev.target.closest('[data-close]') || ev.target === sheet) { sheet.close(); return; }
      const a = ev.target.closest('.jk, .jk-link'); if (!a) return;
      ev.preventDefault();
      sheet.close();
      showTab('kings', true);
      const sec = document.getElementById(a.dataset.k);
      if (sec.classList.contains('hide')) { document.querySelector('#filter [data-f="all"]').click(); }
      try { history.replaceState(null, '', '#' + a.dataset.k); } catch {}
      sec.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    });
  }
  chips('#vfilter', 'v', v => document.querySelectorAll('#scenes .scene').forEach(s => s.classList.toggle('hide', v !== 'all' && s.dataset.v !== v)));

  // 검색: 띄어쓴 낱말이 모두 들어간 것만(띄어쓰기 달라도 찾음 — '기묘 사화' = '기묘사화'), 제목에 있으면 위로
  const qEl = $('#q'), res = $('#sres');
  if (qEl && res) {
    const V = { fact: ['사실', 'v-fact'], adapt: ['각색', 'v-adapt'], fic: ['허구', 'v-fic'] };
    const G = [['k', '👑 왕'], ['dr', '🎬 드라마'], ['ev', '📜 실록 사건'], ['sc', '🎞 드라마 장면']];
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const ns = s => s.toLowerCase().replace(/\s+/g, '');
    let idx = null;
    // 낱말마다 글자 사이 공백을 허용하는 정규식(본문 띄어쓰기가 달라도 강조)
    const termRe = terms => new RegExp(terms.map(t => [...t].map(reEsc).join('\\s*')).join('|'), 'gi');
    const mark = (s, re) => esc(s).replace(new RegExp(re.source, 'gi'), m => `<mark>${m}</mark>`);
    function snippet(body, re) {
      const m = new RegExp(re.source, 'i').exec(body);
      if (!m) return body.length > 70 ? body.slice(0, 70) + '…' : body;
      const a = Math.max(0, m.index - 28), b = Math.min(body.length, m.index + m[0].length + 42);
      return (a ? '…' : '') + body.slice(a, b) + (b < body.length ? '…' : '');
    }
    function run() {
      const q = qEl.value.trim();
      try { history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname); } catch {}
      $('#picks').hidden = !!q;
      if (!q) { res.innerHTML = ''; $('#scount').textContent = ''; return; }
      if (!idx) { $('#scount').textContent = '불러오는 중…'; return; }
      const terms = q.split(/\s+/).filter(Boolean), nterms = terms.map(ns), re = termRe(terms);
      const hits = [];
      for (const it of idx) {
        const h = ns(it.h), all = h + ns(it.s) + ns(it.b);
        if (!nterms.every(t => all.includes(t))) continue;
        hits.push({ it, score: nterms.reduce((a, t) => a + (h.includes(t) ? 10 : 0), 0) });
      }
      hits.sort((a, b) => b.score - a.score);
      $('#scount').textContent = hits.length ? `${hits.length}개 찾았어요` : `「${q}」은(는) 찾지 못했어요. 다른 말로 찾아보세요.`;
      res.innerHTML = G.map(([t, name]) => {
        const g = hits.filter(x => x.it.t === t);
        if (!g.length) return '';
        return `<h2 class="sgroup">${name} ${g.length}</h2><div class="sres">` + g.map(({ it }) => `<a class="hit" href="${esc(it.u)}">
          <span class="hs">${it.v ? `<span class="badge ${V[it.v][1]}">${V[it.v][0]}</span>` : ''}${mark(it.s, re)}</span>
          <b>${mark(it.h, re)}</b><p>${mark(snippet(it.b, re), re)}</p></a>`).join('') + '</div>';
      }).join('');
    }
    qEl.addEventListener('input', run);
    $('#picks').addEventListener('click', ev => { const b = ev.target.closest('[data-q]'); if (b) { qEl.value = b.dataset.q; run(); } });
    qEl.value = new URLSearchParams(location.search).get('q') || '';
    fetch(res.dataset.src).then(r => r.json()).then(d => { idx = d; run(); }).catch(() => { $('#scount').textContent = '검색 자료를 불러오지 못했어요. 새로고침해 주세요.'; });
    if (!qEl.value && matchMedia('(pointer: fine)').matches) qEl.focus();
  }

  document.addEventListener('click', async ev => {
    const sp = ev.target.closest('.spoil');
    if (sp) { sp.closest('.scene').querySelectorAll('.spoil').forEach(x => x.classList.remove('spoil')); return; }
    const cp = ev.target.closest('[data-copy]');
    if (cp) {
      try { await navigator.clipboard.writeText(cp.dataset.copy); toast(`「${cp.dataset.copy}」 복사했어요 — 실록 사이트 검색창에 붙여 넣으세요`); }
      catch { toast(`검색어: ${cp.dataset.copy}`); }
      return;
    }
    if (ev.target.closest('[data-share]')) {
      const data = { title: document.title, url: location.href };
      try {
        if (navigator.share) await navigator.share(data);
        else { await navigator.clipboard.writeText(location.href); toast('주소를 복사했어요'); }
      } catch (e) { if (e && e.name !== 'AbortError') toast('주소: ' + location.href); }
    }
  });
})();
