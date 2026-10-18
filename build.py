# -*- coding: utf-8 -*-
from pathlib import Path
import html,re,json
from datetime import datetime
ROOT=Path(__file__).parent
OUT=ROOT/'dist'; OUT.mkdir(exist_ok=True)
ORIGIN='https://jack-110.github.io/mike-chen'
CATEGORIES=('Tech', 'Course', 'Reading')
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
    result = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} · Mike Chen's Blog</title><meta name="description" content="{esc(description)}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css?v=categories-2"><link rel="alternate" type="application/rss+xml" title="Mike Chen's Blog" href="/feed.xml"><script src="/app.js?v=categories-1" defer></script></head><body><a class="skip" href="#main">Skip to content</a><section class="top"><header><h1><a href="/">Mike Chen's Blog</a></h1></header><nav aria-label="Main navigation"><ul><li><a href="/about/">About</a></li></ul></nav></section><main class="content" id="main">{content}</main></body></html>'''
    return result.replace('href="/', 'href="/mike-chen/').replace('src="/', 'src="/mike-chen/')
import shutil
for asset in ('style.css', 'app.js', 'favicon.svg'):
    if (ROOT/asset).exists(): shutil.copyfile(ROOT/asset, OUT/asset)
posts=[]
for file in sorted(list((ROOT/'content/posts').glob('*.md')) + list(ROOT.glob('spring-*.md')),reverse=True):
    _,front,body=file.read_text().split('---',2)
    meta=dict(line.split(': ',1) for line in front.strip().splitlines())
    category=meta.get('category', 'Tech').strip().title()
    if category not in CATEGORIES:
        raise ValueError(f'{file}: category must be Tech, Course, or Reading')
    meta['category']=category
    meta.update(slug=file.stem,body=body,tags=[t.strip() for t in meta['tags'].split(',')]);posts.append(meta)
posts.sort(key=lambda p:p['date'],reverse=True)
rows=[]
for p in posts:
    date=datetime.strptime(p['date'], '%Y-%m-%d').strftime('%b %d, %Y').replace(' 0', ' ')
    rows.append(f'''<li class="post-row" data-category="{esc(p['category'])}"><div><span class="post-category">{esc(p['category'])}</span><h3><a class="post-link" href="/posts/{esc(p['slug'])}/">{esc(p['title'])}</a></h3></div><time class="post-meta" datetime="{esc(p['date'])}">{date}</time></li>''')
filters=''.join(f'''<button type="button" class="category-filter" data-filter="{category}" aria-pressed="{str(category == 'All').lower()}" aria-controls="post-list">{category}<span class="category-count">{len(posts) if category == 'All' else sum(p['category'] == category for p in posts):02d}</span></button>''' for category in ('All', *CATEGORIES))
home=f'''<div class="home"><div class="category-filters" role="group" aria-label="Filter posts by category" hidden>{filters}</div><div class="post-list-header"><h2 class="post-list-heading">Latest notes</h2><span class="post-count" role="status" aria-live="polite">{len(posts)} {'post' if len(posts) == 1 else 'posts'}</span></div><ul class="post-list" id="post-list">{''.join(rows)}</ul><p class="empty-posts" id="empty-posts" hidden>No posts in this category yet. Check back soon.</p><p class="rss-subscribe">subscribe <a href="/feed.xml">via RSS</a></p></div>'''
(OUT/'index.html').write_text(page('Posts',home))
about=OUT/'about';about.mkdir(exist_ok=True)
about.joinpath('index.html').write_text(page('About', '''<section class="about"><p class="eyebrow">A LITTLE ABOUT ME</p><h1>Hi, I’m Mike.</h1><div class="prose"><p>I’m a software engineer at the GOTO company, with a focus on the lending business. I write about what I’m learning and building with Java, Spring, databases, distributed systems, and AI agents.</p><h2>About this blog</h2><p>Some ideas only become clear when I write them down. This blog is a place to connect scattered observations and leave a trail for the next time I face the same problem.</p><p>Expect source code walkthroughs, notes on system design, and observations from trying new tools.</p><p>Find me on <a href="https://x.com/C0x68en">X</a>, <a href="https://github.com/jack-110">GitHub</a>, and <a href="https://www.linkedin.com/in/c0x68en/">LinkedIn</a>.</p></div></section>''','about'))
for p in posts:
    folder=OUT/'posts'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
    content=f'''<article class="article"><a class="back" href="/">← All posts</a><div class="article-meta"><time>{p['date']}</time><span>{esc(" / ".join(p["tags"]))}</span>{"<span>Sample post</span>" if p.get("sample")=="true" else ""}</div><h1>{esc(p['title'])}</h1><div class="prose">{markdown(p['body'])}</div><div class="article-end">— Mike Chen</div><a class="back" href="/">← Back to all posts</a></article>'''
    folder.joinpath('index.html').write_text(page(p['title'],content))
items=''.join(f'<item><title>{esc(p["title"])}</title><link>{ORIGIN}/posts/{p["slug"]}/</link><guid>{ORIGIN}/posts/{p["slug"]}/</guid><description>A sample post demonstrating the blog layout.</description><pubDate>{datetime.strptime(p["date"],"%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")}</pubDate></item>' for p in posts)
(OUT/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mike Chen Blog</title><link>{ORIGIN}</link><description>Software, systems, and ideas</description><language>en</language>{items}</channel></rss>')
(OUT/'404.html').write_text(page('Page not found','<section class="intro"><p class="eyebrow">404</p><h1>This page hasn’t been written yet.</h1><a class="text-link" href="/">Back to all posts →</a></section>'))
print(f'Built {len(posts)} Markdown post(s), About, RSS and 404.')
