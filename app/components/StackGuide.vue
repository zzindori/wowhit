<script setup lang="ts">
// 층층이 소개: 긴 글 대신 실제 게임 캡처 위에 번호 점 → 마우스를 올리거나(폰은 탭) 누르면 설명.
// 캡처는 public/games/stack/guide/ (게임 화면 760×1240 기준 좌표 — 게임을 크게 바꾸면 다시 찍을 것)
defineProps<{ text?: string, playUrl?: string }>()

const G = '/games/stack/guide'
const IMG_W = 760
const IMG_H = 1240

const spots = [
  { x: 97, y: 25, t: '지갑', d: '가진 돈 / 지갑 한도. 꽉 차면 돈을 더 못 주워요 — 지갑 칸에서 키우세요.' },
  { x: 719, y: 29, t: '설정', d: '소리·진동 켜고 끄기, 가게 미리보기, 처음부터 다시 하기.' },
  { x: 250, y: 198, t: '손님 줄', d: '말풍선 = 사려는 개수, 막대 = 참을성. 오래 기다리면 "빨리빨리!" 하다 화내고 가요.' },
  { x: 455, y: 168, t: '엘리베이터', d: '문 앞에 서면 층 선택판이 열려요. 키보드라면 숫자키로 바로 이동.' },
  { x: 700, y: 170, t: '계단 · 다음 층 열기', d: '생산기 3대를 다 열면 여기서 새 층을 열어요. 계단으로 위아래 층을 오가요.' },
  { x: 300, y: 348, t: '판매 칸', d: '여기 서면 등에 진 물건을 판매대에 내려놓아요. 직접 놓으면 값이 2배!' },
  { x: 490, y: 330, t: '돈더미', d: '판 돈이 쌓이는 곳. 밟으면 지갑으로. 오래 두면 도둑이 와요.' },
  { x: 300, y: 520, t: '주인공 둥실이', d: '물건을 등에 높이 쌓아 날라요. 표정이 바뀌어요(돈 ^^, 황금 ★, 졸음 zZ).' },
  { x: 270, y: 594, t: '일꾼', d: '고용하면 생산기 → 판매대를 알아서 날라요. 층마다 가게 유니폼을 입어요.' },
  { x: 52, y: 424, t: '공통 업그레이드', d: '적재량 · 이동속도 · 지갑. 모든 층에 적용, 맨 위층에 있어요.' },
  { x: 708, y: 424, t: '이 층 업그레이드', d: '자동 수금 · 일꾼 · 판매속도 · 잔업(꺼 둔 동안 수입). 칸 위에 잠깐 서 있으면 결제.' },
  { x: 380, y: 750, t: '생산기', d: '층마다 메뉴가 3가지. 조리하는 모습이 다 보이고, 다 되면 쟁반에 "딩".' },
  { x: 170, y: 820, t: '줍는 칸', d: '회색 칸에 서 있으면 만든 물건이 등에 차곡차곡 쌓여요.' },
  { x: 624, y: 970, t: '보관대 · 생산속도 · 알바 가방', d: '생산기 앞에 더 많이 쌓이게, 더 빨리 만들게, 일꾼이 더 많이 들게.' },
  { x: 27, y: 1048, t: '층 표시', d: '지금 층과 일이 생긴 층(건물주·배달·고장…)을 급한 순서로 보여 줘요.' },
  { x: 380, y: 1186, t: '미션', d: '팔기·모으기·팁·업그레이드 미션이 끝없이 이어지고, 깨면 보상!' }
]

const active = ref<number | null>(null)
const pinned = ref(false)
function hover(i: number | null) {
  if (!pinned.value) active.value = i
}
function tap(i: number) {
  if (pinned.value && active.value === i) {
    pinned.value = false
    active.value = null
    return
  }
  pinned.value = true
  active.value = i
}
// 말풍선: 점 위치에 따라 왼쪽/가운데/오른쪽 정렬, 아래쪽 점이면 위로
const bubble = computed(() => {
  if (active.value === null) return null
  const s = spots[active.value]!
  const px = s.x / IMG_W * 100
  const py = s.y / IMG_H * 100
  const style: Record<string, string> = {}
  if (px < 30) style.left = `${Math.max(px - 4, 1)}%`
  else if (px > 70) style.right = `${Math.max(100 - px - 4, 1)}%`
  else {
    style.left = `${px}%`
    style.transform = 'translateX(-50%)'
  }
  if (py > 55) style.bottom = `${100 - py + 3.5}%`
  else style.top = `${py + 3.5}%`
  return { s, n: active.value + 1, style }
})

const steps = [
  { icon: 'i-lucide-chef-hat', t: '만들기', d: '생산기가 음식을 만들어요' },
  { icon: 'i-lucide-package', t: '나르기', d: '등에 높이 쌓아서' },
  { icon: 'i-lucide-hand-coins', t: '팔기', d: '판매대에 놓으면 손님이 사 가요' },
  { icon: 'i-lucide-building-2', t: '키우기', d: '번 돈으로 업그레이드, 새 층!' }
]

const floors = [
  { n: 1, shop: '층층분식', menu: '떡볶이 · 김밥 · 순대' },
  { n: 2, shop: '따끈 붕어빵', menu: '호떡 · 붕어빵 · 계란빵' },
  { n: 3, shop: '바삭치킨', menu: '양념 · 후라이드 · 간장' },
  { n: 4, shop: '24시 층층편의점', menu: '핫바 · 바나나우유 · 호빵' },
  { n: 5, shop: '한강라면', menu: '즉석 라면 조리기' },
  { n: 6, shop: '♪ 코인노래방', menu: '100점 나오면 음료 캔' },
  { n: 7, shop: '층층 뷰티', menu: '마스크팩 · 쿠션 · 립틴트' },
  { n: 8, shop: '층층 한복대여', menu: '여자 한복 · 남자 한복 · 노리개' },
  { n: 9, shop: '층층 박물관 굿즈샵', menu: '반가사유상 · 달항아리 · 금관' },
  { n: 10, shop: '3D 프린터 공장', menu: '10층부터 끝없이 위로' }
]

const events = [
  { img: 'ev-deliv', t: '🛵 배달 주문', d: '다른 층 음식을 시켜요. 들고 가면 큰돈 + 빨리 가면 배달팁.' },
  { img: 'ev-vip', t: '👑 건물주', d: '직접 건네야 해요. 놓치면 "임대료 올려야겠군!" 하고 잠깐 느려져요.' },
  { img: 'ev-thief', t: '🦹 도둑', d: '돈더미를 노려요. 부딪히면 되찾고 현상금까지!' },
  { img: 'ev-broken', t: '🔧 고장', d: '앞에 잠깐 서 있으면 수리. 2분 넘게 두면 부서져요.' },
  { img: 'ev-gold', t: '✨ 황금 물건', d: '가끔 나오는 잭팟(값 10배). 직접 날라야 하고 60초면 사라져요.' }
]
</script>

<template>
  <div class="space-y-12">
    <!-- 한 줄 소개 + 시작 -->
    <div>
      <p class="text-lg leading-relaxed">
        층마다 다른 가게가 들어선 <b>한국 상가 건물</b>을 키우는 게임이에요.
        음식을 만들어 등에 쌓아 나르고, 팔고, 번 돈으로 건물을 끝없이 올려요.
      </p>
      <UButton
        v-if="playUrl"
        :to="playUrl"
        target="_blank"
        icon="i-lucide-play"
        label="바로 게임 하기"
        size="xl"
        class="mt-5"
      />
    </div>

    <!-- 4단계 -->
    <section>
      <h2 class="text-xl font-bold mb-4">
        이것만 알면 돼요
      </h2>
      <ol class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <li
          v-for="(s, i) in steps"
          :key="s.t"
          class="relative rounded-2xl bg-elevated p-4 text-center"
        >
          <span class="absolute left-3 top-2 text-xs font-bold text-muted">{{ i + 1 }}</span>
          <UIcon
            :name="s.icon"
            class="size-8 text-primary"
          />
          <div class="font-bold mt-1">
            {{ s.t }}
          </div>
          <div class="text-xs text-muted mt-1">
            {{ s.d }}
          </div>
        </li>
      </ol>
      <p class="text-sm text-muted mt-3">
        움직이기: 폰은 화면을 드래그(조이스틱) · PC는 WASD / 방향키
      </p>
    </section>

    <!-- 화면 둘러보기 -->
    <section>
      <h2 class="text-xl font-bold mb-1">
        화면 둘러보기
      </h2>
      <p class="text-sm text-muted mb-4">
        번호에 마우스를 올리거나 눌러 보세요
      </p>
      <div class="flex flex-col md:flex-row gap-6 items-start">
        <div
          class="relative w-full max-w-[400px] mx-auto md:mx-0 shrink-0 select-none"
          @mouseleave="hover(null)"
        >
          <img
            :src="`${G}/main.webp`"
            alt="층층이 게임 화면 (3층 바삭치킨)"
            class="w-full rounded-2xl shadow-lg"
            :width="IMG_W"
            :height="IMG_H"
          >
          <button
            v-for="(s, i) in spots"
            :key="i"
            type="button"
            :aria-label="`${i + 1}. ${s.t}`"
            class="absolute -translate-x-1/2 -translate-y-1/2 size-6 rounded-full text-[11px] font-bold ring-2 ring-white shadow-md transition-transform cursor-pointer"
            :class="active === i ? 'bg-warning text-black scale-125 z-20' : 'bg-primary text-white z-10'"
            :style="{ left: `${s.x / IMG_W * 100}%`, top: `${s.y / IMG_H * 100}%` }"
            @mouseenter="hover(i)"
            @focus="hover(i)"
            @click="tap(i)"
          >
            {{ i + 1 }}
          </button>
          <div
            v-if="bubble"
            class="absolute z-30 w-56 rounded-xl bg-inverted text-inverted p-3 shadow-xl pointer-events-none"
            :style="bubble.style"
          >
            <div class="font-bold text-sm">
              {{ bubble.n }}. {{ bubble.s.t }}
            </div>
            <div class="text-xs mt-1 leading-relaxed opacity-90">
              {{ bubble.s.d }}
            </div>
          </div>
        </div>
        <ol class="grid gap-1 text-sm w-full">
          <li
            v-for="(s, i) in spots"
            :key="i"
            class="flex gap-2 rounded-lg px-2 py-1.5 cursor-pointer transition-colors"
            :class="active === i ? 'bg-warning/15' : 'hover:bg-elevated'"
            @mouseenter="hover(i)"
            @mouseleave="hover(null)"
            @click="tap(i)"
          >
            <span
              class="shrink-0 size-5 rounded-full text-[11px] font-bold grid place-items-center"
              :class="active === i ? 'bg-warning text-black' : 'bg-primary text-white'"
            >{{ i + 1 }}</span>
            <span><b>{{ s.t }}</b> <span class="text-muted">— {{ s.d }}</span></span>
          </li>
        </ol>
      </div>
    </section>

    <!-- 층마다 다른 가게 -->
    <section>
      <h2 class="text-xl font-bold mb-1">
        층마다 다른 가게
      </h2>
      <p class="text-sm text-muted mb-4">
        위층일수록 물건 값이 5배씩! 생산기는 조리하는 모습이 다 보여요
      </p>
      <div class="grid sm:grid-cols-2 gap-3">
        <figure
          v-for="f in floors"
          :key="f.n"
          class="rounded-2xl bg-elevated overflow-hidden"
        >
          <img
            :src="`${G}/floor${f.n}.webp`"
            :alt="`${f.n}층 ${f.shop}`"
            loading="lazy"
            class="w-full aspect-[600/290] object-cover"
          >
          <figcaption class="p-2.5">
            <div class="font-bold text-sm">
              <span class="text-primary">{{ f.n }}층</span> {{ f.shop }}
            </div>
            <div class="text-xs text-muted">
              {{ f.menu }}
            </div>
          </figcaption>
        </figure>
      </div>
    </section>

    <!-- 이벤트 -->
    <section>
      <h2 class="text-xl font-bold mb-4">
        이런 일이 생겨요
      </h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        <figure
          v-for="e in events"
          :key="e.img"
          class="rounded-2xl bg-elevated overflow-hidden"
        >
          <img
            :src="`${G}/${e.img}.webp`"
            :alt="e.t"
            loading="lazy"
            class="w-full aspect-[7/6] object-cover"
          >
          <figcaption class="p-2.5">
            <div class="font-bold text-sm">
              {{ e.t }}
            </div>
            <div class="text-xs text-muted mt-0.5">
              {{ e.d }}
            </div>
          </figcaption>
        </figure>
      </div>
    </section>

    <!-- 긴 설명은 접어 둠 -->
    <details
      v-if="text"
      class="rounded-2xl border border-default p-4 group"
    >
      <summary class="cursor-pointer font-semibold flex items-center gap-2">
        <UIcon
          name="i-lucide-chevron-right"
          class="size-4 transition-transform group-open:rotate-90"
        />
        자세한 설명 전부 보기
      </summary>
      <div class="mt-4">
        <p
          v-for="(line, i) in text.split('\n\n')"
          :key="i"
          class="text-sm text-muted mb-3 last:mb-0 whitespace-pre-line"
        >
          {{ line }}
        </p>
      </div>
    </details>
  </div>
</template>
