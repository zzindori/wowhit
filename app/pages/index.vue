<script setup lang="ts">
import { apps, categoryMeta } from '~/data/apps'
import { getFeaturedPrints, makerWorldProfile } from '~/data/prints'

const featuredPrints = getFeaturedPrints()

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
  if (app.purchaseUrl) {
    const isCredit = app.purchaseLabel === '크레딧 구매'
    links.push({
      icon: isCredit ? 'i-lucide-coins' : 'i-lucide-shopping-cart',
      label: app.purchaseLabel || '이용권 구매',
      to: app.purchaseUrl,
      highlight: true,
      isCredit
    })
  }
  return links
}
</script>

<template>
  <div>
    <UPageHero
      title="wowHit"
      description="App · Web · Watch · 3D Printing 포트폴리오"
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
          <NuxtLink
            :to="`/${app.slug}`"
            class="flex items-start gap-3 flex-1 hover:opacity-80 transition-opacity"
          >
            <img
              v-if="app.iconUrl"
              :src="app.iconUrl"
              :alt="app.name"
              class="size-10 rounded-xl shrink-0 object-cover"
            >
            <UIcon
              v-else
              :name="group.icon"
              class="text-primary mt-0.5 shrink-0 size-5"
            />
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
                <UBadge
                  v-if="app.pricingModel === 'free'"
                  label="무료"
                  icon="i-lucide-badge-check"
                  size="xs"
                  color="success"
                  variant="outline"
                />
                <UBadge
                  v-if="app.pricingModel === 'ads'"
                  label="광고 시청"
                  icon="i-lucide-tv"
                  size="xs"
                  color="neutral"
                  variant="outline"
                />
                <UBadge
                  v-if="app.purchaseUrl"
                  label="AI 유료"
                  icon="i-lucide-sparkles"
                  size="xs"
                  color="warning"
                  variant="outline"
                />
                <span
                  v-if="app.version"
                  class="text-xs text-muted"
                >v{{ app.version }}</span>
              </div>
              <p class="text-sm text-muted mt-1">{{ app.description }}</p>
              <div
                v-if="app.api?.length"
                class="flex flex-wrap gap-1 mt-2"
              >
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
          <div
            v-if="getDirectLinks(app).length"
            class="flex flex-wrap gap-2 pt-2 border-t border-default"
          >
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

    <UPageSection
      title="3D Printing"
      :ui="{ container: 'py-8' }"
    >
      <div class="flex items-center justify-between gap-4 mb-4">
        <p class="text-sm text-muted">
          Bambu Lab · 프라모델 · 디오라마
        </p>
        <UButton
          label="전체 보기"
          to="/3d"
          variant="subtle"
          size="sm"
          icon="i-lucide-arrow-right"
          trailing
        />
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        <component
          :is="print.makerWorldUrl ? 'a' : 'NuxtLink'"
          v-for="print in featuredPrints"
          :key="print.slug"
          :href="print.makerWorldUrl"
          :to="print.makerWorldUrl ? undefined : '/3d'"
          :target="print.makerWorldUrl ? '_blank' : undefined"
          :rel="print.makerWorldUrl ? 'noopener noreferrer' : undefined"
          class="group rounded-xl border border-default overflow-hidden hover:border-primary/50 transition-colors"
        >
          <div class="aspect-square bg-gradient-to-br from-primary/10 to-default">
            <img
              :src="print.imageUrl"
              :alt="print.name"
              class="w-full h-full object-cover"
            >
          </div>
          <p class="text-xs font-medium p-2 truncate group-hover:text-primary transition-colors">
            {{ print.name }}
          </p>
        </component>
      </div>
      <div class="mt-4">
        <UButton
          label="MakerWorld"
          :to="makerWorldProfile"
          target="_blank"
          variant="outline"
          size="sm"
          icon="i-lucide-external-link"
        />
      </div>
    </UPageSection>
  </div>
</template>
