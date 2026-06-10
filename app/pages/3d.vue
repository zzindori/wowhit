<script setup lang="ts">
import {
  makerWorldProfile,
  printCategories,
  printCategoryMeta,
  prints
} from '~/data/prints'

const selectedPrint = ref<(typeof prints)[0] | null>(null)
const galleryOpen = ref(false)

function openGallery(print: (typeof prints)[0]) {
  if (!print.images?.length) return
  selectedPrint.value = print
  galleryOpen.value = true
}

useSeoMeta({
  title: '3D Printing — wowhit',
  description: 'Bambu Lab 3D 프린팅 — MakerWorld'
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
          color: 'primary'
        }
      ]"
    />

    <UPageSection
      v-for="category in printCategories"
      :key="category"
      :title="printCategoryMeta[category].label"
      :ui="{ container: 'py-6' }"
    >
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <UCard
          v-for="print in prints.filter(p => p.category === category)"
          :key="print.slug"
          class="h-full overflow-hidden"
          :ui="{ body: 'p-0' }"
        >
          <div class="block">
            <button
              type="button"
              class="w-full aspect-[4/3] relative overflow-hidden bg-gradient-to-br from-primary/10 via-default to-primary/5"
              :class="print.images?.length ? 'cursor-zoom-in' : 'cursor-default'"
              @click="openGallery(print)"
            >
              <img
                :src="print.imageUrl"
                :alt="print.name"
                class="absolute inset-0 w-full h-full object-cover hover:scale-105 transition-transform duration-300"
              >
              <span
                v-if="print.images?.length"
                class="absolute bottom-2 right-2 text-xs bg-black/50 text-white px-2 py-0.5 rounded-full"
              >
                +{{ print.images.length }}
              </span>
            </button>
            <div class="p-4">
              <h3 class="font-semibold">
                {{ print.name }}
              </h3>
              <p class="text-sm text-muted mt-1">
                {{ print.description }}
              </p>
              <a
                v-if="print.makerWorldUrl"
                :href="print.makerWorldUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs text-muted mt-3 flex items-center gap-1 hover:text-primary transition-colors w-fit"
              >
                <UIcon
                  name="i-lucide-external-link"
                  class="size-3"
                />
                MakerWorld에서 보기
              </a>
            </div>
          </div>
        </UCard>
      </div>
    </UPageSection>

    <UModal
      v-model:open="galleryOpen"
      :ui="{ content: 'max-w-3xl' }"
    >
      <template #content>
        <div
          v-if="selectedPrint"
          class="p-4 space-y-4"
        >
          <h3 class="text-lg font-semibold">
            {{ selectedPrint.name }}
          </h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <img
              :src="selectedPrint.imageUrl"
              :alt="selectedPrint.name"
              class="w-full rounded-xl object-cover"
            >
            <img
              v-for="(src, i) in selectedPrint.images"
              :key="i"
              :src="src"
              :alt="`${selectedPrint.name} ${i + 2}`"
              class="w-full rounded-xl object-cover"
            >
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
