#!/usr/bin/env python3
"""collect.py 결과(raw/도시id.json) → 게임 파일(public/games/jjway/yt/도시id.json).
구글 짝이 있고 60km 안인 곳만. 구글이 이름만 비슷한 다른 가게를 고른 경우를 거르려고 Gemini에게 '같은 곳인가'를 한 번에 물어 아닌 것은 뺌(이름 글자만 봄).
python3 scripts/jjway/yt/export.py 도시id"""
import json, math, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); CID = sys.argv[1]
def env(f, k): return [l.split('=', 1)[1].strip() for l in open(os.path.expanduser(f)) if l.startswith(k + '=')][0]
GEM = env('~/.secrets/itne.env', 'GEMINI_API_KEY')
d = json.load(open(os.path.join(HERE, 'raw', CID + '.json')))
def post(url, data):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, json.dumps(data).encode(), {'Content-Type': 'application/json', 'x-goog-api-key': GEM}), timeout=180))
cand = [p for v in d['videos'] for p in v['places'] if p.get('g')]
bad = set()
# --drop 이름,이름: Gemini를 못 쓸 때 사람이 목록을 보고 뺄 것만 지정(자동 확인 안 함)
DROP = sys.argv[sys.argv.index('--drop') + 1].split(',') if '--drop' in sys.argv else None
if DROP is not None:
    for p in cand:
        if p.get('name') in DROP: bad.add(id(p)); print('뺌:', p.get('name'), '→', p.get('gname'))
for i in range(0, 0 if DROP is not None else len(cand), 60):
    part = cand[i:i + 60]
    q = '\n'.join(f"{j}. 영상: {p.get('name')} ({p.get('ko')}, {p.get('type')}, {p.get('area')}) / 지도: {p.get('gname')}" for j, p in enumerate(part))
    r = post(f"https://generativelanguage.googleapis.com/v1beta/{d['model']}:generateContent", {'contents': [{'parts': [{'text': '각 줄의 영상 속 장소 이름과 지도 검색 결과가 같은 장소로 보이는지 판단하세요. 표기(한글·일본어·영어)가 달라도 같은 곳이면 같음. 이름이 분명히 다른 곳의 번호만 JSON 숫자 배열로 답하세요. 없으면 [].\n' + q}]}], 'generationConfig': {'responseMimeType': 'application/json', 'temperature': 0}})
    for j in json.loads(''.join(x.get('text', '') for x in r['candidates'][0]['content']['parts'])):
        if 0 <= j < len(part): bad.add(id(part[j])); print('뺌:', part[j].get('name'), '→', part[j].get('gname'))
C0 = next(c for c in json.load(open(os.path.join(HERE, '../../../public/games/jjway/places.json')))['cities'] if c['id'] == CID)
near = lambda q: 'lat' in q and math.hypot((q['lat'] - C0['lat']) * 111, (q['lon'] - C0['lon']) * 111 * math.cos(math.radians(C0['lat']))) <= 40
vids = []; seen_err = 0; off = 0
for v in d['videos']:
    if v.get('err'): seen_err += 1
    pl = []
    for p in v['places']:
        if p.get('g') and id(p) not in bad:
            pl.append({k: p[k] for k in ('name', 'ko', 'area', 'type', 't', 'why', 'g', 'lat', 'lon') if k in p})
    # 다른 도시 영상이 검색에 섞인 것 빼기: 나온 곳의 절반 넘게 도시에서 40km 밖이면 이 도시 영상이 아님(예: 오즈 검색에 마쓰야마 영상)
    if pl and sum(near(q) for q in pl) * 2 < len(pl): off += 1; print('다른 도시 영상:', v['title'][:50]); continue
    if pl:
        vids.append({**{k: v[k] for k in ('id', 'title', 'ch', 'who', 'views', 'sec', 'short', 'date', 'thumb')}, 'places': pl})
out = {'city': CID, 'at': d['at'], 'note': '영상 링크·요약·장면 시각은 우리 것, 좌표는 구글(30일 안에 다시 받기 — refresh.py)', 'videos': vids, 'ref': time.strftime('%Y-%m-%d')}
path = os.path.join(HERE, '../../../public/games/jjway/yt', CID + '.json')
json.dump(out, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
print(f"{CID}: 영상 {len(vids)}/{len(d['videos'])} (오류 {seen_err}) · 곳 {sum(len(v['places']) for v in vids)} (후보 {len(cand)}, 뺌 {len(bad)}) · {os.path.getsize(path)//1024}KB")
