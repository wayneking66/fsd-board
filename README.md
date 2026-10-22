# F.S.D 公佈欄

F.S.D平花班 的行前通知／活動公告網站（純靜態、手機優先、無框架）。

```
index.html                 首頁（由 build.py 依 notices.json 產生，請勿手改）
notices.json               公告清單（首頁卡片資料）
notices/*.html             每則公告一頁
templates/notice-template.html  新公告範本（複製後修改）
assets/style.css           共用樣式（黃色主題）
build.py                   重建首頁：python3 build.py [網站網址]
deploy-github-pages.sh     第一次發布到 GitHub Pages
```

## 新增一則公告（約 5 分鐘）

1. 複製範本：`cp templates/notice-template.html notices/2026-12-20-xxx.html`
   （檔名建議 `YYYY-MM-DD-英文代稱.html`）
2. 修改新檔案內容：`<title>`、`og:title`、`og:description`、`description`，以及頁面各區塊
   （不需要的區塊，例如交通管制、賽程，可整段刪除；「本隊有選手」的項目在 `<li>` 加 `class="on"`）。
3. 在 `notices.json` 加一筆：
   ```json
   {
     "date": "2026-12-20",
     "display_date": "12/20（日）",
     "category": "活動",
     "title": "標題",
     "summary": "一句話摘要",
     "url": "notices/2026-12-20-xxx.html",
     "posted": "2026-12-01"
   }
   ```
   （選填）封面照片：再加 `"image": "assets/xxx.jpg"`、`"image_caption": "圖說"`、`"image_credit": "照片來源：…"`、`"image_credit_url": "https://…"`。
   build.py 會把照片放進公告頁的 `<!--BANNER--><!--/BANNER-->` 位置（範本已有），首頁卡片也會顯示縮圖。照片請先縮到約 1600px 寬、350 KB 以下。
   分類 `category` 可用：比賽、活動、公告（有對應顏色；其他文字也可，會用黃色）。首頁自動依日期新→舊排序，
   已過日期的會變淡，最近一則未來公告會標「即將到來」。
4. 重建首頁並發布：
   ```bash
   python3 build.py https://<帳號>.github.io/fsd-board
   git add -A && git commit -m "新增公告" && git push
   ```
   GitHub Pages 約 1 分鐘後更新。

## 第一次發布
`gh auth login` 後執行 `./deploy-github-pages.sh`（建立公開 repo `fsd-board` 並開啟 Pages）。

## 圖片資源
- `assets/logo.png`（透明背景原尺寸）、`assets/logo-512.png`、`assets/logo-192.png`（頁首用）
- `favicon.ico`、`assets/favicon-32.png`、`assets/apple-touch-icon.png`
- `assets/team.jpg` 首頁團體照；`assets/og.jpg` LINE／社群分享預覽圖（1200×630）
- 新公告頁沿用範本中的 `og:image`（`../assets/og.jpg`）；執行 `python3 build.py <網址>` 會自動改成絕對網址（LINE 需要）。
