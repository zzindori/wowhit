import {
  collection,
  query,
  where,
  orderBy,
  getDocs,
  addDoc,
  serverTimestamp,
  type Firestore
} from 'firebase/firestore'

export interface Comment {
  id: string
  author: string
  content: string
  createdAt: Date
}

export function useComments(appSlug: string) {
  const { $db } = useNuxtApp() as { $db: Firestore }
  const comments = ref<Comment[]>([])
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref<string | null>(null)

  async function fetchComments() {
    loading.value = true
    try {
      const q = query(
        collection($db, 'wowhit_comments'),
        where('appSlug', '==', appSlug),
        orderBy('createdAt', 'desc')
      )
      const snap = await getDocs(q)
      comments.value = snap.docs.map(doc => ({
        id: doc.id,
        author: doc.data().author as string,
        content: doc.data().content as string,
        createdAt: doc.data().createdAt?.toDate?.() ?? new Date()
      }))
    } catch (e) {
      error.value = '댓글을 불러오지 못했습니다.'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function addComment(author: string, content: string): Promise<boolean> {
    if (!author.trim() || !content.trim()) return false
    submitting.value = true
    try {
      await addDoc(collection($db, 'wowhit_comments'), {
        appSlug,
        author: author.trim().slice(0, 20),
        content: content.trim().slice(0, 300),
        createdAt: serverTimestamp()
      })
      await fetchComments()
      return true
    } catch (e) {
      error.value = '댓글 등록에 실패했습니다.'
      console.error(e)
      return false
    } finally {
      submitting.value = false
    }
  }

  function formatDate(date: Date): string {
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
