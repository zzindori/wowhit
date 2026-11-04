#!/usr/bin/env python3
"""jjWay places.json 만들기: cities_seed.txt(사람이 고른 목록) → 위키데이터 좌표 → 구글 장소 ID → 검증.

  python3 build_places.py wd      # 위키데이터 좌표만(무료). cache_wd.json에 저장, 문제 있으면 표로 출력
  python3 build_places.py google  # 장소 ID(한 번도 안 찾은 것만). GMAPS_KEY 필요, 호출 수 제한 --max
  python3 build_places.py write   # 시코쿠 기존 데이터 + 새 데이터 → public/games/jjway/places.json

좌표는 위키데이터(CC0)만 저장. 구글은 장소 ID만 저장(약관상 좌표·평점은 오래 저장 안 함).
기존 도시·명소의 순서·id는 절대 안 바꿈(사용자 기록 키가 도시id:번호).
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, 'cities_seed.txt')
OUT = os.path.join(HERE, '../../public/games/jjway/places.json')
MAP = os.path.join(HERE, '../../public/games/jjway/map.json')
CW = os.path.join(HERE, 'cache_wd.json')
CG = os.path.join(HERE, 'cache_gid.json')
UA = {'User-Agent': 'jjWay-places/1.0 (https://wowhit.org; zzindori hobby project)'}


def parse():
    prefs, foods, cities, pref, region, city = [], {}, [], None, None, None
    for raw in open(SEED, encoding='utf8'):
        ln = raw.strip()
        if not ln or ln.startswith('# jjWay') or ln.startswith('# 현:') or ln.startswith('# 지역'):
            continue
        p = [x.strip() for x in ln[1:].split('|')]
        if ln[0] == '#':
            pref, region = p[0], p[1]
            if pref not in prefs: prefs.append(pref)
        elif ln[0] == '%':
            foods[pref] = [x.strip() for x in ln[1:].split(',')]
        elif ln[0] == '@':
            f = p[4].split() if len(p) > 4 else []
            city = {'id': p[0], 'ko': p[1], 'ja': p[2], 'pref': pref, 'region': region, 'intro': p[3], 'spots': []}
            if 'big' in f: city['big'] = 1
            if 'ferry' in f: city['ferry'] = True
            q = [x for x in f if re.fullmatch(r'Q\d+', x)]
            if q: city['q'] = q[0]
            cities.append(city)
        elif ln[0] == '-':
            f = p[4].split() if len(p) > 4 else []
            s = {'ko': p[0], 'ja': p[1], 't': p[2], 'd': p[3]}
            if 'ferry' in f: s['ferry'] = True
            q = [x for x in f if re.fullmatch(r'Q\d+', x)]
            if q: s['q'] = q[0]
            city['spots'].append(s)
    return prefs, foods, cities


def get(url, headers=None, data=None):
    for i in range(4):
        try:
            rq = urllib.request.Request(url, headers={**UA, **(headers or {})}, data=data)
            return json.load(urllib.request.urlopen(rq, timeout=30))
        except Exception as e:
            err = e
            time.sleep(2 + i * 3)
    raise err


API = 'https://www.wikidata.org/w/api.php?'


def wd_search(q, lang='ja'):
    r = get(API + urllib.parse.urlencode({'action': 'wbsearchentities', 'search': q, 'language': lang, 'uselang': lang, 'type': 'item', 'limit': 12, 'format': 'json'}))
    return [x['id'] for x in r.get('search', [])]


def wd_ents(ids):
    if not ids: return {}
    r = get(API + urllib.parse.urlencode({'action': 'wbgetentities', 'ids': '|'.join(ids[:50]), 'props': 'claims|labels|aliases|sitelinks', 'languages': 'ja|ko|en', 'format': 'json'}))
    out = {}
    for k, e in r.get('entities', {}).items():
        c = e.get('claims', {}).get('P625')
        if not c: continue
        try: v = c[0]['mainsnak']['datavalue']['value']
        except KeyError: continue
        out[k] = {'lat': v['latitude'], 'lon': v['longitude'], 'ja': e.get('labels', {}).get('ja', {}).get('value', ''),
                  'al': [a['value'] for a in e.get('aliases', {}).get('ja', [])], 'n': len(e.get('sitelinks', {})),
                  'p31': [x['mainsnak'].get('datavalue', {}).get('value', {}).get('id') for x in e.get('claims', {}).get('P31', [])]}
    return out


def km(a, b):
    return math.hypot((a['lon'] - b['lon']) * 91.19, (a['lat'] - b['lat']) * 110.57)


def clean(q):
    return re.sub(r'\s*[（(].*?[)）]\s*', '', q).strip()


def pick(name, cen=None, maxkm=None, want=None):
    """이름으로 찾고, 라벨이 정확히 같은 것 > 가까운 것 > 문서 많은 것."""
    q = clean(name)
    ids = wd_search(name) if q != name else []
    ids += [i for i in wd_search(q) if i not in ids]
    es = wd_ents(ids)
    best, bs = None, -1e9
    for k, e in es.items():
        d = km(e, cen) if cen else 0
        if maxkm and d > maxkm: continue
        exact = e['ja'] == q or e['ja'] == name or q in e['al']
        if not exact and q not in e['ja'] and e['ja'] not in q: continue
        if want and want not in e['p31'] and not exact: continue
        s = (100 if exact else 0) + e['n'] * .5 - d * .5
        if s > bs: best, bs = {**e, 'wd': k, 'km': round(d, 1), 'exact': exact}, s
    return best


# 도·현 경계 판정(map.json — 1:1000만 정도라 해안에선 조금 어긋날 수 있음 → 가장 가까운 현까지 봄)
def load_adm():
    m = json.load(open(MAP, encoding='utf8')); q = m['proj']['q']; polys = {}
    for a in m['adm']:
        if a['c'] != 'JPN': continue
        rings = []
        for r in a['r']:
            x, y, pts = r[0], r[1], []
            pts.append((x / q, y / q))
            for i in range(2, len(r), 2):
                x += r[i]; y += r[i + 1]; pts.append((x / q, y / q))
            rings.append(pts)
        polys[a['ko']] = rings
    return polys, m['proj']


def inpoly(px, py, rings):
    c = False
    for pts in rings:
        for i in range(len(pts)):
            x1, y1 = pts[i]; x2, y2 = pts[i - 1]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
    return c


def pref_of(lat, lon, polys, pr):
    x, y = (lon - pr['lon0']) * pr['kx'], -(lat - pr['lat0']) * pr['ky']
    for k, r in polys.items():
        if inpoly(x, y, r): return k
    return None


def cmd_wd():
    prefs, foods, cities = parse()
    c = json.load(open(CW)) if os.path.exists(CW) else {}
    polys, pr = load_adm(); bad = []
    for ci in cities:
        ck = 'city:' + ci['ja'] + ':' + ci['pref']
        if ck not in c:
            if ci.get('q'):
                e = wd_ents([ci['q']]).get(ci['q']); hit = {**e, 'wd': ci['q'], 'km': 0, 'exact': True} if e else None
            else:
                hit = pick(ci['ja'])
            if hit: c[ck] = hit
            time.sleep(.15)
        h = c.get(ck)
        if not h: bad.append(('도시 없음', ci['ko'], ci['ja'], '')); continue
        pf = pref_of(h['lat'], h['lon'], polys, pr)
        if pf != ci['pref']: bad.append(('현 다름?', ci['ko'], ci['ja'], f"{pf} ({h['lat']:.3f},{h['lon']:.3f}) {h['wd']}"))
        for s in ci['spots']:
            sk = 'spot:' + ci['id'] + ':' + s['ja']
            if sk not in c:
                R = 70 if ci['id'] in ('tokyo', 'shari', 'kushiro', 'hirosaki') else 45
                if s.get('q'):
                    e = wd_ents([s['q']]).get(s['q'])
                    hit = {**e, 'wd': s['q'], 'km': round(km(e, h), 1), 'exact': True} if e else None
                else:
                    hit = pick(s['ja'], h, R)
                if hit: c[sk] = hit
                time.sleep(.15)
            e = c.get(sk)
            if not e: bad.append(('명소 없음', ci['ko'], s['ko'], s['ja']))
            elif e['km'] > 25: bad.append(('멀음', ci['ko'], s['ko'], f"{e['km']}km {e['ja']} {e['wd']}"))
            elif not e['exact']: bad.append(('이름 다름', ci['ko'], s['ko'], f"{s['ja']} → {e['ja']} {e['wd']} {e['km']}km"))
        json.dump(c, open(CW, 'w'), ensure_ascii=False)
    print(f'도시 {len(cities)} · 명소 {sum(len(x["spots"]) for x in cities)} · 문제 {len(bad)}')
    for b in bad: print(' | '.join(map(str, b)))


def gsearch(q, lat, lon, key, rad):
    body = json.dumps({'textQuery': q, 'languageCode': 'ko', 'locationBias': {'circle': {'center': {'latitude': lat, 'longitude': lon}, 'radius': rad}}, 'pageSize': 10}).encode()
    return get('https://places.googleapis.com/v1/places:searchText', {
        'Content-Type': 'application/json', 'X-Goog-Api-Key': key, 'Referer': 'https://wowhit.org/',
        'X-Goog-FieldMask': 'places.id,places.displayName,places.location,places.userRatingCount,places.types'}, body).get('places', [])


def cmd_google():
    mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 500
    key = next(l.split('=', 1)[1].strip() for l in open(os.path.expanduser('~/.secrets/jjway.env')) if l.startswith('GMAPS_KEY'))
    _, _, cities = parse(); w = json.load(open(CW)); g = json.load(open(CG)) if os.path.exists(CG) else {}; n = 0
    for ci in cities:
        for s in ci['spots']:
            k = ci['id'] + ':' + s['ja']; e = w.get('spot:' + k)
            if not e or k in g: continue
            if n >= mx: print('호출 상한', mx); json.dump(g, open(CG, 'w'), ensure_ascii=False, indent=0); return
            wide = s['t'] in ('view', 'mountain', 'valley', 'sea', 'island', 'onsen', 'town', 'garden', 'ruins', 'market')
            lim = 3000 if wide else 800
            ps = gsearch(clean(s['ja']), e['lat'], e['lon'], key, 1000.0); n += 1; best, bs = None, -1
            for p in ps:
                d = km({'lat': p['location']['latitude'], 'lon': p['location']['longitude']}, e) * 1000
                if d > lim or 'parking' in p.get('types', []): continue
                sc = (p.get('userRatingCount', 0) + 1) / (1 + d / 100)
                if sc > bs: best, bs = {'g': p['id'], 'name': p['displayName']['text'], 'm': round(d), 'rv': p.get('userRatingCount', 0)}, sc
            g[k] = best
            time.sleep(.05)
    json.dump(g, open(CG, 'w'), ensure_ascii=False, indent=0)
    print('구글 호출', n, '· 짝 있음', sum(1 for v in g.values() if v), '/', len(g))


def cmd_write():
    prefs, foods, cities = parse(); w = json.load(open(CW)); g = json.load(open(CG)) if os.path.exists(CG) else {}
    old = json.load(open(OUT, encoding='utf8'))
    SH = json.load(open(os.path.join(HERE, 'cache_shore.json'))) if os.path.exists(os.path.join(HERE, 'cache_shore.json')) else {}
    keep = [c for c in old['cities'] if c.get('region') == 'shikoku' and not any(c['id'] == x['id'] for x in cities)]
    if not keep or any(c['id'] in {'tokyo', 'kyoto'} for c in keep): raise SystemExit('기존 시코쿠 도시 확인 필요')
    out = []
    for ci in cities:
        h = w.get('city:' + ci['ja'] + ':' + ci['pref'])
        if not h: print('뺌(도시):', ci['ko']); continue
        c = {k: ci[k] for k in ('id',)}; c.update(wd=h['wd'], ko=ci['ko'], ja=ci['ja'], pref=ci['pref'], region=ci['region'], lat=round(h['lat'], 6), lon=round(h['lon'], 6), intro=ci['intro'])
        for f in ('big', 'ferry'):
            if ci.get(f): c[f] = ci[f]
        c['spots'] = []
        for s in ci['spots']:
            e = w.get('spot:' + ci['id'] + ':' + s['ja'])
            if not e: print('뺌(명소):', ci['ko'], s['ko']); continue
            sh = SH.get(ci['id'] + ':' + clean(s['ja']))   # 물 위 좌표면 물가로(shore.py)
            n = {'ko': s['ko'], 'ja': clean(s['ja']), 't': s['t'], 'lat': round(sh['lat'] if sh else e['lat'], 6), 'lon': round(sh['lon'] if sh else e['lon'], 6), 'wd': e['wd']}
            gg = g.get(ci['id'] + ':' + s['ja'])
            if gg: n['g'] = gg['g']
            if s.get('ferry'): n['ferry'] = True
            n['d'] = s['d']; c['spots'].append(n)
        if c['spots']: out.append(c)
        else: print('뺌(명소 0):', ci['ko'])
    for c in keep:   # 큰 도시 표시만 더함(순서·명소는 그대로)
        if c['id'] in ('takamatsu', 'matsuyama', 'tokushima', 'kochi'): c['big'] = 1
    allc = out + keep
    d = {'checked': time.strftime('%Y-%m-%d'), 'source': '도시·명소 좌표와 이름: 위키데이터(CC0, 호수·바다 명소는 가장 가까운 물가로 옮김) · 소개 글은 jjWay가 직접 작성', 'regions': {'hokkaido': '홋카이도', 'tohoku': '도호쿠', 'kanto': '간토', 'chubu': '주부', 'kansai': '간사이', 'chugoku': '주고쿠', 'shikoku': '시코쿠', 'kyushu': '규슈·오키나와'},
         'prefs': prefs_order(prefs), 'foods': {**old['foods'], **foods}, 'cities': allc}
    json.dump(d, open(OUT, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('도시', len(allc), '· 명소', sum(len(c['spots']) for c in allc), '· 큰 도시', sum(1 for c in allc if c.get('big')), '· 구글 ID 있는 명소', sum(1 for c in allc for s in c['spots'] if s.get('g')), '· 파일', os.path.getsize(OUT) // 1024, 'KB')


def prefs_order(prefs):
    # 시코쿠 4현은 주고쿠 뒤·규슈 앞(북 → 남)
    sk = ['가가와현', '에히메현', '도쿠시마현', '고치현']
    base = [p for p in prefs if p not in sk]
    i = base.index('후쿠오카현')
    return base[:i] + sk + base[i:]


if __name__ == '__main__':
    {'wd': cmd_wd, 'google': cmd_google, 'write': cmd_write}[sys.argv[1]]()
