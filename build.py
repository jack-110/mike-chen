# -*- coding: utf-8 -*-
from pathlib import Path
import html,re,json
from datetime import datetime
ROOT=Path(__file__).parent
OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)
ORIGIN='https://jack-110.github.io/mike-chen'
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
def page(title,content,active='posts',description='Notes on Java, Spring, databases, distributed systems, and AI agents by Mike Chen.'):
    result = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} · Mike Chen</title><meta name="description" content="{esc(description)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><link rel="alternate" type="application/rss+xml" title="Mike Chen Blog" href="/feed.xml"><script>try{{if(localStorage.theme==='dark'||(!localStorage.theme&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.dataset.theme='dark'}}catch(e){{}}</script><script defer src="/app.js"></script></head><body><a class="skip" href="#main">Skip to content</a><div class="shell"><header><a class="brand" href="/">Mike Chen<span class="brand-dot">.</span></a><nav aria-label="Main navigation"><a href="/" {'aria-current="page"' if active=='posts' else ''}>Writing</a><a href="/about/" {'aria-current="page"' if active=='about' else ''}>About</a><button class="theme" aria-label="Toggle color theme" title="Toggle theme">◐</button></nav></header><main id="main">{content}</main><footer><span>© 2026 Mike Chen</span><div><a href="/feed.xml">RSS ↗</a><span class="footer-note">Stay curious. Keep writing.</span></div></footer></div></body></html>'''
    return result.replace('href="/', 'href="/mike-chen/').replace('src="/', 'src="/mike-chen/')
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
    rows.append(f'<article class="post-row" data-tags="{esc(json.dumps(p["tags"]))}"><time datetime="{p["date"]}">{p["date"][5:].replace("-", " / ")}</time><div><h2><a href="/posts/{p["slug"]}/">{esc(p["title"])}</a></h2><p class="post-sub">{tags}{"<span class=sample>Sample post</span>" if p.get("sample")=="true" else ""}</p></div><a class="row-arrow" tabindex="-1" aria-hidden="true" href="/posts/{p["slug"]}/">↗</a></article>')
filters=''.join(f'<button data-filter="{esc(t)}" aria-pressed="false">{esc(t)}</button>' for t in sorted({t for p in posts for t in p['tags']}))
home=f'''<section class="posts" style="padding-top:56px" aria-labelledby="posts-title"><div class="section-top"><h2 id="posts-title">Writing <span>/ NOTES</span></h2><span class="count">{len(posts):02d} posts</span></div><div class="filters" role="group" aria-label="Filter posts by tag"><button class="selected" data-filter="all" aria-pressed="true">All</button>{filters}</div><div class="year">2026</div>{''.join(rows)}<p id="empty" hidden>No posts with this tag yet.</p><p class="end-note">One note at a time. One idea a little clearer.</p></section>'''
(OUT/'index.html').write_text(page('Writing',home))
about=OUT/'about';about.mkdir(exist_ok=True)
about.joinpath('index.html').write_text(page('About', '''<section class="about"><p class="eyebrow">A LITTLE ABOUT ME</p><h1>Hi, I’m Mike.</h1><div class="prose"><p>I’m a software engineer. I write about what I’m learning and building with Java, Spring, databases, distributed systems, and AI agents.</p><h2>About this blog</h2><p>Some ideas only become clear when I write them down. This blog is a place to connect scattered observations and leave a trail for the next time I face the same problem.</p><p>Expect source code walkthroughs, notes on system design, and observations from trying new tools.</p><h2>Keep writing</h2><p>I write in English. Subscribe via RSS to follow along as new notes are published.</p><a class="text-link" href="/feed.xml">Subscribe via RSS ↗</a></div><a class="back" href="/">← Back to all posts</a></section>''','about'))
for p in posts:
    folder=OUT/'posts'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
    content=f'''<article class="article"><a class="back" href="/">← All posts</a><div class="article-meta"><time>{p['date']}</time><span>{esc(" / ".join(p["tags"]))}</span>{"<span>Sample post</span>" if p.get("sample")=="true" else ""}</div><h1>{esc(p['title'])}</h1>{"<aside class=notice>Sample post · A demonstration of the reading experience, not a published technical article.</aside>" if p.get('sample')=='true' else ''}<div class="prose">{markdown(p['body'])}</div><div class="article-end">— Mike Chen</div><a class="back" href="/">← Back to all posts</a></article>'''
    folder.joinpath('index.html').write_text(page(p['title'],content))
items=''.join(f'<item><title>{esc(p["title"])}</title><link>{ORIGIN}/posts/{p["slug"]}/</link><guid>{ORIGIN}/posts/{p["slug"]}/</guid><description>A sample post demonstrating the blog layout.</description><pubDate>{datetime.strptime(p["date"],"%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate></item>' for p in posts)
(OUT/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mike Chen Blog</title><link>{ORIGIN}</link><description>Software, systems, and ideas</description><language>en</language>{items}</channel></rss>')
(OUT/'404.html').write_text(page('Page not found','<section class="intro"><p class="eyebrow">404</p><h1>This page hasn’t been written yet.</h1><a class="text-link" href="/">Back to all posts →</a></section>'))
print(f'Built {len(posts)} Markdown post(s), About, RSS and 404.')
