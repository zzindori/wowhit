<script setup>
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'ko'
  }
})

useSeoMeta({
  title: 'wowhit',
  description: 'App · Web · Watch 앱 개발 포트폴리오',
  ogTitle: 'wowHit',
  ogDescription: 'App · Web · Watch 앱 개발 포트폴리오'
})
</script>

<template>
  <UApp>
    <UHeader>
      <template #left>
        <NuxtLink to="/">
          <AppLogo />
        </NuxtLink>
      </template>

      <template #right>
        <UColorModeButton />
      </template>
    </UHeader>

    <UMain>
      <NuxtPage />
    </UMain>

    <UFooter>
      <template #left>
        <div class="text-sm text-muted space-y-0.5">
          <p>© {{ new Date().getFullYear() }} wowHit. All rights reserved.</p>
          <p>Powered by YL Company (Yoon &amp; Lee) | 사업자등록번호: 515-68-00370</p>
        </div>
      </template>
    </UFooter>
  </UApp>
</template>
