#!/bin/bash
# 홈서버 타이머(jjway-yt-refresh.timer, 매달 1·15일 04:00)가 부름: 갱신 → 영상 파일만 커밋·푸시(다른 작업 중인 파일은 안 건드림) → Vercel 재배포
set -e
cd /home/zzindori/dev/workspace/portfolio/wowhit
python3 scripts/jjway/yt/refresh.py
if git diff --quiet -- public/games/jjway/yt; then echo "바뀐 것 없음"; exit 0; fi
git add public/games/jjway/yt
git commit -q -m "jjWay 영상 데이터 갱신(자동: 유튜브 정보·구글 좌표 30일 갱신)" -- public/games/jjway/yt
git push -q || { git pull -q --rebase --autostash && git push -q; }
echo "올림: $(git log --oneline -1)"
