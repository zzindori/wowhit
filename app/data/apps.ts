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
  youtubeUrl?: string
  shorts?: string[]
  storeReleased?: boolean
}

export const apps: App[] = [
  // Flutter 앱
  { slug: 'careway', name: 'careWay', category: 'flutter', description: '부모님 복지 혜택 매니저', iconUrl: '/apps/careway/icon.png', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/careway-v1.0.0/careWay.apk' },
  { slug: 'codi-d', name: 'CODI:D', category: 'flutter', description: 'AI 패션 코디네이터', api: ['Gemini', 'Grok'], iconUrl: '/apps/codi-d/icon.png', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codi-d-v1.0.0/CODI_D.apk' },
  { slug: 'farmguide', name: 'farmGuide', category: 'flutter', description: '스마트 농업 경영 앱 (토지/작물 등록~수익정산)', iconUrl: '/apps/farmguide/icon.png', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/farmguide-v1.0.0/farmGuide.apk' },
  { slug: 'gateflow', name: 'gateFlow', category: 'flutter', description: '공항 동선 오케스트레이터 & 출국 스트레스 제거 비서', iconUrl: '/apps/gateflow/icon.png' },
  { slug: 'igomoya', name: 'igoMoya', category: 'flutter', description: '궁금한 것 찍으면 바로 AI 설명 + 타임라인 사진 정리', api: ['Gemini'], iconUrl: '/apps/igomoya/icon.png', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/igomoya-v1.0.0/igoMoya.apk' },
  { slug: 'itne', name: 'itNe', category: 'flutter', description: '냉장고 식재료 관리 + 남은 재료로만 AI 레시피 추천', iconUrl: '/apps/itne/icon.png', webUrl: 'https://itneapp.web.app/', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/itne-v1.0.0/itNe.apk' },
  { slug: 'joa', name: 'JoA', category: 'flutter', description: 'AI 이미지 생성 앱', api: ['Grok (xAI)'], iconUrl: '/apps/joa/icon.png' },
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
  { slug: 'onbidway', name: 'onbidWay', category: 'flutter', description: '온비드(공매) 정보 앱', iconUrl: '/apps/onbidway/icon.png' },
  { slug: 'pingway', name: 'pingWay', category: 'flutter', description: '알림/메시지 앱', api: ['Firebase'], iconUrl: '/apps/pingway/icon.png' },
  {
    slug: 'shotway',
    name: 'shotWay',
    category: 'flutter',
    description: '실시간 카메라 공유 앱',
    longDescription: `누군가 사진을 찍으면, 방에 함께한 모두의 핸드폰에 알림이 옵니다. 바로 그 사진이요.\n\n같은 공간이라면 QR 코드 한 번이면 연결됩니다. 멀리 있다면 6자리 숫자만 알려주면 돼요. 번호 교환도, 친구 추가도, 앱 설치도 필요 없습니다.\n\n아이폰이든 안드로이드든 상관없이 쓸 수 있고, 완전 무료입니다. 광고도 없어요.`,
    api: ['Firebase', 'Supabase'],
    iconUrl: '/apps/shotway/icon.png',
    webUrl: 'https://shotway-5f153.web.app',
    apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/shotway-v1.0.0/shotWay.apk',
    storeReleased: false
  },
  { slug: 'talkway', name: 'talkWay', category: 'flutter', description: '실시간 화자분리 자막 앱 (청각장애인용)', iconUrl: '/apps/talkway/icon.png' },
  { slug: 'txtfit', name: 'txtFit', category: 'flutter', description: '텍스트 분할 · 정제 유틸리티', iconUrl: '/apps/txtfit/icon.png' },
  { slug: 'codeway', name: 'codeWay', category: 'flutter', description: '멀티 QR 스캔으로 대용량 텍스트 수신 · SHA256 무결성 검증', iconUrl: '/apps/codeway/icon.png', webUrl: 'https://zzindori.github.io/codeWay/', apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codeway-v1.0.0/codeWay.apk' },

  // Web 앱
  { slug: 'bbangway', name: 'BBangWay', category: 'web', description: '베이커리 빵 인식 관리자', api: ['Gemini'], iconUrl: '/apps/bbangway/icon.png', webUrl: 'https://zzindori.github.io/BBangWay/' },
  { slug: 'postest', name: 'posTest', category: 'web', description: '베이커리 POS 연습 앱', iconUrl: '/apps/postest/icon.png', webUrl: 'https://zzindori.github.io/posTest/' },

  // 기타
  { slug: 'bbibbiwatch', name: 'BBiBBi', category: 'other', description: '워치 앱', platform: 'Android Watch', api: ['Firebase'] }
]

export const categoryMeta = {
  flutter: { label: 'Flutter 앱', icon: 'i-lucide-smartphone' },
  web: { label: 'Web 앱', icon: 'i-lucide-globe' },
  other: { label: '기타', icon: 'i-lucide-layers' }
} as const
