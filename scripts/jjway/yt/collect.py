#!/usr/bin/env python3
"""jjWay 📺 유튜브·쇼츠 추천 모으기(시험): 도시 하나 → 유튜브 검색(한국어·일본어) → Gemini가 영상을 직접 보고 나온 곳 뽑기 → 구글 장소 검색으로 짝 맞추기.
저장: 영상 정보(제목·채널·조회수·썸네일 주소·길이)와 나온 곳(이름·장면 시각·한 줄 이유·구글 장소 ID). 영상 자체는 저장 안 함.
키는 ~/.secrets(소스에 안 넣음): YOUTUBE_API_KEY·GEMINI_API_KEY = itne.env(시험용), GMAPS_KEY = jjway.env(웹사이트 제한이라 Referer를 붙임)
python3 scripts/jjway/yt/collect.py 도시id [영상 수] → raw/도시id.json(git 안 올림) → export.py 도시id"""
import json, os, sys, re, math, time, urllib.request, urllib.error, urllib.parse, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
def env(f, k): return [l.split('=', 1)[1].strip() for l in open(os.path.expanduser(f)) if l.startswith(k + '=')][0]
YT, GEM, GMAP = env('~/.secrets/itne.env', 'YOUTUBE_API_KEY'), env('~/.secrets/itne.env', 'GEMINI_API_KEY'), env('~/.secrets/jjway.env', 'GMAPS_KEY')
# 검색어: 다른 곳과 헷갈리는 이름은 현·지방을 붙임. 좌표·이름은 places.json에서
QJA = {'takamatsu': '高松', 'matsuyama': '愛媛 松山', 'kanazawa': '金沢', 'kumamoto': '熊本', 'yufu': '由布院', 'nagasaki': '長崎', 'kagoshima': '鹿児島', 'kurashiki': '倉敷', 'hiroshima': '広島', 'hakodate': '函館', 'takayama': '飛騨高山'}
QKO = {'yufu': '유후인'}
CID = sys.argv[1] if len(sys.argv) > 1 else 'takamatsu'; N = int(sys.argv[2]) if len(sys.argv) > 2 else 16
_c = next(c for c in json.load(open(os.path.join(HERE, '../../../public/games/jjway/places.json')))['cities'] if c['id'] == CID)
city = {'ko': QKO.get(CID, re.sub(r'\s*\(.*', '', _c['ko'])), 'ja': QJA.get(CID, _c['ja'].rstrip('市町村')), 'lat': _c['lat'], 'lon': _c['lon']}

def get(url, data=None, headers={}):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers={'Content-Type': 'application/json', **headers})
    return json.load(urllib.request.urlopen(r, timeout=300))
def yt(path, **q): return get(f'https://www.googleapis.com/youtube/v3/{path}?' + urllib.parse.urlencode({**q, 'key': YT}))

# 1) 영상 찾기: 한국어(한국 여행자) · 일본어(현지인)
vids = {}
for lang, q in [('ko', f"{city['ko']} 맛집"), ('ko', f"{city['ko']} 여행"), ('ja', f"{city['ja']} グルメ"), ('ja', f"{city['ja']} 観光")]:
    r = yt('search', part='snippet', q=q, type='video', maxResults=10, relevanceLanguage=lang, regionCode='KR' if lang == 'ko' else 'JP', order='relevance')
    for it in r.get('items', []): vids.setdefault(it['id']['videoId'], {'q': q, 'lang': lang})
ids = list(vids)
st = {}
for i in range(0, len(ids), 50):
    for it in yt('videos', part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).get('items', []): st[it['id']] = it
def dur(s):
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or ''); return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0
V = []
for vid, meta in vids.items():
    it = st.get(vid)
    if not it: continue
    sn = it['snippet']; t = sn['title'] + ' ' + sn.get('description', '')[:300]
    who = 'ko' if re.search('[가-힣]', sn['title']) else 'ja' if re.search('[ぁ-ゖァ-ヺ]', t) else meta['lang']   # 글쓴이 쪽(제목 글자로) — 채널 나라 정보는 대부분 비어 있음
    d = dur(it['contentDetails'].get('duration'))
    V.append({'id': vid, 'title': sn['title'], 'ch': sn['channelTitle'], 'who': who, 'views': int(it['statistics'].get('viewCount', 0)), 'sec': d, 'short': d <= 180,
              'date': sn['publishedAt'][:10], 'thumb': (sn['thumbnails'].get('medium') or sn['thumbnails'].get('default'))['url']})
V = [v for v in V if v['sec'] <= 1500]   # 25분 넘는 긴 영상은 시험에서 뺌(토큰)
V.sort(key=lambda v: -v['views']); V = V[:N]
RAW = os.path.join(HERE, 'raw', f'{CID}.json'); DONE = []
if os.path.exists(RAW):   # 지난번에 오류 난 영상만 다시 봄(토큰 절약) — 그때 고른 영상 목록 그대로
    old = json.load(open(RAW))['videos']; DONE = [v for v in old if not v.get('err')]; V = [{k: x for k, x in v.items() if k not in ('places', 'err', 'tok')} for v in old if v.get('err')]
print(f'영상 {len(V)}개 (한국 {sum(v["who"]=="ko" for v in V)} · 일본 {sum(v["who"]=="ja" for v in V)} · 쇼츠 {sum(v["short"] for v in V)})', flush=True)

# 2) Gemini가 영상 보기 — 모델은 키로 목록 받아 가장 새 flash(소스에 버전 안 넣음)
ms = get('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', headers={'x-goog-api-key': GEM})['models']
ver = lambda n: float((re.search(r'gemini-(\d+(?:\.\d+)?)-flash$', n) or [0, 0])[1])
MODEL = max((m['name'] for m in ms if ver(m['name']) and 'generateContent' in m.get('supportedGenerationMethods', [])), key=ver)
PROMPT = (f"이 영상은 일본 {city['ja']}({city['ko']}) 주변 여행·맛집 영상이에요. 영상에 실제로 나오는(방문하거나 소개하는) 가게·식당·카페·관광지만 뽑아 주세요. "
          "말로만 스쳐 지나가는 곳, 확실하지 않은 이름은 빼세요. 이름은 간판·자막에 나온 원래 이름(일본어면 일본어) 그대로. "
          'JSON 배열만: [{"name": "원래 이름", "ko": "한글 표기", "area": "있는 시·정·섬 이름(일본어, 예: 琴平町·直島)", "type": "우동집/카페/관광지 등", "t": "처음 나오는 시각 m:ss", "why": "영상에서 말한 좋은 점 한 줄(한국어)"}]')
def watch(v):
    body = {'contents': [{'parts': [{'file_data': {'file_uri': f"https://www.youtube.com/watch?v={v['id']}"}}, {'text': PROMPT}]}],
            'generationConfig': {'responseMimeType': 'application/json', 'temperature': 0}}
    t0 = time.time()
    err = None
    for a in range(3):   # 일시 오류(429·5xx)만 다시
        try:
            r = get(f'https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent', body, {'x-goog-api-key': GEM})
            txt = ''.join(p.get('text', '') for p in r['candidates'][0]['content']['parts'])
            return v, json.loads(txt), r.get('usageMetadata', {}), time.time() - t0, None
        except urllib.error.HTTPError as e:
            err = f'{e.code}'
            if e.code != 429 and e.code < 500: break
            time.sleep(20 * (a + 1))
        except Exception as e: err = str(e)[:120]; break
    return v, [], {}, time.time() - t0, err

# 3) 구글 장소 짝 맞추기: '이름 + 동네(Gemini가 뽑은 시·정·섬)'로, 도시 50km 바이어스, 60km 안일 때만
#    (예전엔 '이름 + 高松'·15km라 고토히라궁이 다카마쓰 시내 같은 이름 작은 신사에, 나오시마 이에 프로젝트가 다카마쓰 가게에 붙었음)
def match(name):
    r = get('https://places.googleapis.com/v1/places:searchText', {'textQuery': name, 'languageCode': 'ko', 'maxResultCount': 1, 'locationBias': {'circle': {'center': {'latitude': city['lat'], 'longitude': city['lon']}, 'radius': 50000}}},
            {'X-Goog-Api-Key': GMAP, 'Referer': 'https://wowhit.org/', 'X-Goog-FieldMask': 'places.id,places.displayName,places.location,places.primaryTypeDisplayName'})
    p = (r.get('places') or [None])[0]
    if not p: return None
    d = math.hypot((p['location']['latitude'] - city['lat']) * 111, (p['location']['longitude'] - city['lon']) * 111 * math.cos(math.radians(city['lat'])))
    return {'g': p['id'], 'gname': p['displayName']['text'], 'km': round(d, 1), 'lat': p['location']['latitude'], 'lon': p['location']['longitude']} if d < 60 else {'far': round(d), 'gname': p['displayName']['text']}

tok = 0
with cf.ThreadPoolExecutor(4) as ex:
    for v, places, use, sec, err in ex.map(watch, V):
        tok += use.get('totalTokenCount', 0)
        v['places'] = []
        for pl in places if isinstance(places, list) else []:
            m = match(f"{pl.get('name', '')} {pl.get('area') or city['ja']}") if pl.get('name') else None
            v['places'].append({**pl, **(m or {})})
        v['err'] = err; v['tok'] = use.get('totalTokenCount', 0)
        ok = sum(1 for p in v['places'] if p.get('g'))
        print(f"{'🇰🇷' if v['who']=='ko' else '🇯🇵'} {'쇼츠' if v['short'] else f'{v['sec']//60}분'} 조회 {v['views']:,} | {v['title'][:40]} → {len(v['places'])}곳(구글 맞음 {ok}) {sec:.0f}초 {v['tok']:,}토큰{' ⚠️ ' + err if err else ''}", flush=True)
os.makedirs(os.path.join(HERE, 'raw'), exist_ok=True)
json.dump({'city': CID, 'model': MODEL, 'at': time.strftime('%Y-%m-%d'), 'videos': DONE + V}, open(RAW, 'w'), ensure_ascii=False, indent=1)
print('모델', MODEL, '· 토큰 합계', f'{tok:,}')
