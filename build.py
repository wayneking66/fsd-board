#!/usr/bin/env python3
"""Regenerate index.html (the F.S.D 公佈欄 home page) from notices.json.

Usage:  python3 build.py [BASE_URL]
BASE_URL (optional, e.g. https://example.github.io/fsd-board) is used for absolute
og:url values. Only the Python standard library is needed.
"""
import json, html, sys, pathlib

ROOT = pathlib.Path(__file__).parent
BASE = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")
items = json.loads((ROOT / "notices.json").read_text(encoding="utf-8"))
items.sort(key=lambda n: (n["date"], n.get("posted", "")), reverse=True)
cats = []
for n in items:
    if n["category"] not in cats:
        cats.append(n["category"])

def esc(s): return html.escape(s, quote=True)

cards = "\n".join(f'''    <a class="item" href="{esc(n["url"])}" data-cat="{esc(n["category"])}" data-date="{esc(n["date"])}">
      <div class="row"><span class="cat {esc(n["category"])}">{esc(n["category"])}</span><time datetime="{esc(n["date"])}">{esc(n.get("display_date") or n["date"])}</time></div>
      <h2>{esc(n["title"])}</h2>
      <p>{esc(n["summary"])}</p>
      <span class="more">查看詳情 ›</span>
    </a>''' for n in items)
buttons = "".join(f'<button type="button" data-f="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in cats)
og_url = f'<meta property="og:url" content="{esc(BASE)}/">' if BASE else ""
desc = "Defly逆飛輪 的行前通知與活動公告，最新消息都在這裡。"

page = f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>F.S.D 公佈欄</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FFD60A">
<meta property="og:type" content="website">
<meta property="og:site_name" content="F.S.D 公佈欄">
<meta property="og:title" content="F.S.D 公佈欄">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="zh_TW">
{og_url}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
</head>
<body style="padding-bottom:24px">
<main class="wrap">
  <header class="home-hero">
    <span class="eyebrow">Defly逆飛輪</span>
    <h1>F.S.D 公佈欄</h1>
    <p>行前通知・活動公告，最新消息都在這裡 🛼</p>
  </header>
  <nav class="filters" aria-label="分類篩選"><button type="button" data-f="" aria-pressed="true">全部</button>{buttons}</nav>
  <div class="list" id="list">
{cards}
  </div>
  <p class="empty" id="empty" hidden>這個分類目前沒有公告</p>
  <footer>F.S.D 公佈欄・Defly逆飛輪</footer>
</main>
<script>
(function(){{
  var today=new Date(), t=today.getFullYear()+'-'+('0'+(today.getMonth()+1)).slice(-2)+'-'+('0'+today.getDate()).slice(-2);
  var items=[].slice.call(document.querySelectorAll('.item'));
  items.forEach(function(a){{ var d=a.getAttribute('data-date');
    if(d<t) a.classList.add('past');
    else if(items.indexOf(a)===items.filter(function(x){{return x.getAttribute('data-date')>=t}}).length-1){{
      var s=document.createElement('span'); s.className='new'; s.textContent='即將到來'; a.querySelector('.row').appendChild(s);}}
  }});
  var btns=[].slice.call(document.querySelectorAll('.filters button'));
  btns.forEach(function(b){{ b.addEventListener('click',function(){{
    var f=b.getAttribute('data-f'), n=0;
    btns.forEach(function(x){{x.setAttribute('aria-pressed', x===b?'true':'false')}});
    items.forEach(function(a){{ var show=!f||a.getAttribute('data-cat')===f; a.hidden=!show; if(show)n++; }});
    document.getElementById('empty').hidden=n>0;
  }}); }});
}})();
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(page, encoding="utf-8")

# Fill absolute og:url into each notice page (marker <!--OG_ABS--> or existing tag)
if BASE:
    import re
    for n in items:
        p = ROOT / n["url"]
        if not p.exists(): continue
        s = p.read_text(encoding="utf-8")
        tag = f'<meta property="og:url" content="{esc(BASE)}/{esc(n["url"])}"><!--OG_ABS-->'
        s = re.sub(r'(<meta property="og:url"[^>]*>)?<!--OG_ABS-->', tag, s, count=1)
        p.write_text(s, encoding="utf-8")
print(f"index.html rebuilt with {len(items)} notice(s)")
