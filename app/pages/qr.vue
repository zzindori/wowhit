<script setup lang="ts">
import QRCode from 'qrcode'

useSeoMeta({ title: 'API Key QR — wowhit' })

const input = ref('')
const qrDataUrl = ref('')
const copied = ref(false)

async function generateQR() {
  if (!input.value.trim()) return
  qrDataUrl.value = await QRCode.toDataURL(input.value, {
    width: 400,
    margin: 2,
    color: { dark: '#000000', light: '#ffffff' }
  })
}

function clearAll() {
  input.value = ''
  qrDataUrl.value = ''
}

async function copyToClipboard() {
  await navigator.clipboard.writeText(input.value)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 1500)
}

watch(input, () => {
  if (input.value.trim()) generateQR()
  else qrDataUrl.value = ''
})
</script>

<template>
  <UPageSection>
    <div class="max-w-lg mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold mb-1">
          API Key → QR 변환
        </h1>
        <p class="text-sm text-muted">
          긴 API 키를 QR 코드로 변환해 앱/웹앱에서 스캔하세요.
        </p>
      </div>

      <div class="space-y-4">
        <UFormField label="API Key">
          <div class="relative">
            <UTextarea
              v-model="input"
              placeholder="API 키를 붙여넣으세요..."
              :rows="4"
              class="w-full font-mono text-sm"
            />
          </div>
        </UFormField>

        <div class="flex gap-2">
          <UButton
            v-if="input"
            :icon="copied ? 'i-lucide-check' : 'i-lucide-copy'"
            :label="copied ? '복사됨' : '복사'"
            variant="subtle"
            color="neutral"
            size="sm"
            @click="copyToClipboard"
          />
          <UButton
            v-if="input"
            icon="i-lucide-x"
            label="초기화"
            variant="subtle"
            color="neutral"
            size="sm"
            @click="clearAll"
          />
        </div>

        <!-- QR 코드 -->
        <div
          v-if="qrDataUrl"
          class="flex flex-col items-center gap-4 pt-4"
        >
          <div class="bg-white p-4 rounded-2xl shadow-md inline-block">
            <img
              :src="qrDataUrl"
              alt="QR Code"
              class="w-64 h-64"
            >
          </div>
          <p class="text-xs text-muted text-center">
            앱/웹앱에서 이 QR 코드를 스캔하면 API 키가 자동 입력됩니다.
          </p>
          <UButton
            icon="i-lucide-download"
            label="QR 이미지 저장"
            variant="subtle"
            color="neutral"
            size="sm"
            :to="qrDataUrl"
            download="api-key-qr.png"
          />
        </div>

        <UAlert
          v-else-if="!input"
          icon="i-lucide-scan-qr-code"
          title="API 키를 입력하면 QR 코드가 자동 생성됩니다"
          color="neutral"
          variant="subtle"
        />
      </div>
    </div>
  </UPageSection>
</template>
