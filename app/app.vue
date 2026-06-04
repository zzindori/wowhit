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
  description: 'Flutter · Web · Watch 앱 개발 포트폴리오',
  ogTitle: 'wowhit',
  ogDescription: 'Flutter · Web · Watch 앱 개발 포트폴리오'
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
        <p class="text-sm text-muted">
          © {{ new Date().getFullYear() }} wowhit
        </p>
      </template>
    </UFooter>
  </UApp>
</template>
