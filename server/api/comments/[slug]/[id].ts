const HOME_API = 'https://api.wowhit.org'

export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug')
  const id = getRouterParam(event, 'id')

  if (event.method === 'DELETE') {
    const body = await readBody(event)
    return $fetch(`${HOME_API}/api/comments/${slug}/${id}`, {
      method: 'DELETE',
      body: { password: body.password },
    })
  }

  throw createError({ statusCode: 405, message: 'Method Not Allowed' })
})