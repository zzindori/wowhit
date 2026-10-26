# 1월 띠(01_1)에 '청단'이라고 잘못 그려진 것 → '청' 글자 획만 지우고(주변 띠 색으로 번지게) '홍'을 씀.
# cut_cards.py 다음에 돌릴 것(자른 원본을 고침).
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
P = Path(__file__).resolve().parents[2] / 'public/games/gostop/cards/01_1.webp'
im = Image.open(P).convert('RGB')
a = np.asarray(im).astype(float)
x0, y0, x1, y1 = 46, 78, 96, 142            # '청' 글자 자리(200×300 기준)
sub = a[y0:y1, x0:x1]
ink = sub.sum(-1) < 360                      # 검은 획
m = Image.fromarray((ink * 255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
hole = np.asarray(m) > 0
full = np.zeros(a.shape[:2], bool); full[y0:y1, x0:x1] = hole
known = ~full
out = a.copy()
for _ in range(400):                         # 바깥에서 안으로 이웃 평균으로 메움
    acc = np.zeros_like(out); cnt = np.zeros(a.shape[:2])
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        k = np.roll(known, (dy, dx), (0, 1)); v = np.roll(out, (dy, dx), (0, 1))
        acc += v * k[..., None]; cnt += k
    new = (~known) & (cnt > 0)
    out[new] = acc[new] / cnt[new][:, None]
    known = known | new
    if known.all(): break
# 메운 자리에 종이 결 조금
rng = np.random.default_rng(3)
out[full] += rng.normal(0, 4, (full.sum(), 3))
im = Image.fromarray(out.clip(0, 255).astype('uint8'))
# '단'과 같은 먹색으로 '홍'
font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc', 38, index=1)
t = Image.new('RGBA', (70, 70), (0, 0, 0, 0))
ImageDraw.Draw(t).text((35, 35), '홍', font=font, fill=(38, 24, 22, 230), anchor='mm')
t = t.rotate(9, resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.45))
im.paste(t, (36, 74), t)
im.save(P, quality=88, method=6)
