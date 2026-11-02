// jjWay: 구글 지도 짧은 링크(maps.app.goo.gl 등)를 풀어서 실제 주소(좌표가 든 긴 링크)를 돌려줌.
// 브라우저에선 CORS 때문에 리다이렉트를 따라갈 수 없어서 여기서 대신. 구글 지도 주소만 허용.
const GOOGLE = /^(maps\.app\.goo\.gl|goo\.gl|g\.co|(maps|www)\.google\.[a-z.]+|google\.[a-z.]+)$/
const SHORT = /^(maps\.app\.goo\.gl|goo\.gl|g\.co)$/

export default defineEventHandler(async (event) => {
  let url = String(getQuery(event).url || '').trim()
  for (let i = 0; i < 6; i++) {
    let host: string
    try {
      host = new URL(url).hostname
    } catch {
      throw createError({ statusCode: 400, message: 'bad url' })
    }
    if (!GOOGLE.test(host)) throw createError({ statusCode: 400, message: 'not a google maps link' })
    if (!SHORT.test(host)) break
    const res = await fetch(url, { redirect: 'manual', headers: { 'User-Agent': 'Mozilla/5.0 (jjWay link expander)' } })
    const loc = res.headers.get('location')
    if (!loc) break
    url = new URL(loc, url).toString()
  }
  setHeader(event, 'Cache-Control', 'public, max-age=86400')
  return { url }
})
