#!/usr/bin/env bash
# One-time setup: publish this folder to GitHub Pages.
# Requires: gh authenticated (gh auth login) with repo scope.
# Usage: ./deploy-github-pages.sh [repo-name]   (default: fsd-board)
set -euo pipefail
cd "$(dirname "$0")"
REPO="${1:-fsd-board}"
OWNER="$(gh api user -q .login)"
BASE="https://${OWNER}.github.io/${REPO}"
python3 build.py "$BASE"
[ -d .git ] || git init -b main
git add -A && git commit -qm "Update F.S.D 公佈欄" || true
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  git push -u origin main
fi
gh api -X POST "repos/$OWNER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 || true
echo "Home:   $BASE/"
echo "Notice: $BASE/notices/2026-11-01-zhongzheng-cup.html"
