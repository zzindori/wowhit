// jjWay 가족 코드: 코드가 맞으면 구글 지도 키를 돌려줌(폰은 메모리에만 둠).
// 코드·키는 Vercel 환경변수 JJWAY_FAMILY_CODE·JJWAY_GMAPS_KEY. 코드를 바꾸면 다음에 켤 때부터 못 받음.
import { createHash, timingSafeEqual } from 'node:crypto'

const hash = (s: string) => createHash('sha256').update(s).digest()

export default defineEventHandler((event) => {
  setHeader(event, 'Cache-Control', 'no-store')
  const want = (process.env.JJWAY_FAMILY_CODE || '').trim()
  const key = (process.env.JJWAY_GMAPS_KEY || '').trim()
  const got = String(getQuery(event).code || '').trim()
  if (!want || !key) throw createError({ statusCode: 503, message: 'not configured' })
  if (!got || !timingSafeEqual(hash(got), hash(want))) throw createError({ statusCode: 403, message: 'bad code' })
  return { key }
})
