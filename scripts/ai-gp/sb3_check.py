# 검증: 같은 서킷·차·점수 규칙을 파이썬으로 옮겨 Stable-Baselines3 PPO로 학습 → 우리 자바스크립트 PPO와 랩타임 비교.
# 서킷 좌표는 core.js가 만든 것을 그대로 읽음(node scripts/ai-gp/train.cjs 0 --track 먼저).
# 실행: ~/.venvs/aigp/bin/python scripts/ai-gp/sb3_check.py [샘플 수]
import sys, json, math, time
from pathlib import Path
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.callbacks import BaseCallback

OUT = Path(__file__).resolve().parent / 'out'
T = json.load(open(OUT / 'track.json'))
N, L, W = T['N'], T['L'], T['W']
CX, CY, TX, TY, NX, NY, ANG, H = (np.array(T[k]) for k in ['cx', 'cy', 'tx', 'ty', 'nx', 'ny', 'ang', 'h'])
LX, LY, RX, RY = (np.array(T[k]) for k in ['lx', 'ly', 'rx', 'ry'])
S = np.arange(N) * (L / N)
HILLS = T['hills']
DT = 1 / 30
ACC, BRK, VTOP, ROLL, DRAG, RMIN, GRIP, SCRUB, SCRUB_MAX, G = 260, 520, 380, 8, 0.0003, 30, 650, 0.6, 700, 350
RAYS, RAY_LEN = [-1.2, -0.7, -0.3, 0, 0.3, 0.7, 1.2], 250
RW_PROG, RW_CRASH, RW_STEER = 0.01, 2, 0.02
WIN = np.arange(-15, 70)

def wrap(a): return (a + math.pi) % (2 * math.pi) - math.pi
def grad(x, y):
    gx = gy = 0.0
    for hx, hy, A, s in HILLS:
        dx, dy = x - hx, y - hy; e = A * math.exp(-(dx * dx + dy * dy) / (2 * s * s)) / (s * s)
        gx -= e * dx; gy -= e * dy
    return gx, gy

class Car(gym.Env):
    observation_space = gym.spaces.Box(-np.inf, np.inf, (18,), np.float32)
    action_space = gym.spaces.Box(-1, 1, (2,), np.float32)   # SB3도 자바스크립트처럼 뽑은 값은 그대로 두고 차에 줄 때만 −1~1로 자름
    clock = 0
    def __init__(self, i): self.i = i; self.start = i * N // 24
    def place(self, idx):
        self.idx = idx; self.x, self.y, self.th, self.v = CX[idx], CY[idx], ANG[idx], 0.0
        self.s = S[idx]; self.lat = 0; self.lap_valid = False; self.stuck = self.back = 0; self.ps = self.pt = 0
    def reset(self, seed=None, options=None):
        if not hasattr(self, 'idx'): self.place(self.start)
        return self.obs(), {}
    def locate(self):
        j = (self.idx + np.arange(-6, 15)) % N
        d = (self.x - CX[j]) ** 2 + (self.y - CY[j]) ** 2
        b = int(j[np.argmin(d)]); self.idx = b
        dx, dy = self.x - CX[b], self.y - CY[b]
        self.lat = dx * NX[b] + dy * NY[b]
        return (S[b] + dx * TX[b] + dy * TY[b]) % L
    def rays(self):
        i = (self.idx + WIN) % N; j = (i + 1) % N
        out = []
        for a in RAYS:
            dx, dy = math.cos(self.th + a), math.sin(self.th + a); best = RAY_LEN
            for ax, ay, bx, by in ((LX[i], LY[i], LX[j], LY[j]), (RX[i], RY[i], RX[j], RY[j])):
                ex, ey = bx - ax, by - ay; den = dx * ey - dy * ex
                qx, qy = ax - self.x, ay - self.y
                with np.errstate(divide='ignore', invalid='ignore'):
                    u = (qx * ey - qy * ex) / den; w = (qx * dy - qy * dx) / den
                ok = (np.abs(den) > 1e-9) & (u > 0) & (w >= 0) & (w <= 1)
                if ok.any(): best = min(best, float(u[ok].min()))
            out.append(best / RAY_LEN)
        return out
    def obs(self):
        he = wrap(self.th - ANG[self.idx]); gx, gy = grad(self.x, self.y)
        o = self.rays() + [self.v / VTOP, math.sin(he), math.cos(he), self.lat / (W / 2)]
        o += [wrap(ANG[(self.idx + a) % N] - ANG[self.idx]) / math.pi for a in (15, 35, 60)]
        o += [(gx * math.cos(self.th) + gy * math.sin(self.th)) * 2, (H[(self.idx + 30) % N] - H[self.idx]) / 50, self.ps, self.pt]
        return np.array(o, np.float32)
    def step(self, a):
        st, th = float(np.clip(a[0], -1, 1)), float(np.clip(a[1], -1, 1))
        c, s = math.cos(self.th), math.sin(self.th); gx, gy = grad(self.x, self.y)
        acc = ACC * th * (1 - self.v / VTOP) if th >= 0 else BRK * th
        acc -= G * (gx * c + gy * s) + ROLL + DRAG * self.v * self.v
        self.v = max(0.0, self.v + acc * DT)
        yaw = self.v * st / RMIN; lat = abs(self.v * yaw)
        if lat > GRIP:
            yaw = math.copysign(GRIP / self.v, yaw); self.v = max(0.0, self.v - min((lat - GRIP) * SCRUB, SCRUB_MAX) * DT)
        self.th = wrap(self.th + yaw * DT)
        self.x += math.cos(self.th) * self.v * DT; self.y += math.sin(self.th) * self.v * DT
        ps = self.s; ns = self.locate(); ds = ns - ps
        if ds < -L / 2: ds += L
        elif ds > L / 2: ds -= L
        self.s = ns
        r = ds * RW_PROG - RW_STEER * (st - self.ps) ** 2; self.ps, self.pt = st, th
        info = {}
        t = Car.clock
        if ds > 0 and ps > L - 60 and ns < 60:
            if self.lap_valid: info['lap'] = (t - self.lap_start) * DT
            self.lap_start = t; self.lap_valid = True
        elif ds < 0 and ps < 60 and ns > L - 60: self.lap_valid = False
        done = False
        if abs(self.lat) > W / 2 - 4: done = True; r -= RW_CRASH
        self.stuck = self.stuck + DT if self.v < 8 else 0
        if not done and self.stuck > 3: done = True; r -= RW_CRASH * .5
        self.back = self.back + DT if abs(wrap(self.th - ANG[self.idx])) > 2 else 0
        if not done and self.back > 1: done = True; r -= RW_CRASH
        if done: self.place((self.idx - 8) % N)
        return self.obs(), r, done, False, info

class Laps(BaseCallback):
    def __init__(self): super().__init__(); self.laps = []; self.best = math.inf; self.t0 = time.time(); self.next = 30720
    def _on_step(self):
        Car.clock += 1
        for inf in self.locals['infos']:
            if 'lap' in inf:
                self.laps.append((self.num_timesteps, inf['lap'])); self.best = min(self.best, inf['lap'])
        if self.num_timesteps >= self.next:
            self.next += 30720
            rec = [t for _, t in self.laps[-50:]]
            print(json.dumps({'samples': self.num_timesteps, 'sec': round(time.time() - self.t0), 'laps': len(self.laps),
                              'best': round(self.best, 2) if self.laps else None, 'avg': round(sum(rec) / len(rec), 2) if rec else 0}), flush=True)
        return True

if __name__ == '__main__':
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 460800
    env = VecNormalize(DummyVecEnv([lambda i=i: Car(i) for i in range(24)]), norm_obs=True, norm_reward=True, clip_obs=5, clip_reward=10, gamma=.99)
    model = PPO('MlpPolicy', env, n_steps=128, batch_size=512, n_epochs=4, gamma=.99, gae_lambda=.95, clip_range=.2, learning_rate=3e-4,
                ent_coef=.0005, max_grad_norm=.5, target_kl=.03, verbose=0, device='cpu',
                policy_kwargs=dict(net_arch=dict(pi=[64, 64], vf=[64, 64]), activation_fn=__import__('torch').nn.Tanh, log_std_init=-.5))
    cb = Laps(); model.learn(total, callback=cb)
    json.dump({'laps': cb.laps}, open(OUT / 'sb3_laps.json', 'w'))
