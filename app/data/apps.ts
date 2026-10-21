export interface App {
  slug: string
  name: string
  category: 'flutter' | 'web' | 'other'
  description: string
  longDescription?: string
  api?: string[]
  platform?: string
  iconUrl?: string
  screenshots?: string[]
  androidUrl?: string
  iosUrl?: string
  webUrl?: string
  apkUrl?: string
  purchaseUrl?: string
  purchaseLabel?: string
  pricingModel?: 'free' | 'ads'
  version?: string
  youtubeUrl?: string
  shorts?: string[]
  storeReleased?: boolean
  sourceCodeUrl?: string
  platformNotice?: string
}

export const apps: App[] = [
  // Flutter 앱 — 완성도 순
  {
    slug: 'menuway',
    name: 'menuWay',
    category: 'flutter',
    description: '해외 메뉴판을 찍으면 음식을 이해할 수 있게 설명해주는 AI 여행 앱',
    longDescription: `여행 가면 누구나 한 번쯤 겪는 순간.\n번역은 되지만, 어떤 음식인지 이해하기 어려울 때가 있습니다.\n\nmenuWay는 메뉴판을 촬영하면 메뉴 이름과 설명을 함께 제공합니다.\n\n단순 번역이 아니라,\n음식을 이해할 수 있도록 돕는 앱입니다.\n\n이제 주문 앞에서 멈추지 마세요.\n\nTranslate. Order. Enjoy.\n\nGoogle Play / App Store 버전은 광고가 포함되어 있습니다. 광고 없이 쓰고 싶다면 APK 직접 설치나 웹앱을 이용하세요 — 설치 시 5회는 무료로 체험할 수 있고, 이후에는 본인의 Gemini API 키를 등록(BYOK)하거나 스마트스토어에서 크레딧을 구매해 계속 사용할 수 있습니다.\n\nAndroid 직접 설치는 위 버튼으로 APK를 다운로드한 후 파일을 열어 설치합니다. 처음 설치 시 알 수 없는 앱 설치 허용 설정이 필요할 수 있습니다.`,
    api: ['Gemini'],
    storeReleased: true,
    iconUrl: '/apps/menuway/icon.png',
    screenshots: [
      '/apps/menuway/MenuWay_iOS_01.png',
      '/apps/menuway/MenuWay_iOS_02.png',
      '/apps/menuway/MenuWay_iOS_03.png',
      '/apps/menuway/MenuWay_iOS_04.png',
      '/apps/menuway/MenuWay_iOS_05.png',
      '/apps/menuway/MenuWay_LAST.png'
    ],
    androidUrl: 'https://play.google.com/store/apps/details?id=com.menuway.app&hl=ko',
    iosUrl: 'https://apps.apple.com/kr/app/menuway/id6758591797',
    webUrl: 'https://menuway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/menuwayall-v1.0.4%2B12/app-release.apk',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13657566636',
    purchaseLabel: '크레딧 구매',
    youtubeUrl: 'https://www.youtube.com/@zzindori/shorts',
    shorts: ['D_w3q4XwCa4', 'gTf98JexFGo', 'ss76szvONxo', '0DK2QBaTMac'],
    version: '1.0.4+12'
  },
  {
    slug: 'shotway',
    name: 'shotWay',
    category: 'flutter',
    description: '실시간 찍은 사진 공유 앱',
    longDescription: `누군가 사진을 찍으면, 방에 함께한 모두의 핸드폰에 알림이 옵니다. 바로 그 사진이요.\n\n같은 공간이라면 QR 코드 한 번이면 연결됩니다. 멀리 있다면 6자리 숫자만 알려주면 돼요. 번호 교환도, 친구 추가도, 앱 설치도 필요 없습니다.\n\n아이폰이든 안드로이드든 상관없이 쓸 수 있고, 완전 무료입니다. 광고도 없어요.\n\n📸 실시간 공유\n사진을 찍는 즉시 같은 방에 있는 모든 사람의 핸드폰으로 푸시 알림이 전송됩니다. 여행, 행사, 워크숍에서 한 사람이 찍은 사진을 모두가 바로 받아볼 수 있습니다. 사진은 클라우드에 안전하게 보관되며, 방에 있는 누구나 자유롭게 다운로드할 수 있습니다.\n\n🔗 연결方式\n같은 공간에서는 QR 코드로, 멀리 있는 사람은 6자리 코드로 연결됩니다. 복잡한 회원가입도, 친구 추가도 없습니다. 방을 만든 사람이 코드를 공유하면 끝입니다.\n\n🔄 크로스 플랫폼\niPhone과 Android 모두 동일한 경험으로 사용할 수 있습니다. 웹 버전도 제공되어 PC에서도 사진을 확인할 수 있습니다.\n\n💰 완전 무료\n광고도, 인앱 결제도, 구독료도 없습니다. 사진 공유는 누구에게나 자유로워야 한다고 생각합니다.`,
    api: ['Firebase', 'Supabase'],
    iconUrl: '/apps/shotway/icon.png',
    screenshots: [
      '/apps/shotway/shotWay01.jpg',
      '/apps/shotway/shotWay02.png'
    ],
    webUrl: 'https://shotway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/shotway-v1.0.0/shotWay.apk',
    pricingModel: 'free',
    version: '1.0.0+3',
    storeReleased: false
  },
  {
    slug: 'joa',
    name: 'JoA',
    category: 'flutter',
    description: 'AI 이미지 생성 앱',
    longDescription: `복잡한 설정 없이, 버튼 몇 번으로 만드는 자연스러운 한국인 옷핏 레퍼런스.\n\nJoA는 Google Gemini 이미지 생성 모델을 활용합니다. 남자·여자 카테고리, 연령, 체형, 스타일, 날씨 무드를 선택하면 9:16 세로 이미지가 바로 생성됩니다. 현재 날씨를 반영한 이미지 생성도 가능하며, 생성된 이미지는 히스토리로 저장됩니다.\n\n앱 설치 없이 Android, iPhone, PC 브라우저 어디서든 동일하게 사용할 수 있습니다.\n\n가입이나 로그인 없이 5장을 무료로 먼저 체험해볼 수 있습니다.\n\n이용권을 구매하면 하루 30장 생성 권한이 매일 자정에 자동 충전됩니다. 30일 기준 최대 900장이며, 미사용 분은 다음 날로 이월되지 않습니다. 인증 코드는 스마트폰, PC 등 여러 기기에서 동시에 사용할 수 있지만, 하루 30장 카운트는 기기 구분 없이 공유됩니다.\n\nGemini API Key를 직접 발급받아 앱 설정에 입력하는 방법으로도 이용할 수 있습니다. 이 경우 이용권 구매 없이 사용할 수 있지만, Google API 사용량에 따라 구글에 직접 요금이 부과됩니다. API Key는 이 사이트의 QR 변환 메뉴를 활용하면 스캔으로 간편하게 입력할 수 있습니다.\n\nAndroid 설치는 위 직접 설치 버튼으로 APK를 다운로드한 후 파일을 열어 설치합니다. 처음 설치 시 알 수 없는 앱 설치 허용 설정이 필요할 수 있습니다. 삭제는 아이콘을 길게 누르거나 설정 앱에서 제거할 수 있습니다.`,
    api: ['Gemini'],
    iconUrl: '/apps/joa/icon.png',
    screenshots: [
      '/apps/joa/Screenshot_20260607_165645.jpg',
      '/apps/joa/Screenshot_20260607_165650.jpg',
      '/apps/joa/Screenshot_20260607_165702.jpg',
      '/apps/joa/Screenshot_20260607_165859.jpg',
      '/apps/joa/Screenshot_20260607_170008.jpg'
    ],
    webUrl: 'https://joa.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/joa-v1.0.0.9/JoA.apk',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13625209650',
    version: '1.0.0+9',
    platformNotice: '웹앱은 생성 이미지를 브라우저에만 저장합니다. iOS(Safari)는 7일간 미접속 시 데이터가 자동 삭제되니 반드시 "홈 화면에 추가"로 실행하세요. Android는 데이터 보존을 위해 APK 직접 설치를 권장합니다.'
  },
  {
    slug: 'itne',
    name: 'itNe',
    category: 'flutter',
    description: '냉장고 식재료 관리 + 남은 재료로만 AI 레시피 추천',
    longDescription: `냉장고 문을 열고 "이걸로 뭘 만들지?" 고민한 적 있으신가요?\n\nitNe는 냉장고 속 식재료를 사진으로 찍으면 자동으로 인식하고 목록을 만들어줍니다. 그리고 남은 재료로만 만들 수 있는 레시피를 AI가 추천해줍니다.\n\n없는 재료를 사러 나가지 않아도 됩니다. 있는 것만으로 충분합니다.\n\n냉장고를 요리사로 만드는 앱.\n\n📸 식재료 자동 인식\nML Kit 기반 이미지 인식으로 식재료 사진을 찍으면 AI가 자동으로 무슨 재료인지 분류합니다. 양파, 당근, 애호박 같은 기본 채소부터 각종 양념과 소스류까지 폭넓게 인식합니다. 잘못 인식된 재료는 직접 수정할 수 있어 정확도를 계속 높여갈 수 있습니다.\n\n🗂 냉장고 목록 관리\n인식된 식재료는 카테고리(채소·과일·육류·해산물·유제품·양념·기타)별로 정리됩니다. 유통기한을 직접 입력하면 임박한 순서대로 정렬되며, 유통기한이 지난 재료는 자동으로 강조 표시됩니다. 소진한 재료는 스와이프로 빠르게 삭제할 수 있습니다.\n\n🍳 AI 레시피 추천\n현재 냉장고에 있는 재료만으로 만들 수 있는 요리를 Gemini AI가 추천합니다. 재료 소진 우선순위(유통기한 임박)를 반영하고, 한국식·중식·양식·일식 등 카테고리별 필터도 지원합니다. 각 레시피에는 조리 시간, 난이도, 필요 재료, 단계별 조리법이 포함됩니다.\n\n📱 크로스 플랫폼 지원\nAndroid APK 설치부터 웹 브라우저 접속까지 자유롭게 선택할 수 있습니다. 모든 데이터는 클라우드에 동기화되어 기기를 바꿔도 이어서 사용할 수 있습니다.\n\n💳 이용권\n무료 체험 후 네이버 스마트스토어에서 이용권을 구매하면 매일 일정 횟수의 레시피 생성 권한이 자정에 자동 충전됩니다. 미사용 횟수는 다음 날로 이월되지 않습니다.`,
    api: ['Gemini', 'MLKit'],
    iconUrl: '/apps/itne/icon.png',
    screenshots: [
      '/apps/itne/itne_01.jpg',
      '/apps/itne/itne_02.jpg',
      '/apps/itne/itne_03.jpg',
      '/apps/itne/itne_04.jpg',
      '/apps/itne/itne_05.jpg',
      '/apps/itne/itne_06.jpg'
    ],
    webUrl: 'https://itne.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/itne-v1.5.5.32/app-release.apk',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13644369839',
    version: '1.5.6+33',
    platformNotice: '웹앱은 냉장고 데이터를 브라우저에만 저장합니다. iOS(Safari)는 7일간 미접속 시 데이터가 자동 삭제되니 반드시 "홈 화면에 추가"로 실행하세요. Android는 데이터 보존을 위해 APK 직접 설치를 권장합니다.'
  },
  {
    slug: 'codi-d',
    name: 'CODI:D',
    category: 'flutter',
    description: 'AI 패션 코디네이터',
    longDescription: `옷은 많은데 뭘 입을지 모르겠다면, CODI:D에게 맡기세요.\n\n카메라로 옷을 찍으면 AI가 분석하고, 어울리는 코디를 직접 이미지로 생성해줍니다. Gemini로 스타일을 분석하고 Imagen으로 코디 이미지를 만들어냅니다.\n\n체형별 마네킹(슬림·커브·상하체 비만·플러스 사이즈 등)으로 내 몸에 맞는 스타일을 추천합니다. 코디를 쌓아갈수록 나만의 패션 아바타가 진화합니다.\n\n웹 데이터 영구 보존(IndexedDB), iOS 홈 화면 추가 지원.\n\n옷장이 스타일리스트가 되는 앱.\n\n👗 AI 코디 생성\n옷장에 있는 아이템을 하나씩 촬영해 등록하세요. CODI:D가 각 아이템의 스타일·색상·소재·계절감을 분석하고, 서로 어울리는 조합을 찾아냅니다. 상의·하의·아우터·신발·액세서리까지 풀코디 이미지를 Imagen이 생성해줍니다. '오늘 뭐 입지?' 고민은 이제 CODI:D가 대신합니다.\n\n🧍 체형 맞춤 마네킹\n내 몸에 맞는 코디가 진짜 코디입니다. 슬림, 커브핏, 상체비만, 하체비만, 플러스 사이즈까지 — CODI:D는 다양한 체형 마네킹에 옷을 입혀 보여줍니다. 내 체형과 비슷한 마네킹을 선택하면, 실제로 입었을 때 어떤 느낌일지 미리 확인할 수 있습니다.\n\n🔄 스타일 진화\n코디를 생성할 때마다 AI가 내 취향을 학습합니다. 자주 선택하는 색감, 선호하는 핏, 즐겨 입는 스타일을 파악해 점점 더 나에게 맞는 코디를 제안합니다. 마치 나만의 패션 어시스턴트를 키워가는 기분입니다.\n\n📱 어디서나 접근\nFlutter로 제작되어 Android, iOS, 웹 브라우저 어디서든 동일한 경험을 제공합니다. 웹 버전은 IndexedDB를 활용해 생성된 코디 이미지를 브라우저에 영구 저장하며, iOS에서는 홈 화면에 추가해 네이티브 앱처럼 사용할 수 있습니다.`,
    api: ['Gemini', 'Imagen'],
    iconUrl: '/apps/codi-d/icon.png',
    screenshots: [
      '/apps/codi-d/codi_d01.jpg',
      '/apps/codi-d/codi_d02.jpg',
      '/apps/codi-d/codi_d03.jpg',
      '/apps/codi-d/codi_d04.jpg',
      '/apps/codi-d/codi_d05.jpg',
      '/apps/codi-d/codi_d06.jpg',
      '/apps/codi-d/codi_d07.jpg'
    ],
    webUrl: 'https://codi-d.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codi-d-v1.0.6.7/CODI_D.apk',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13646465925',
    purchaseLabel: '크레딧 구매',
    version: '1.0.6+7',
    platformNotice: '웹앱은 생성한 코디 이미지를 브라우저에만 저장합니다. iOS(Safari)는 7일간 미접속 시 데이터가 자동 삭제되니 반드시 "홈 화면에 추가"로 실행하세요. Android는 데이터 보존을 위해 APK 직접 설치를 권장합니다.'
  },
  {
    slug: 'careway',
    name: 'careWay',
    category: 'flutter',
    description: '부모님 복지 혜택 매니저',
    longDescription: `복지 혜택은 찾기 어렵고, 찾아도 신청은 더 복잡합니다.\n\ncareWay는 부모님의 나이, 지역, 건강 상태를 등록하면 받을 수 있는 복지 서비스를 자동으로 찾아줍니다. 중앙부처 복지 API와 전국 지자체 홈페이지를 함께 수집하고, AI가 부모님 프로필과 대조해 우선 확인·검토 후·알아두기 세 단계로 분류해줍니다.\n\n찾는 것에서 끝나지 않고, 신청 진행 상황과 서류까지 가족이 함께 관리할 수 있습니다.\n\n부모님 복지, 이제 자녀가 직접 챙겨드릴 수 있습니다.\n\n🎯 맞춤 혜택 자동 매칭\n부모님의 나이·지역·요양등급·독거 여부 같은 태그를 등록하면, AI가 전국 복지 서비스 중 실제로 해당되는 것만 우선 확인/검토 후/알아두기로 나눠 보여줍니다. 서비스마다 AI 요약과 해당 사유 태그가 함께 표시돼 왜 추천됐는지 바로 이해할 수 있습니다.\n\n👨‍👩‍👧 가족 공유\nQR 코드나 6자리 코드 하나로 부모님 프로필을 가족에게 공유할 수 있습니다. 형제자매도 앱에 로그인만 하면, 부모님 정보를 처음부터 다시 입력할 필요 없이 코드 하나로 같은 혜택 목록과 신청 현황을 그대로 이어받습니다.\n\n📋 신청 진행 관리\n관심 있는 혜택을 저장됨 → 준비 중 → 신청 완료 단계로 관리하고, 진행 상황을 가족끼리 타임라인 메모로 남길 수 있습니다. "주민센터 방문 예정", "서류 제출 완료" 처럼 짧게 남겨도 누가 어디까지 진행했는지 가족 모두가 바로 확인할 수 있습니다.\n\n📁 서류 보관함\n신청에 필요한 서류를 사진으로 찍어 부모님별로 보관합니다. 스캔된 서류는 신청 항목에 바로 첨부하거나 다운로드할 수 있어, 매번 서류를 다시 찾을 필요가 없습니다.`,
    api: ['Gemini', 'Supabase'],
    iconUrl: '/apps/careway/icon.png',
    screenshots: [
      '/apps/careway/careway_01.jpg',
      '/apps/careway/careway_02.jpg',
      '/apps/careway/careway_03.jpg',
      '/apps/careway/careway_04.jpg',
      '/apps/careway/careway_05.jpg',
      '/apps/careway/careway_06.jpg',
      '/apps/careway/careway_07.jpg',
      '/apps/careway/careway_08.jpg'
    ],
    webUrl: 'https://careway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/careway-v1.2.2.19/careWay.apk',
    pricingModel: 'free',
    version: '1.2.2+19'
  },
  {
    slug: 'farmguide',
    name: 'farmWay',
    category: 'flutter',
    description: '스마트 농업 경영 앱 (토지/작물 등록~수익정산)',
    longDescription: `농사는 기억에만 의존하기엔 너무 복잡합니다.\n\nfarmWay는 토지 등록부터 작물 선택, 파종·수확 일정 관리, 인력 기록, 수익 정산까지 농업 경영 전 과정을 하나의 앱에서 관리합니다.\n\n네이버 지도 지적도를 직접 탭해서 내 농지를 등록하고, 심은 작물의 파종일부터 수확예정일까지 진행률로 확인할 수 있습니다. 날씨와 연동된 병해충 위험 경보로 미리 대비하고, 수확이 끝나면 차트로 수익과 비용을 한눈에 확인할 수 있습니다.\n\n농부를 위한 스마트 경영 도우미.\n\n🗺️ 지적도 기반 토지 등록\n네이버 지도의 지적도 레이어에서 내 땅을 직접 탭하거나 주소를 검색해서 토지를 등록합니다. 지목·면적·지번이 자동으로 채워지고, 등록한 토지는 지도 위에서 한눈에 관리됩니다.\n\n📅 재배 캘린더 & 진행률\n등록한 작물마다 파종일부터 수확예정일까지 D-day와 진행률(%)이 자동 계산됩니다. 여러 작물을 동시에 재배할 때도 캘린더 뷰에서 전체 일정을 겹쳐서 확인할 수 있습니다.\n\n🌦️ 날씨 연동 병해충 경보\n기상청 단기예보를 재배 중인 작물·지역과 대조해 역병·탄저병 같은 병해충 발생 위험을 위험/주의 단계로 미리 알려줍니다. 고온다습 조건처럼 위험 사유도 함께 표시돼 바로 대응할 수 있습니다.\n\n🌱 지역 맞춤 작물 추천\n현재 위치의 기온·날씨를 기준으로 지금 심기 좋은 작물과 그 지역 추천 작물을 보여줍니다. 작물 데이터는 FAO·농촌진흥청(RDA) 자료로 교차검증돼 있습니다.\n\n✨ AI 파종 조언\n작물·위치·면적·파종일과 현재 기온, 진행 중인 병해충 정보를 종합해 Gemini AI가 파종 타이밍, 지역별 재배 주의사항, 실전 팁, 시세 전망까지 맞춤 조언을 생성해줍니다.\n\n👥 인력 수급 매칭\n파종·수확 시기에 필요한 일손을 구인 등록하거나, 반대로 일용직으로 구직 등록할 수 있습니다. 작업 유형·인원·일당·지역 조건으로 농번기 인력난을 완화합니다.\n\n💰 수익 정산 & 판매 관리\n작물별·재배별로 비용과 매출을 기록하고 월별 차트로 순이익을 추적합니다. 판매 채널·판매량·단가·구매자까지 남겨 다음 시즌 판매 전략에 참고할 수 있습니다.`,
    api: ['Supabase', 'Naver Maps', 'Gemini'],
    iconUrl: '/apps/farmguide/icon.png',
    screenshots: [
      '/apps/farmguide/farmguide_01.jpg',
      '/apps/farmguide/farmguide_02.jpg',
      '/apps/farmguide/farmguide_03.jpg',
      '/apps/farmguide/farmguide_04.jpg',
      '/apps/farmguide/farmguide_05.jpg',
      '/apps/farmguide/farmguide_06.jpg',
      '/apps/farmguide/farmguide_07.jpg'
    ],
    webUrl: 'https://farmway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/farmguide-v1.0.0.2/farmGuide.apk',
    version: '1.0.0+2'
  },
  {
    slug: 'gateflow',
    name: 'gateFlow',
    category: 'flutter',
    description: '공항 동선 오케스트레이터 & 출국 스트레스 제거 비서',
    longDescription: `공항에서 헤매거나, 뭔가를 빠뜨린 채 출국한 경험 있으신가요?\n\ngateFlow는 출국 전 준비 체크리스트, 공항 터미널 동선 안내, 여권 보안 저장소까지 출국의 모든 과정을 함께합니다.\n\n여권을 카메라로 찍으면 OCR이 자동으로 정보를 읽어냅니다. 저장된 여권 정보는 생체인증으로만 접근할 수 있어 안전합니다.\n\n출발 타이머와 AI 여행 조언으로 첫 해외여행도 자신 있게.`,
    api: ['Gemini', 'MLKit OCR'],
    iconUrl: '/apps/gateflow/icon.png',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/gateflow-v0.1.0/app-release.apk',
    pricingModel: 'free',
    version: '0.1.0+1',
    storeReleased: false
  },
  {
    slug: 'igomoya',
    name: 'igoMoya',
    category: 'flutter',
    description: '궁금한 것 찍으면 바로 AI 설명 + 타임라인 사진 정리',
    longDescription: `길을 걷다, 음식을 보다, 궁금한 게 생기는 순간.\n\nigoMoya는 카메라를 대면 AI가 바로 설명해줍니다. 분할 화면으로 찍는 순간 결과를 바로 확인할 수 있습니다.\n\n찍은 사진들은 위치와 시간순으로 타임라인에 정리되고, 지도 위에서도 한눈에 확인할 수 있습니다. 오늘 어디서 무엇을 봤는지 기억하고 싶을 때 꺼내보세요.\n\n궁금함을 바로 해결하는 AI 카메라 메모.\n\n📸 분할 화면 실시간 분석\n위는 카메라, 아래는 결과. 찍는 순간 AI가 바로 분석을 시작해 신뢰도(%)와 함께 결과를 실시간으로 보여줍니다. 음식이든 간판이든 브랜드 캐릭터든, 무엇이든 구체적으로 짚어냅니다.\n\n📝 깊이 있는 분석 결과\n한 줄 요약뿐 아니라 유래·재료·문화적 배경까지 담은 상세 설명, 대화 소재로 쓸 수 있는 이야기거리, 태그까지 한 번에 정리해줍니다.\n\n🗂️ 위치·시간순 이미지 창고\n찍은 사진들이 촬영 장소와 시간 기준으로 자동 그룹핑되어 타임라인으로 정리됩니다. "그날 거기서 뭘 봤더라" 할 때 바로 찾아볼 수 있습니다.\n\n🗺️ 사진 지도\n찍은 사진들이 원형 썸네일 마커로 지도 위에 표시됩니다. 마커를 탭하면 그 자리에서 분석 결과를 바로 볼 수 있습니다.\n\n💳 무료 7장 + 크레딧\n설치 후 7장은 바로 무료로 체험할 수 있습니다. 이후에는 본인의 Gemini API 키를 등록(BYOK)하거나 스마트스토어에서 크레딧을 구매해 계속 사용할 수 있습니다.\n\n🌐 웹앱 지원\n설치 없이 브라우저에서 바로 써볼 수 있습니다. iOS 사용자도 앱스토어 없이 바로 체험 가능합니다.`,
    api: ['Gemini'],
    iconUrl: '/apps/igomoya/icon.png',
    screenshots: [
      '/apps/igomoya/igomoya_01.jpg',
      '/apps/igomoya/igomoya_02.jpg',
      '/apps/igomoya/igomoya_03.jpg',
      '/apps/igomoya/igomoya_04.jpg',
      '/apps/igomoya/igomoya_05.jpg',
      '/apps/igomoya/igomoya_06.jpg'
    ],
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/igomoya-v0.1.6.7/igoMoya.apk',
    webUrl: 'https://igomoya.wowhit.org',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13659737802',
    purchaseLabel: '크레딧 구매',
    version: '0.1.6+7',
    platformNotice: '웹앱은 찍은 사진/분석 결과를 브라우저에만 저장합니다. iOS(Safari)는 7일간 미접속 시 데이터가 자동 삭제되니 반드시 "홈 화면에 추가"로 실행하세요. Android는 데이터 보존을 위해 APK 직접 설치를 권장합니다.'
  },
  {
    slug: 'onbidway',
    name: 'onbidWay',
    category: 'flutter',
    description: '온비드(공매) 정보 앱',
    longDescription: `공매 물건을 찾으러 매번 온비드 사이트에 들어가야 한다면 번거롭습니다.\n\nonbidWay는 공공데이터 API를 기반으로 부동산, 동산, 차량 공매 정보를 한곳에서 조회합니다. 실시간 데이터로 최신 공매 현황을 확인할 수 있습니다.\n\n관심 있는 물건은 찜해두고, 같은 물건의 여러 회차를 한눈에 비교할 수 있습니다.\n\n공매 정보를 손 안에서.`,
    api: ['공공데이터포털'],
    iconUrl: '/apps/onbidway/icon.png',
    webUrl: 'https://onbidway.wowhit.org'
  },
  {
    slug: 'pingway',
    name: 'pingWay',
    category: 'flutter',
    description: '알림/메시지 앱',
    longDescription: `받은 메일함은 넘치고, 캘린더는 정리되지 않은 채 하루가 지나갑니다.\n\npingWay는 Gmail과 Google Calendar를 AI로 연결합니다. Gemini가 받은 메일을 자동으로 분류하고, 중요한 일정을 정리해줍니다.\n\nFire기반 푸시 알림으로 중요한 소식을 놓치지 않습니다. 메일과 일정이 하나의 앱에서 AI 비서처럼 작동합니다.\n\n흩어진 알림을 하나로.`,
    api: ['Gemini', 'Firebase', 'Gmail', 'Google Calendar'],
    iconUrl: '/apps/pingway/icon.png'
  },
  {
    slug: 'talkway',
    name: 'talkWay',
    category: 'flutter',
    description: '실시간 화자분리 자막 앱 (청각장애인용)',
    longDescription: `소리가 잘 들리지 않는 환경에서도 대화를 이어갈 수 있어야 합니다.\n\ntalkWay는 실시간으로 주변 소리를 인식해 자막으로 변환합니다. Google STT와 Naver CLOVA 두 엔진을 지원해 인식 정확도를 높였습니다.\n\n화자 분리 기능으로 누가 말하는지도 구분할 수 있습니다. 회의, 강의, 일상 대화 어디서든 자막이 따라옵니다.\n\n청각 장애인과 소음이 심한 환경을 위한 실시간 자막 앱.`,
    api: ['Google STT', 'Naver CLOVA'],
    iconUrl: '/apps/talkway/icon.png',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/talkway-v1.0.0%2B1/app-release.apk',
    version: '1.0.0+1',
    storeReleased: false
  },
  {
    slug: 'txtfit',
    name: 'txtFit',
    category: 'flutter',
    description: '텍스트 분할 · 정제 유틸리티',
    longDescription: `긴 텍스트를 AI 채팅에 붙여넣으면 글자 수 제한에 막힐 때가 있습니다.\n\ntxtFit은 두 가지 기능을 제공합니다. 긴 텍스트를 원하는 글자 수 단위로 나눠 [1/3], [2/3] 형식으로 순서대로 복사할 수 있는 분할 기능, 그리고 나눠진 블럭들을 다시 깔끔하게 이어붙이는 결합 기능입니다.\n\n분할 헤더가 자동으로 붙고, 반대로 제거하는 것도 가능합니다.\n\n글자 수 제한을 넘어, 내 텍스트를 내 마음대로.`,
    iconUrl: '/apps/txtfit/icon.png',
    webUrl: 'https://txtfit.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/txtfit-v1.0.1/txtFit.apk',
    version: '1.0.1',
    sourceCodeUrl: '/apps/txtfit/index.html'
  },
  {
    slug: 'codeway',
    name: 'codeWay',
    category: 'flutter',
    description: '멀티 QR 스캔으로 대용량 텍스트 수신 · SHA256 무결성 검증',
    longDescription: `파일 전송 없이 텍스트를 전달하고 싶을 때.\n\ncodeWay는 대용량 텍스트를 QR 코드 여러 장으로 분할해 전송하고, 수신 측에서 순서대로 스캔해 원문을 복원합니다. SHA256 해시 검증으로 데이터 무결성을 보장합니다.\n\n앱 설치 없이 웹 버전으로도 동작합니다. 인터넷 연결이 없는 환경에서도 안전하게 텍스트를 전달할 수 있습니다.\n\n보안이 필요한 텍스트 전달에 적합한 멀티 QR 유틸리티.`,
    iconUrl: '/apps/codeway/icon.png',
    webUrl: 'https://codeway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codeway-v1.0.0/codeWay.apk',
    version: '1.0.0'
  },

  {
    slug: 'bibleway',
    name: 'bibleWay',
    category: 'flutter',
    description: '개역한글 성경 읽기 + AI 해설',
    longDescription: `성경을 읽다 보면 낯선 인물, 지명, 표현이 나올 때가 많습니다.\n\nbibleWay는 개역한글 성경을 읽으면서 궁금한 절을 터치하면 AI가 바로 해설해주는 앱입니다. Gemini AI가 쉬운 말 풀이, 현대어 재진술, 한줄 요약, 화자/청자 정보까지 알려줍니다.\n\n통독 진행률과 N회독 카운트로 꾸준한 읽기 습관을 도와줍니다. 사도신경과 주기도문도 새번역/전통 버전으로 함께 볼 수 있습니다.\n\nAI 해설은 최초 조회 시 생성되어 캐싱되므로, 같은 절을 다시 볼 때는 즉시 표시됩니다. Supabase로 여러 기기에서 읽기 진도를 동기화할 수 있습니다.\n\n말씀을 더 깊이 이해하고 싶은 분들을 위한 AI 성경 읽기 도우미.`,
    api: ['Gemini', 'Supabase'],
    iconUrl: '/apps/bibleway/icon.png',
    screenshots: [
      '/apps/bibleway/bibleway_01.jpg',
      '/apps/bibleway/bibleway_02.jpg',
      '/apps/bibleway/bibleway_03.jpg',
      '/apps/bibleway/bibleway_04.jpg',
      '/apps/bibleway/bibleway_05.jpg'
    ],
    webUrl: 'https://bibleway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/bibleway-v1.0.1.2/bibleWay.apk',
    pricingModel: 'free',
    version: '1.0.1+2'
  },

  // Web 앱
  {
    slug: 'bbangway',
    name: 'BBangWay',
    category: 'web',
    description: '베이커리 빵 인식 관리자',
    longDescription: `베이커리에서 빵 이름과 가격을 일일이 입력하는 건 번거롭습니다.\n\nBBangWay는 빵 이미지를 촬영하면 Gemini AI가 자동으로 인식하고 분류합니다. 점포별 메뉴 설정, QR 코드 생성까지 베이커리 관리에 필요한 기능을 담았습니다.\n\n3D 모델 뷰어로 상품을 시각적으로 확인할 수도 있습니다.\n\nAI가 도와주는 베이커리 관리 도구.`,
    api: ['Gemini'],
    iconUrl: '/apps/bbangway/icon.png',
    webUrl: 'https://bbangway.wowhit.org'
  },
  {
    slug: 'postest',
    name: 'posTest',
    category: 'web',
    description: '베이커리 POS 연습 앱',
    longDescription: `베이커리 POS 기기 사용이 처음이라면 실수가 걱정됩니다.\n\nposTest는 실제 POS 화면과 동일한 환경에서 연습할 수 있는 시뮬레이터입니다. 상품을 선택하고 결제하는 기본 흐름을 반복 연습할 수 있습니다.\n\n퀴즈 모드에서는 상품명을 맞추는 타이머 도전이 가능합니다. 점수가 쌓이면 랭킹에 기록됩니다.\n\n출근 전 5분, POS 완벽 적응.`,
    iconUrl: '/apps/postest/icon.png',
    webUrl: 'https://postest.wowhit.org'
  },
  {
    slug: 'qrmaker',
    name: 'qrMaker',
    category: 'web',
    description: '대용량 텍스트를 여러 QR 코드로 분할 생성하는 오프라인 유틸리티',
    longDescription: `긴 텍스트나 소스코드를 QR 코드로 전송해야 할 때, 한 장으로는 용량 제한 때문에 불가능합니다.\n\nqrMaker는 입력된 텍스트를 UTF-8 바이트 기준으로 자동 분할해 여러 개의 QR 코드로 생성합니다. SHA256 해시를 QR 헤더에 포함해 수신 측에서 무결성을 검증할 수 있습니다.\n\n📱 오프라인 동작\n인터넷 연결 없이 브라우저에서 바로 작동합니다. file:// 프로토콜에서도 실행 가능해 로컬 파일로 저장해두면 언제든 사용할 수 있습니다.\n\n🔀 스캔 기기별 밀도 선택\n생성 전 "스캔 기기"를 고를 수 있습니다. Android/Chrome은 네이티브 디코더가 강력해 고밀도(청크당 최대 2,874바이트)로 QR 장수를 줄이고, iOS Safari는 JS 디코더라 저밀도(청크당 약 1,074바이트)로 QR을 더 쪼개는 대신 인식률을 높입니다. 각 QR에는 [인덱스/전체:해시] 헤더가 붙어 codeWay 같은 멀티 QR 스캐너로 순서대로 읽으면 원문이 복원됩니다.\n\n🖥 반응형 QR 뷰어\n생성된 QR 코드는 전용 뷰어 탭에서 확인할 수 있습니다. 윈도우 크기에 맞춰 QR이 정사각형을 유지하며 자동 조절되고, 키보드 화살표로 QR을 넘길 수 있습니다.\n\n🔒 완전한 오프라인\n외부 CDN, API 호출 없이 SHA256 순수 JS 구현과 QR 인코더가 내장되어 있습니다. 네트워크가 차단된 환경에서도 안전하게 동작합니다.`,
    iconUrl: '/apps/qrmaker/icon.png',
    webUrl: 'https://zzindori.github.io/qrMaker/',
    sourceCodeUrl: '/apps/qrmaker/index.html'
  },
  {
    slug: 'woweditor',
    name: 'wowEditor',
    category: 'web',
    description: 'Monaco 기반 브라우저 코드 에디터 + AI 채팅',
    longDescription: `설치 없이 브라우저에서 바로 여는 코드 에디터입니다.\n\nMonaco Editor(VS Code와 같은 엔진)를 오프라인 번들로 통째로 넣어서, File System Access API로 로컬 폴더를 열고 그대로 저장까지 할 수 있습니다.\n\n오른쪽 채팅창에서 Gemini API Key를 등록하면, 지금 열어둔 폴더 구조와 파일 내용을 맥락으로 AI에게 바로 질문하고 코드를 고칠 수 있습니다.\n\n탭 편집, 폴더 트리, Diff 뷰, 이미지/PDF 미리보기까지 파일 하나로 동작하는 단일 HTML 에디터입니다.`,
    webUrl: 'https://wowEditor.wowhit.org'
  },

  // 기타
  {
    slug: 'bbibbiwatch',
    name: 'BBiBBi',
    category: 'other',
    description: '워치 앱',
    longDescription: `손목 위에서 알림을 주고받는 스마트워치 앱.\n\nBBiBBi는 Android Wear OS용 앱입니다. 방을 만들거나 코드로 방에 입장해 연결된 사람들과 간단한 신호를 주고받을 수 있습니다.\n\nFirebase 기반 푸시로 상대방이 신호를 보내면 즉시 진동으로 알려줍니다.\n\n말 없이 손목으로 연결되는 신호 앱.`,
    platform: 'Android Watch',
    api: ['Firebase']
  },
  {
    slug: 'hclinkway',
    name: 'HCLink (한국어화)',
    category: 'other',
    description: '중국산 브이로그 미러링 스크린용 앱을 한국어화 + 버그 수정한 리패치 버전',
    longDescription: `이 앱은 제가 처음부터 만든 게 아니라, 시중에 판매 중인 중국산 "브이로그 스크린"(폰 후면 카메라 화면을 무선/유선으로 미러링해주는 소형 모니터) 부속 앱 HCLink를 뜯어고친 버전입니다.\n\n원본 앱은 전체 UI가 중국어로만 되어 있고, 재서명하면 자체 변조 감지(Pairip) 때문에 강제종료되고, 무선(WiFi Direct) 연결도 기기 자체 결함으로 거의 항상 실패하는 상태였습니다.\n\nAPK를 디컴파일해서 다음을 고쳤습니다.\n\n🇰🇷 전체 UI 한국어 번역\n중국어 문자열 79개를 리소스 단에서 한국어로 교체.\n\n🔓 Pairip 라이선스체크 우회\n재서명한 APK를 정품이 아니라고 판단해 실행 즉시 죽이던 로직 제거.\n\n📡 무선 연결 구조 개선\n원본 앱의 WiFi Direct 구현 자체에 그룹 역할 판정 버그가 있어 정상적인 연결도 실패로 처리되던 것을 수정하고, 능동적으로 기기를 찾아 접속하는 서브넷 스캔 로직을 새로 추가했습니다. 그래도 기기 자체 하드웨어 한계로 불안정해서, 최종적으로는 안드로이드 기본 스마트뷰(Miracast)로 바로 연결되도록 우회 처리했습니다.\n\n리버스 엔지니어링 및 스마리(smali) 바이트코드 패치로 진행한 개인용 프로젝트입니다.`,
    platform: 'Android (APK 재서명)',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/hclinkway-v1.2.0-ko/hclink_ko_signed.apk',
    version: '1.2.0',
    storeReleased: false
  },
  {
    slug: 'stack',
    name: '층층이',
    category: 'other',
    description: '쌓고 팔고, 빨리빨리! 김밥·붕어빵·치킨… 층마다 다른 가게를 키우며 한국 상가 건물을 끝없이 올리는 아이들 아케이드 게임 (시제품)',
    longDescription: `층마다 다른 가게가 들어선 한국 상가 건물을 키우는 아이들 아케이드 게임입니다. 김밥을 말고, 붕어빵을 굽고, 치킨을 튀겨 등에 높이 쌓아 나르고, 번 돈으로 일꾼을 고용해 자동화하면서 건물을 끝없이 올려 갑니다. 손님들은 기다리다 "빨리빨리!"를 외치니 서둘러야 합니다.

▶ 처음 이렇게 해요
1. 화면 아무 데나 드래그하면 조이스틱이 생깁니다(PC는 WASD·방향키).
2. 생산기 앞 회색 칸에 서 있으면 만든 물건이 등 뒤에 차곡차곡 쌓입니다.
3. 파란 '판매' 칸에 서면 판매대에 내려놓고, 줄 선 손님이 사 갑니다.
4. 초록 매트 위 돈다발을 밟아 돈을 챙깁니다.
5. 바닥의 점선 칸 위에 서 있으면 돈이 조금씩 들어가며 업그레이드됩니다.
6. 생산기 3대를 다 열면 오른쪽 위 노란 칸에서 다음 층을 열 수 있습니다. 새 층을 열면 개업 화환이 섭니다.

🏢 층층이 상가
• 층마다 생산기 3대가 메뉴가 다 달라요(5층 한강라면은 라면만, 6층 노래방은 음료 맛만 달라요). 한 층 물건은 값이 같아서 손님은 그 층 것이면 아무거나 받아요.
• 1층 층층분식: 떡볶이 철판(국자로 컵에 담기) · 김밥 말이대(김발로 말아 썰기) · 순대 찜통(뚜껑이 덜컹, 도마에서 썰기)
• 2층 따끈 붕어빵: 호떡 철판(누르개로 꾹) · 붕어빵 손수레(무쇠 틀이 탁) · 계란빵 틀(달걀을 톡)
• 3층 바삭치킨: 양념 버무림 볼(흔들흔들) · 후라이드 튀김기(바구니 탈탈) · 간장 석쇠(붓으로 쓱쓱)
• 4층 24시 층층편의점: 핫바 온장고(빙글빙글) · 바나나우유 냉장고 · 호빵 찜기(김이 뭉게뭉게)
• 5층 한강라면: 한강 편의점 즉석 라면 기계만 3대 — 창밖 한강 다리를 보며 은박 그릇 라면
• 6층 ♪ 코인노래방: 노래방 기계 3대 — '100점!'이 뜨면 옆 냉장고에서 음료 캔. 기계마다 식혜 · 민트 · 포도 캔
• 7층부터는 3D 프린터 공장이 이어지고, 층은 끝없이 올라갑니다. 위층일수록 물건 값이 5배씩 오릅니다.
• 층마다 손님도 다릅니다(교복 학생, 퇴근길 직장인, 할머니, 등산모자 아저씨, 밀짚모자 관광객…). 맨 앞에 오면 "김밥 2줄이요!", "반반 무 많이요!"처럼 주문합니다.

🧍 손님
• 머리 위 말풍선에 사고 싶은 개수가, 그 밑 막대에 참을성이 보입니다.
• 손님은 자기 층 물건만 삽니다. 다른 층 물건은 등에 남습니다(배달 주문에 쓸 수 있음).
• 오래 기다리게 하면 "빨리빨리!" 재촉하다가 "에이, 안 사!" 하고 떠납니다. 빨리 채워 주면 팁 20%를 줍니다.

📦 직접 나르면 더 벌어요
• 주인공이 직접 판매대에 내려놓은 물건은 2배 값에 팔립니다(판매대 위 파란 테두리).
• 가끔 반짝이는 황금 물건이 나옵니다. 어느 층에서 나왔든 지금 가장 높은 층 물건 값의 10배라 아래층 황금도 잭팟입니다. 일꾼은 나르지 못하고, 60초 안에 가져가지 않으면 사라집니다(10초 전부터 깜빡임).

💰 돈
• 돈은 만·억·조 단위로 표시됩니다.
• 판매 대금은 층마다 돈더미에 쌓입니다. 손님 40명분이 쌓이면 꽉 차서(MAX) 챙길 때까지 그 층 판매가 멈춥니다.
• 지갑은 모든 층이 함께 쓰고 한도가 있습니다. 꽉 차면 돈을 쓰거나 지갑을 키워야 다시 챙길 수 있습니다.
• 자동 수금(층마다): 다른 층에 있을 때 그 층 돈더미가 알아서 지갑으로 들어옵니다. 산 층에는 ₩ 수금 로봇이 돈더미 주위를 돕니다.
• 잔업(오프라인, 층마다): 게임을 꺼 둔 동안에도 그 층 일꾼이 평소 속도의 절반으로 벌어 보물상자 '잔업수당'에 쌓아 둡니다. 일꾼이 1명 이상 있어야 하고, 최대 시간은 1 → 2 → 4 → 8시간으로 늘어납니다. 다시 들어오면 층마다 가서 상자를 밟아 챙깁니다(비어 있으면 닫힌 상자에 달, 차 있으면 뚜껑이 열리고 빛이 납니다).

⚙️ 업그레이드
• 1층에서만(모든 층 공통): 적재량, 이동속도, 지갑, 엘리베이터 설치
• 층마다 따로: 생산기 열기, 일꾼 고용(최대 3명), 판매속도, 자동 수금, 잔업(오프라인), 다음 층 열기
• 층 이동: 오른쪽 위에 엘리베이터 문, 내려가는 계단(▼), 올라가는 계단(▲)이 나란히 있습니다. 엘리베이터를 설치하면 문 앞에 서서 원하는 층으로 바로 갑니다.

🚨 이런 일이 생겨요
• 배달 주문 🛵: 어느 층 손님이 다른 층 음식을 시킵니다(노래방에서 치킨처럼). 그 층 물건을 들고 가 초록 칸 손님에게 건네면, 어느 층 물건이든 개당 지금 가장 높은 층 물건 값의 6배를 받습니다. 시간이 절반 넘게 남았으면 배달팁 50%와 '총알 배달!'. 다 주고 나서도 같은 층 물건이 등에 남아 있으면 배달 손님이 "남은 거 떨이로 다 주세요!" 하고 반값에 사 갑니다. 주인공만 할 수 있고, 놓쳐도 벌칙은 없습니다.
• 건물주 👑: 일꾼은 상대하지 못하는 손님입니다. 제한 시간 안에 옆에 가서 물건을 건네면 물건 값의 5배, 황금을 건네면 그 물건은 또 5배입니다. 놓치면 "임대료 올려야겠군!" 하고 떠나고, 10초 동안 일꾼보다도 느리게 걷습니다(엘리베이터 설치 전에는 지금 층 건물주만 해당).
• 먹튀범: 돈더미를 오래 놔두면 위·아래·왼쪽·오른쪽 아무 데서나 나타나 절반을 들고 도망갑니다. 부딪히면 되찾고 현상금을 받습니다. 훔치기 전에 막으면 현상금 2배('철통 방어!').
• 생산기 고장: 아무 층 생산기나 멈출 수 있습니다. 그 앞에 잠깐 서 있으면 고쳐집니다. 2분 넘게 두면 부서져서 쌓인 물건이 사라지고, '다시 제작' 칸에서 돈을 내야 합니다(30초 전부터 경고).

📍 화면 보는 법
• 왼쪽 아래 층 표시: 지금 층과 일이 생긴 층을 급한 순서로 최대 5개(더 있으면 +N). 건물주 > 배달 > 부서지기 직전 > 화나기 직전 손님 > 고장 > ₩MAX > 손님 대기. (황금 물건은 엘리베이터 층 선택판에만 표시)
• 아래쪽: 미션 카드, 그 위에 진행 중인 배달 카드('N층으로 배달', 받을 돈, 남은 시간), 그 위에 알림.
• 판매대가 화면 밖일 때 손님이 기다리면 위쪽에 '▲ 손님 N명 대기'가 뜹니다.

🎯 미션
물건 팔기, 돈 챙기기, 팁 받기, 업그레이드, 황금 물건 팔기 미션이 하나씩 끝없이 이어지고, 깨면 보상을 받습니다.

🎮 설정
• 오른쪽 위 '설정'에서 소리·진동(안드로이드)을 켜고 끄거나 처음부터 다시 시작할 수 있습니다.
• '가게 미리보기'를 누르면 지금 층을 1~6층 가게 모습으로 바꿔 볼 수 있습니다(그림만 바뀜).
• 진행 상황은 이 기기, 이 브라우저에 자동으로 저장됩니다.

그림 파일 없이 HTML 캔버스와 코드만으로 그린 시제품입니다. 쇼츠 광고에서 자주 보이는 '쌓고 파는' 장르를 한국 상가 테마로 직접 만들어 봤습니다.`,
    platform: 'Web (HTML5 Canvas)',
    webUrl: 'https://wowhit.org/games/stack/'
  },
  {
    slug: 'anyway',
    name: 'anyWay',
    category: 'flutter',
    description: '6자리 코드로 빠르고 간편하게 파일 전송',
    longDescription: `복잡한 설정 없이 6자리 코드만으로 파일을 주고받는 전송 앱.\n\n보내는 사람이 파일을 선택하면 6자리 코드와 QR이 생성됩니다. 받는 사람이 코드를 입력하거나 QR을 스캔하면 실시간으로 파일이 전송됩니다.\n\n• 최대 100MB\n• 5분 코드 만료\n• 다운로드(저장) 완료 즉시 서버에서 삭제\n• Web + Android 지원`,
    platform: 'Flutter · Web',
    iconUrl: '/apps/anyway/icon.png',
    webUrl: 'https://anyway.wowhit.org',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/anyway-v1.1.0.2/anyWay.apk',
    version: '1.1.0',
    storeReleased: false
  }
]

export const categoryMeta = {
  flutter: { label: 'Flutter 앱', icon: 'i-lucide-smartphone' },
  web: { label: 'Web 앱', icon: 'i-lucide-globe' },
  other: { label: '기타', icon: 'i-lucide-layers' }
} as const
