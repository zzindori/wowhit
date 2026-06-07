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
  version?: string
  youtubeUrl?: string
  shorts?: string[]
  storeReleased?: boolean
}

export const apps: App[] = [
  // Flutter 앱
  {
    slug: 'careway',
    name: 'careWay',
    category: 'flutter',
    description: '부모님 복지 혜택 매니저',
    longDescription: `복지 혜택은 찾기 어렵고, 찾아도 신청은 더 복잡합니다.\n\ncareWay는 부모님의 나이, 지역, 상황을 입력하면 받을 수 있는 복지 서비스를 자동으로 찾아줍니다. AI가 전국 공공데이터를 분석해 부모님께 맞는 혜택을 추천하고 분류합니다.\n\n신청 상태도 함께 관리됩니다. 어떤 서비스를 신청했는지, 어떤 게 아직 남아있는지 한눈에 볼 수 있습니다.\n\n부모님 복지, 이제 자녀가 직접 챙겨드릴 수 있습니다.`,
    api: ['Gemini', 'Supabase'],
    iconUrl: '/apps/careway/icon.png',
    webUrl: 'https://careway-jet.vercel.app',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/careway-v1.0.0.1/careWay.apk',
    version: '1.0.0+1'
  },
  {
    slug: 'codi-d',
    name: 'CODI:D',
    category: 'flutter',
    description: 'AI 패션 코디네이터',
    longDescription: `옷은 많은데 뭘 입을지 모르겠다면, CODI:D에게 맡기세요.\n\n카메라로 옷을 찍으면 AI가 분석하고, 어울리는 코디를 직접 이미지로 생성해줍니다. Gemini로 스타일을 분석하고 Grok으로 코디 이미지를 만들어냅니다.\n\nMLKit 기반 체형·얼굴 분석으로 내 몸에 맞는 스타일을 추천합니다. 코디를 쌓아갈수록 나만의 패션 아바타가 진화합니다.\n\n옷장이 스타일리스트가 되는 앱.`,
    api: ['Gemini', 'Grok'],
    iconUrl: '/apps/codi-d/icon.png',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codi-d-v1.0.0.1/CODI_D.apk',
    version: '1.0.0+1'
  },
  {
    slug: 'farmguide',
    name: 'farmGuide',
    category: 'flutter',
    description: '스마트 농업 경영 앱 (토지/작물 등록~수익정산)',
    longDescription: `농사는 기억에만 의존하기엔 너무 복잡합니다.\n\nfarmGuide는 토지 등록부터 작물 선택, 파종·수확 일정 관리, 인력 기록, 수익 정산까지 농업 경영 전 과정을 하나의 앱에서 관리합니다.\n\n네이버 지도 기반으로 농지를 직접 선택하고 관리할 수 있습니다. 수확이 끝나면 차트로 수익과 비용을 한눈에 확인할 수 있습니다.\n\n농부를 위한 스마트 경영 도우미.`,
    api: ['Supabase', 'Naver Maps'],
    iconUrl: '/apps/farmguide/icon.png',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/farmguide-v1.0.0.1/farmGuide.apk',
    version: '1.0.0+1'
  },
  {
    slug: 'gateflow',
    name: 'gateFlow',
    category: 'flutter',
    description: '공항 동선 오케스트레이터 & 출국 스트레스 제거 비서',
    longDescription: `공항에서 헤매거나, 뭔가를 빠뜨린 채 출국한 경험 있으신가요?\n\ngateFlow는 출국 전 준비 체크리스트, 공항 터미널 동선 안내, 여권 보안 저장소까지 출국의 모든 과정을 함께합니다.\n\n여권을 카메라로 찍으면 OCR이 자동으로 정보를 읽어냅니다. 저장된 여권 정보는 생체인증으로만 접근할 수 있어 안전합니다.\n\n출발 타이머와 AI 여행 조언으로 첫 해외여행도 자신 있게.`,
    api: ['Gemini', 'MLKit OCR'],
    iconUrl: '/apps/gateflow/icon.png'
  },
  {
    slug: 'igomoya',
    name: 'igoMoya',
    category: 'flutter',
    description: '궁금한 것 찍으면 바로 AI 설명 + 타임라인 사진 정리',
    longDescription: `길을 걷다, 음식을 보다, 궁금한 게 생기는 순간.\n\nigoMoya는 카메라를 대면 AI가 바로 설명해줍니다. 분할 화면으로 찍는 순간 결과를 바로 확인할 수 있습니다.\n\n찍은 사진들은 위치와 시간순으로 타임라인에 정리됩니다. 오늘 어디서 무엇을 봤는지 기억하고 싶을 때 꺼내보세요.\n\n궁금함을 바로 해결하는 AI 카메라 메모.`,
    api: ['Gemini'],
    iconUrl: '/apps/igomoya/icon.png',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/igomoya-v0.1.0.1/igoMoya.apk',
    version: '0.1.0+1'
  },
  {
    slug: 'itne',
    name: 'itNe',
    category: 'flutter',
    description: '냉장고 식재료 관리 + 남은 재료로만 AI 레시피 추천',
    longDescription: `냉장고 문을 열고 "이걸로 뭘 만들지?" 고민한 적 있으신가요?\n\nitNe는 냉장고 속 식재료를 사진으로 찍으면 자동으로 인식하고 목록을 만들어줍니다. 그리고 남은 재료로만 만들 수 있는 레시피를 AI가 추천해줍니다.\n\n없는 재료를 사러 나가지 않아도 됩니다. 있는 것만으로 충분합니다.\n\n냉장고를 요리사로 만드는 앱.`,
    api: ['Gemini', 'MLKit'],
    iconUrl: '/apps/itne/icon.png',
    webUrl: 'https://itneapp.web.app/',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/itne-v1.0.0.1/itNe.apk',
    version: '1.0.0+1'
  },
  {
    slug: 'joa',
    name: 'JoA',
    category: 'flutter',
    description: 'AI 이미지 생성 앱',
    longDescription: `복잡한 설정 없이, 버튼 몇 번으로 만드는 자연스러운 한국인 옷핏 레퍼런스.\n\nJoA는 Google Gemini 이미지 생성 모델을 활용합니다. 카테고리(남/여/풍경), 연령, 체형, 스타일, 날씨 무드를 선택하면 9:16 세로 이미지가 바로 생성됩니다. 현재 날씨를 반영한 이미지 생성도 가능하며, 생성된 이미지는 히스토리로 저장됩니다.\n\n앱 설치 없이 Android, iPhone, PC 브라우저 어디서든 동일하게 사용할 수 있습니다.\n\n가입이나 로그인 없이 5장을 무료로 먼저 체험해볼 수 있습니다.\n\n이용권을 구매하면 하루 30장 생성 권한이 매일 자정에 자동 충전됩니다. 30일 기준 최대 900장이며, 미사용 분은 다음 날로 이월되지 않습니다. 인증 코드는 스마트폰, PC 등 여러 기기에서 동시에 사용할 수 있지만, 하루 30장 카운트는 기기 구분 없이 공유됩니다.\n\nGemini API Key를 직접 발급받아 앱 설정에 입력하는 방법으로도 이용할 수 있습니다. 이 경우 이용권 구매 없이 사용할 수 있지만, Google API 사용량에 따라 구글에 직접 요금이 부과됩니다. API Key는 이 사이트의 QR 변환 메뉴를 활용하면 스캔으로 간편하게 입력할 수 있습니다.\n\nAndroid 설치는 위 직접 설치 버튼으로 APK를 다운로드한 후 파일을 열어 설치합니다. 처음 설치 시 알 수 없는 앱 설치 허용 설정이 필요할 수 있습니다. 삭제는 아이콘을 길게 누르거나 설정 앱에서 제거할 수 있습니다.`,
    api: ['Gemini'],
    iconUrl: '/apps/joa/icon.png',
    screenshots: [
      '/apps/joa/Screenshot_20260607_165645.jpg',
      '/apps/joa/Screenshot_20260607_165650.jpg',
      '/apps/joa/Screenshot_20260607_165702.jpg',
      '/apps/joa/Screenshot_20260607_165859.jpg',
      '/apps/joa/Screenshot_20260607_170008.jpg'
    ],
    webUrl: 'https://web-tau-nine-22.vercel.app',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/joa-v1.0.0.3/JoA.apk',
    purchaseUrl: 'https://smartstore.naver.com/wowhit/products/13625209650',
    version: '1.0.0+3'
  },
  {
    slug: 'menuway',
    name: 'menuWay',
    category: 'flutter',
    description: '해외 메뉴판을 찍으면 음식을 이해할 수 있게 설명해주는 AI 여행 앱',
    longDescription: `여행 가면 누구나 한 번쯤 겪는 순간.\n번역은 되지만, 어떤 음식인지 이해하기 어려울 때가 있습니다.\n\nmenuWay는 메뉴판을 촬영하면 메뉴 이름과 설명을 함께 제공합니다.\n\n단순 번역이 아니라,\n음식을 이해할 수 있도록 돕는 앱입니다.\n\n이제 주문 앞에서 멈추지 마세요.\n\nTranslate. Order. Enjoy.`,
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
    youtubeUrl: 'https://www.youtube.com/@zzindori/shorts',
    shorts: ['D_w3q4XwCa4', 'gTf98JexFGo', 'ss76szvONxo', '0DK2QBaTMac']
  },
  {
    slug: 'onbidway',
    name: 'onbidWay',
    category: 'flutter',
    description: '온비드(공매) 정보 앱',
    longDescription: `공매 물건을 찾으러 매번 온비드 사이트에 들어가야 한다면 번거롭습니다.\n\nonbidWay는 공공데이터 API를 기반으로 부동산, 동산, 차량 공매 정보를 한곳에서 조회합니다. 실시간 데이터로 최신 공매 현황을 확인할 수 있습니다.\n\n관심 있는 물건은 찜해두고, 같은 물건의 여러 회차를 한눈에 비교할 수 있습니다.\n\n공매 정보를 손 안에서.`,
    api: ['공공데이터포털'],
    iconUrl: '/apps/onbidway/icon.png',
    webUrl: 'https://onbidway-web.vercel.app'
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
    slug: 'shotway',
    name: 'shotWay',
    category: 'flutter',
    description: '실시간 찍은 사진 공유 앱',
    longDescription: `누군가 사진을 찍으면, 방에 함께한 모두의 핸드폰에 알림이 옵니다. 바로 그 사진이요.\n\n같은 공간이라면 QR 코드 한 번이면 연결됩니다. 멀리 있다면 6자리 숫자만 알려주면 돼요. 번호 교환도, 친구 추가도, 앱 설치도 필요 없습니다.\n\n아이폰이든 안드로이드든 상관없이 쓸 수 있고, 완전 무료입니다. 광고도 없어요.`,
    api: ['Firebase', 'Supabase'],
    iconUrl: '/apps/shotway/icon.png',
    webUrl: 'https://shotway-5f153.web.app',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/shotway-v1.0.0/shotWay.apk',
    version: '1.0.0+3',
    storeReleased: false
  },
  {
    slug: 'talkway',
    name: 'talkWay',
    category: 'flutter',
    description: '실시간 화자분리 자막 앱 (청각장애인용)',
    longDescription: `소리가 잘 들리지 않는 환경에서도 대화를 이어갈 수 있어야 합니다.\n\ntalkWay는 실시간으로 주변 소리를 인식해 자막으로 변환합니다. Google STT와 Naver CLOVA 두 엔진을 지원해 인식 정확도를 높였습니다.\n\n화자 분리 기능으로 누가 말하는지도 구분할 수 있습니다. 회의, 강의, 일상 대화 어디서든 자막이 따라옵니다.\n\n청각 장애인과 소음이 심한 환경을 위한 실시간 자막 앱.`,
    api: ['Google STT', 'Naver CLOVA'],
    iconUrl: '/apps/talkway/icon.png'
  },
  {
    slug: 'txtfit',
    name: 'txtFit',
    category: 'flutter',
    description: '텍스트 분할 · 정제 유틸리티',
    longDescription: `긴 텍스트를 AI 채팅에 붙여넣으면 글자 수 제한에 막힐 때가 있습니다.\n\ntxtFit은 두 가지 기능을 제공합니다. 긴 텍스트를 원하는 글자 수 단위로 나눠 [1/3], [2/3] 형식으로 순서대로 복사할 수 있는 분할 기능, 그리고 나눠진 블럭들을 다시 깔끔하게 이어붙이는 결합 기능입니다.\n\n분할 헤더가 자동으로 붙고, 반대로 제거하는 것도 가능합니다.\n\n글자 수 제한을 넘어, 내 텍스트를 내 마음대로.`,
    iconUrl: '/apps/txtfit/icon.png',
    webUrl: 'https://zzindori.github.io/TxtFit-web/',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/txtfit-v1.0.0/txtFit.apk',
    version: '1.0.0'
  },
  {
    slug: 'codeway',
    name: 'codeWay',
    category: 'flutter',
    description: '멀티 QR 스캔으로 대용량 텍스트 수신 · SHA256 무결성 검증',
    longDescription: `파일 전송 없이 텍스트를 전달하고 싶을 때.\n\ncodeWay는 대용량 텍스트를 QR 코드 여러 장으로 분할해 전송하고, 수신 측에서 순서대로 스캔해 원문을 복원합니다. SHA256 해시 검증으로 데이터 무결성을 보장합니다.\n\n앱 설치 없이 웹 버전으로도 동작합니다. 인터넷 연결이 없는 환경에서도 안전하게 텍스트를 전달할 수 있습니다.\n\n보안이 필요한 텍스트 전달에 적합한 멀티 QR 유틸리티.`,
    iconUrl: '/apps/codeway/icon.png',
    webUrl: 'https://zzindori.github.io/codeWay/',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codeway-v1.0.0/codeWay.apk',
    version: '1.0.0'
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
    webUrl: 'https://zzindori.github.io/BBangWay/'
  },
  {
    slug: 'postest',
    name: 'posTest',
    category: 'web',
    description: '베이커리 POS 연습 앱',
    longDescription: `베이커리 POS 기기 사용이 처음이라면 실수가 걱정됩니다.\n\nposTest는 실제 POS 화면과 동일한 환경에서 연습할 수 있는 시뮬레이터입니다. 상품을 선택하고 결제하는 기본 흐름을 반복 연습할 수 있습니다.\n\n퀴즈 모드에서는 상품명을 맞추는 타이머 도전이 가능합니다. 점수가 쌓이면 랭킹에 기록됩니다.\n\n출근 전 5분, POS 완벽 적응.`,
    iconUrl: '/apps/postest/icon.png',
    webUrl: 'https://zzindori.github.io/posTest/'
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
  }
]

export const categoryMeta = {
  flutter: { label: 'Flutter 앱', icon: 'i-lucide-smartphone' },
  web: { label: 'Web 앱', icon: 'i-lucide-globe' },
  other: { label: '기타', icon: 'i-lucide-layers' }
} as const
