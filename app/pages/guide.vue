<script setup lang="ts">
import { apps } from '~/data/apps'

useSeoMeta({
  title: '이용 안내 — wowhit',
  description: '웹앱 홈 화면 추가 방법, 이용권/크레딧 구매, Gemini API 키 직접 사용까지 상세 안내',
  ogTitle: 'wowHit 이용 안내',
  ogDescription: '웹앱 홈 화면 추가 방법, 이용권/크레딧 구매, Gemini API 키 직접 사용까지 상세 안내'
})

const installTab = ref('android')

const creditApps = apps.filter(a => a.purchaseUrl)

const pricingRows = [
  { model: 'Gemini 2.5 Flash Image (Nano Banana)', use: 'JoA 이미지 생성', price: '이미지 1장당 약 $0.039 (약 55원)' },
  { model: 'Imagen 4', use: 'CODI:D 코디 이미지 생성', price: '이미지 1장당 $0.02~$0.06 (약 28원~85원)' },
  { model: 'Gemini 2.5/3.5 Flash (텍스트)', use: 'itNe 레시피 생성, 재료 인식', price: '무료 한도 내 사용 시 0원 (한도 초과분만 소액 과금)' }
]

const faqs = [
  {
    label: '이용권을 구매했는데 다른 기기에서도 쓸 수 있나요?',
    content: '네. 인증 코드(또는 계정)는 스마트폰, PC 등 여러 기기에서 동시에 사용할 수 있습니다. 다만 하루 사용 횟수는 기기 구분 없이 전체가 공유됩니다.'
  },
  {
    label: '미사용 횟수가 다음 날로 이월되나요?',
    content: '아니요. 매일 자정에 사용 횟수가 새로 충전되며, 그날 다 쓰지 못한 횟수는 다음 날로 이월되지 않습니다.'
  },
  {
    label: 'Gemini API 키를 직접 쓰면 정말 이용권보다 저렴한가요?',
    content: '사용량이 적다면 무료 한도 안에서 해결될 수 있어 더 저렴할 수 있습니다. 다만 텍스트 생성과 달리 이미지 생성 모델은 대부분 무료 한도가 없어 소량이라도 비용이 청구됩니다. 사용량이 많다면 오히려 정액 이용권이 더 저렴할 수 있으니, 하루 사용량을 가늠해보고 선택하는 것을 추천합니다.'
  },
  {
    label: 'API 키가 유출되면 어떻게 되나요?',
    content: 'API 키는 곧 결제 수단과 같습니다. 절대 타인에게 공유하지 마세요. 키가 유출된 것 같다면 Google AI Studio에서 즉시 키를 삭제(Delete)하고 새로 발급받으시기 바랍니다.'
  },
  {
    label: '홈 화면에 추가한 아이콘을 지우면 데이터도 사라지나요?',
    content: '앱마다 다릅니다. 서버(클라우드)에 데이터를 저장하는 앱은 아이콘을 지워도 데이터가 유지됩니다. 반면 웹 브라우저에만 데이터를 저장하는 앱(예: CODI:D의 코디 이미지)은 브라우저 저장공간을 초기화하거나 아이콘과 함께 앱 데이터를 완전히 삭제하면 데이터도 함께 사라질 수 있습니다.'
  }
]
</script>

<template>
  <UPageSection>
    <div class="max-w-3xl mx-auto space-y-16">
      <!-- 헤더 -->
      <div>
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
          <UIcon
            name="i-lucide-book-open-text"
            class="text-primary size-8"
          />
          <h1 class="text-3xl font-bold">
            이용 안내
          </h1>
        </div>
        <p class="text-muted">
          wowHit의 웹앱들을 앱처럼 설치하는 방법부터, 이용권 구매와 Gemini API 키 직접 사용까지
          한 번에 정리했습니다.
        </p>
      </div>

      <!-- 1. 홈 화면에 추가 -->
      <section>
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-lucide-smartphone"
            class="size-5 text-primary"
          />
          웹앱을 앱처럼 설치하기 (홈 화면에 추가)
        </h2>
        <p class="text-sm text-muted mb-6">
          별도의 앱스토어 설치 없이, 웹앱 주소를 스마트폰 홈 화면에 추가하면
          아이콘을 눌러 실제 앱처럼 실행할 수 있습니다. 주소창 없이 전체 화면으로 보이고,
          홈 화면·앱 서랍에서 바로 찾을 수 있습니다.
        </p>

        <UTabs
          v-model="installTab"
          :items="[
            { label: 'Android (Chrome)', value: 'android', icon: 'i-simple-icons-android' },
            { label: 'iPhone (Safari)', value: 'ios', icon: 'i-simple-icons-safari' }
          ]"
          class="w-full"
        >
          <template #content="{ item }">
            <div
              v-if="item.value === 'android'"
              class="pt-4"
            >
              <ol class="space-y-3 text-sm">
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">1</span>
                  <span><strong>Chrome 브라우저</strong>로 웹앱 주소(예: joa.wowhit.org)에 접속합니다.</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">2</span>
                  <span>화면 우측 상단의 <strong>점 3개(⋮) 메뉴</strong>를 누릅니다.</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">3</span>
                  <span><strong>"앱 설치"</strong> 또는 <strong>"홈 화면에 추가"</strong>를 선택합니다. (메뉴 이름은 기기/버전에 따라 다를 수 있습니다)</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">4</span>
                  <span>확인을 누르면 홈 화면과 앱 서랍에 아이콘이 생깁니다. 이후 이 아이콘으로 실행하면 앱처럼 전체 화면으로 열립니다.</span>
                </li>
              </ol>
              <UAlert
                icon="i-lucide-info"
                color="neutral"
                variant="subtle"
                title="삼성 인터넷 브라우저를 쓰는 경우"
                description="하단 메뉴 바의 '삼성 인터넷 메뉴' 버튼 → '홈 화면에 추가'로 동일하게 설치할 수 있습니다."
                class="mt-4"
              />
            </div>

            <div
              v-else
              class="pt-4"
            >
              <ol class="space-y-3 text-sm">
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">1</span>
                  <span>반드시 <strong>Safari 브라우저</strong>로 웹앱 주소에 접속합니다. (Chrome 등 다른 브라우저에서는 이 기능이 보이지 않습니다)</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">2</span>
                  <span>화면 하단(또는 상단) <strong>공유 버튼</strong>(사각형 안에 위쪽 화살표)을 누릅니다.</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">3</span>
                  <span>공유 메뉴를 아래로 스크롤해 <strong>"홈 화면에 추가"</strong>를 선택합니다.</span>
                </li>
                <li class="flex gap-3">
                  <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">4</span>
                  <span>아이콘 이름을 확인하고 우측 상단 <strong>"추가"</strong>를 누르면 완료됩니다.</span>
                </li>
              </ol>
              <UAlert
                icon="i-lucide-check-circle"
                color="success"
                variant="subtle"
                title="아이폰에서도 App Store 없이 설치 가능"
                description="JoA, itNe, CODI:D 등 wowHit 웹앱은 모두 이 방식으로 iPhone에서 앱처럼 사용할 수 있습니다. App Store 심사를 거치지 않아도 되어 업데이트도 더 빠르게 반영됩니다."
                class="mt-4"
              />
            </div>
          </template>
        </UTabs>
      </section>

      <!-- 1-1. Android APK 직접 설치 -->
      <section>
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-simple-icons-android"
            class="size-5 text-primary"
          />
          Android 직접 설치(APK) 시 나오는 안내들
        </h2>
        <p class="text-sm text-muted mb-6">
          아직 Google Play에 정식 출시하지 않은 앱(JoA, itNe, CODI:D, careWay 등)은
          "Android 직접 설치" 버튼으로 APK 파일을 내려받아 설치합니다. Play 스토어를
          거치지 않다 보니 중간에 낯선 확인창이 여러 번 뜨는데, 전부 정상적인 절차입니다.
        </p>
        <ol class="space-y-4 text-sm">
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">1</span>
            <div>
              <p><strong>다운로드 경고</strong> — "이 파일 형식은 기기에 손상을 줄 수 있습니다" 같은 문구가 뜨면 <strong>"다운로드"</strong> 또는 <strong>"무시하고 다운로드"</strong>를 눌러 계속 진행합니다.</p>
            </div>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">2</span>
            <div>
              <p><strong>출처를 알 수 없는 앱 차단</strong> — "이 출처의 앱 설치가 차단되었습니다"라는 화면이 뜨면 <strong>"설정"</strong>을 누른 뒤, 사용 중인 브라우저(Chrome, 삼성 인터넷 등)의 <strong>"이 출처 허용"</strong> 토글을 켜고 뒤로 돌아와 다시 설치를 시도합니다. 한 번 허용해두면 다음 설치부터는 다시 묻지 않습니다.</p>
            </div>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">3</span>
            <div>
              <p><strong>Play 프로텍트 경고</strong> — "알 수 없는 앱입니다", "이 앱은 확인되지 않았습니다" 같은 경고가 뜰 수 있습니다. <strong>"세부정보"</strong>를 펼쳐 <strong>"무시하고 설치"</strong>를 선택하면 진행됩니다. 이는 Play 스토어에 등록되지 않은 APK 전체에 공통으로 뜨는 안내이며, 악성 코드 여부와는 무관합니다.</p>
            </div>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">4</span>
            <div>
              <p><strong>설치 완료</strong> — 설치가 끝나면 <strong>"열기"</strong>를 눌러 바로 실행하거나, 홈 화면/앱 서랍에서 아이콘을 찾아 실행합니다.</p>
            </div>
          </li>
        </ol>
        <UAlert
          icon="i-lucide-shield-check"
          color="neutral"
          variant="subtle"
          title="삭제는 언제든 간단하게"
          description="홈 화면 아이콘을 길게 눌러 '삭제' 또는 '앱 정보 > 제거'를 선택하면 됩니다. 설정 앱 > 앱 목록에서도 동일하게 제거할 수 있습니다."
          class="mt-4"
        />
      </section>

      <!-- 2. 이용 방법 두 가지 -->
      <section>
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-lucide-sparkles"
            class="size-5 text-primary"
          />
          AI 기능, 어떻게 이용하나요?
        </h2>
        <p class="text-sm text-muted mb-6">
          JoA, itNe, CODI:D처럼 AI(Gemini)로 이미지나 레시피를 생성하는 앱은
          <strong>이용권(크레딧) 구매</strong>와 <strong>본인 Gemini API 키 직접 입력</strong>,
          두 가지 방법 중 하나로 이용할 수 있습니다.
        </p>

        <div class="grid sm:grid-cols-2 gap-4">
          <div class="rounded-2xl border border-default p-5">
            <div class="flex items-center gap-2 mb-2">
              <UIcon
                name="i-lucide-shopping-cart"
                class="size-5 text-warning"
              />
              <h3 class="font-semibold">
                이용권 / 크레딧 구매
              </h3>
              <UBadge
                label="추천"
                color="warning"
                variant="subtle"
                size="sm"
              />
            </div>
            <p class="text-sm text-muted mb-3">
              네이버 스마트스토어에서 결제하면 인증 코드를 받습니다.
              앱에 코드만 입력하면 바로 사용할 수 있어, AI API 키 발급 같은
              복잡한 과정이 전혀 필요 없습니다.
            </p>
            <ul class="text-sm space-y-1.5 text-muted">
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-check"
                  class="size-4 text-success shrink-0 mt-0.5"
                />
                Google 계정, 결제 정보 등록 불필요
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-check"
                  class="size-4 text-success shrink-0 mt-0.5"
                />
                하루 사용량이 매일 자정 자동 충전
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-check"
                  class="size-4 text-success shrink-0 mt-0.5"
                />
                여러 기기에서 코드 하나로 동시 사용
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-x"
                  class="size-4 text-error shrink-0 mt-0.5"
                />
                정액 결제라 사용량이 적어도 비용은 동일
              </li>
            </ul>
          </div>

          <div class="rounded-2xl border border-default p-5">
            <div class="flex items-center gap-2 mb-2">
              <UIcon
                name="i-lucide-key-round"
                class="size-5 text-primary"
              />
              <h3 class="font-semibold">
                Gemini API 키 직접 사용
              </h3>
              <UBadge
                label="고급 사용자용"
                color="neutral"
                variant="subtle"
                size="sm"
              />
            </div>
            <p class="text-sm text-muted mb-3">
              Google AI Studio에서 본인 명의로 API 키를 발급받아 앱 설정에 입력하는 방식입니다.
              이용권 구매 없이 사용할 수 있지만, 사용한 만큼 Google에서 본인에게 직접 요금을 청구합니다.
            </p>
            <ul class="text-sm space-y-1.5 text-muted">
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-check"
                  class="size-4 text-success shrink-0 mt-0.5"
                />
                사용량이 적으면 무료 한도 내에서 해결 가능
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-check"
                  class="size-4 text-success shrink-0 mt-0.5"
                />
                이용권 구매/결제 절차 없음
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-x"
                  class="size-4 text-error shrink-0 mt-0.5"
                />
                Google 계정 + API 키 발급 과정 필요 (아래 안내 참고)
              </li>
              <li class="flex gap-2">
                <UIcon
                  name="i-lucide-x"
                  class="size-4 text-error shrink-0 mt-0.5"
                />
                과금 방식을 잘못 이해하면 예상보다 많은 요금이 나올 수 있음
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 3. API 키 발급 방법 -->
      <section>
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-lucide-key-round"
            class="size-5 text-primary"
          />
          Gemini API 키 발급받는 방법
        </h2>
        <p class="text-sm text-muted mb-6">
          이용권 구매 없이 직접 사용하고 싶다면, 아래 순서로 본인 명의 API 키를 발급받으세요.
        </p>
        <ol class="space-y-3 text-sm">
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">1</span>
            <span>
              <UButton
                to="https://aistudio.google.com/apikey"
                target="_blank"
                variant="link"
                label="Google AI Studio"
                trailing-icon="i-lucide-external-link"
                class="p-0"
              />
              에 본인 Google 계정으로 로그인합니다.
            </span>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">2</span>
            <span><strong>"API 키 만들기(Create API key)"</strong>를 눌러 새 프로젝트에 키를 생성합니다.</span>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">3</span>
            <span>이미지 생성 기능(JoA, CODI:D)을 쓰려면 결제 계정 연결(Billing) 설정이 필요합니다. 텍스트 전용 기능(itNe 레시피 등)은 무료 한도 안에서는 결제 등록 없이도 사용 가능합니다.</span>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">4</span>
            <span>발급된 키를 복사해 각 앱의 <strong>설정 &gt; API 키 입력</strong> 화면에 붙여넣습니다.</span>
          </li>
          <li class="flex gap-3">
            <span class="shrink-0 size-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">5</span>
            <span>
              PC에서 발급받아 스마트폰에 옮겨야 한다면, 이 사이트의
              <NuxtLink
                to="/qr"
                class="text-primary hover:underline"
              >QR 변환</NuxtLink>
              메뉴에 키를 붙여넣어 QR 코드로 만든 뒤, 앱에서 QR 스캔으로 간편하게 입력할 수 있습니다.
            </span>
          </li>
        </ol>
        <UAlert
          icon="i-lucide-triangle-alert"
          color="warning"
          variant="subtle"
          title="API 키는 비밀번호와 같습니다"
          description="타인에게 공유하거나 공개된 곳에 올리지 마세요. 유출이 의심되면 Google AI Studio에서 즉시 삭제 후 재발급받으세요."
          class="mt-4"
        />
      </section>

      <!-- 4. 가격 안내 -->
      <section>
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-lucide-circle-dollar-sign"
            class="size-5 text-primary"
          />
          Gemini 요금은 얼마나 나오나요?
        </h2>
        <p class="text-sm text-muted mb-6">
          본인 API 키로 직접 사용할 경우 기준입니다. 이용권을 구매해 사용하는 경우 아래 요금과 무관하게
          정액 이용권 가격만 지불하면 됩니다.
        </p>

        <div class="overflow-x-auto rounded-xl border border-default">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-default bg-elevated/50">
                <th class="text-left font-medium p-3">
                  모델
                </th>
                <th class="text-left font-medium p-3">
                  어떤 앱에서 쓰나요
                </th>
                <th class="text-left font-medium p-3">
                  대략적인 가격
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in pricingRows"
                :key="row.model"
                class="border-b border-default last:border-0"
              >
                <td class="p-3 font-medium">
                  {{ row.model }}
                </td>
                <td class="p-3 text-muted">
                  {{ row.use }}
                </td>
                <td class="p-3 text-muted">
                  {{ row.price }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p class="text-xs text-muted mt-3">
          * 위 가격은 2026년 7월 기준 참고용 대략치이며, 원/달러 환율과 Google 정책에 따라 달라질 수 있습니다.
          정확한 최신 가격은
          <UButton
            to="https://ai.google.dev/gemini-api/docs/pricing"
            target="_blank"
            variant="link"
            label="Google 공식 가격 페이지"
            trailing-icon="i-lucide-external-link"
            class="p-0 text-xs"
          />
          에서 확인하세요.
        </p>

        <UAlert
          icon="i-lucide-lightbulb"
          color="neutral"
          variant="subtle"
          title="쉽게 비교하면"
          description="이미지 1장 생성에 약 30~90원 수준입니다. 하루 한두 장 정도만 가볍게 쓴다면 직접 키를 발급받는 편이 이용권보다 저렴할 수 있고, 매일 여러 장을 생성한다면 정액 이용권이 더 유리할 수 있습니다."
          class="mt-4"
        />
      </section>

      <!-- 5. 앱별 이용권 -->
      <section v-if="creditApps.length">
        <h2 class="text-xl font-bold mb-1 flex items-center gap-2">
          <UIcon
            name="i-lucide-store"
            class="size-5 text-primary"
          />
          앱별 이용권 / 크레딧 구매
        </h2>
        <p class="text-sm text-muted mb-6">
          네이버 스마트스토어에서 결제 후 안내되는 인증 코드를 앱에 입력하면 바로 이용할 수 있습니다.
        </p>
        <div class="grid sm:grid-cols-2 gap-3">
          <NuxtLink
            v-for="app in creditApps"
            :key="app.slug"
            :to="`/${app.slug}`"
            class="flex items-center gap-3 rounded-xl border border-default p-4 hover:border-primary transition-colors"
          >
            <img
              v-if="app.iconUrl"
              :src="app.iconUrl"
              :alt="app.name"
              class="size-10 rounded-xl object-cover shrink-0"
            >
            <div class="min-w-0">
              <p class="font-medium">
                {{ app.name }}
              </p>
              <p class="text-xs text-muted truncate">
                {{ app.description }}
              </p>
            </div>
            <UIcon
              name="i-lucide-chevron-right"
              class="size-4 text-muted ml-auto shrink-0"
            />
          </NuxtLink>
        </div>
      </section>

      <!-- 6. FAQ -->
      <section>
        <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
          <UIcon
            name="i-lucide-circle-help"
            class="size-5 text-primary"
          />
          자주 묻는 질문
        </h2>
        <UAccordion :items="faqs">
          <template #content="{ item }">
            <p class="text-sm text-muted px-1 pb-3">
              {{ item.content }}
            </p>
          </template>
        </UAccordion>
      </section>
    </div>
  </UPageSection>
</template>
