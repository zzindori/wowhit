export type PrintCategory = 'motorcycle' | 'diorama' | 'figurine' | 'accessory'

export interface Print {
  slug: string
  name: string
  description: string
  category: PrintCategory
  imageUrl: string
  images?: string[]
  makerWorldUrl?: string
}

export const makerWorldProfile = 'https://makerworld.com/ko/@jinsukYoon'

export const printCategoryMeta = {
  motorcycle: { label: '바이크 미니어처', icon: 'i-lucide-bike' },
  diorama: { label: '디오라마', icon: 'i-lucide-store' },
  figurine: { label: '프라모델 · 피규어', icon: 'i-lucide-bot' },
  accessory: { label: '키링 · 소품', icon: 'i-lucide-key' },
} as const

export const printCategories = ['motorcycle', 'diorama', 'figurine', 'accessory'] as const

export const prints: Print[] = [
  // 바이크 미니어처
  {
    slug: 'yamaha-xv1600-roadstar',
    name: 'Yamaha XV1600 Roadstar',
    description: '야마하 로드스타 미니어처',
    category: 'motorcycle',
    imageUrl: '/prints/yamaha-xv1600-roadstar.jpg',
    makerWorldUrl: 'https://makerworld.com/ko/models/1219647-yamaha_xv1600_roadstar',
  },
  {
    slug: 'honda-z50j',
    name: 'Honda Z50J',
    description: '혼다 Z50J 미니 바이크',
    category: 'motorcycle',
    imageUrl: '/prints/honda-z50j.jpg',
    makerWorldUrl: 'https://makerworld.com/ko/models/1188380-honda-z50j-motorcycle',
  },
  {
    slug: 'kymco-ak550',
    name: 'Kymco AK550',
    description: '킴코 AK550 고디테일 미니 모델',
    category: 'motorcycle',
    imageUrl: '/prints/kymco-ak550.jpg',
    makerWorldUrl: 'https://makerworld.com/ko/models/1397085-kymco-ak550-high-detail-3d-printed-mini-model',
  },
  {
    slug: 'honda-z50j-inspired',
    name: 'Honda Z50J Inspired',
    description: '혼다 Z50J 스타일 미니 모델',
    category: 'motorcycle',
    imageUrl: '/prints/honda-z50j-inspired.jpg',
    makerWorldUrl: 'https://makerworld.com/ko/models/1392638-honda-z50j-inspired-3d-printable-mini-model',
  },
  {
    slug: 'honda-cub-c100',
    name: 'Honda Cub C100',
    description: '혼다 슈퍼커브 C100 미니어처',
    category: 'motorcycle',
    imageUrl: '/prints/honda-cub-c100.jpg',
    makerWorldUrl: 'https://makerworld.com/ko/models/1188323-honda-cub-c100-motorcycle',
  },

  // 디오라마
  {
    slug: 'coffee-takeout-truck',
    name: 'Coffee Take Out Truck',
    description: '테이크아웃 커피 트럭 디오라마 · 에스프레소 바',
    category: 'diorama',
    imageUrl: '/prints/coffee-truck-diorama.jpg',
    images: ['/prints/coffee-truck-scene.jpg', '/prints/coffee-truck-interior.jpg'],
  },

  // 프라모델 · 피규어
  {
    slug: 'mecha-figure',
    name: 'Mecha Figure',
    description: '3D 프린트 메카 로봇 (미도색)',
    category: 'figurine',
    imageUrl: '/prints/mecha-figure.jpg',
  },
  {
    slug: 'f1-helmet-collection',
    name: 'F1 Helmet Collection',
    description: 'F1 레이싱 헬멧 미니어처 · 레드불 바이크',
    category: 'figurine',
    imageUrl: '/prints/f1-helmet-bike.jpg',
  },
  {
    slug: 'doosan-bears-figures',
    name: 'Doosan Bears Figures',
    description: '두산 베어스 유니폼 곰 마스코트 피규어',
    category: 'figurine',
    imageUrl: '/prints/doosan-bears-figures.jpg',
  },
  {
    slug: 'character-figures',
    name: 'Character Figures',
    description: '베노머 로봇 · 두산 베어스 마스코트',
    category: 'figurine',
    imageUrl: '/prints/character-figures.jpg',
  },

  // 키링 · 소품
  {
    slug: 'doosan-bears-keychain',
    name: 'Doosan Bears Keychain',
    description: '두산 베어스 2015 로고 키링',
    category: 'accessory',
    imageUrl: '/prints/doosan-bears-keychain.jpg',
  },
  {
    slug: 'doosan-bears-script-keychain',
    name: 'Doosan Bears Script Keychain',
    description: '두산 베어스 스크립트 로고 키링',
    category: 'accessory',
    imageUrl: '/prints/doosan-bears-script-keychain.jpg',
  },
  {
    slug: 'hellokitty-doosan-bears-keychain',
    name: 'Hello Kitty × Doosan Bears',
    description: '헬로키티 두산 베어스 키링',
    category: 'accessory',
    imageUrl: '/prints/hellokitty-doosan-bears-keychain.jpg',
  },
  {
    slug: 'doosan-bears-token',
    name: 'Doosan Bears Token',
    description: '두산 베어스 로고 3D 프린트 토큰',
    category: 'accessory',
    imageUrl: '/prints/doosan-bears-token.jpg',
  },
  {
    slug: 'mini-baseball-cap',
    name: 'Mini Baseball Cap',
    description: '미니 야구 모자 (두산 D 로고)',
    category: 'accessory',
    imageUrl: '/prints/mini-baseball-cap.jpg',
  },
]

export const featuredPrintSlugs = [
  'yamaha-xv1600-roadstar',
  'coffee-takeout-truck',
  'f1-helmet-collection',
  'doosan-bears-keychain',
  'honda-cub-c100',
]

export function getPrintsByCategory(category: PrintCategory) {
  return prints.filter(p => p.category === category)
}

export function getFeaturedPrints() {
  return featuredPrintSlugs
    .map(slug => prints.find(p => p.slug === slug))
    .filter((p): p is Print => !!p)
}