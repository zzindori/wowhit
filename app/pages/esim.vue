<script setup lang="ts">
useSeoMeta({
  title: 'ドシラクeSIM インストールガイド（iPhone）',
  description: '韓国旅行前にiPhoneへドシラクeSIMをインストールする方法をご案内します。',
  ogTitle: 'ドシラクeSIM インストールガイド',
  ogDescription: '韓国旅行前にiPhoneへドシラクeSIMをインストールする方法をご案内します。'
})

useHead({ htmlAttrs: { lang: 'ja' } })
</script>

<template>
  <UPageSection>
    <div class="max-w-xl mx-auto space-y-8">

      <!-- ヘッダー -->
      <div class="text-center space-y-2">
        <div class="flex justify-center gap-2 mb-3">
          <UBadge color="neutral" variant="subtle" label="iPhone" icon="i-lucide-smartphone" />
          <UBadge color="primary" variant="subtle" label="韓国旅行用eSIM" icon="i-lucide-sim-card" />
        </div>
        <h1 class="text-2xl font-bold">
          ドシラクeSIM<br>インストールガイド
        </h1>
        <p class="text-sm text-muted">
          韓国に出発する前に完了させてください
        </p>
      </div>

      <!-- 事前確認 -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          事前確認事項
        </p>
        <UAlert
          icon="i-lucide-info"
          color="warning"
          variant="subtle"
          title="商品ページで事前インストール可否を確認"
          description="各商品の詳細ページで「インストール基準（事前インストール可否）」を必ず確認してください。"
        />
        <UAlert
          icon="i-lucide-calendar"
          color="warning"
          variant="subtle"
          title="到着後インストールが必要な商品に注意"
          description="インストール即日から日数がカウントされる商品は、韓国到着後にインストールしてください。"
        />
        <UAlert
          icon="i-lucide-wifi"
          color="warning"
          variant="subtle"
          title="Wi-Fi環境でインストールしてください"
          description="eSIMの追加はWi-Fiなどのネットワーク環境でのみ可能です。"
        />
        <UAlert
          icon="i-lucide-plane"
          color="warning"
          variant="subtle"
          title="出国前に既存回線を確認"
          description="既存のメイン回線のデータローミング OFF、データ自動切替え OFF になっていることを確認してください。"
        />
      </div>

      <!-- STEP 1 -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          STEP 1 — eSIMインストール
        </p>

        <!-- 方法① -->
        <UCard>
          <div class="space-y-4">
            <div class="flex items-center gap-2">
              <UBadge color="primary" label="方法①" />
              <span class="font-bold">アプリ / ウェブからバロ設置（推奨）</span>
            </div>

            <div class="space-y-3 text-sm">
              <div>
                <p class="font-semibold text-muted mb-1.5">
                  <UIcon name="i-lucide-globe" class="size-3.5 align-middle mr-1" />ウェブサイトの場合
                </p>
                <div class="bg-elevated rounded-lg px-4 py-3 space-y-1 text-xs leading-relaxed">
                  <p>マイページ <span class="text-primary font-bold">›</span> 購入履歴 <span class="text-primary font-bold">›</span> eSIM詳細</p>
                  <p><span class="text-primary font-bold">›</span> インストール情報(QR) 詳細表示</p>
                  <p><span class="text-primary font-bold">›</span> <UBadge size="sm" color="primary" label="バロ設置" /> をタップ</p>
                </div>
              </div>

              <div>
                <p class="font-semibold text-muted mb-1.5">
                  <UIcon name="i-lucide-smartphone" class="size-3.5 align-middle mr-1" />アプリの場合
                </p>
                <div class="bg-elevated rounded-lg px-4 py-3 space-y-1 text-xs leading-relaxed">
                  <p>私のeSIM <span class="text-primary font-bold">›</span> QRを見る</p>
                  <p><span class="text-primary font-bold">›</span> QRコード下の <UBadge size="sm" color="primary" label="バロ設置" /> をタップ</p>
                </div>
              </div>

              <UAlert
                icon="i-lucide-user"
                color="neutral"
                variant="subtle"
                size="sm"
                description="非会員の方は注文番号と携帯電話番号（またはメールアドレス）で照会できます。"
              />
            </div>
          </div>
        </UCard>

        <!-- 方法② -->
        <UCard>
          <div class="space-y-4">
            <div class="flex items-center gap-2">
              <UBadge color="neutral" variant="solid" label="方法②" />
              <span class="font-bold">QRコードで手動インストール</span>
            </div>

            <ol class="space-y-3 text-sm">
              <li class="flex items-start gap-3">
                <span class="size-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">1</span>
                <div>
                  <p><strong>設定</strong>を開く</p>
                  <p class="text-xs text-muted mt-0.5">設定 → モバイル通信 → 「eSIMを追加」をタップ</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="size-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">2</span>
                <div>
                  <p><strong>「その他のオプション」</strong>を選択</p>
                </div>
              </li>
              <li class="flex items-start gap-3">
                <span class="size-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">3</span>
                <div>
                  <p><strong>「QRコードを使用」</strong>を選択</p>
                  <p class="text-xs text-muted mt-0.5">ドシラクのQRコードをカメラで読み取ってください</p>
                </div>
              </li>
            </ol>
          </div>
        </UCard>
      </div>

      <!-- STEP 2 -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          STEP 2 — eSIMの有効化
        </p>

        <UCard>
          <ol class="space-y-3 text-sm">
            <li class="flex items-start gap-3">
              <span class="size-6 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">1</span>
              <div>
                <p>有効化のポップアップが表示されたら <strong>「有効化」</strong> をタップ</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <span class="size-6 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">2</span>
              <div>
                <p>有効化が完了するまで待つ</p>
                <UBadge class="mt-1.5" color="success" variant="subtle" icon="i-lucide-clock" label="約1分" />
              </div>
            </li>
          </ol>
        </UCard>
      </div>

      <!-- STEP 3 -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          STEP 3 — 回線ラベルと使用回線の設定
        </p>

        <UCard>
          <ol class="space-y-3 text-sm">
            <li class="flex items-start gap-3">
              <span class="size-6 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">1</span>
              <div>
                <p>eSIMの使用場所として <strong>「海外」</strong> を選択</p>
              </div>
            </li>
            <li class="flex items-start gap-3">
              <span class="size-6 rounded-full bg-primary flex items-center justify-center text-xs font-bold text-white flex-shrink-0 mt-0.5">2</span>
              <div>
                <p>料金プランを選択</p>
                <p class="text-xs text-muted mt-0.5">データのみ、または音声＋データ</p>
              </div>
            </li>
          </ol>
        </UCard>
      </div>

      <!-- STEP 4 -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          STEP 4 — インストール確認
        </p>

        <UCard class="border border-success/30 bg-success/5">
          <div class="space-y-2 text-sm">
            <p class="font-bold text-success flex items-center gap-1.5">
              <UIcon name="i-lucide-circle-check" class="size-4" />
              インストール完了チェックリスト
            </p>
            <ul class="space-y-2 mt-3">
              <li class="flex items-start gap-2">
                <UIcon name="i-lucide-check" class="size-4 text-success flex-shrink-0 mt-0.5" />
                <span>正常にインストールされているか確認する</span>
              </li>
              <li class="flex items-start gap-2">
                <UIcon name="i-lucide-check" class="size-4 text-success flex-shrink-0 mt-0.5" />
                <span>確認後、eSIMを <strong>「OFF」</strong> に設定する（韓国到着まで使わない）</span>
              </li>
              <li class="flex items-start gap-2">
                <UIcon name="i-lucide-check" class="size-4 text-success flex-shrink-0 mt-0.5" />
                <span>有効化完了まで最大 <strong>2時間</strong> かかる場合があります</span>
              </li>
            </ul>
          </div>
        </UCard>
      </div>

      <!-- カスタマーサポート -->
      <div class="space-y-3">
        <p class="text-xs font-bold text-muted tracking-widest uppercase">
          カスタマーサポート
        </p>

        <UCard class="text-center">
          <div class="space-y-1">
            <p class="text-xs text-muted">お問い合わせ（韓国語のみ）</p>
            <p class="text-3xl font-bold tracking-wider text-primary">1566-9070</p>
            <p class="text-sm text-muted">平日 09:00 〜 18:00</p>
            <p class="text-xs text-muted">昼休み 12:00〜13:00 を除く</p>
          </div>
        </UCard>
      </div>

      <!-- フッターノート -->
      <p class="text-xs text-center text-muted pb-4">
        ドシラクeSIM公式ガイドを日本語に翻訳したものです。<br>
        最新情報は
        <ULink to="https://dosirakesim.com" target="_blank" class="text-primary">
          dosirakesim.com
        </ULink>
        をご確認ください。
      </p>

    </div>
  </UPageSection>
</template>
