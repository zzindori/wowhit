const HOME_API = 'https://api.wowhit.org'

export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug')
  const method = event.method

  if (method === 'GET') {
    return $fetch(`${HOME_API}/api/comments/${slug}`)
  }

  if (method === 'POST') {
    const body = await readBody(event)
    const params: Record<string, string> = {
      author: body.author,
      content: body.content
    }
    if (body.parent_id) params.parent_id = String(body.parent_id)
    return $fetch(`${HOME_API}/api/comments/${slug}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(params).toString()
    })
  }

  throw createError({ statusCode: 405, message: 'Method Not Allowed' })
})
