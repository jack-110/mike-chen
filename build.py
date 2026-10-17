# -*- coding: utf-8 -*-
from pathlib import Path
import html,re,json
from datetime import datetime
ROOT=Path(__file__).parent
OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)
ORIGIN='https://jack-110.github.io'
def esc(s): return html.escape(s,quote=True)
def inline(s):
    s=esc(s)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
def markdown(s):
    result=[]; code=False; buf=[]; listing=False
    for line in s.splitlines()+['']:
        if line.startswith('```'):
            if code:
                raw=esc('\n'.join(buf))
                raw=re.sub(r'\b(public|void|class|new|return|throws)\b',r'<span class="kw">\1</span>',raw)
                raw=re.sub(r'(@\w+)',r'<span class="annotation">\1</span>',raw)
                result.append('<div class="code-label">JAVA</div><pre><code>'+raw+'</code></pre>');buf=[]
            code=not code;continue
        if code: buf.append(line);continue
        if not line.startswith('- ') and listing: result.append('</ul>');listing=False
        if line.startswith('## '): result.append('<h2>'+inline(line[3:])+'</h2>')
        elif line.startswith('> '): result.append('<blockquote>'+inline(line[2:])+'</blockquote>')
        elif line.startswith('- '):
            if not listing: result.append('<ul>');listing=True
            result.append('<li>'+inline(line[2:])+'</li>')
        elif line: result.append('<p>'+inline(line)+'</p>')
    return '\n'.join(result)
def page(title,content,active='posts',description='Mike Chen 的技术笔记，记录 Java、Spring、数据库、分布式系统与 AI Agent 的学习和实践。'):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} · Mike Chen</title><meta name="description" content="{esc(description)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><link rel="alternate" type="application/rss+xml" title="Mike Chen Blog" href="/feed.xml"><script>try{{if(localStorage.theme==='dark'||(!localStorage.theme&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.dataset.theme='dark'}}catch(e){{}}</script><script defer src="/app.js"></script></head><body><a class="skip" href="#main">跳到正文</a><div class="shell"><header><a class="brand" href="/">Mike Chen<span class="brand-dot">.</span></a><nav aria-label="主导航"><a href="/" {'aria-current="page"' if active=='posts' else ''}>文章</a><a href="/about/" {'aria-current="page"' if active=='about' else ''}>关于</a><button class="theme" aria-label="切换深浅色主题" title="切换主题">◐</button></nav></header><main id="main">{content}</main><footer><span>© 2026 Mike Chen</span><div><a href="/feed.xml">RSS ↗</a><span class="footer-note">保持好奇，持续记录。</span></div></footer></div></body></html>'''
import shutil
for asset in ('style.css', 'app.js', 'favicon.svg'):
    if (ROOT/asset).exists(): shutil.copyfile(ROOT/asset, OUT/asset)
posts=[]
for file in sorted(list((ROOT/'content/posts').glob('*.md')) + list(ROOT.glob('spring-*.md')),reverse=True):
    _,front,body=file.read_text().split('---',2)
    meta=dict(line.split(': ',1) for line in front.strip().splitlines())
    meta.update(slug=file.stem,body=body,tags=[t.strip() for t in meta['tags'].split(',')]);posts.append(meta)
posts.sort(key=lambda p:p['date'],reverse=True)
rows=[]
for p in posts:
    tags=' '.join(f'<span>{esc(t)}</span>' for t in p['tags'])
    rows.append(f'<article class="post-row" data-tags="{esc(json.dumps(p["tags"]))}"><time datetime="{p["date"]}">{p["date"][5:].replace("-", " / ")}</time><div><h2><a href="/posts/{p["slug"]}/">{esc(p["title"])}</a></h2><p class="post-sub">{tags}{"<span class=sample>示例文章</span>" if p.get("sample")=="true" else ""}</p></div><a class="row-arrow" tabindex="-1" aria-hidden="true" href="/posts/{p["slug"]}/">↗</a></article>')
filters=''.join(f'<button data-filter="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in sorted({t for p in posts for t in p['tags']}))
home=f'''<section class="intro"><p class="eyebrow">NOTES ON SOFTWARE & BEYOND</p><h1>写代码，也写下思考。</h1><p class="intro-copy">我是 Mike Chen，一名软件工程师。<br>这里记录技术的细节、系统的设计，以及实践中的发现。</p><a class="text-link" href="/about/">关于我 <span>→</span></a></section><section class="posts" aria-labelledby="posts-title"><div class="section-top"><h2 id="posts-title">文章 <span>/ POSTS</span></h2><span class="count">{len(posts):02d} 篇</span></div><div class="filters" role="group" aria-label="按标签筛选"><button class="selected" data-filter="all" aria-pressed="true">全部</button>{filters}</div><div class="year">2026</div>{''.join(rows)}<p id="empty" hidden>这个标签下还没有文章。</p><p class="end-note">慢慢积累，把问题想清楚。</p></section>'''
(OUT/'index.html').write_text(page('文章',home))
about=OUT/'about';about.mkdir(exist_ok=True)
about.joinpath('index.html').write_text(page('关于', '''<section class="about"><p class="eyebrow">A LITTLE ABOUT ME</p><h1>你好，我是 Mike。</h1><div class="prose"><p>我是一名软件工程师。这里记录我对 Java、Spring、数据库、分布式系统与 AI Agent 的学习和实践。</p><h2>关于这个博客</h2><p>有些问题，在写下来的过程中才会变得清楚。我希望把零散的理解整理成笔记，也为下一次遇到相同问题的自己留下一条线索。</p><p>这里会有源码阅读、系统设计，以及使用新工具时的观察。</p><h2>持续记录</h2><p>文章以中文为主，也会尝试用英文表达。你可以通过 RSS 订阅后续更新。</p><a class="text-link" href="/feed.xml">订阅 RSS ↗</a></div><a class="back" href="/">← 回到文章列表</a></section>''','about'))
for p in posts:
    folder=OUT/'posts'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
    content=f'''<article class="article"><a class="back" href="/">← 所有文章</a><div class="article-meta"><time>{p['date']}</time><span>{esc(" / ".join(p["tags"]))}</span>{"<span>示例文章</span>" if p.get("sample")=="true" else ""}</div><h1>{esc(p['title'])}</h1>{"<aside class=notice>排版示例 · 本文用于展示阅读体验，非正式发布内容。</aside>" if p.get('sample')=='true' else ''}<div class="prose">{markdown(p['body'])}</div><div class="article-end">— Mike Chen</div><a class="back" href="/">← 回到文章列表</a></article>'''
    folder.joinpath('index.html').write_text(page(p['title'],content))
items=''.join(f'<item><title>{esc(p["title"])}</title><link>{ORIGIN}/posts/{p["slug"]}/</link><guid>{ORIGIN}/posts/{p["slug"]}/</guid><description>排版示例，非正式发布内容。</description><pubDate>{datetime.strptime(p["date"],"%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate></item>' for p in posts)
(OUT/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mike Chen Blog</title><link>{ORIGIN}</link><description>软件、系统与思考</description><language>zh-cn</language>{items}</channel></rss>')
(OUT/'404.html').write_text(page('页面未找到','<section class="intro"><p class="eyebrow">404</p><h1>这一页还没有写下。</h1><a class="text-link" href="/">回到文章列表 →</a></section>'))
print(f'Built {len(posts)} Markdown post(s), About, RSS and 404.')
