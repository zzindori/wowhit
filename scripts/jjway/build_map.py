#!/usr/bin/env python3
"""jjWay 지도 데이터 만들기.

입력(받아 둔 폴더): Natural Earth 10m(admin_0 countries · admin_1 · populated_places, 저작권 없음),
OurAirports airports.csv(저작권 없음).
  받기: scripts/jjway/README 참고 — python3 -I build_map.py <데이터 폴더>
출력: public/games/jjway/map.json

좌표: 경도 132·위도 35 기준 정거원통(km). x = 동쪽 km, y = 남쪽 km. 저장은 0.25km 단위 정수, 고리마다 첫 점 + 차이.
"""
import csv, json, math, sys, os

SRC = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '../../public/games/jjway/map.json')
ROUTES = os.path.join(HERE, '../../public/games/jjway/routes.json')

LON0, LAT0 = 132.0, 35.0
KX = 111.32 * math.cos(math.radians(LAT0))
KY = 110.57
Q = 4  # 0.25km

def proj(lon, lat):
    return ((lon - LON0) * KX, -(lat - LAT0) * KY)

# 보이는 범위(조금 넉넉히) — 이웃 나라는 이 밖을 테두리에 붙여 자름
BB = (*proj(116, 48), *proj(152, 21))  # x0, y0, x1, y1
def clampP(p):
    return (min(max(p[0], BB[0]), BB[2]), min(max(p[1], BB[1]), BB[3]))

def dp(pts, tol):
    """더글러스-포이커(반복). 닫힌 고리는 첫 점·가장 먼 점으로 나눠서."""
    if len(pts) < 4:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]; bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        best, bi = -1, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / L if L > 1e-9 else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

def ring_area(r):
    return abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2

def simplify_ring(r, tol):
    if len(r) < 8:
        return r
    # 가장 먼 점으로 둘로 나눠 각각 줄이기(닫힌 고리 처리)
    far = max(range(len(r)), key=lambda i: (r[i][0] - r[0][0]) ** 2 + (r[i][1] - r[0][1]) ** 2)
    a = dp(r[:far + 1], tol)
    b = dp(r[far:] + [r[0]], tol)
    return a[:-1] + b[:-1]

def enc(r):
    out, px, py = [], 0, 0
    for x, y in r:
        ix, iy = round(x * Q), round(y * Q)
        out += [ix - px, iy - py]
        px, py = ix, iy
    return out

def rings_of(geom):
    if geom['type'] == 'Polygon':
        return geom['coordinates']
    if geom['type'] == 'MultiPolygon':
        return [r for poly in geom['coordinates'] for r in poly]
    return []

def in_ring(x, y, r):
    c = False
    j = len(r) - 1
    for i in range(len(r)):
        xi, yi = r[i]; xj, yj = r[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c

def main():
    R = json.load(open(ROUTES, encoding='utf-8'))
    out = {'proj': {'lon0': LON0, 'lat0': LAT0, 'kx': KX, 'ky': KY, 'q': Q}, 'land': {}, 'adm': [], 'places': [], 'airports': {}}

    # 1) 나라 땅
    C = json.load(open(os.path.join(SRC, 'ne_10m_admin_0_countries.geojson')))
    tol = {'KOR': 0.6, 'JPN': 0.6, 'PRK': 2.5, 'CHN': 4, 'RUS': 4, 'TWN': 2}
    minA = {'KOR': 1.5, 'JPN': 1.5}
    stat = {}
    for f in C['features']:
        a3 = f['properties']['ADM0_A3']
        if a3 not in tol:
            continue
        rs = []
        for ring in rings_of(f['geometry']):
            pts = [proj(lon, lat) for lon, lat in ring[:-1]]
            if a3 not in ('KOR', 'JPN'):
                if not any(BB[0] <= x <= BB[2] and BB[1] <= y <= BB[3] for x, y in pts):
                    continue
                pts = [clampP(p) for p in pts]
            if ring_area(pts) < minA.get(a3, 30):
                continue
            s = simplify_ring(pts, tol[a3])
            if len(s) >= 3:
                rs.append(enc(s))
        out['land'][a3] = rs
        stat[a3] = sum(len(r) // 2 for r in rs)

    # 2) 도·현 (한국·일본)
    A = json.load(open(os.path.join(SRC, 'ne_10m_admin_1_states_provinces.geojson')))
    adm_raw = []
    for f in A['features']:
        p = f['properties']
        if p.get('adm0_a3') not in ('KOR', 'JPN'):
            continue
        raw = [[proj(lon, lat) for lon, lat in r[:-1]] for r in rings_of(f['geometry'])]
        adm_raw.append((p, raw))
        rs = [enc(simplify_ring(r, 1.2)) for r in raw if ring_area(r) > 4]
        cx = sum(x for r in raw for x, _ in r) / max(1, sum(len(r) for r in raw))
        cy = sum(y for r in raw for _, y in r) / max(1, sum(len(r) for r in raw))
        big = max(raw, key=ring_area)  # 이름 자리 = 가장 큰 섬의 무게중심
        bx = sum(x for x, _ in big) / len(big); by = sum(y for _, y in big) / len(big)
        out['adm'].append({'c': p['adm0_a3'], 'ko': p.get('name_ko') or p.get('name'), 'ja': p.get('name_ja') or '',
                           'lx': round(bx, 1), 'ly': round(by, 1), 'r': [r for r in rs if len(r) >= 6]})
    stat['adm'] = sum(len(r) // 2 for a in out['adm'] for r in a['r'])

    def pref_of(x, y):
        for p, raw in adm_raw:
            for r in raw:
                if in_ring(x, y, r):
                    return p.get('name_ko') or p.get('name')
        # 바다 위 공항(간사이·주부 등) → 가장 가까운 도·현
        best, bn = 1e18, ''
        for p, raw in adm_raw:
            for r in raw:
                for px, py in r[::5]:
                    d = (px - x) ** 2 + (py - y) ** 2
                    if d < best:
                        best, bn = d, p.get('name_ko') or p.get('name')
        return bn

    # 3) 도시
    P = json.load(open(os.path.join(SRC, 'ne_10m_populated_places.geojson')))
    for f in P['features']:
        p = f['properties']
        if p.get('ADM0_A3') not in ('KOR', 'JPN'):
            continue
        x, y = proj(p['LONGITUDE'], p['LATITUDE'])
        ko = (p.get('NAME_KO') or p['NAME'])
        out['places'].append({'c': p['ADM0_A3'], 'ko': ko, 'ja': p.get('NAME_JA') or '', 'x': round(x, 1), 'y': round(y, 1),
                              'pop': p.get('POP_MAX') or 0, 'rank': p.get('SCALERANK', 9)})
    out['places'].sort(key=lambda d: -d['pop'])

    # 4) 공항 좌표
    want = set(R['kr']) | set(R['jp'])
    with open(os.path.join(SRC, 'airports.csv'), encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            code = row['iata_code']
            if code in want and row['iso_country'] in ('KR', 'JP') and code not in out['airports']:
                x, y = proj(float(row['longitude_deg']), float(row['latitude_deg']))
                out['airports'][code] = {'x': round(x, 1), 'y': round(y, 1), 'pref': pref_of(x, y),
                                         'c': 'KOR' if row['iso_country'] == 'KR' else 'JPN'}
    miss = want - set(out['airports'])
    if miss:
        sys.exit(f'공항 좌표 없음: {miss}')

    js = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    open(OUT, 'w', encoding='utf-8').write(js)
    print('points', stat, 'places', len(out['places']), 'airports', len(out['airports']), 'bytes', len(js.encode()))

main()
