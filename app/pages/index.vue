<script setup lang="ts">
import { apps, categoryMeta } from '~/data/apps'

const categories = (['flutter', 'web', 'other'] as const).map(key => ({
  key,
  ...categoryMeta[key],
  apps: apps.filter(a => a.category === key)
}))

function getDirectLinks(app: (typeof apps)[0]) {
  const links = []
  if (app.androidUrl) links.push({ icon: 'i-simple-icons-googleplay', label: 'Play', to: app.androidUrl })
  if (app.iosUrl) links.push({ icon: 'i-simple-icons-appstore', label: 'App Store', to: app.iosUrl })
  if (app.webUrl) links.push({ icon: 'i-lucide-globe', label: 'Web', to: app.webUrl })
  if (app.apkUrl) links.push({ icon: 'i-simple-icons-android', label: 'Android 설치', to: app.apkUrl })
  if (app.purchaseUrl) links.push({ icon: 'i-lucide-shopping-cart', label: '이용권 구매', to: app.purchaseUrl, highlight: true })
  return links
}
</script>

<template>
  <div>
    <UPageHero
      title="wowHit"
      description="App · Web · Watch 앱 개발 포트폴리오"
    />

    <UPageSection
      v-for="group in categories"
      :key="group.key"
      :title="group.label"
      :ui="{ container: 'py-8' }"
    >
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard
          v-for="app in group.apps"
          :key="app.slug"
          class="h-full flex flex-col"
          :ui="{ body: 'flex-1 flex flex-col gap-3' }"
        >
          <!-- 상세설명으로 이동 -->
          <NuxtLink :to="`/${app.slug}`" class="flex items-start gap-3 flex-1 hover:opacity-80 transition-opacity">
            <img v-if="app.iconUrl" :src="app.iconUrl" :alt="app.name" class="size-10 rounded-xl shrink-0 object-cover" />
            <UIcon v-else :name="group.icon" class="text-primary mt-0.5 shrink-0 size-5" />
            <div class="min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <h3 class="font-semibold">{{ app.name }}</h3>
                <UBadge
                  v-if="app.storeReleased"
                  label="출시"
                  size="xs"
                  color="success"
                  variant="subtle"
                />
                <span v-if="app.version" class="text-xs text-muted">v{{ app.version }}</span>
              </div>
              <p class="text-sm text-muted mt-1">{{ app.description }}</p>
              <div v-if="app.api?.length" class="flex flex-wrap gap-1 mt-2">
                <UBadge
                  v-for="a in app.api"
                  :key="a"
                  :label="a"
                  size="xs"
                  variant="outline"
                />
              </div>
            </div>
          </NuxtLink>

          <!-- 직접 링크 버튼 -->
          <div v-if="getDirectLinks(app).length" class="flex flex-wrap gap-2 pt-2 border-t border-default">
            <UButton
              v-for="link in getDirectLinks(app)"
              :key="link.label"
              :icon="link.icon"
              :label="link.label"
              :to="link.to"
              target="_blank"
              size="xs"
              :variant="link.highlight ? 'subtle' : 'subtle'"
              :color="link.highlight ? 'warning' : 'neutral'"
            />
          </div>
        </UCard>
      </div>
    </UPageSection>
  </div>
</template>
