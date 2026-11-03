#!/usr/bin/env python3
"""jjWay 📺 영상 데이터 갱신(Gemini 없이): public/games/jjway/yt/*.json
- 유튜브 제목·채널·조회수·썸네일·날짜를 다시 받음(유튜브 개발자 정책: API로 받은 정보는 30일 안에 새로 받거나 지우기) — 지워진·비공개 영상은 뺌
- 구글 장소 ID로 좌표·영업 상태를 다시 받음(구글 약관: 좌표는 30일까지) — 폐업·없어진 곳은 뺌
- 'ref'에 갱신 날짜. 게임은 ref가 31일 넘게 지나면 위치를 안 씀(안전장치)
키: ~/.secrets/itne.env YOUTUBE_API_KEY(시험용 — jjWay용 키 생기면 바꿀 것), ~/.secrets/jjway.env GMAPS_KEY
python3 scripts/jjway/yt/refresh.py"""
import json, os, glob, time, urllib.request, urllib.parse, urllib.error
def env(f, k): return [l.split('=', 1)[1].strip() for l in open(os.path.expanduser(f)) if l.startswith(k + '=')][0]
YT, GMAP = env('~/.secrets/itne.env', 'YOUTUBE_API_KEY'), env('~/.secrets/jjway.env', 'GMAPS_KEY')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../public/games/jjway/yt'))
def get(url, headers={}):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60))
for path in sorted(glob.glob(os.path.join(ROOT, '*.json'))):
    d = json.load(open(path)); before = json.dumps(d, sort_keys=True)
    ids = [v['id'] for v in d['videos']]; got = {}
    for i in range(0, len(ids), 50):
        r = get('https://www.googleapis.com/youtube/v3/videos?' + urllib.parse.urlencode({'part': 'snippet,statistics', 'id': ','.join(ids[i:i + 50]), 'key': YT}))
        for it in r.get('items', []): got[it['id']] = it
    keep, gone, closed = [], 0, 0
    for v in d['videos']:
        it = got.get(v['id'])
        if not it: gone += 1; continue
        sn = it['snippet']; v.update(title=sn['title'], ch=sn['channelTitle'], views=int(it['statistics'].get('viewCount', 0)), date=sn['publishedAt'][:10],
                                     thumb=(sn['thumbnails'].get('medium') or sn['thumbnails'].get('default'))['url'])
        pl = []
        for p in v['places']:
            try:
                q = get(f"https://places.googleapis.com/v1/places/{urllib.parse.quote(p['g'])}", {'X-Goog-Api-Key': GMAP, 'Referer': 'https://wowhit.org/', 'X-Goog-FieldMask': 'id,location,businessStatus'})
            except urllib.error.HTTPError as e:
                if e.code == 404: closed += 1; continue   # 없어진 장소
                raise
            if q.get('businessStatus') == 'CLOSED_PERMANENTLY': closed += 1; continue
            if q.get('id') and q['id'] != p['g']: p['g'] = q['id']   # 장소 ID가 바뀌었으면 새 것으로
            p['lat'], p['lon'] = q['location']['latitude'], q['location']['longitude']; pl.append(p)
        v['places'] = pl
        if pl: keep.append(v)
    d['videos'] = keep; d['ref'] = time.strftime('%Y-%m-%d')
    json.dump(d, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(f"{os.path.basename(path)}: 영상 {len(keep)} (지워진 영상 {gone}) · 곳 {sum(len(v['places']) for v in keep)} (폐업·없어짐 {closed}) · 바뀜 {'예' if json.dumps(d, sort_keys=True) != before else '아니오'}")
