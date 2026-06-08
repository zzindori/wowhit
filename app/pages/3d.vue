<script setup lang="ts">
import { makerWorldProfile, prints } from '~/data/prints'

useSeoMeta({
  title: '3D Printing — wowhit',
  description: 'Bambu Lab로 제작한 3D 프린팅 작품 — MakerWorld @jinsukYoon',
})
</script>

<template>
  <div>
    <UPageHero
      title="3D Printing"
      description="Bambu Lab · 프라모델 · 디오라마"
      :links="[
        {
          label: 'MakerWorld 프로필',
          icon: 'i-lucide-external-link',
          to: makerWorldProfile,
          target: '_blank',
          color: 'primary',
        },
      ]"
    />

    <UPageSection
      title="작품"
      :ui="{ container: 'py-8' }"
    >
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard
          v-for="print in prints"
          :key="print.slug"
          class="h-full overflow-hidden"
          :ui="{ body: 'p-0' }"
        >
          <a
            :href="print.makerWorldUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="block group"
          >
            <div
              class="aspect-[4/3] bg-gradient-to-br from-primary/10 via-default to-primary/5 flex items-center justify-center relative overflow-hidden"
            >
              <img
                v-if="print.imageUrl"
                :src="print.imageUrl"
                :alt="print.name"
                class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              >
              <UIcon
                v-else
                name="i-lucide-box"
                class="size-16 text-primary/40 group-hover:text-primary/60 transition-colors"
              />
            </div>
            <div class="p-4">
              <h3 class="font-semibold group-hover:text-primary transition-colors">
                {{ print.name }}
              </h3>
              <p class="text-sm text-muted mt-1">
                {{ print.description }}
              </p>
              <p class="text-xs text-muted mt-3 flex items-center gap-1">
                <UIcon
                  name="i-lucide-external-link"
                  class="size-3"
                />
                MakerWorld에서 보기
              </p>
            </div>
          </a>
        </UCard>
      </div>
    </UPageSection>
  </div>
</template>