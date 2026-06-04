export interface App {
  slug: string
  name: string
  category: 'flutter' | 'web' | 'other'
  description: string
  longDescription?: string
  api?: string[]
  platform?: string
  androidUrl?: string
  iosUrl?: string
  webUrl?: string
  apkUrl?: string
  storeReleased?: boolean
}

export const apps: App[] = [
  // Flutter 앱
  { slug: 'careway', name: 'careWay', category: 'flutter', description: '부모님 복지 혜택 매니저' },
  { slug: 'codi-d', name: 'CODI:D', category: 'flutter', description: 'AI 패션 코디네이터', api: ['Gemini', 'Grok'], apkUrl: 'https://github.com/zzindori/wowhit-releases/releases/download/codi-d-v1.0.0/CODI_D.apk' },
  { slug: 'farmguide', name: 'farmGuide', category: 'flutter', description: '스마트 농업 경영 앱 (토지/작물 등록~수익정산)' },
  { slug: 'gateflow', name: 'gateFlow', category: 'flutter', description: '공항 동선 오케스트레이터 & 출국 스트레스 제거 비서' },
  { slug: 'igomoya', name: 'igoMoya', category: 'flutter', description: '궁금한 것 찍으면 바로 AI 설명 + 타임라인 사진 정리', api: ['Gemini'] },
  { slug: 'itne', name: 'itNe', category: 'flutter', description: '스플릿 스크린 카메라 앱' },
  { slug: 'joa', name: 'JoA', category: 'flutter', description: 'AI 이미지 생성 앱', api: ['Grok (xAI)'] },
  { slug: 'menuway', name: 'menuway', category: 'flutter', description: '메뉴 관리 MVP', storeReleased: true, androidUrl: 'https://play.google.com/store/apps/details?id=com.menuway.app&hl=ko', iosUrl: 'https://apps.apple.com/kr/app/menuway/id6758591797' },
  { slug: 'onbidway', name: 'onbidWay', category: 'flutter', description: '온비드(공매) 정보 앱' },
  { slug: 'pingway', name: 'pingWay', category: 'flutter', description: '알림/메시지 앱', api: ['Firebase'] },
  {
    slug: 'shotway',
    name: 'shotWay',
    category: 'flutter',
    description: '실시간 카메라 공유 앱',
    longDescription: `누군가 사진을 찍으면, 방에 함께한 모두의 핸드폰에 알림이 옵니다. 바로 그 사진이요.\n\n같은 공간이라면 QR 코드 한 번이면 연결됩니다. 멀리 있다면 6자리 숫자만 알려주면 돼요. 번호 교환도, 친구 추가도, 앱 설치도 필요 없습니다.\n\n아이폰이든 안드로이드든 상관없이 쓸 수 있고, 완전 무료입니다. 광고도 없어요.`,
    api: ['Firebase', 'Supabase'],
    webUrl: 'https://shotway-5f153.web.app',
    storeReleased: false
  },
  { slug: 'talkway', name: 'talkWay', category: 'flutter', description: '실시간 화자분리 자막 앱 (청각장애인용)' },
  { slug: 'qr-scanner', name: 'qr_scanner', category: 'flutter', description: 'QR 스캐너' },

  // Web 앱
  { slug: 'bbangway', name: 'BBangWay', category: 'web', description: '베이커리 빵 인식 관리자', api: ['Gemini'], webUrl: 'https://zzindori.github.io/BBangWay/' },
  { slug: 'postest', name: 'posTest', category: 'web', description: '베이커리 POS 연습 앱', webUrl: 'https://zzindori.github.io/posTest/' },

  // 기타
  { slug: 'bbibbiwatch', name: 'BBiBBi', category: 'other', description: '워치 앱', platform: 'Android Watch', api: ['Firebase'] }
]

export const categoryMeta = {
  flutter: { label: 'Flutter 앱', icon: 'i-lucide-smartphone' },
  web: { label: 'Web 앱', icon: 'i-lucide-globe' },
  other: { label: '기타', icon: 'i-lucide-layers' }
} as const
