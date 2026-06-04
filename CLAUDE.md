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
```bash
gh release create [앱명]-v1.0.0 ./app-release.apk \
  --repo zzindori/wowhit-releases \
  --title "[앱명] v1.0.0" \
  --notes "설명"
```
업로드 후 `apps.ts`의 해당 앱 `apkUrl` 필드에 아래 URL 형식으로 추가:
```
https://github.com/zzindori/wowhit-releases/releases/download/[태그]/app-release.apk
```

## 작업 히스토리

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
