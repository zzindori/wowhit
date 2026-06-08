export interface Reply {
  id: number
  author: string
  content: string
  created_at: string
  parent_id: number
}

export interface Comment {
  id: number
  author: string
  content: string
  created_at: string
  parent_id: null
  replies: Reply[]
}

export function useComments(appSlug: string) {
  const comments = ref<Comment[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref<string | null>(null)

  async function fetchComments() {
    loading.value = true
    error.value = null
    try {
      const data = await $fetch<Comment[]>(`/api/comments/${appSlug}`)
      comments.value = data
    }
    catch (e) {
      error.value = '댓글을 불러오지 못했습니다.'
      console.error(e)
    }
    finally {
      loading.value = false
    }
  }

  async function addComment(author: string, content: string, parentId?: number): Promise<boolean> {
    if (!author.trim() || !content.trim()) return false
    submitting.value = true
    error.value = null
    try {
      await $fetch(`/api/comments/${appSlug}`, {
        method: 'POST',
        body: { author: author.trim(), content: content.trim(), parent_id: parentId },
      })
      await fetchComments()
      return true
    }
    catch (e) {
      error.value = '댓글 등록에 실패했습니다.'
      console.error(e)
      return false
    }
    finally {
      submitting.value = false
    }
  }

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr)
    const now = new Date()
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000)
    if (diff < 60) return '방금 전'
    if (diff < 3600) return `${Math.floor(diff / 60)}분 전`
    if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`
    if (diff < 2592000) return `${Math.floor(diff / 86400)}일 전`
    return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
  }

  onMounted(fetchComments)

  return { comments, loading, submitting, error, addComment, formatDate }
}
