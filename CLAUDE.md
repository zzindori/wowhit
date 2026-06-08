# wowhit 포트폴리오 사이트

## Claude에게
이 프로젝트에서 작업을 마칠 때마다 반드시 아래 **작업 히스토리** 섹션에 날짜와 작업 내용을 추가하고 `git push`까지 완료할 것. 사용자가 요청하지 않아도 자동으로 수행한다.

## 프로젝트 개요
- **URL**: https://wowhit.vercel.app (Vercel 자동 배포, main 브랜치 push 시 갱신)
- **GitHub**: https://github.com/zzindori/wowhit
- **APK 배포**: https://github.com/zzindori/wowhit-releases (릴리스로 APK 관리)
- **기술 스택**: Nuxt 3 + Nuxt UI + Tailwind CSS

## 구조
- `app/data/apps.ts` — 앱 목록 데이터 (여기만 수정하면 카드/상세 자동 반영)
- `app/pages/index.vue` — 메인 페이지 (카테고리별 앱 카드 그리드)
- `app/pages/[slug].vue` — 앱 상세 페이지
- `app/components/AppLogo.vue` — 헤더 로고
- `app/app.vue` — 전체 레이아웃 (헤더, 푸터)

## APK 업로드 방법
파일명을 앱 이름으로 복사한 뒤 업로드한다 (다운로드 시 파일명이 앱명으로 표시되도록).
```bash
cp /path/to/app-release.apk /tmp/앱이름.apk
gh release create [앱명]-v1.0.0 /tmp/앱이름.apk \
  --repo zzindori/wowhit-releases \
  --title "[앱명] v1.0.0" \
  --notes "설명"
```
업로드 후 `apps.ts`의 해당 앱 `apkUrl` 필드에 아래 URL 형식으로 추가:
```
https://github.com/zzindori/wowhit-releases/releases/download/[태그]/앱이름.apk
```

## 작업 히스토리

### 2026-06-08
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
  - 앱 subdomain (careway/itne/joa 등.wowhit.org) Cloudflare Tunnel → 홈서버 redirect 서버(3002)
  - `app/data/apps.ts` 웹앱 URL 전부 appname.wowhit.org 형식으로 변경
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
