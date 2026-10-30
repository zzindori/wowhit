// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  // Your custom configs here
  // 게임 학습 확인 스크립트(public/games의 core.js를 그대로 읽어 돌림)는 게임 코드와 같은 모양으로 둠
  { ignores: ['scripts/ai-gp/**'] }
)
