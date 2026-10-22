# g/*.png (cap_main.py · cap_scenes.py 결과) → public/games/stack/guide/*.webp
from PIL import Image
D = '../../public/games/stack/guide'
def sv(n, w, q=82):
    im = Image.open(f'g/{n}.png').convert('RGB'); h = round(im.size[1]*w/im.size[0])
    im.resize((w, h), Image.LANCZOS).save(f'{D}/{n.replace("_", "-")}.webp', quality=q)
sv('main', 900)
for n in ['ev_deliv', 'ev_vip', 'ev_thief', 'ev_broken', 'ev_gold']: sv(n, 420)
for i in range(1, 11): sv(f'floor{i}', 600)
