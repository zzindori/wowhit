# 자료실 '전통 수채화 화투 48장 한지 콜라주.png'(1720×914, 4줄 × 12장)를 한 장씩 잘라 webp로.
# 그림 속 자리 → 월·순서는 POS. 빨간 테두리 바깥을 기준으로 자름.
import sys
from pathlib import Path
from PIL import Image
import numpy as np

SRC = Path.home() / 'dev/workspace/tgbot/uploads/web/전통 수채화 화투 48장 한지 콜라주.png'
OUT = Path(__file__).resolve().parents[2] / 'public/games/gostop/cards'
W, H = 200, 300  # 저장 크기(2:3)

# (줄, 시작 칸) → 월. 그 월의 4장은 칸 순서대로 0~3
POS = {(0, 0): 1, (0, 4): 5, (0, 8): 9, (1, 0): 2, (1, 4): 6, (1, 8): 10,
       (2, 0): 3, (2, 4): 7, (2, 8): 11, (3, 0): 4, (3, 4): 8, (3, 8): 12}

im = Image.open(sys.argv[1] if len(sys.argv) > 1 else SRC).convert('RGB')
a = np.asarray(im).astype(int)
red = (a[..., 0] > 170) & (a[..., 1] < 110) & (a[..., 2] < 100)

def runs(prof, thr, gap):
    on = prof > thr
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        if not v and s is not None: out.append([s, i - 1]); s = None
    if s is not None: out.append([s, len(on) - 1])
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] < gap: merged[-1][1] = r[1]
        else: merged.append(r)
    return merged

rows = runs(red.sum(1), 900, 3)            # 위·아래 테두리 줄이 번갈아
rows = [(rows[i][0], rows[i + 1][1]) for i in range(0, len(rows), 2)]
# 세로는 띠 그림이 테두리처럼 잡혀서 재 둔 값 그대로(왼쪽·오른쪽 테두리 바깥)
cols = list(zip([11, 155, 299, 440, 583, 725, 868, 1010, 1152, 1295, 1438, 1581],
                [141, 285, 426, 568, 711, 853, 995, 1137, 1280, 1423, 1566, 1709]))
assert len(rows) == 4 and len(cols) == 12, (rows, cols)

OUT.mkdir(parents=True, exist_ok=True)
for (r, c0), m in POS.items():
    y0, y1 = rows[r]
    for k in range(4):
        x0, x1 = cols[c0 + k]
        card = im.crop((x0, y0, x1 + 1, y1 + 1)).resize((W, H), Image.LANCZOS)
        card.save(OUT / f'{m:02d}_{k}.webp', quality=88, method=6)
print('rows', rows); print('cols', cols); print('saved 48 →', OUT)
