// AI 그랑프리 학습을 화면 없이 확인: node scripts/ai-gp/train.cjs [학습 횟수] [--check] [--track]
// --check: 신경망 역전파를 수치 미분과 비교 / --track: 서킷 좌표를 out/track.json으로 / --obst: 모래·웅덩이·콘 놓은 서킷
// --exam=N: 시험 서킷 N(0 거꾸로 · 1 콩 · 2 눈+다리 · 3 사막 점프)에서 배움 / --test: 10번마다 시험 서킷 전부 시험(점수 %)
const path = require('path'), fs = require('fs');
// core.js는 브라우저용 일반 스크립트(저장소가 type: module이라 require 대신 직접 읽어 실행)
const G = (() => { const module = { exports: {} }; new Function('module', fs.readFileSync(path.join(__dirname, '../../public/games/ai-gp/core.js'), 'utf8'))(module); return module.exports; })();
const OUT = path.join(__dirname, 'out'); fs.mkdirSync(OUT, { recursive: true });
const args = process.argv.slice(2), N = parseInt(args.find(a => /^\d+$/.test(a)) || '100');
const OBST = { patches: [[480, 580, 45, 'sand'], [905, 420, 50, 'water'], [300, 92, 40, 'sand']], cones: [[640, 568], [130, 210], [380, 452]] };
const ex = args.find(a => a.startsWith('--exam='));
const T = G.buildTrack(ex ? G.EXAM[+ex.slice(7)] : args.includes('--obst') ? { ...G.CIRCUITS.main, ...OBST } : G.CIRCUITS.main);

if (args.includes('--track')) {
  fs.writeFileSync(path.join(OUT, 'track.json'), JSON.stringify(G.trackData(T)));
  let minR = Infinity; for (let i = 0; i < T.N; i++) minR = Math.min(minR, 1 / Math.max(Math.abs(T.k[i]), 1e-6));
  console.log('track N', T.N, 'L', Math.round(T.L), 'min radius', minR.toFixed(1), 'h range', Math.min(...T.h).toFixed(0), Math.max(...T.h).toFixed(0));
}
if (args.includes('--check')) {
  const tr = new G.Trainer(T, null), net = tr.pi, B = 3, X = new Float32Array(B * G.OBS).map(() => Math.random() * 2 - 1);
  const dY = new Float32Array(B * 2).map(() => Math.random() - .5);
  const loss = () => { const y = net.forward(X, B); let s = 0; for (let i = 0; i < y.length; i++) s += y[i] * dY[i]; return s; };
  net.G.fill(0); loss(); net.backward(dY);
  let worst = 0;
  for (let t = 0; t < 40; t++) {
    const i = (Math.random() * net.n) | 0, o = net.P[i], h = 1e-2;
    net.P[i] = o + h; const a = loss(); net.P[i] = o - h; const b = loss(); net.P[i] = o;
    const num = (a - b) / (2 * h), err = Math.abs(num - net.G[i]) / Math.max(1e-3, Math.abs(num) + Math.abs(net.G[i]));
    worst = Math.max(worst, err);
  }
  console.log('grad check worst rel err', worst.toExponential(2));
}

const tr = new G.Trainer(T, null);
let best = Infinity, laps = [], crashes = 0, far = 0, t0 = Date.now(), jumps = 0, falls = 0, splash = 0;
const log = [];
for (let u = 0; u < N; u++) {
  let done = false;
  while (!done) {
    const ev = []; done = tr.tick(ev);
    for (const e of ev) {
      if (e.k === 'lap') { laps.push(e.t); if (e.t < best) best = e.t; }
      if (e.k === 'crash') { crashes++; far = Math.max(far, e.run); if (e.why === 4) falls++; if (e.why === 5) splash++; }
      if (e.k === 'jump') jumps++;
    }
  }
  if ((u + 1) % 10 === 0) {
    const L = tr.last, recent = laps.slice(-50), avg = recent.length ? recent.reduce((a, b) => a + b) / recent.length : 0;
    const row = { u: u + 1, samples: tr.samples, sec: Math.round((Date.now() - t0) / 1000), laps: laps.length, best: +best.toFixed(2), avg: +avg.toFixed(2),
      crashes, far: +far.toFixed(2), rew: +L.rew.toFixed(2), kl: +L.kl.toFixed(4), std: +L.std.toFixed(3) };
    if (T.jumps.length) Object.assign(row, { jumps, falls }); if (T.bridges.length) row.splash = splash;
    if (args.includes('--test')) row.test = [T === null ? 0 : G.exam(tr, { ...G.CIRCUITS.main }), ...G.EXAM.map(c => G.exam(tr, c))].map(r => Math.round(r.pct * 100) + (r.laps >= 2 ? '✔' : '')).join(' ');
    jumps = falls = splash = 0;
    log.push(row); console.log(JSON.stringify(row)); crashes = 0; far = 0;
  }
}
fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify({ log, laps }));
fs.writeFileSync(path.join(OUT, 'brain.json'), JSON.stringify(tr.dump()));
