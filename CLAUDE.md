# wowhit 포트폴리오 사이트

## Claude에게
이 프로젝트에서 작업을 마칠 때마다 반드시 아래 **작업 히스토리** 섹션에 날짜와 작업 내용을 추가하고 `git push`까지 완료할 것. 사용자가 요청하지 않아도 자동으로 수행한다.

## 프로젝트 개요
- **URL**: https://wowhit.vercel.app (Vercel 자동 배포, main 브랜치 push 시 갱신)
- **GitHub**: https://github.com/zzindori/wowhit
- **APK 배포**: https://github.com/zzindori/wowhit-releases (릴리스로 APK 관리)
- **기술 스택**: Nuxt 4 + Nuxt UI + Tailwind CSS
- **커스텀 도메인**: wowhit.org (Cloudflare DNS)

## 구조
- `app/data/apps.ts` — 앱 목록 데이터 (여기만 수정하면 카드/상세 자동 반영)
- `app/data/prints.ts` — 3D 프린팅 갤러리 데이터 (카테고리·이미지·MakerWorld 링크)
- `app/pages/index.vue` — 메인 페이지 (앱 카드 + 하단 3D 대표 미리보기)
- `app/pages/[slug].vue` — 앱 상세 페이지 (댓글 포함)
- `app/pages/3d.vue` — 3D Printing 갤러리 (카테고리별 섹션)
- `app/components/AppLogo.vue` — 헤더 로고
- `app/app.vue` — 전체 레이아웃 (헤더: 이용 안내·3D·QR, 푸터)
- `app/pages/guide.vue` — 이용 안내 페이지 (홈 화면 추가, 이용권/API키 사용법, Gemini 가격)
- `public/prints/` — 3D 작품 썸네일 이미지 (slug 파일명 권장)
- `server/api/comments/` — 댓글 Vercel 프록시 → api.wowhit.org

## 인프라
- **포트폴리오** (wowhit.org, wowhit.vercel.app): Vercel 배포, 집 서버 불필요
- **웹앱 subdomain** (`*.wowhit.org`, api 제외): Cloudflare Redirect Rules → Vercel/Firebase/GitHub Pages
  - redirect 매핑 원본: `/home/zzindori/dev/server/wowhit-api/redirect.js` (참고용, 서비스 비활성화됨)
  - DNS: 각 subdomain `A 192.0.2.1` proxied (터널 CNAME 아님)
- **댓글 API** (api.wowhit.org): Cloudflare Tunnel → 집 서버 `wowhit-api` (포트 3001)
  - 코드: `/home/zzindori/dev/server/wowhit-api/index.js`
  - 관리자 삭제 암호: `wowhit-api/.env` → `WOWHIT_ADMIN_PASSWORD`
  - systemd: `wowhit-api.service`, `cloudflared.service`

## 3D Printing 추가 방법
1. 이미지를 `public/prints/슬러그.jpg`로 저장
2. `app/data/prints.ts`에 항목 추가 (`category`: motorcycle | diorama | figurine | accessory)
3. MakerWorld 모델이면 `makerWorldUrl` 추가
4. 추가 사진 있으면 `images: ['/prints/...']` (카드 클릭 시 갤러리 모달)
5. 메인 대표 노출은 `featuredPrintSlugs` 배열 수정

## APK 업로드 방법

### 태그 규칙
`{appname-lowercase}-v{version}.{build}` (예: `careway-v1.1.1.16`, `itne-v1.5.5.32`)

### 업로드 절차
1. 각 앱에서 `flutter build apk --release`
2. APK를 앱 이름으로 복사: `cp app-release.apk /tmp/앱이름.apk`
3. wowhit-releases에 릴리스 생성:
```bash
gh release create [앱명소문자]-v[버전].[빌드] /tmp/앱이름.apk \
  --repo zzindori/wowhit-releases \
  --title "[앱명] v[버전].[빌드]" \
  --notes "변경 사항 설명"
```
4. `apps.ts`의 해당 앱 `apkUrl`과 `version` 업데이트:
```
apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/[태그]/앱이름.apk'
version: 'x.y.z+build'
```
5. `git push` → Vercel 자동 배포

### 주의
- **절대 APK를 소스 repo에 커밋하지 않는다** (용량 초과 + private repo는 다운로드 404)
- wowhit-releases는 공개(public) repo — private이면 릴리스 assets 다운로드 불가
- 기존 릴리스 교체 시: `gh release delete {old-tag} --repo zzindori/wowhit-releases --yes`

## 쌓고팔기(public/games/stack) 남은 할 일
- **충돌 범위**: 프린터(생산기)·판매대는 2026-10-20에 넣음(`collide()` → `pushOut()`, 일꾼은 `detour()`로 프린터 사이 통로 경유).
  돈더미 등 나머지는 그림 넣을 때 같이 — `collide()`에 `pushOut()` 한 줄 추가(범위는 그림보다 약간 작게, 벽 따라 미끄러짐)
- 주제(테마): 한국 상가 건물로 가는 중(2026-10-20 사용자 동의) — 층마다 다른 가게(1층 분식·2층 붕어빵·3층 치킨·4층 편의점·5층 한강라면(PC방 대신, 사용자 결정 — 즉석 라면 조리기·은박 그릇)·6층 노래방), 위는 '공사 중'.
  테마는 6층까지(사용자 확정), 7층부터는 원래 스타일(3D 프린터 + KINDS 기본 물건) — `THEMES` 1~6층 완성(2026-10-20). 실제 브랜드명·로고는 쓰지 않음.
  제목 '층층이'(부제 '쌓고 팔고, 빨리빨리!') 확정. 시안: 자료실 '층층이_상가건물시안'·'층층이_1-3층가게시안'

## 작업 히스토리

### 2026-10-20
- 쌓고팔기 VIP 벌칙 다시 변경(20%→회복은 체감 안 됨): 10초 동안 고정 속도 = 일꾼 속도 × 60%(`CFG.vip.slowSpd`, 약 57) — 업그레이드와 상관없이 일꾼보다 느림. `slowMin`·회복 곡선 삭제
- 쌓고팔기 금고 ↔ 야간 금고 칸 자리 맞바꿈(사용자 요청): 금고(SAFE) 645,370 · 야간 금고 칸(AWAY_PAD) 500,370, 자동 수금 645,250 그대로.
  금고 상자가 돈더미 밑 '자동 수금' 글자(CASH.y+58)를 덮던 문제도 같이 해결. (자동 수금↔야간 금고 칸을 바꿨던 건 잘못 이해한 것 → 되돌림)
- 쌓고팔기 '야간 금고' 칸 이름 → '잔업(오프라인)'(사용자 요청 — 칸과 금색 '금고' 상자가 둘 다 금고라 헷갈림). 금색 상자 이름은 '잔업수당'(바닥 글자·토스트·설명, 글자는 상자 너비에 맞춰 줄임). 코드 id `away`·`SAFE`·저장값(`Z.safe`)은 그대로
  잔업수당 상자 그림: 비었으면 회색 닫힌 상자(자물쇠도 회색), 돈 있으면 금색 상자 + 위에 금화 더미(최대치 대비 1~6개) + 반짝임 ✦
- 쌓고팔기 잔업 못 받는 이유 표시('2·3층 중 한 층만 생긴다' 문의): 일꾼 0명이거나 생산기가 전부 고장·부서지면 그 층은 0원(설계대로 — 고장은 꺼 둔 동안에도 남음).
  `awayWhy(Z)` → 복귀 토스트 끝에 '못 받음: 2층(생산기 고장) 3층(일꾼 없음)', 빈 잔업수당 상자 밑에 빨간 '잔업 멈춤 · 이유'
- 쌓고팔기 효과(보는 맛) 1차 — 그림 없이 코드로, 그림 넣어도 그대로 유지:
  파티클 `burst()`(spark/conf/dust)·`ring()`, 지갑으로 날아가는 동전 `coinsToWallet()`(도착 시 돈 칩 튀기 .bump + 짤랑), 화면 흔들림 `shake()`(toS에 SHK 더함),
  가운데 배너 `showBanner()`(줄 세움 bannerQ), 돈 숫자 촤르륵(`dispMoney`), 떠오르는 글자 튀어나오기+테두리, 연달아 줍는 돈 글자 합치기 `floatSum()`,
  등짐 쌓일 때 눌렸다 펴짐(`e.bump`), 걷는 방향으로 기울기(`personBody` 분리), 빨리 걸으면 먼지, 업그레이드 완료 칸 '뿅'(`pad.pop`)+원+색종이,
  층 오픈·미션 완료·VIP 대만족 배너, 결제 반짝이(팁이면 금색), 떠나는 손님 ♥, 황금 생산·수리·도둑 잡기 반짝이, 고장 연기+흔들림.
  prefers-reduced-motion이면 흔들림 끄고 파티클 1/3 (`RM`)
- 쌓고팔기 생산기 → 3D 프린터(사용자가 Gemini 그림 풍을 보고 '프린터형' 시안 선택. 그림 파일이 아니라 코드로 그린 SVG를 data URI로 내장 `PRN`).
  몸체는 SVG, 움직이는 건 `drawPrinter()`: 노즐 좌우 이동 + 빛줄기 깜빡임 + 받침대 위 물건이 아래부터 차오름(s.t 진행도) + 반짝이,
  다 되면 받침대 → 앞 더미로 날아감(`rt(z).pfly[k]` 날아가는 개수만큼 더미에서 빼고 그림). 고장 = 조종탑 화면 빨강 깜빡·노즐 화면 빨강·빛 꺼짐.
  예전 진행 막대·'생산 중' 글자 없앰(움직임이 대신), '가득 참'·고장 글자는 프린터 위(py-160). SVG 좌표→월드 `prnW()`(0.625배, 바닥 = 생산기 칸 y-30).
  ART_SRC.machine에 그림을 넣으면 예전처럼 그 그림 사용. 시안 원본은 자료실 '쌓고팔기_생산기시안2_*'
- 쌓고팔기 프린터 충돌(사용자: '사람이 가로질러 가는 것만 봐줘'): 프린터 몸체 x ±62, y = 칸 y-70 ~ y-28(`MACH`), 몸 반지름 10.
  주인공·일꾼 모두 `collide()`로 가장 적게 파고든 쪽으로 밀어냄 → 막히면 벽 따라 미끄러짐. 일꾼은 프린터 줄 위아래를 오갈 때 `detour()`로
  판매대 쪽 통로(x 275/275/485, `CORRIDOR`)를 경유. 20초 시뮬레이션에서 몸체 안 진입 0회, 판매 정상 확인
- 쌓고팔기 '잔업이 지금 있는 층만 쌓인다' 문의 원인: 잔업 계산은 모든 층에 정상으로 됐지만, 자동 수금을 산 층은 다른 층에 있으면 첫 프레임에 잔업수당(`Z.safe`)을 지갑으로 바로 빨아들여서
  그 층 상자가 늘 비어 보였음(돈은 지갑에 들어갔음). → 자동 수금은 돈더미만, 잔업수당은 층마다 상자에 남아 직접 가서 챙김(사용자 기대대로). apps.ts 설명도 수정
- 쌓고팔기 판매대 시안 3종(게임엔 아직 안 넣음, 사용자 선택 대기): A 계산대(컨베이어+금전등록기) · B 쇼케이스(유리 진열장+호출벨) · C 마켓 가판대(줄무늬 천+칠판).
  프린터와 같은 그림체(테두리 #38445a, 하늘·살구색), SVG 240×170·0.625배 = 판매대 폭 약 112. 자료실 '쌓고팔기_판매대시안_*'. SVG 안 글자는 넣을 때 캔버스 글자로 바꿀 것(이미지 SVG는 Jua 글꼴 못 씀)
- 쌓고팔기 손님 말풍선 '0/3' 글자가 칸 밖으로 삐져나옴 수정: 폭을 글자 길이에 맞춰 계산(여백 7 + 물건 14 + 4 + 글자 + 9), 알약 모양(반지름 = 높이/2), 물건 아이콘 세로 가운데(z 66+3)
- 쌓고팔기 판매대 시안 2차(사용자: '계산대 다른 디자인'): D 편의점(스캐너·손님 화면) · E 카페(나무 판넬·단말기·팁병·케이크 돔) · F 레트로 황동 금전등록기 · G 셀프 키오스크. 자료실 '쌓고팔기_판매대시안2_*'
- 쌓고팔기 판매대 → F 레트로 계산대(사용자 선택): 짙은 나무 계산대 + 황동 금전등록기 SVG를 data URI로 내장(`DSK`, 240×170 · 0.625배, 바닥 = DESK.y+14).
  움직이는 건 `drawDesk()`: 물건 하나 건넬 때마다 손잡이 당김(`rt(z).pull`), 결제하면 숫자판이 튀어오르며 ₩ 빨강 + 서랍(지폐)이 툭 나왔다 들어감 + 금색 반짝이(`rt(z).ring`).
  판매대 위 물건 자리는 금전등록기를 피해 왼쪽으로(deskPos x DESK.x-44~), '+N'은 판매대 왼쪽. ART_SRC.desk가 있으면 그 그림 우선.
  충돌 `DESK_BOX`(x ±54, 바닥 DESK.y-8 ~ +12): 주인공이 판매대 아래서 위로 걸으면 막히고 옆으로 미끄러져 돌아감. 20초 시뮬레이션 진입 0회·판매 33개 정상
- 쌓고팔기 돈더미·자동 수금 시안(게임엔 아직 안 넣음, 사용자 선택 대기): 돈 = 띠지 두른 돈다발(초록 / 노란 지폐), 받침은 돈더미 크기(x ±40)로 작게 + 밟는 칸은 옅게 유지.
  A 나무 팔레트 + 수금 튜브 · B 초록 매트 + ₩ 수금 로봇(돈더미 주위를 돎) · C 철망 바구니 + 집게 크레인. 자동 수금 산 층에만 장치가 보이는 안. 코드로 그려서 화면 합성(그림 파일 아님) — 자료실 '쌓고팔기_돈더미시안_ABC_20261020.png'
- 쌓고팔기 돈더미 → B안 적용(사용자 선택): 돈 = 띠지 두른 초록 돈다발(`bill()`, 날아가는 돈·도둑 등 전부 같은 그림), 받침 = 초록 펠트 매트(`slab()`, x ±40, 높이 3 → `cashPos` z +3),
  밟는 칸은 옅게. 자동 수금 산 층은 ₩ 수금 로봇(`cashRobot`/`drawRobot`)이 돈더미 주위를 돎(장식, 충돌 없음 — 주인공 그대로 지나감, y 정렬로 앞뒤 가림),
  그 층에 들어오면 '삑삑'(`sfx.robot`) + 1.2초 빠르게 회전(`rt(z).spin`). '자동 수금' 바닥 글자는 당분간 유지
- 쌓고팔기 잔업수당 상자 → 보물상자(`drawChest`, 사용자 요청 '잔업수당 상자 디자인도 바꿔줘'): 비었으면 닫힌 빛바랜 상자 + 회색 자물쇠 + 위에 둥실대는 노란 초승달(밤에 쌓인다는 뜻),
  있으면 뚜껑 열림 + 뒤에서 도는 금빛 + 금화 더미(최대치 대비 높이·개수) + 빨간 도장 월급봉투 + 반짝임. 바닥 칸·글자는 그대로
- 제목 논의: Ppalli Ppalli Factory → Tower → 층층타워 → 층층웨이 → '층층이' 쪽으로(미확정). 게임을 한국적으로(상가 건물) 가기로 하고 시안 2장 자료실에 올림(게임엔 아직 안 넣음):
  ① 상가 건물 전경(층마다 간판, 세로 간판, 개업 화환, 배달 오토바이, 옥상 '7층 공사 중' = 다음 층 열기)
  ② 1~3층 가게: 분식(떡볶이 철판+김밥 말이대 → 김밥 도시락), 붕어빵(손수레+무쇠 틀, '3개 1,000원' → 붕어빵 봉투), 치킨(튀김기 180℃ → 치킨 상자). 물건은 등에 쌓이게 상자형, 실제 게임 크기 미리보기 포함
- 게임 이름 '쌓고팔기' → '층층이'(사용자 확정): 탭 제목 '층층이 · 쌓고 팔고, 빨리빨리!', 캔버스 aria-label, apps.ts name·description. 주소(/games/stack)·slug·저장 키(stack-sell-v2)는 그대로라 진행 상황 유지
- 층층이 한국 상가 테마 1단계 — 1층 분식집(사용자 요청 '1층 분식집부터 넣어서 한번 보자'):
  생산기 = 분식 조리대 SVG(`BUN`, 프린터와 같은 240×200 틀이라 `prnW`·충돌 `MACH` 그대로) + `drawBunsik()`: 메뉴판 '떡볶이 · 김밥'(고장이면 빨간 '고장!' 깜빡), 떡볶이 김·양념 보글보글,
  김발 위 김밥이 진행도 70%까지 돌돌 말리고 → 칼이 오르내리며 썰고 도시락이 아래부터 차오름 → 더미로 날아감(`BUN_ITEM`). 고장 연기·수리 막대·'가득 참'은 `machLabel()`로 공통화.
  물건 KINDS[0] = '김밥'(shape 'kimbap': 크라프트 도시락 + 위에 김밥 3알 + 빨간 딱지) — 등짐·판매대·손님 말풍선·날아가는 물건 모두 적용.
  층 맨 위 벽에 '층층분식' 빨간 간판 + 줄무늬 차양(`SHOP[z]`, `shopSign()`), 바닥 층 이름도 '1층 층층분식 · 김밥'. 2층부터는 아직 프린터
- 테마 없는 층은 원래 모양(사용자 요청): KINDS[0]을 '상자'로 되돌리고 테마 물건은 `THEME_ITEM[층]`에 따로 — `kindOf(kind)`가 그 층 번호와 정확히 같을 때만 테마 물건(7층은 다시 주황 상자)
- 층층이 2~4층 가게 + 가게 미리보기(사용자: '7층까지 만들기 힘드니 바꿔가며 볼 수 있나?' / '일단 4층까지'):
  테마 표 `THEMES[층]`(shop·간판색 sign/ink/awn·img·anim·spot·reveal·up·item)로 정리 — 그릴 땐 `drawThemed()`가 몸체 → `anim` → 진행도 reveal부터 물건 차오름 → `machLabel()`.
  2층 붕어빵 손수레(`animBung`: 반죽→노릇, 60%쯤 무쇠 덮개 탁, '3개 1,000원') · 3층 튀김기(`animFry`: 기름 방울, 바구니 잠김→쑥 올라와 탈탈+기름 방울, 180℃/OFF) ·
  4층 편의점 냉장고(`animMart`: 유리문 빛 지나감, 고장 = 냉장 꺼짐 어둡게). 물건 붕어빵 봉투 'bung' · 치킨 상자 'chicken' · 바나나우유 'bmilk'(처음 삼각김밥 → 사용자 요청. 첫 모양은 목이 좁은 병이라 '그 단지 모양 아님' 지적 → 아래가 통통한 항아리 + 넓은 입구 + 은박 뚜껑 + 몸통 위 흰 띠로 다시 그림, 상표 글자 없음. 냉장고 아래 선반도 같은 단지). 5층부터 원래 스타일.
  설정 '가게 미리보기'(`PREVIEW`, `TH(z)`): 층대로 → 1~4층 가게 → 원래 스타일 순환, 지금 층 그림만 바뀜(값·저장 그대로, 새로고침하면 층대로)
- 층층이 5·6층 가게 — 이로써 테마 1~6층 완성, 7층부터 원래 스타일:
  5층 한강라면(`RAM`, `animRamen`): 왼쪽 창밖 밤 한강 다리(불빛 반짝)+라면 봉지 선반, 오른쪽 즉석 라면 조리기 — 은박 그릇에 물줄기(~30%) → 빨간 국물 보글보글+김(~80%) → 젓가락 꽂힌 완성 라면. 표시창 물 붓기/끓는 중/완성!/OFF. 물건 'ramen'
  6층 ♪ 코인노래방(`KAR`, `animKaraoke`): 미러볼 빛 점이 돌고, 화면 가사 두 줄이 분홍으로 차오르며 스피커에서 ♪ → '100점!' 깜빡 → 옆 작은 냉장고 아래에 음료 캔. 고장 = 화면 '고장!'. 물건 'can'(민트 캔)
- 층층이 층별 손님 + 말풍선(테마 층): `THEMES[].guests/order/thanks`, 손님 종류 `GUESTS`(교복 학생·초등학생(노란 모자+가방끈)·직장인(흰 셔츠+넥타이+사원증)·할머니(쪽머리+꽃무늬)·
  등산모자 아저씨·관광객(밀짚모자+하와이안+카메라)·후드티 청년) → `guestBody()`/`guestHead()`. 1층 학생·초등 / 2층 직장인·할머니 / 3층 직장인·아저씨 / 4층 학생·직장인·청년 / 5층 관광객·청년 / 6층 청년·직장인·학생.
  말풍선 `speech()`: 맨 앞에 오면 주문('김밥 {n}줄이요!', 'Ramyeon {n}, please!' …), 참을성 35% 아래면 빨간 재촉('빨리빨리!' 등, 모든 층), 다 사면 감사, 화나서 떠나면 '에이, 안 사!'(예전 '화났어요!' 글자 대신).
  한 층에 말풍선 하나씩(`say()`가 다른 손님 말풍선을 0.3초로 줄임). 7층부터는 원래 색 손님 + 재촉·화남만
- 층층이 도둑 등장 방향 무작위(사용자 요청): `THIEF_SIDES` 위쪽·왼쪽(-50,330)·오른쪽(W+50,330)·아래쪽(W+40, 층 바닥 아래 — 프린터 줄을 안 뚫게 오른쪽 바깥) 중 하나에서 나오고, 도망 방향도 따로 무작위(`thief.out`). 토스트에 방향 표시('도둑이 왼쪽에서 나타났어요!'). 16번 반복 테스트로 네 방향 모두 확인
- 층층이 도둑 길: 계단·엘리베이터를 가로지르지 않게 경유점 경로(`THIEF_SIDES` [[바깥],[경유점]…] → 돈더미, 도망은 다른 쪽 경로를 거꾸로). 위쪽은 판매대와 엘리베이터 사이 통로 x 395로 내려옴.
  엘리베이터 문 충돌(설치 후, 주인공·일꾼): x ELEV ±35, y ELEV.y-40 ~ ELEV.y — 문 앞 타는 자리(ELEV_ZONE)는 그대로
- 층층이 계단 깜빡임 수정(위로 계속 누르면 위·아래층을 오가던 것): `P.stairArm`이 다시 켜지는 조건 = 계단 밖에서 손을 뗐거나(입력 없음) 계단에서 50 넘게 내려왔을 때. 4초 누르고 있어도 한 층만 올라감 확인
- 층층이 배달 주문(사용자 선택 1번) + 손님은 그 층 물건만 삼: 판매대에 내려놓을 때 등짐에서 그 층 물건 중 맨 위 것만 꺼냄(`topOf`, `floorOfItem` — 황금도 나온 층 기준), 없으면 'N층 물건만 팔려요'.
  층 이벤트 비율 고장 40% · VIP 30% · 배달 30%(층 2개 이상). `startDeliv/updDeliv/drawDeliv`, 손님 자리 `DELIV_SPOT`(180,390, 초록 칸), 머리 위 🛵+물건+개수+시간 막대, 말풍선.
  `CFG.deliv`: 50초 + 층 차이당 10초, 2~4개, 보상 물건 값 × 3(지갑 한도 무시), 시간 절반 넘게 남기면 배달팁 30% + '총알 배달!' 배너. 놓쳐도 벌칙 없음. 층 표시 '배달'(zoneAlert 8, 초록 깜빡). apps.ts 설명에 배달 주문 추가
- 층층이 화면 정리(사용자 폰 캡처 피드백):
  ① 배달 주문 카드 `#orders`: 미션 카드 바로 위에 진행 중인 배달을 계속 표시('🛵 3층 치킨 0/3 → 4층 24시 층층마트 · 59초', 15초 미만 빨강)
  ② 알림(토스트)을 화면 위 → 아래로: 미션 카드 → 배달 카드 → 알림/안내 순으로 쌓임(CSS 변수 --ordB/--stackB를 0.5초마다 계산)
  ③ '화면을 드래그해서 움직여요'는 처음 한 번만(`S.tut.moved`, 처음 움직이면 끝). 예전엔 HTML 첫 문구가 튜토리얼 끝난 뒤에도 계속 남아 있던 버그였음
  ④ 층 칩이 층 늘면 여러 줄로 화면을 덮던 것: 한 줄(nowrap) + 지금 층과 경고 있는 층만 보이고 급한 순서로 앞에(`ALERT_RANK`: VIP > 배달 > 황금 > 부서지기 직전 > 화나기 직전 > 고장 > MAX > 대기). 전체 층은 엘리베이터 선택판
  → 그래도 가린다(사용자) → 칩 작게(12px), 경고 층은 급한 것 2개까지 + '+N'(`CHIP_MAX`), 배달은 위 칩에서 빼고 배달 카드로만(`zoneAlert(z, noDeliv)`, 엘리베이터 선택판엔 그대로)
  → 사용자 제안대로: 돈 표시 작게(22→16px, 동전 아이콘 20px) + 층 칩은 왼쪽 아래 세로(`#zones` fixed, 알림 줄 위), 지금 층 + 경고 층 4개 = 최대 5칸 + '+N'(CHIP_MAX 4). 화면 위쪽은 돈·설정만 남음
  배달은 갈 층이 잘 보이게(사용자): 배달 카드 맨 앞에 초록 강조 'N층으로 배달' · 가져갈 물건 n/m개 · 남은 초, 세로 층 칩에도 배달 층 다시 표시(자리 생겨서)
- 층층이 도둑 잡으면 현상금(사용자 요청): 그 층 물건 값 × 15 + 훔쳐 가던 돈의 50%(`CFG.thief.bounty/lootBonus`), 지갑 한도 무시. 동전 날아감 + '🚓 도둑 검거!' 배너 + '현상금 +₩' 글자, 훔치기 전에 잡아도 받음. apps.ts 설명 보강
  → 훔치기 전에 잡으면 기본 현상금 2배 + 훔쳤을 돈(돈더미 × 50%)의 50% + '🛡️ 철통 방어!'(사용자: 못 훔치고 잡아도 보상 있어야 — 예전엔 놔뒀다 잡는 쪽이 이득이었음)
- 층층이 개업 화환 + 이벤트 이름(사용자 요청): 층 열면 `Z.openedAt` 저장 → 5분 동안 왼쪽 위(x 60·128)에 화환 2개(`drawWreath`: 꽃 둥근 판 흔들림 + 리본 '축개업'/'대박나세요'),
  배너 '🎉 N층 가게이름 개업!', 토스트 '축 개업!'. 이름: VIP → 건물주(층 칩·느려짐 배지·토스트·머리 위 글자, 말풍선 '어디, 장사 잘 되나 볼까?'/놓치면 '임대료 올려야겠군!'/
  황금 받으면 '임대료 깎아 줘야겠네!'), 도둑 → 먹튀범('먹튀범이 왼쪽에서 나타났어요!', '먹튀당했어요', '🚓 먹튀범 검거!', 머리 위 '먹튀!'). 코드 변수명(vip·thief)은 그대로.
  apps.ts 설명도 이름 바꾸고 '화면 표시' 항목을 지금 화면(왼쪽 아래 세로 층 표시·배달 카드)에 맞게 다시 씀
- 층층이 배달 보상 상향(사용자: '어렵네, 많이 받아야'): 개당 = 지금 최고층 물건 값 × 6(`delivEach`, 예전 그 물건 값 × 3이라 아래층 배달은 몇 원), 배달팁 30→50%, 시간 50+10/층 → 60+15/층. 배달 카드에 받을 돈 표시

### 2026-10-19
- 쌓고팔기(아이들 아케이드 게임 시제품) 추가 — "기타" 카테고리
  - 게임 본체: `public/games/stack/index.html` (독립 정적 HTML, 캔버스, 외부 의존은 Google Fonts Jua뿐)
    → https://wowhit.org/games/stack/
  - `apps.ts`에 `stack` 항목 추가 (category: 'other', webUrl 절대주소 — 상대경로면 NuxtLink가 내부 라우트로 처리함)
  - 게임 HUD의 "소개" 버튼 → `/stack` 상세 페이지
  - 진행 상황은 localStorage(`stack-sell-proto-v1`)에 저장. 주제(테마)는 아직 미정
- 쌓고팔기 v2: 구역 무한 확장(위로 쌓임, 구역 칩으로 순간이동, 구역별 일꾼, 다른 구역 수익 자동 수금),
  손님(줄 서서 구매, 참을성 바 → 화내고 떠남, 빨리 채우면 팁), 돈더미 MAX(꽉 차면 판매 정지),
  효과음(WebAudio 합성, 파일 없음)·진동(navigator.vibrate), 설정 패널(소리/진동/처음부터)
  - 밸런스는 파일 맨 위 `CFG`, 그림은 `ART_SRC`에 경로만 넣으면 도형 대신 그림으로 그림
  - 저장 키 `stack-sell-v2` (v1 저장은 자동 이전)
- 쌓고팔기 지갑 한도: 500 × 2^레벨, 업그레이드 '지갑' 칸(비용 = 현재 한도의 60%라 항상 살 수 있음).
  지갑이 차면 돈더미를 못 줍고, 다른 구역 자동 수금도 남은 자리만큼만 들어옴
- 쌓고팔기 미션·황금 물건: 미션은 sell/collect/tip/upgrade/golden 순환, 단계마다 목표·보상 증가(현재 최고 구역 값 기준),
  보상은 지갑 한도 무시. 진행은 `S.stats` 누적값 - 미션 시작 시점값. 황금 물건 = 1000+구역번호, 생산 확률 3%·값 10배(`CFG.gold`),
  생산기에선 맨 위에 쌓여 먼저 집힘(`sp.golden` 개수)
- 쌓고팔기 도둑·구역 이름: 지금 있는 구역 돈더미를 12초 이상 방치하면 도둑이 위쪽에서 나타나 절반을 들고 위로 도망(`CFG.thief`),
  부딪히면 잡아서 돈더미로 되돌림. 처음엔 오른쪽 끝에서 나와서 폰 화면에 안 보였음 → 위쪽으로 바꿈.
  구역 이름은 `zoneName(z)` 자동 생성(형용사 10 × 장소 10, 10곳마다 '2호'…), 바닥 표시·구역 칩·다른 구역 수익 알림에 사용
- 쌓고팔기 손님 경고: 다른 구역은 구역 칩에 노랑 테두리(대기)/빨강 깜빡+!(참을성 35% 미만), 화나서 떠나면 10초에 한 번 알림.
  지금 구역은 판매대가 화면 위로 벗어나면 '▲ 손님 N명 대기' 표시(화나기 직전이면 빨강 깜빡). `zoneAlert(z)`
- 쌓고팔기 수금 방식 변경(사용자 선택 2번): 다른 구역 돈도 그 구역 돈더미에 쌓임(예전엔 바로 지갑으로 → 다른 구역 돈더미가 늘 비어 보였음).
  구역마다 '자동 수금' 칸(`CFG.autoCost` 1500 × 8^구역, 위치 645,250)을 사면 그 구역만 지갑으로 자동(`Z.auto`).
  다른 구역 돈더미 MAX면 구역 칩이 노랑 '₩MAX'(`zoneAlert`=3, 손님 상태는 `custAlert`) + 30초에 한 번 알림. 지갑은 전 구역 공용
- 쌓고팔기 업그레이드 범위(사용자 선택 2번): 공통(지갑·적재량·이동속도)은 1구역에만 칸이 있음(`vis: z === 0`).
  구역별은 일꾼·판매속도·생산기·자동 수금. 순간이동은 구매제(`S.warp`, `CFG.warpCost` 1500, 1구역 110,300 칸, 구역 2개 이상일 때 보임) —
  사기 전엔 구역 칩이 반투명(locked)이고 누르면 '1구역에서 살 수 있어요' 안내만, 경고 표시는 그대로
- 쌓고팔기 구역 → 층 전환(사용자 선택 2번 '진짜 층'): 자동 이름(zoneName) 삭제, 층마다 화면 분리(카메라·이동 범위가 지금 층 안, 다른 층은 안 그림).
  층 사이는 계단(계단 밖으로 한 번 나갔다 다시 밟아야 이동 `P.stairArm`), 순간이동 → 엘리베이터(층 버튼 '1F 2F').
  → 이후 사용자 요청으로 계단실처럼 오른쪽 위에 나란히 배치: 엘리베이터 문(ELEV 455) · 내려가는 계단(STAIR_DN 580,80) · 올라가는 계단/다음 층 열기(STAIR_UP 700,80).
    올라가면 바로 옆 내려가는 계단 앞에 도착. 엘리베이터는 1층 문 자리에서 설치, 문 앞(ELEV_ZONE)에 서면 층 선택판(#elev, 경고 색 표시) 열림
  카메라는 층 위 -90 / 아래 +170 여유(돈 표시·미션 카드에 바닥 끝이 가리지 않게). 내부 변수명은 여전히 zone(z)
- 쌓고팔기 층 이벤트(자동화 끝난 층에도 갈 이유): 평균 50초마다(처음 60초 후) 무작위 층에 ① 생산기 고장(생산 멈춤, 주인공이 그 앞에 2초 서 있으면 수리)
  ② VIP 손님(VIP_SPOT 110,300, 일꾼은 못 상대, 주인공이 옆에서 등의 물건을 건넴, 40초 제한, 보상 = 물건 값 × 5 지갑 한도 무시). `CFG.events/broken/vip`
  층 칩은 누르는 기능 없앰(span 표시판) — 층 이동은 엘리베이터 문 앞에서만(사용자 요청). 경고 단계 `zoneAlert`: 5 VIP > 4 고장 > 3 ₩MAX > 2 화나기 직전 > 1 대기
- 쌓고팔기 직접 나르기 이유: ① 직접 납품 보너스 — 주인공이 판매대에 내려놓은 물건은 큐에 MINE(10000)을 더해 저장, 값 ×2(`CFG.direct`), 파란 테두리
  ② 황금 물건은 일꾼이 못 나름(`normalCount`, 일꾼은 일반 물건만 집음), 황금 대기 층은 층 표시 '황금'(zoneAlert 6)
  ③ 황금 값 = 지금 최고층 물건 값 × 10(어느 층 황금이든 같음 — 아래층 황금이 무가치해서 안 가지러 가고 쌓이던 문제),
     황금마다 수명 60초(`sp.goldLife`, 먼저 나온 것부터 사라짐, 10초 전부터 깜빡임, 예전 저장은 60초로 보정)
- 쌓고팔기 돈더미 MAX는 금액이 아니라 장수(결제 횟수) 기준: `Z.bills` 결제 1번 = 1장, 40장이면 MAX(`CFG.cashMax`).
  돈이 빠지면(수금·자동수금·도둑) `takeCash`가 장수도 같은 비율로 줄임. 예전엔 '그 층 값 × 40'이라 아래층에서 최고층 기준 황금 하나만 팔려도 바로 MAX였음
- CI(lint) 실패 원인이던 `[slug].vue` 64번 줄(setTimeout 한 줄에 문장 2개) 고침 — 2026-08 wowEditor 커밋 때부터 실패 상태였음
- 게임 설명(apps.ts longDescription)은 2026-10-19 전체를 가이드 형식으로 다시 정리함 — 기능 추가 시 해당 섹션에 맞춰 넣을 것(뒤에 덧붙이지 말 것).
  상세 페이지 문단에 `whitespace-pre-line` 추가(문단 안 한 줄 바꿈이 보이게 — 다른 앱 설명의 '제목\n내용'도 줄이 나뉘어 보임)
- 쌓고팔기 고장 누적·부서짐: 한 층에 고장 1대 제한 없앰(멀쩡한 생산기가 있는 층 중에서 골라 고장, 예전엔 이미 고장 난 층이 뽑히면 이벤트가 그냥 사라졌음).
  고장 난 채로 120초(`CFG.broken.ruin`) 지나면 부서짐(`s.ruined`, 쌓인 물건·황금 사라짐, 30초 전부터 경고 토스트+'N초 뒤 부서짐!'),
  그 자리에 '다시 제작' 칸(100 × 8^층, `CFG.broken.rebuild`). 부서져도 `on`은 유지라 다음 층 열기 조건은 안 깨짐. 일꾼은 부서진 생산기를 대상으로 안 고름
- 쌓고팔기 VIP 놓치면 벌칙: 15초(`CFG.vip.slow`) 동안 이동속도가 Lv0 속도로(`S.slow`, 저장됨 — 새로고침으로 못 피함).
  엘리베이터(`S.warp`) 없으면 지금 층 VIP만 벌칙(먼 층은 40초 안에 못 가서). 겹치면 15초부터 다시.
  표시(사용자 선택: 원인이 VIP인 게 보이게): 머리 위 왕관 쓴 화난 먹구름+비(`vipCloud`), 발밑 진흙 웅덩이+걸을 때 진흙 발자국(`muds`, 저장 안 함),
  지갑 아래 빨간 배지 '🐢 VIP 화남 · 느려짐 N초'(#slowChip)
- 쌓고팔기 야간 금고(자리 비운 동안 수익, 층별 업그레이드): 칸 AWAY_PAD(645,370), 단계마다 최대 1→2→4→8시간(`CFG.away`, 비용 300 × 4^단계 × 8^층).
  일꾼 1명 이상인 층만, 속도 = min(생산, 일꾼 운반, 손님) × 그 층 값 × 50%(`awayRate`). 돈은 그 층 금고 `Z.safe`(SAFE 500,370, 금색 — 초록 돈더미와 구별)에 쌓이고
  밟아서 챙김(지갑 한도 적용, 자동 수금 산 층은 다른 층에 있을 때 자동). 계산: save()마다 `S.seen` 기록 → frame()에서 60초 이상 비었으면 `grantAway` + 토스트.
  게임 끔·다른 화면(rAF 멈춤) 둘 다 같은 방식. 자리 비운 동안 이벤트(고장·VIP·도둑·황금)는 없음. 예전 저장(seen 없음)은 첫 실행 때 계산 안 함
- 쌓고팔기 업그레이드 칸 글자 넘침 수정: '자동 수금' 칸 '다른 층에 있을 때'가 칸 밖으로 삐져나옴 → `text()`에 maxW 인자(넘치면 글자 크기 줄임), 칸 글자 3줄 모두 칸 너비-12에 맞춤
- 쌓고팔기 층 경고 우선순위 변경(남은 시간 짧고 손해 큰 순): VIP(5) > 황금(6) > 부서지기 30초 전 고장(7, 새 'ruin' 빨강 깜빡 '고장!') > 화나기 직전(2) > 고장·부서짐(4) > ₩MAX(3) > 대기(1).
  예전: VIP > 고장 > ₩MAX > 황금 > 손님 — 황금(60초에 사라짐)이 고장·MAX에 가려졌음. 층 선택판 버튼도 같은 `ALERT_CLS` 사용
- 쌓고팔기 VIP 벌칙 강화(사용자 선택 3번): 속도 = 지금 속도 × (20% → 100%를 10초에 걸쳐 회복)(`CFG.vip.slow` 10, `slowMin` 0.2). 업그레이드 안 했어도 체감됨
- 쌓고팔기 VIP 황금 보너스: VIP에게 황금을 건네면 그 물건 값 × `CFG.vip.goldMul`(5) 추가(원래 최고층 값 × 10 → × 5 → 보상 × 5), '황금! ×5' + '대만족!!' 토스트·효과음, 머리 위 '· 황금N'
- 쌓고팔기 칸 위치: 자동 수금·야간 금고·금고를 가운데 줄 → 금고만 오른쪽 정렬로 옮겨 봤다가 사용자 요청으로 원래 자리로 원복
  (자동 수금 645,250 · 야간 금고 칸 645,370 · 금고 500,370). 칸 글자 자동 줄임(maxW)은 유지
- 쌓고팔기 일꾼 복장: 회색 옷 + 반사띠 주황 조끼 + 노란 안전모 (`person(..., gear='worker')`, 주인공 파란 옷과 구별)
  - standalone 페이지라 `[hidden]{display:none!important}` 필요 (없으면 패널이 처음부터 열림)

### 2026-07-25
- HCLink(한국어화) 포트폴리오 추가 — "기타" 카테고리
  - 중국산 브이로그 미러링 스크린 부속 앱을 디컴파일해 한국어화 + Pairip 우회 +
    무선연결(스마트뷰 우회) 패치한 개인 프로젝트, 직접 만든 게 아니라 리패치임을
    설명에 명시
  - `apps.ts`에 `hclinkway` 항목 추가 (category: 'other')
  - APK를 wowhit-releases에 `hclinkway-v1.2.0-ko` 릴리스로 업로드
  - 소스(smali 패치, 별도 private repo)는 방문자가 접근 못하므로 포트폴리오에서
    링크하지 않음

### 2026-07-12
- menuWayAll v1.0.4+12 APK 업데이트 (Gemini 응답 토큰 상한 추가 — wowhit-api 프록시의 thinking
  모드 낭비 수정과 짝을 이루는 클라이언트측 변경)
  - wowhit-releases에 `menuwayall-v1.0.4+12` 릴리스 생성
  - `apps.ts`의 menuway 항목 apkUrl/version 갱신

### 2026-07-09
- bibleWay 포트폴리오 추가 (아이콘 + 앱 데이터)
  - 자료실(digi.wowhit.org)에서 bibleWay (1).png 아이콘 가져와 1024x1024 리사이즈
  - `apps.ts`에 bibleWay 항목 추가: Flutter, 개역한글 성경 읽기 + AI(DeepSeek) 해설

### 2026-07-07
- talkWay 아이콘 교체: Flutter 앱 실제 아이콘 (xxxhdpi) → 1024x1024 업스케일 적용

### 2026-07-06 (추가 3)
- 무료/광고와 구분되는 "AI 유료" 배지 추가 (purchaseUrl 있는 앱 대상, 주황색, 아래 구매 버튼과 톤 통일)

### 2026-07-06 (추가 2)
- `/guide`에 Android APK 직접 설치 시 뜨는 확인창(다운로드 경고 → 출처 미확인 차단 → Play 프로텍트 경고 → 설치 완료) 단계별 안내 섹션 추가

### 2026-07-06 (추가)
- 앱 카드 무료/광고 시청 배지 추가
  - `apps.ts`에 `pricingModel?: 'free' | 'ads'` 필드 추가
  - menuWay: `ads` (google_mobile_ads 사용 확인), shotWay·careWay: `free`
  - 나머지 앱은 미표시 (이용권/크레딧 구매는 기존 purchaseUrl 버튼으로 구분됨)
  - 메인 카드(`index.vue`)와 상세 페이지(`[slug].vue`) 배지 영역에 표시

### 2026-07-06
- 이용 안내 페이지 신규 추가 (`/guide`)
  - 홈 화면에 추가(PWA 설치) Android(Chrome)/iPhone(Safari) 탭별 단계 안내
  - 이용권·크레딧 구매 vs Gemini API 키 직접 사용 비교, API 키 발급 절차
  - Gemini 2.5 Flash Image/Imagen 4/텍스트 모델 대략적 가격표 (출처: ai.google.dev/gemini-api/docs/pricing)
  - 앱별 이용권 구매 링크(JoA/itNe/CODI:D), FAQ 아코디언
  - 헤더에 "이용 안내" 메뉴 추가

### 2026-07-03
- careWay v1.1.1+16 APK + 웹 업데이트
  - APK: wowhit-releases에 `careway-v1.1.1.16` 릴리스 생성, `careWay.apk` 업로드
  - 웹: Vercel 자동 배포 (careway.wowhit.org)
  - apps.ts: apkUrl, version 업데이트

### 2026-06-29
- shotWay, itNe, CODI:D 상세 페이지 JoA 수준으로 전면 강화
  - shotWay: 스크린샷 2장 + 상세 설명 (실시간 공유/연결방식/크로스플랫폼/완전무료)
  - itNe: 스크린샷 6장 + 상세 설명 (자동인식/냉장고관리/AI레시피/크로스플랫폼/이용권)
  - CODI:D: 스크린샷 7장 + 상세 설명 (AI코디생성/체형맞춤마네킹/스타일진화/어디서나접근)
  - 이미지는 digi.wowhit.org에 앱별로 업로드 후 public/apps/로 복사

### 2026-06-13
- ドシラクeSIM 일본어 가이드 추가 (`public/esim/index.html`)
  - URL: wowhit.org/esim (wowhit Nuxt 앱과 완전 무관한 독립 정적 HTML)
  - 일본 친구에게 eSIM 등록 방법 공유용
  - iOS 17.4 이후(v2) / iOS 17.4 이전(v1) 탭 전환
  - 도시락eSIM 원본 스크린샷 이미지(CDN URL) 전부 포함
  - 사전확인 → STEP 1~4 전 단계 → 완료 체크리스트 → 고객센터

### 2026-06-12
- 디지털 비서 프로필 이미지 추가 (한국인 여성, 세상에서 가장 아름다운 컨셉)
  - `public/digital-assistant-profiles/` 폴더 생성 및 업로드
    - profile-01.jpg (기본)
    - profile-02.jpg (아름다움 극대화)
    - profile-03.jpg (우아한 헤어/스타일 변형)
  - preview.html (미리보기 페이지) + README.md 포함
  - apps.ts에는 등록하지 않음 (사용자 요청 — 포트폴리오 메인에 프로젝트 카드로 노출 X)
  - Vercel 배포 후 웹 주소:
    - https://wowhit.vercel.app/digital-assistant-profiles/preview.html
    - https://wowhit.org/digital-assistant-profiles/preview.html
  - 로컬에서도 `pnpm dev` 후 /digital-assistant-profiles/preview.html 로 확인 가능

### 2026-06-09
- 메인 3D 대표 이미지를 바이크 5종만 노출 (`featuredPrintSlugs`)
- MakerWorld 버튼 라벨 `MakerWorld @jinsukYoon` → `MakerWorld`
- 3D 명칭 수정: 시카고/Boston → 두산 베어스 (script 키링, 헬로키티 키링, 토큰)
  - 이미지 파일명 정리: `doosan-bears-token.jpg`, `doosan-bears-script-keychain.jpg`, `hellokitty-doosan-bears-keychain.jpg`
- 3D 갤러리 전면 정리 (총 15개, 4카테고리)
  - 바이크 5 · 디오라마 1(커피 트럭 +갤러리 2장) · 프라모델 4 · 키링 5
  - `public/prints/` 이미지 slug 파일명으로 정리
  - `/3d` 카테고리별 섹션, 메인은 `featuredPrintSlugs` 바이크 5개만
  - 문구: `Bambu Lab · 프라모델 · 디오라마` (A1 mini 제거), `/3d` 「작품」 제목 제거
  - 메인 3D 섹션 위치: 앱 목록 맨 아래
- 오토바이 썸네일 5장 연결 (`prints.ts` imageUrl)

### 2026-06-08
- 앱 subdomain redirect Cloudflare Redirect Rules로 이전 (집 서버 불필요)
  - API 토큰: DNS-only 권한 토큰은 Rules API 실패 → WAF Edit 권한 토큰으로 재등록
  - Rules 10개 + DNS 터널 CNAME → A 192.0.2.1(proxied)
  - `~/.cloudflared/config.yml` ingress에서 앱 subdomain 제거 (api만 유지)
  - `wowhit-redirect.service` 비활성화
- 3D Printing 섹션 추가: MakerWorld @jinsukYoon 프로필 + 바이크 5개
  - `app/data/prints.ts`, `/3d` 페이지, 헤더 「3D」 링크
- 댓글 삭제: 길게 누르기(600ms) → 관리자 암호 → 삭제 (원댓글 삭제 시 답글도 함께)
  - 홈서버 `DELETE /api/comments/:slug/:id`, 암호 `wowhit-api/.env`
  - Vercel 프록시 `server/api/comments/[slug]/[id].ts`
- 대댓글 순서 버그 수정: root_id 미보정 답글 backfill + parent_id 기준 분류
- 대댓글 기능 추가: DB root_id 컬럼, 답글에도 답글 가능, 모두 한 칸 들여쓰기 표시, @멘션 강조
- api.wowhit.org DNS CNAME 재등록 (--overwrite-dns)으로 터널 라우팅 복구, 522 에러 해결
- Vercel 서버 프록시로 hairpin NAT 문제 해결 (집 공유기가 loopback NAT 미지원)
  - `server/api/comments/[slug].ts` 추가: Vercel이 대신 api.wowhit.org 호출
  - `app/composables/useComments.ts`: API 경로를 `/api/comments/...` (상대경로)로 변경
- 댓글 POST 요청을 form 인코딩으로 변경해 CORS preflight 우회 (회사 방화벽 대응)
  - `app/composables/useComments.ts`: `application/x-www-form-urlencoded` 사용, URLSearchParams로 body 직렬화
  - 홈서버 API `index.js`에 `express.urlencoded()` 미들웨어 추가, 요청 로그 강화
- 댓글 API 홈서버 구축 (Firebase → 집 리눅스 미니PC + SQLite)
  - Cloudflare Tunnel로 포트포워딩 없이 외부 공개 (api.wowhit.org)
  - Express + better-sqlite3 REST API (GET/POST /api/comments/:appSlug)
  - fnm Node.js v24 기반 systemd 서비스 (wowhit-api.service)
  - `app/composables/useComments.ts` Firebase → REST API 전면 재작성
  - `app/plugins/firebase.client.ts` 삭제, firebase 패키지 제거
- wowhit.org 도메인 구입 (Cloudflare, $8.5/yr), Vercel 커스텀 도메인 연결
  - wowhit.org, www.wowhit.org → wowhit.vercel.app 동시 접속 가능
  - `app/data/apps.ts` 웹앱 URL 전부 appname.wowhit.org 형식으로 변경
  - (이후 6/8) subdomain redirect를 Cloudflare Rules로 이전, 터널 redirect 폐기
- Firebase (itneapp 프로젝트) 기반 댓글 시스템 추가
  - `app/plugins/firebase.client.ts`: Firebase 초기화 플러그인
  - `app/composables/useComments.ts`: wowhit_comments 컬렉션 CRUD (fetchComments, addComment, formatDate)
  - `app/pages/[slug].vue`: 댓글 섹션 UI (닉네임+내용 입력폼, 목록, 로딩 스피너)
  - firebase 패키지 추가 (package.json)
  - Firestore 보안 규칙 필요: wowhit_comments 공개 읽기/쓰기 허용

### 2026-06-07
- 앱 버전 표시 추가 (메인 카드 + 상세 페이지 배지), apps.ts version 필드 추가
- APK 자동 업로드 스크립트 (upload-apk.sh): pubspec.yaml 빌드번호까지 체크, apps.ts apkUrl+version 자동 수정, git push까지 자동화
- APK 파일 변경 감지 자동 실행 스크립트 (watch-apk.sh): inotifywait 기반, tmux 세션에서 상시 실행
- API Key → QR 변환 페이지 추가 (/qr), 헤더 메뉴 연결
- JoA 상세 페이지 대폭 업데이트: 스크린샷 교체(5장), 아이콘 교체, API Gemini로 변경, 상세설명 전면 재작성 (무료체험/BYOK/이용권/멀티기기 안내), 이용권 구매 링크 추가 (네이버 스마트스토어)
- JoA 스크린샷 갤러리 6장 추가 (public/apps/joa/)
- JoA longDescription에 Android APK 설치/삭제 방법 안내 추가

### 2026-06-06
- JoA 웹앱 URL 추가 (https://web-tau-nine-22.vercel.app)

### 2026-06-05
- JoA release APK 빌드 및 GitHub 릴리스 업로드 (joa-v1.0.0), apkUrl 연결
- 상세 페이지 스크린샷 갤러리 모바일 overflow 수정 (페이지 가로 밀림 방지, 이미지 높이 축소, snap scroll 추가)


- BBangWay, posTest 아이콘 추가
- MenuWay에 YouTube 쇼츠 링크 추가 (https://www.youtube.com/@zzindori/shorts)
- `qr_scanner` → `codeWay`로 이름/설명/아이콘 정리 (프로젝트 위치: workspace/qr_scanner/)
- CODI:D APK 파일명 `app-release.apk` → `CODI_D.apk` 로 재업로드
- APK 업로드 규칙 수정: 앱 이름으로 복사 후 업로드
- `dayLOg`, `MakeImg` 앱 미등록 상태 (설명 필요)
- 앱 아이콘 추가 (12개 Flutter + 2개 Web)
- menuWay 상세 페이지 강화: 스크린샷 갤러리, YouTube 쇼츠 썸네일+모달 플레이어, 전문 설명
- menuWay → `menuWay` 이름 수정, 전문 설명/태그라인 추가
- itNe 웹앱 연결: https://itneapp.web.app/
- codeWay 웹앱 연결: https://zzindori.github.io/codeWay/
- txtFit 앱 추가 (웹앱 + APK, 아이콘)
- APK 전체 업로드 (careWay, farmGuide, igoMoya, itNe, shotWay, codeWay)
- onBidWay 아이콘 교체 + Flutter 빌드 아이콘 적용 (flutter_launcher_icons)
- careWay 아이콘 교체 + Flutter 빌드 아이콘 적용
- YL Company 로고를 푸터에 추가 (public/apps/ylcompany.png)
- shotWay 설명 수정: 실시간 찍은 사진 공유 앱
- 아이콘 처리 규칙: 비정사각형 이미지는 Python PIL로 center crop → 1024x1024 변환 후 사용

### 2026-06-04
- Nuxt 스타터 템플릿 기반으로 포트폴리오 사이트 초기 구성
- GitHub 저장소 생성 및 Vercel 연동 (자동 배포)
- `wowhit` → `wowHit` 로 브랜딩 통일 (로고, 히어로, SEO)
- 설명 태그라인 `Flutter · Web · Watch` → `App · Web · Watch` 변경
- 푸터에 사업자 정보 추가: YL Company (Yoon & Lee) | 515-68-00370
- `wowhit-releases` 저장소 생성 (APK 전용 관리)
- CODI:D APK 업로드 및 `apkUrl` 연결 (404 수정 포함)
- APK 버튼 라벨 `APK 다운로드` → `Android 직접 설치` (Android 아이콘)
- 앱 설명 업데이트:
  - `igoMoya`: 궁금한 것 찍으면 바로 AI 설명 + 타임라인 사진 정리 (Gemini)
  - `itNe`: 냉장고 식재료 관리 + 남은 재료로만 AI 레시피 추천
  - `CODI_D` → `CODI:D` 이름 수정
