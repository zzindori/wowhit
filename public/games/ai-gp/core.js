/* AI 그랑프리 — 서킷·차 물리 + PPO(강화학습) 학습 일꾼.
   index.html이 Web Worker로 띄움. 화면도 같은 파일을 <script>로 읽어 서킷 만들기·센서 그리기에 씀(window.GPCORE).
   Node에서도 읽어서 화면 없이 학습만 돌려 볼 수 있음(scripts/ai-gp/train.cjs). 라이브러리 없이 신경망·역전파·Adam 직접 구현 */
(function () {
'use strict';

const DT = 1 / 30;                       // 물리 한 칸 = 1/30초
// 차: 가속·브레이크·최고 속도·구름 저항·공기 저항·최소 회전 반지름·타이어 접지(옆으로 버티는 힘)·미끄러질 때 속도 손실·언덕 힘
const CAR = { ACC: 260, BRK: 520, VTOP: 380, ROLL: 8, DRAG: 0.0003, RMIN: 30, GRIP: 650, SCRUB: 0.6, SCRUB_MAX: 700, G: 350 };
const RAYS = [-1.2, -0.7, -0.3, 0, 0.3, 0.7, 1.2], RAY_LEN = 250;   // 벽까지 거리 센서 7개(라디안, 앞 기준)
const OBS = RAYS.length + 17, ACT = 2;   // 보는 것 24개 → 핸들·페달 2개
// 바닥: 모래 = 느려지고 조금 미끄러움 · 웅덩이 = 많이 미끄러움. 콘은 닿으면 사고
const SURF = [null, { drag: 1.2, grip: .75 }, { drag: .25, grip: .4 }], CONE_R = 6, CAR_R = 5;
const PPO = { cars: 24, T: 128, epochs: 4, mb: 512, gamma: 0.99, lam: 0.95, clip: 0.2, lr: 3e-4, ent: 0.0005,
  maxGrad: 0.5, hidden: 64, kl: 0.03 };
// 점수 규칙: 앞으로 간 거리 + / 벽에 박음 − / 핸들 홱 꺾음 −(조금)
const RW = { prog: 0.01, crash: 2, steer: 0.02 };

const CIRCUITS = {
  main: { name: '층층 서킷', width: 56,
    pts: [[240, 578], [480, 582], [760, 570], [880, 535], [930, 450], [905, 360], [840, 305], [740, 300], [665, 255], [650, 180],
      [590, 105], [420, 82], [250, 92], [140, 140], [100, 240], [170, 320], [300, 325], [400, 370], [380, 445], [250, 465], [130, 470], [72, 520], [110, 572]],
    hills: [[905, 420, 70, 85], [420, 80, 55, 100], [255, 395, -45, 80]] },     // [x, y, 높이(−면 골짜기), 퍼짐]
};

const wrap = a => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;

/* ── 서킷: 점들을 부드러운 곡선(Catmull-Rom)으로 잇고 4마다 다시 찍음 ── */
function buildTrack(c) {
  const P = c.pts, n = P.length, raw = [];
  for (let i = 0; i < n; i++) {
    const p0 = P[(i - 1 + n) % n], p1 = P[i], p2 = P[(i + 1) % n], p3 = P[(i + 2) % n];
    for (let k = 0; k < 40; k++) {
      const t = k / 40, t2 = t * t, t3 = t2 * t, f = d => .5 * (2 * p1[d] + (-p0[d] + p2[d]) * t +
        (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2 + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3);
      raw.push([f(0), f(1)]);
    }
  }
  const m = raw.length, seg = new Float64Array(m);
  let tot = 0;
  for (let i = 0; i < m; i++) { const a = raw[i], b = raw[(i + 1) % m]; seg[i] = Math.hypot(b[0] - a[0], b[1] - a[1]); tot += seg[i]; }
  const N = Math.round(tot / 4), step = tot / N;
  const T = { name: c.name, W: c.width, hills: c.hills || [], patches: c.patches || [], cones: c.cones || [], N, L: tot, step };
  for (const k of ['cx', 'cy', 'tx', 'ty', 'nx', 'ny', 'ang', 'k', 's', 'h', 'lx', 'ly', 'rx', 'ry']) T[k] = new Float64Array(N);
  let j = 0, acc = 0;
  for (let i = 0; i < N; i++) {
    const want = i * step;
    while (acc + seg[j] < want && j < m - 1) { acc += seg[j]; j++; }
    const u = seg[j] ? (want - acc) / seg[j] : 0, a = raw[j], b = raw[(j + 1) % m];
    T.cx[i] = a[0] + (b[0] - a[0]) * u; T.cy[i] = a[1] + (b[1] - a[1]) * u; T.s[i] = want;
  }
  for (let i = 0; i < N; i++) {
    const a = (i - 1 + N) % N, b = (i + 1) % N, dx = T.cx[b] - T.cx[a], dy = T.cy[b] - T.cy[a], l = Math.hypot(dx, dy);
    T.tx[i] = dx / l; T.ty[i] = dy / l; T.nx[i] = -T.ty[i]; T.ny[i] = T.tx[i]; T.ang[i] = Math.atan2(dy, dx);
  }
  for (let i = 0; i < N; i++) {
    T.k[i] = wrap(T.ang[(i + 1) % N] - T.ang[(i - 1 + N) % N]) / (2 * step);
    T.h[i] = height(T, T.cx[i], T.cy[i]);
    const hw = T.W / 2;
    T.lx[i] = T.cx[i] + T.nx[i] * hw; T.ly[i] = T.cy[i] + T.ny[i] * hw;
    T.rx[i] = T.cx[i] - T.nx[i] * hw; T.ry[i] = T.cy[i] - T.ny[i] * hw;
  }
  return T;
}
function height(T, x, y) {
  let h = 0;
  for (const [hx, hy, A, s] of T.hills) { const dx = x - hx, dy = y - hy; h += A * Math.exp(-(dx * dx + dy * dy) / (2 * s * s)); }
  return h;
}
function grad(T, x, y) {
  let gx = 0, gy = 0;
  for (const [hx, hy, A, s] of T.hills) {
    const dx = x - hx, dy = y - hy, e = A * Math.exp(-(dx * dx + dy * dy) / (2 * s * s)) / (s * s);
    gx -= e * dx; gy -= e * dy;
  }
  return [gx, gy];
}

// 바닥 종류: 0 아스팔트 · 1 모래 · 2 웅덩이(나중에 놓은 게 위)
function surfAt(T, x, y) {
  let k = 0;
  for (const [px, py, r, t] of T.patches) { const dx = x - px, dy = y - py; if (dx * dx + dy * dy < r * r) k = t === 'water' ? 2 : 1; }
  return k;
}
// 서킷 검사: 너무 급한 커브·길끼리 너무 가까움·밖으로 나감 → {ok, i(문제 자리), why}
function checkTrack(T) {
  const hw = T.W / 2;
  for (let i = 0; i < T.N; i++) {
    if (Math.abs(T.k[i]) * hw * .95 > 1) return { ok: false, i, why: 'curve' };
    for (const [x, y] of [[T.lx[i], T.ly[i]], [T.rx[i], T.ry[i]]]) if (x < 10 || y < 10 || x > 990 || y > 630) return { ok: false, i, why: 'out' };
  }
  const gap = Math.ceil(T.W * 2.4 / T.step), lim = (T.W * 1.2) ** 2;
  for (let i = 0; i < T.N; i += 2) for (let j = i + gap; j < T.N; j += 2) {
    if (T.N - (j - i) < gap) continue;
    const dx = T.cx[i] - T.cx[j], dy = T.cy[i] - T.cy[j];
    if (dx * dx + dy * dy < lim) return { ok: false, i, why: 'near' };
  }
  if (T.L < 1200) return { ok: false, i: 0, why: 'short' };
  return { ok: true };
}

/* ── 차 ── */
// keep: 경주 중엔 사고 나도 랩 기록을 이어감
function place(T, car, idx, keep, lat = 0) {
  car.idx = idx; car.x = T.cx[idx] + T.nx[idx] * lat; car.y = T.cy[idx] + T.ny[idx] * lat; car.th = T.ang[idx]; car.v = 0; car.s = T.s[idx]; car.lat = lat;
  car.stuck = 0; car.back = 0; car.ps = 0; car.pt = 0; car.slide = 0; car.run = 0;
  if (!keep) { car.lapValid = false; car.trail = []; }
}
function locate(T, car) {
  let best = car.idx, bd = Infinity;
  for (let k = -6; k <= 14; k++) {
    const j = (car.idx + k + T.N) % T.N, dx = car.x - T.cx[j], dy = car.y - T.cy[j], d = dx * dx + dy * dy;
    if (d < bd) { bd = d; best = j; }
  }
  car.idx = best;
  const dx = car.x - T.cx[best], dy = car.y - T.cy[best];
  car.lat = dx * T.nx[best] + dy * T.ny[best];
  const s = T.s[best] + dx * T.tx[best] + dy * T.ty[best];
  return ((s % T.L) + T.L) % T.L;
}
function segHit(px, py, dx, dy, ax, ay, bx, by, best) {
  const ex = bx - ax, ey = by - ay, den = dx * ey - dy * ex;
  if (den > -1e-9 && den < 1e-9) return best;
  const qx = ax - px, qy = ay - py, u = (qx * ey - qy * ex) / den, w = (qx * dy - qy * dx) / den;
  return u > 0 && u < best && w >= 0 && w <= 1 ? u : best;
}
// 센서: 차 앞 방향 + a 쪽으로 벽(서킷 양쪽 가장자리)까지 거리. 가까운 구간만 봄
function ray(T, car, a) {
  const dx = Math.cos(car.th + a), dy = Math.sin(car.th + a);
  let best = RAY_LEN;
  for (let k = -15; k < 70; k++) {
    const i = (car.idx + k + T.N) % T.N, j = (i + 1) % T.N;
    best = segHit(car.x, car.y, dx, dy, T.lx[i], T.ly[i], T.lx[j], T.ly[j], best);
    best = segHit(car.x, car.y, dx, dy, T.rx[i], T.ry[i], T.rx[j], T.ry[j], best);
  }
  for (const [cx, cy] of T.cones) {   // 콘도 센서에 걸림
    const fx = cx - car.x, fy = cy - car.y, pr = fx * dx + fy * dy;
    if (pr <= 0 || pr - CONE_R > best) continue;
    const pp = fx * fx + fy * fy - pr * pr;
    if (pp < CONE_R * CONE_R) { const u = pr - Math.sqrt(CONE_R * CONE_R - pp); if (u > 0 && u < best) best = u; }
  }
  return best;
}
function observe(T, car, o, off) {
  for (let r = 0; r < RAYS.length; r++) o[off + r] = ray(T, car, RAYS[r]) / RAY_LEN;
  let k = off + RAYS.length;
  o[k++] = car.v / CAR.VTOP;
  const he = wrap(car.th - T.ang[car.idx]);
  o[k++] = Math.sin(he); o[k++] = Math.cos(he);
  o[k++] = car.lat / (T.W / 2);
  for (const ah of [15, 35, 60]) o[k++] = wrap(T.ang[(car.idx + ah) % T.N] - T.ang[car.idx]) / Math.PI;   // 앞 커브
  const [gx, gy] = grad(T, car.x, car.y);
  o[k++] = (gx * Math.cos(car.th) + gy * Math.sin(car.th)) * 2;                 // 지금 오르막(+)·내리막(−)
  o[k++] = (T.h[(car.idx + 30) % T.N] - T.h[car.idx]) / 50;                    // 120 앞 높이 차
  o[k++] = car.ps; o[k++] = car.pt;
  const here = surfAt(T, car.x, car.y);   // 바닥: 지금·앞 60·앞 140 (모래, 웅덩이)
  o[k++] = here === 1; o[k++] = here === 2;
  for (const d of [60, 140]) { const f = surfAt(T, car.x + Math.cos(car.th) * d, car.y + Math.sin(car.th) * d); o[k++] = f === 1; o[k++] = f === 2; }
}
// 한 칸 움직이고 점수·끝남·사건 돌려줌. time = 학습 전체 칸 수
function stepCar(T, car, a0, a1, time, ev, ci) {
  const st = clamp(a0, -1, 1), th = clamp(a1, -1, 1);
  const c = Math.cos(car.th), s = Math.sin(car.th), [gx, gy] = grad(T, car.x, car.y);
  const sf = SURF[surfAt(T, car.x, car.y)], grip = CAR.GRIP * (sf ? sf.grip : 1);
  let acc = th >= 0 ? CAR.ACC * th * (1 - car.v / CAR.VTOP) : CAR.BRK * th;
  acc -= CAR.G * (gx * c + gy * s) + CAR.ROLL + CAR.DRAG * car.v * car.v + (sf ? sf.drag * car.v : 0);
  car.v = Math.max(0, car.v + acc * DT);
  let yaw = car.v * st / CAR.RMIN;
  const lat = Math.abs(car.v * yaw);
  car.slide = 0;
  if (lat > grip) {   // 접지 넘음 → 덜 돌고 속도 깎임(밀려 나감)
    yaw = Math.sign(yaw) * grip / car.v;
    car.v = Math.max(0, car.v - Math.min((lat - grip) * CAR.SCRUB, CAR.SCRUB_MAX) * DT); car.slide = 1;
  }
  car.th = wrap(car.th + yaw * DT);
  car.x += Math.cos(car.th) * car.v * DT; car.y += Math.sin(car.th) * car.v * DT;
  const ps = car.s, ns = locate(T, car);
  let ds = ns - ps;
  if (ds < -T.L / 2) ds += T.L; else if (ds > T.L / 2) ds -= T.L;
  car.s = ns; car.run += ds;
  let r = ds * RW.prog - RW.steer * (st - car.ps) * (st - car.ps);
  car.ps = st; car.pt = th;
  // 출발선·구간
  if (ds > 0 && ps > T.L - 60 && ns < 60) {
    if (car.lapValid) {
      car.secs[2] = (time - car.secStart) * DT;
      ev.push({ k: 'lap', c: ci, t: (time - car.lapStart) * DT, sec: car.secs.slice(), line: car.trail });
    }
    car.lapStart = time; car.secStart = time; car.lapValid = true; car.secs = [0, 0, 0]; car.trail = [];
  } else if (ds < 0 && ps < 60 && ns > T.L - 60) car.lapValid = false;
  if (car.lapValid && ds > 0) for (let b = 1; b <= 2; b++) {
    const at = T.L * b / 3;
    if (ps < at && ns >= at) { car.secs[b - 1] = (time - car.secStart) * DT; car.secStart = time; ev.push({ k: 'sec', c: ci, b: b - 1, t: car.secs[b - 1] }); }
  }
  if (car.lapValid && (time & 1)) car.trail.push(Math.round(car.x * 10) / 10, Math.round(car.y * 10) / 10);
  // 벽·멈춤·거꾸로
  let done = 0;
  if (Math.abs(car.lat) > T.W / 2 - 4) { done = 1; r -= RW.crash; }
  if (!done) for (const [cx, cy] of T.cones) { const dx = car.x - cx, dy = car.y - cy; if (dx * dx + dy * dy < (CONE_R + CAR_R) ** 2) { done = 1; r -= RW.crash; break; } }
  car.stuck = car.v < 8 ? car.stuck + DT : 0;
  if (!done && car.stuck > 3) { done = 2; r -= RW.crash * .5; }
  car.back = Math.abs(wrap(car.th - T.ang[car.idx])) > 2 ? car.back + DT : 0;
  if (!done && car.back > 1) { done = 3; r -= RW.crash; }
  if (done) {
    ev.push({ k: 'crash', c: ci, x: car.x, y: car.y, why: done, run: car.run / T.L });
    // 다시 출발: 조금 뒤 + 옆으로 살짝 흩어서. 같은 곳에서 3번 연속 박으면(콘 바로 뒤 등) 서킷 아무 데서나(학습 차만)
    car.fails = car.run < T.L * .05 ? (car.fails || 0) + 1 : 0;
    let idx = (car.idx - 20 + T.N) % T.N;
    if (!car.race && car.fails >= 3) { idx = Math.floor(Math.random() * T.N); car.fails = 0; }
    place(T, car, idx, car.race, car.race ? 0 : (Math.random() - .5) * T.W * .4);
  }
  return [r, done ? 1 : 0];
}

/* ── 신경망(tanh 두 층) + Adam ── */
function randn() { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
class MLP {
  constructor(sizes, outGain) {
    this.sizes = sizes; this.L = sizes.length - 1;
    let n = 0; this.off = [];
    for (let l = 0; l < this.L; l++) { this.off.push([n, n + sizes[l] * sizes[l + 1]]); n += sizes[l] * sizes[l + 1] + sizes[l + 1]; }
    this.P = new Float32Array(n); this.G = new Float32Array(n); this.n = n;
    for (let l = 0; l < this.L; l++) {
      const [w] = this.off[l], fi = sizes[l], fo = sizes[l + 1], g = (l === this.L - 1 ? outGain : Math.SQRT2) / Math.sqrt(fi);
      for (let i = 0; i < fi * fo; i++) this.P[w + i] = randn() * g;
    }
    this.acts = []; this.buf = {};
  }
  forward(X, B) {
    const S = this.sizes; this.acts[0] = X; this.B = B;
    let A = X;
    for (let l = 0; l < this.L; l++) {
      const fi = S[l], fo = S[l + 1], [w, b] = this.off[l], P = this.P, key = l + ':' + B;
      const Z = this.buf[key] || (this.buf[key] = new Float32Array(B * fo));
      for (let r = 0; r < B; r++) {
        const ro = r * fo, ri = r * fi;
        for (let o = 0; o < fo; o++) Z[ro + o] = P[b + o];
        for (let i = 0; i < fi; i++) {
          const a = A[ri + i]; if (a === 0) continue;
          const wi = w + i * fo;
          for (let o = 0; o < fo; o++) Z[ro + o] += a * P[wi + o];
        }
        if (l < this.L - 1) for (let o = 0; o < fo; o++) Z[ro + o] = Math.tanh(Z[ro + o]);
      }
      this.acts[l + 1] = Z; A = Z;
    }
    return A;
  }
  backward(dY) {   // dY: B×출력, G에 더함
    const S = this.sizes, B = this.B, P = this.P, G = this.G;
    let D = dY;
    for (let l = this.L - 1; l >= 0; l--) {
      const fi = S[l], fo = S[l + 1], [w, b] = this.off[l], A = this.acts[l];
      const key = 'd' + l + ':' + B, dA = l > 0 ? (this.buf[key] || (this.buf[key] = new Float32Array(B * fi))) : null;
      for (let r = 0; r < B; r++) {
        const ro = r * fo, ri = r * fi;
        for (let o = 0; o < fo; o++) G[b + o] += D[ro + o];
        for (let i = 0; i < fi; i++) {
          const a = A[ri + i], wi = w + i * fo;
          let s = 0;
          for (let o = 0; o < fo; o++) { const d = D[ro + o]; G[wi + o] += a * d; s += P[wi + o] * d; }
          if (dA) dA[ri + i] = s * (1 - a * a);   // tanh 미분
        }
      }
      D = dA;
    }
  }
}
class Adam {
  constructor(n) { this.m = new Float32Array(n); this.v = new Float32Array(n); this.t = 0; }
  step(P, G, lr) {
    const b1 = .9, b2 = .999; this.t++;
    const c1 = 1 - b1 ** this.t, c2 = 1 - b2 ** this.t, m = this.m, v = this.v;
    for (let i = 0; i < P.length; i++) {
      const g = G[i]; m[i] = b1 * m[i] + (1 - b1) * g; v[i] = b2 * v[i] + (1 - b2) * g * g;
      P[i] -= lr * (m[i] / c1) / (Math.sqrt(v[i] / c2) + 1e-8);
    }
  }
}
function clipGrad(arrs, max) {
  let s = 0; for (const a of arrs) for (let i = 0; i < a.length; i++) s += a[i] * a[i];
  const n = Math.sqrt(s); if (n > max) { const f = max / n; for (const a of arrs) for (let i = 0; i < a.length; i++) a[i] *= f; }
  return n;
}
class RMS {   // 평균·분산을 계속 갱신(보는 값·점수 크기 맞추기)
  constructor(n) { this.mean = new Float64Array(n); this.var = new Float64Array(n).fill(1); this.count = 1e-4; this.n = n; }
  update(X, B) {
    const n = this.n, bm = new Float64Array(n), bv = new Float64Array(n);
    for (let r = 0; r < B; r++) for (let i = 0; i < n; i++) bm[i] += X[r * n + i];
    for (let i = 0; i < n; i++) bm[i] /= B;
    for (let r = 0; r < B; r++) for (let i = 0; i < n; i++) { const d = X[r * n + i] - bm[i]; bv[i] += d * d; }
    const tot = this.count + B;
    for (let i = 0; i < n; i++) {
      bv[i] /= B; const d = bm[i] - this.mean[i];
      this.mean[i] += d * B / tot;
      this.var[i] = (this.var[i] * this.count + bv[i] * B + d * d * this.count * B / tot) / tot;
    }
    this.count = tot;
  }
}

/* ── PPO 학습기: 차 여러 대가 뇌 하나를 같이 씀 ── */
class Trainer {
  constructor(T, saved) {
    const H = PPO.hidden, nC = PPO.cars, n = PPO.T * nC;
    this.T = T; this.nC = nC;
    this.pi = new MLP([OBS, H, H, ACT], .01); this.vf = new MLP([OBS, H, H, 1], 1);
    this.pi.P[this.pi.off[2][1] + 1] = .5;   // 처음엔 페달을 조금 밟는 쪽으로(앞으로 가 봐야 배움)
    this.logstd = new Float32Array(ACT).fill(-.5); this.gls = new Float32Array(ACT);
    this.oPi = new Adam(this.pi.n); this.oVf = new Adam(this.vf.n); this.oLs = new Adam(ACT);
    this.obsRms = new RMS(OBS); this.retRms = new RMS(1); this.ret = new Float64Array(nC);
    this.time = 0; this.samples = 0; this.updates = 0; this.t = 0; this.last = {};
    this.raw = new Float32Array(n * OBS); this.obs = new Float32Array(n * OBS); this.act = new Float32Array(n * ACT);
    this.logp = new Float32Array(n); this.val = new Float32Array(n); this.rew = new Float32Array(n); this.done = new Float32Array(n);
    this.adv = new Float32Array(n); this.retn = new Float32Array(n);
    this.cur = new Float32Array(nC * OBS); this.curN = new Float32Array(nC * OBS);
    if (saved) this.load(saved);
    this.cars = [];
    for (let i = 0; i < nC; i++) { const c = {}; place(T, c, Math.floor(i * T.N / nC)); c.secs = [0, 0, 0]; this.cars.push(c); }
  }
  norm(src, dst, B) {
    const m = this.obsRms.mean, v = this.obsRms.var;
    for (let r = 0; r < B; r++) for (let i = 0; i < OBS; i++) {
      const k = r * OBS + i; dst[k] = clamp((src[k] - m[i]) / Math.sqrt(v[i] + 1e-8), -5, 5);
    }
  }
  // 모든 차 한 칸. 모으는 칸이 다 차면 학습(update)까지
  tick(ev) {
    const T = this.T, nC = this.nC, t = this.t, std = [Math.exp(this.logstd[0]), Math.exp(this.logstd[1])];
    for (let c = 0; c < nC; c++) observe(T, this.cars[c], this.cur, c * OBS);
    this.norm(this.cur, this.curN, nC);
    const mu = this.pi.forward(this.curN, nC), V = this.vf.forward(this.curN, nC);
    for (let c = 0; c < nC; c++) {
      const k = t * nC + c;
      this.raw.set(this.cur.subarray(c * OBS, c * OBS + OBS), k * OBS);
      this.obs.set(this.curN.subarray(c * OBS, c * OBS + OBS), k * OBS);
      let lp = 0;
      for (let j = 0; j < ACT; j++) {
        const z = randn(), a = mu[c * ACT + j] + std[j] * z;
        this.act[k * ACT + j] = a; lp += -.5 * z * z - this.logstd[j] - .9189385;
      }
      this.logp[k] = lp; this.val[k] = V[c];
    }
    for (let c = 0; c < nC; c++) {
      const k = t * nC + c, [r, d] = stepCar(T, this.cars[c], this.act[k * ACT], this.act[k * ACT + 1], this.time, ev, c);
      this.ret[c] = this.ret[c] * PPO.gamma + r;
      this.rew[k] = r; this.done[k] = d;
      if (d) this.ret[c] = 0;
    }
    this.retRms.update(Float32Array.from(this.ret), nC);
    this.time++; this.t++; this.samples += nC;
    if (this.t === PPO.T) { this.update(); this.t = 0; return true; }
    return false;
  }
  update() {
    const T = this.T, nC = this.nC, n = PPO.T * nC, g = PPO.gamma, lam = PPO.lam;
    for (let c = 0; c < nC; c++) observe(T, this.cars[c], this.cur, c * OBS);
    this.norm(this.cur, this.curN, nC);
    const lastV = Float32Array.from(this.vf.forward(this.curN, nC));
    const rs = Math.sqrt(this.retRms.var[0] + 1e-8);
    for (let c = 0; c < nC; c++) {
      let gae = 0;
      for (let t = PPO.T - 1; t >= 0; t--) {
        const k = t * nC + c, nv = t === PPO.T - 1 ? lastV[c] : this.val[k + nC], live = 1 - this.done[k];
        const delta = clamp(this.rew[k] / rs, -10, 10) + g * nv * live - this.val[k];
        gae = delta + g * lam * live * gae;
        this.adv[k] = gae; this.retn[k] = gae + this.val[k];
      }
    }
    this.obsRms.update(this.raw, n);
    const idx = new Int32Array(n); for (let i = 0; i < n; i++) idx[i] = i;
    const mb = PPO.mb, X = new Float32Array(mb * OBS), dMu = new Float32Array(mb * ACT), dV = new Float32Array(mb);
    let kl = 0, cf = 0, cnt = 0, vl = 0, stop = false;
    for (let ep = 0; ep < PPO.epochs && !stop; ep++) {
      for (let i = n - 1; i > 0; i--) { const j = (Math.random() * (i + 1)) | 0, t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
      let ekl = 0, en = 0;
      for (let s0 = 0; s0 + mb <= n; s0 += mb) {
        let am = 0, as = 0;
        for (let r = 0; r < mb; r++) { const a = this.adv[idx[s0 + r]]; am += a; as += a * a; }
        am /= mb; as = Math.sqrt(Math.max(as / mb - am * am, 0)) + 1e-8;
        for (let r = 0; r < mb; r++) X.set(this.obs.subarray(idx[s0 + r] * OBS, idx[s0 + r] * OBS + OBS), r * OBS);
        const mu = this.pi.forward(X, mb), V = this.vf.forward(X, mb);
        const std = [Math.exp(this.logstd[0]), Math.exp(this.logstd[1])];
        this.pi.G.fill(0); this.vf.G.fill(0); this.gls.fill(0);
        for (let r = 0; r < mb; r++) {
          const k = idx[s0 + r], A = (this.adv[k] - am) / as;
          let lp = 0; const z = [0, 0];
          for (let j = 0; j < ACT; j++) { z[j] = (this.act[k * ACT + j] - mu[r * ACT + j]) / std[j]; lp += -.5 * z[j] * z[j] - this.logstd[j] - .9189385; }
          const lr = lp - this.logp[k], ratio = Math.exp(lr);
          ekl += -lr; en++;
          const clipped = (A > 0 && ratio > 1 + PPO.clip) || (A < 0 && ratio < 1 - PPO.clip);
          if (clipped) cf++;
          for (let j = 0; j < ACT; j++) {
            if (clipped) { dMu[r * ACT + j] = 0; continue; }
            const co = -A * ratio / mb;
            dMu[r * ACT + j] = co * z[j] / std[j];
            this.gls[j] += co * (z[j] * z[j] - 1);
          }
          const e = V[r] - this.retn[k]; dV[r] = e / mb; vl += e * e; cnt++;
        }
        for (let j = 0; j < ACT; j++) this.gls[j] -= PPO.ent;
        this.pi.backward(dMu); this.vf.backward(dV);
        clipGrad([this.pi.G, this.gls], PPO.maxGrad); clipGrad([this.vf.G], PPO.maxGrad);
        this.oPi.step(this.pi.P, this.pi.G, PPO.lr); this.oLs.step(this.logstd, this.gls, PPO.lr); this.oVf.step(this.vf.P, this.vf.G, PPO.lr);
        for (let j = 0; j < ACT; j++) this.logstd[j] = clamp(this.logstd[j], -3, .5);
      }
      kl = ekl / en;
      if (kl > PPO.kl) stop = true;   // 한 번에 너무 많이 바뀌면 그만(PPO 안전장치)
    }
    let rsum = 0; for (let i = 0; i < n; i++) rsum += this.rew[i];
    this.updates++;
    this.last = { kl, clip: cf / Math.max(cnt, 1), vloss: vl / Math.max(cnt, 1), rew: rsum / nC, std: Math.exp(this.logstd[0]) };
  }
  setTrack(T) {   // 새 서킷: 뇌는 그대로, 차만 새 자리로
    this.T = T; this.t = 0; this.ret.fill(0);
    this.cars.forEach((c, i) => place(T, c, Math.floor(i * T.N / this.nC)));
  }
  drive(car) {   // 경주용: 흔들림 없이 뇌가 제일 좋다고 보는 대로
    observe(this.T, car, this.cur, 0); this.norm(this.cur, this.curN, 1);
    const m = this.pi.forward(this.curN, 1); return [m[0], m[1]];
  }
  dump() {
    const r = a => Array.from(a, x => Math.round(x * 1e5) / 1e5);
    return { v: 1, pi: r(this.pi.P), vf: r(this.vf.P), ls: r(this.logstd), om: r(this.obsRms.mean), ov: r(this.obsRms.var), oc: this.obsRms.count,
      rv: this.retRms.var[0], rc: this.retRms.count, samples: this.samples, updates: this.updates, time: this.time };
  }
  load(s) {
    if (!s || s.v !== 1 || s.pi.length !== this.pi.n || s.vf.length !== this.vf.n) return;
    this.pi.P.set(s.pi); this.vf.P.set(s.vf); this.logstd.set(s.ls); this.obsRms.mean.set(s.om); this.obsRms.var.set(s.ov); this.obsRms.count = s.oc;
    this.retRms.var[0] = s.rv; this.retRms.count = s.rc; this.samples = s.samples; this.updates = s.updates; this.time = s.time;
  }
}

function trackData(T) {
  const o = { name: T.name, W: T.W, N: T.N, L: T.L, hills: T.hills };
  for (const k of ['cx', 'cy', 'tx', 'ty', 'nx', 'ny', 'ang', 'k', 'h', 'lx', 'ly', 'rx', 'ry']) o[k] = Array.from(T[k]);
  return o;
}

/* ── Web Worker 연결 ── */
if (typeof importScripts === 'function') {
  let T, tr, speed = 0, paused = false, ahead = 0, timer = 0, race = null;
  const FV = 5;   // 차 한 대 = x, y, 방향, 속도, 미끄러짐
  const pack = (cars, frames) => { const f = new Float32Array(cars.length * FV); cars.forEach((c, i) => f.set([c.x, c.y, c.th, c.v, c.slide], i * FV)); frames.push(f); };
  const post = (frames, ev, nc, extra) => {
    const buf = new Float32Array(frames.length * nc * FV);
    frames.forEach((f, i) => buf.set(f, i * nc * FV));
    postMessage({ type: 'frames', n: frames.length, nc, buf, ev, samples: tr.samples, ...extra }, [buf.buffer]);
  };
  // 경주: 나(0)·AI(1) 두 대, 화면이 받아 간 만큼만 앞서 만듦(실제 속도)
  const raceLoop = () => {
    const frames = [], ev = [];
    while (ahead < 3) {
      if (race.go) {
        const e = [], a = tr.drive(race.cars[1]);
        stepCar(T, race.cars[0], race.input[0], race.input[1], race.t, e, 0);
        stepCar(T, race.cars[1], a[0], a[1], race.t, e, 1);
        race.t++;
        for (const x of e) { x.f = frames.length; ev.push(x); }
      }
      pack(race.cars, frames); ahead++;
    }
    if (frames.length) post(frames, ev, 2, { race: { t: race.t, ls: race.cars.map(c => c.lapValid ? c.lapStart : -1) } });
  };
  const loop = () => {
    timer = 0;
    if (!tr) return;
    if (race) { raceLoop(); timer = setTimeout(loop, 8); return; }
    if (paused) return;
    const limit = speed ? Math.max(60, speed * 45) : Infinity, every = speed ? 1 : 3;
    const frames = [], ev = [], t0 = Date.now();
    let upd = false;
    while (ahead < limit && Date.now() - t0 < 30) {
      const e = [];
      if (tr.tick(e)) upd = true;
      for (const x of e) { x.f = frames.length; ev.push(x); }
      if (speed || tr.time % every === 0) { pack(tr.cars, frames); if (speed) ahead++; }
    }
    if (frames.length || ev.length) post(frames, ev, tr.nC, { stat: upd ? { ...tr.last, updates: tr.updates, samples: tr.samples, time: tr.time } : null });
    timer = setTimeout(loop, ahead >= limit ? 16 : 0);
  };
  const kick = () => { if (!timer) timer = setTimeout(loop, 0); };
  self.onmessage = e => {
    const m = e.data;
    if (m.cmd === 'init') { T = buildTrack(m.circuit || CIRCUITS.main); tr = new Trainer(T, m.saved); postMessage({ type: 'ready', cars: tr.nC, samples: tr.samples, updates: tr.updates }); kick(); }
    else if (m.cmd === 'circuit') { T = buildTrack(m.circuit); if (m.keep) tr.setTrack(T); else tr = new Trainer(T, null); ahead = 0; postMessage({ type: 'reset' }); kick(); }
    else if (m.cmd === 'speed') { speed = m.v; ahead = 0; kick(); }
    else if (m.cmd === 'pause') { paused = m.v; if (!paused) kick(); }
    else if (m.cmd === 'ack') { ahead = Math.max(0, ahead - m.v); kick(); }
    else if (m.cmd === 'save') postMessage({ type: 'save', data: tr.dump() });
    else if (m.cmd === 'reset') { tr = new Trainer(T, null); ahead = 0; postMessage({ type: 'reset' }); kick(); }
    else if (m.cmd === 'race') {
      ahead = 0;
      if (m.v) {
        const st = (T.N - 10) % T.N, mk = lat => { const c = { race: true, secs: [0, 0, 0] }; place(T, c, st, false, lat); return c; };
        race = { cars: [mk(T.W * .22), mk(-T.W * .22)], input: [0, 0], t: 0, go: false };
      } else race = null;
      kick();
    }
    else if (m.cmd === 'input') { if (race) race.input = m.v; }
    else if (m.cmd === 'go') { if (race) race.go = true; }
  };
}
const API = { DT, CAR, PPO, RW, OBS, CIRCUITS, CONE_R, buildTrack, checkTrack, surfAt, Trainer, height, grad, ray, place, stepCar, trackData, RAYS, RAY_LEN };
if (typeof module !== 'undefined') module.exports = API;
else if (typeof window !== 'undefined') window.GPCORE = API;
})();
