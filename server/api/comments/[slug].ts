const HOME_API = 'https://api.wowhit.org'

export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug')
  const method = event.method

  if (method === 'GET') {
    return $fetch(`${HOME_API}/api/comments/${slug}`)
  }

  if (method === 'POST') {
    const body = await readBody(event)
    return $fetch(`${HOME_API}/api/comments/${slug}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ author: body.author, content: body.content }).toString(),
    })
  }

  throw createError({ statusCode: 405, message: 'Method Not Allowed' })
})
