<script setup lang="ts">
import { apps, categoryMeta } from '~/data/apps'

const route = useRoute()
const app = apps.find(a => a.slug === route.params.slug)

if (!app) {
  throw createError({ statusCode: 404, message: '앱을 찾을 수 없습니다.' })
}

const meta = categoryMeta[app.category]

const links = computed(() => {
  const result = []
  if (app.androidUrl) {
    result.push({ label: 'Google Play', icon: 'i-simple-icons-googleplay', to: app.androidUrl, target: '_blank', color: 'primary' as const })
  }
  if (app.iosUrl) {
    result.push({ label: 'App Store', icon: 'i-simple-icons-appstore', to: app.iosUrl, target: '_blank', color: 'primary' as const })
  }
  if (app.webUrl) {
    result.push({ label: '웹앱 열기', icon: 'i-lucide-globe', to: app.webUrl, target: '_blank', color: 'primary' as const })
  }
  if (app.apkUrl) {
    result.push({ label: 'Android 직접 설치', icon: 'i-simple-icons-android', to: app.apkUrl, color: 'neutral' as const, variant: 'outline' as const })
  }
  if (app.purchaseUrl) {
    result.push({ label: '이용권 구매', icon: 'i-lucide-shopping-cart', to: app.purchaseUrl, target: '_blank', color: 'warning' as const })
  }
  return result
})

const selectedShort = ref<string | null>(null)
const shortModalOpen = ref(false)
function openShort(id: string) {
  selectedShort.value = id
  shortModalOpen.value = true
}

const { comments, loading: commentsLoading, submitting, error: commentError, addComment, formatDate } = useComments(app.slug)
const newAuthor = ref('')
const newContent = ref('')
const replyingTo = ref<{ id: number, author: string } | null>(null)
const replyContent = ref('')

async function handleSubmit() {
  const ok = await addComment(newAuthor.value, newContent.value)
  if (ok) newContent.value = ''
}

function openReply(comment: { id: number, author: string }) {
  replyingTo.value = comment
  replyContent.value = `@${comment.author} `
}

function closeReply() {
  replyingTo.value = null
  replyContent.value = ''
}

async function handleReply() {
  if (!replyingTo.value) return
  const ok = await addComment(newAuthor.value, replyContent.value, replyingTo.value.id)
  if (ok) closeReply()
}

useSeoMeta({ title: `${app.name} — wowhit` })
</script>

<template>
  <div>
    <UPageSection>
      <div class="max-w-2xl mx-auto">
        <NuxtLink
          to="/"
          class="inline-flex items-center gap-1 text-sm text-muted hover:text-default mb-8"
        >
          <UIcon
            name="i-lucide-arrow-left"
            class="size-4"
          />
          목록으로
        </NuxtLink>

        <div class="flex items-center gap-3 mb-2">
          <img
            v-if="app.iconUrl"
            :src="app.iconUrl"
            :alt="app.name"
            class="size-14 rounded-2xl object-cover shrink-0"
          >
          <UIcon
            v-else
            :name="meta.icon"
            class="text-primary size-8"
          />
          <h1 class="text-3xl font-bold">
            {{ app.name }}
          </h1>
        </div>

        <div class="flex flex-wrap gap-2 mb-6">
          <UBadge
            :label="meta.label"
            variant="subtle"
          />
          <UBadge
            v-if="app.version"
            :label="`v${app.version}`"
            variant="outline"
            color="neutral"
          />
          <UBadge
            v-if="app.platform"
            :label="app.platform"
            variant="outline"
          />
          <UBadge
            v-if="app.storeReleased"
            label="스토어 출시"
            color="success"
            variant="subtle"
          />
          <UBadge
            v-for="a in app.api"
            :key="a"
            :label="a"
            variant="outline"
            color="neutral"
          />
        </div>

        <!-- 스크린샷 갤러리 -->
        <div
          v-if="app.screenshots?.length"
          class="mb-8 overflow-hidden"
        >
          <div class="flex gap-3 overflow-x-auto pb-2 snap-x snap-mandatory">
            <img
              v-for="(src, i) in app.screenshots"
              :key="i"
              :src="src"
              :alt="`${app.name} 스크린샷 ${i + 1}`"
              class="h-64 sm:h-80 w-auto rounded-2xl object-cover shadow-md shrink-0 snap-start"
            >
          </div>
        </div>

        <div class="mb-8">
          <template v-if="app.longDescription">
            <p
              v-for="(line, i) in app.longDescription.split('\n\n')"
              :key="i"
              class="text-base text-muted mb-3 last:mb-0"
            >
              {{ line }}
            </p>
          </template>
          <p
            v-else
            class="text-lg text-muted"
          >
            {{ app.description }}
          </p>
        </div>

        <div
          v-if="links.length"
          class="flex flex-wrap gap-3 mb-10"
        >
          <UButton
            v-for="link in links"
            :key="link.label"
            v-bind="link"
          />
        </div>

        <div
          v-else
          class="mb-10"
        >
          <UAlert
            icon="i-lucide-clock"
            title="출시 준비 중"
            description="스토어 출시 또는 웹앱 전환이 예정되어 있습니다."
            color="neutral"
            variant="subtle"
          />
        </div>

        <!-- 쇼츠 갤러리 -->
        <div
          v-if="app.shorts?.length"
          class="mb-10"
        >
          <h2 class="text-lg font-semibold mb-3">
            YouTube 쇼츠
          </h2>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <button
              v-for="id in app.shorts"
              :key="id"
              class="relative rounded-xl overflow-hidden aspect-[9/16] cursor-pointer group"
              @click="openShort(id)"
            >
              <img
                :src="`https://img.youtube.com/vi/${id}/hqdefault.jpg`"
                :alt="`쇼츠 ${id}`"
                class="w-full h-full object-cover"
              >
              <div class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <UIcon
                  name="i-lucide-play-circle"
                  class="size-12 text-white"
                />
              </div>
            </button>
          </div>
        </div>

        <!-- 댓글 -->
        <div class="mt-12 pt-8 border-t border-default">
          <h2 class="text-base font-semibold text-muted mb-6 uppercase tracking-wider">
            댓글
          </h2>

          <!-- 댓글 목록 -->
          <div
            v-if="commentsLoading"
            class="flex justify-center py-10"
          >
            <UIcon
              name="i-lucide-loader-circle"
              class="size-5 animate-spin text-muted"
            />
          </div>
          <div
            v-else-if="comments.length === 0"
            class="text-sm text-muted py-6"
          >
            아직 댓글이 없어요.
          </div>
          <div
            v-else
            class="space-y-5 mb-8"
          >
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="flex flex-col gap-1"
            >
              <!-- 댓글 본문 -->
              <div class="flex items-baseline gap-2">
                <span class="text-sm font-medium">{{ comment.author }}</span>
                <span class="text-xs text-muted">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="text-sm text-muted whitespace-pre-wrap leading-relaxed">
                {{ comment.content }}
              </p>
              <button
                class="text-xs text-muted hover:text-default w-fit"
                @click="openReply(comment)"
              >
                답글
              </button>

              <!-- 대댓글 목록 -->
              <div
                v-if="comment.replies.length > 0"
                class="mt-2 ml-4 pl-3 border-l-2 border-default space-y-3"
              >
                <div
                  v-for="reply in comment.replies"
                  :key="reply.id"
                  class="flex flex-col gap-1"
                >
                  <div class="flex items-baseline gap-2">
                    <span class="text-sm font-medium">{{ reply.author }}</span>
                    <span class="text-xs text-muted">{{ formatDate(reply.created_at) }}</span>
                  </div>
                  <p class="text-sm text-muted whitespace-pre-wrap leading-relaxed">
                    <span
                      v-if="reply.content.startsWith('@')"
                      class="text-primary font-medium"
                    >{{ reply.content.split(' ')[0] }} </span>{{ reply.content.startsWith('@') ? reply.content.slice(reply.content.indexOf(' ') + 1) : reply.content }}
                  </p>
                </div>
              </div>

              <!-- 답글 입력 폼 -->
              <div
                v-if="replyingTo?.id === comment.id"
                class="mt-2 ml-4 pl-3 border-l-2 border-primary"
              >
                <div class="flex gap-2">
                  <UInput
                    v-model="newAuthor"
                    placeholder="닉네임"
                    maxlength="20"
                    class="w-24 shrink-0"
                    size="sm"
                  />
                  <UInput
                    v-model="replyContent"
                    placeholder="답글을 입력하세요"
                    maxlength="300"
                    class="flex-1"
                    size="sm"
                    @keydown.enter.prevent="handleReply"
                  />
                  <UButton
                    icon="i-lucide-send"
                    size="sm"
                    :loading="submitting"
                    :disabled="!newAuthor.trim() || !replyContent.trim()"
                    variant="subtle"
                    @click="handleReply"
                  />
                  <UButton
                    icon="i-lucide-x"
                    size="sm"
                    variant="ghost"
                    color="neutral"
                    @click="closeReply"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 댓글 작성 폼 -->
          <div class="space-y-3 pt-6 border-t border-default">
            <div class="flex gap-2">
              <UInput
                v-model="newAuthor"
                placeholder="닉네임"
                maxlength="20"
                class="w-32 shrink-0"
              />
              <UInput
                v-model="newContent"
                placeholder="댓글을 남겨주세요"
                maxlength="300"
                class="flex-1"
                @keydown.enter.prevent="handleSubmit"
              />
              <UButton
                icon="i-lucide-send"
                :loading="submitting"
                :disabled="!newAuthor.trim() || !newContent.trim()"
                variant="subtle"
                @click="handleSubmit"
              />
            </div>
            <p
              v-if="commentError"
              class="text-xs text-red-500"
            >
              {{ commentError }}
            </p>
          </div>
        </div>
      </div>
    </UPageSection>

    <!-- 쇼츠 모달 -->
    <UModal
      v-model:open="shortModalOpen"
      :ui="{ content: 'max-w-sm p-0 overflow-hidden' }"
    >
      <template #content>
        <div class="relative aspect-[9/16] w-full">
          <iframe
            v-if="selectedShort"
            :src="`https://www.youtube.com/embed/${selectedShort}?autoplay=1`"
            class="absolute inset-0 w-full h-full"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
          />
        </div>
      </template>
    </UModal>
  </div>
</template>
