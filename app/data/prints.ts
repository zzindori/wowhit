export interface Print {
  slug: string
  name: string
  description: string
  makerWorldUrl: string
  imageUrl?: string
}

export const makerWorldProfile = 'https://makerworld.com/ko/@jinsukYoon'

export const prints: Print[] = [
  {
    slug: 'yamaha-xv1600-roadstar',
    name: 'Yamaha XV1600 Roadstar',
    description: '야마하 로드스타 미니어처 모델',
    makerWorldUrl: 'https://makerworld.com/ko/models/1219647-yamaha_xv1600_roadstar',
    imageUrl: '/prints/yamaha-xv1600-roadstar.jpg',
  },
  {
    slug: 'honda-z50j',
    name: 'Honda Z50J',
    description: '혼다 Z50J 미니 바이크',
    makerWorldUrl: 'https://makerworld.com/ko/models/1188380-honda-z50j-motorcycle',
    imageUrl: '/prints/honda-z50j.jpg',
  },
  {
    slug: 'kymco-ak550',
    name: 'Kymco AK550',
    description: '킴코 AK550 고디테일 미니 모델',
    makerWorldUrl: 'https://makerworld.com/ko/models/1397085-kymco-ak550-high-detail-3d-printed-mini-model',
    imageUrl: '/prints/kymco-ak550.jpg',
  },
  {
    slug: 'honda-z50j-inspired',
    name: 'Honda Z50J Inspired',
    description: '혼다 Z50J 스타일 3D 프린팅 미니 모델',
    makerWorldUrl: 'https://makerworld.com/ko/models/1392638-honda-z50j-inspired-3d-printable-mini-model',
    imageUrl: '/prints/honda-z50j-inspired.jpg',
  },
  {
    slug: 'honda-cub-c100',
    name: 'Honda Cub C100',
    description: '혼다 슈퍼커브 C100 미니어처',
    makerWorldUrl: 'https://makerworld.com/ko/models/1188323-honda-cub-c100-motorcycle',
    imageUrl: '/prints/honda-cub-c100.jpg',
  },
]