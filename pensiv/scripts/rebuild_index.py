#!/usr/bin/env python3
"""Rebuild the pensiv index page from the entry folders on disk.

    python3 rebuild_index.py [--root DIR]

Every entry folder holds a meta.json, so the index is derived entirely from
disk. Entries added, edited or deleted by hand are picked up on the next run.
Standard library only.
"""

import argparse
import html
import json
import os
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_ROOT = Path.home() / "dev" / "pensiv"


def resolve_root(explicit=None):
    """--root beats $PENSIV_ROOT beats ~/dev/pensiv."""
    if explicit:
        return Path(explicit).expanduser().resolve()
    env = os.environ.get("PENSIV_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_ROOT


def load_entries(root):
    entries = []
    for meta_path in sorted(root.glob("*/meta.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"건너뜀 {meta_path}: {exc}")
            continue
        meta["dir"] = meta_path.parent.name
        if not (meta_path.parent / meta.get("file", "index.html")).exists():
            meta["missing"] = True
        entries.append(meta)
    entries.sort(key=lambda m: (m.get("date", ""), m.get("dir", "")), reverse=True)
    return entries


CSS = """
:root {
  --bg: #f1f3f5;
  --surface: #ffffff;
  --ink: #1b2026;
  --ink-soft: #596573;
  --ink-faint: #8b96a3;
  --rule: #dde2e8;
  --accent: #41688f;
  --accent-soft: #e6edf4;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #12161a;
    --surface: #1a2026;
    --ink: #e4e9ee;
    --ink-soft: #9aa7b4;
    --ink-faint: #6b7784;
    --rule: #28313a;
    --accent: #7fa6c9;
    --accent-soft: #1e2831;
    color-scheme: dark;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 400 16px/1.7 -apple-system, "Apple SD Gothic Neo", "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
}
.wrap {
  max-width: 54rem;
  margin: 0 auto;
  padding: 3rem 1.25rem 5rem;
}
header { margin-bottom: 2.5rem; }
h1 {
  margin: 0 0 .4rem;
  font-size: 1.9rem;
  letter-spacing: -.02em;
}
.sub { margin: 0; color: var(--ink-soft); font-size: .95rem; }
.filter {
  margin-top: 1.5rem;
  width: 100%;
  padding: .6rem .85rem;
  font: inherit;
  font-size: .95rem;
  color: var(--ink);
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 6px;
}
.filter:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
.year {
  margin: 2.5rem 0 .75rem;
  font: 500 .72rem/1 ui-monospace, Menlo, monospace;
  letter-spacing: .14em;
  color: var(--accent);
}
ul.entries { list-style: none; margin: 0; padding: 0; }
li.entry {
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: 1rem 1.1rem;
  margin-bottom: .6rem;
}
li.entry.missing { opacity: .55; }
.row { display: flex; flex-wrap: wrap; align-items: baseline; gap: .5rem .9rem; }
time {
  font: 400 .78rem ui-monospace, Menlo, monospace;
  color: var(--ink-faint);
  font-variant-numeric: tabular-nums;
}
a.title {
  font-size: 1.02rem;
  font-weight: 600;
  color: var(--ink);
  text-decoration: none;
  min-width: 0;
}
a.title:hover { color: var(--accent); text-decoration: underline; }
p.note { margin: .45rem 0 0; color: var(--ink-soft); font-size: .92rem; }
.meta { margin-top: .55rem; display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; }
.tag {
  font: 400 .72rem ui-monospace, Menlo, monospace;
  padding: .1rem .45rem;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent);
}
a.source {
  font-size: .78rem;
  color: var(--ink-faint);
  text-decoration: none;
  border-bottom: 1px dotted currentColor;
}
a.source:hover { color: var(--accent); }
.gone { font: 400 .72rem ui-monospace, Menlo, monospace; color: #c0563c; }
.offline {
  font: 400 .72rem ui-monospace, Menlo, monospace;
  padding: .1rem .45rem;
  border-radius: 999px;
  border: 1px solid var(--rule);
  color: var(--ink-faint);
  cursor: help;
}
.empty {
  background: var(--surface);
  border: 1px dashed var(--rule);
  border-radius: 6px;
  padding: 2.5rem 1.25rem;
  text-align: center;
  color: var(--ink-soft);
}
footer {
  margin-top: 3rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--rule);
  font: 400 .76rem ui-monospace, Menlo, monospace;
  color: var(--ink-faint);
}
#noresult { display: none; }
"""

JS = """
var box = document.getElementById('filter');
if (box) {
  box.addEventListener('input', function () {
    var q = this.value.trim().toLowerCase();
    var shown = 0;
    document.querySelectorAll('li.entry').forEach(function (li) {
      var hit = !q || li.dataset.search.indexOf(q) !== -1;
      li.hidden = !hit;
      if (hit) shown++;
    });
    document.querySelectorAll('.year').forEach(function (h) {
      var any = false, n = h.nextElementSibling;
      if (n) n.querySelectorAll('li.entry').forEach(function (li) { if (!li.hidden) any = true; });
      h.hidden = !any;
      if (n) n.hidden = !any;
    });
    document.getElementById('noresult').style.display = shown ? 'none' : 'block';
  });
}
"""


def link_host(url):
    """Label an outbound link by where it actually goes."""
    try:
        host = urlparse(url).netloc
    except ValueError:
        host = ""
    return host or "링크"


def render_entry(e):
    esc = html.escape
    folder = esc(e["dir"])
    fname = esc(e.get("file", "index.html"))
    title = esc(e.get("title") or e["dir"])
    date_s = esc(e.get("date", ""))
    note = e.get("note") or ""
    tags = e.get("tags") or []
    source = e.get("source") or ""
    searchable = " ".join([e.get("title", ""), note, " ".join(tags), date_s]).lower()

    out = ['<li class="entry%s" data-search="%s">' % (
        " missing" if e.get("missing") else "", esc(searchable))]
    out.append('<div class="row">')
    out.append('<time>%s</time>' % date_s)
    out.append('<a class="title" href="%s/%s">%s</a>' % (folder, fname, title))
    if e.get("missing"):
        out.append('<span class="gone">파일 없음</span>')
    out.append('</div>')
    if note:
        out.append('<p class="note">%s</p>' % esc(note))
    hosts = e.get("remote_hosts") or []
    if tags or source or hosts:
        out.append('<div class="meta">')
        for t in tags:
            out.append('<span class="tag">%s</span>' % esc(t))
        if source:
            out.append('<a class="source" href="%s" target="_blank" rel="noopener">\u2197 %s</a>'
                       % (esc(source), esc(link_host(source))))
        if hosts:
            out.append('<span class="offline" title="%s">외부 리소스</span>'
                       % esc(", ".join(hosts)))
        out.append('</div>')
    out.append('</li>')
    return "".join(out)


def render_index(entries, root):
    esc = html.escape
    parts = [
        '<!doctype html>',
        '<html lang="ko"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>펜시브</title>',
        '<style>%s</style></head><body><div class="wrap">' % CSS,
        '<header><h1>펜시브</h1>',
        '<p class="sub">꺼내서 담아둔 것 %d개 · %s</p>' % (len(entries), esc(str(root))),
    ]
    if entries:
        parts.append('<input id="filter" class="filter" type="search" '
                     'placeholder="제목, 메모, 태그로 거르기" autocomplete="off">')
    parts.append('</header>')

    if not entries:
        parts.append('<p class="empty">아직 비어 있다.<br>'
                     'store_entry.py 로 HTML 하나 넣으면 여기에 쌓인다.</p>')
    else:
        current_year = None
        open_list = False
        for e in entries:
            year = (e.get("date") or "????")[:4]
            if year != current_year:
                if open_list:
                    parts.append('</ul>')
                parts.append('<h2 class="year">%s</h2><ul class="entries">' % esc(year))
                current_year = year
                open_list = True
            parts.append(render_entry(e))
        if open_list:
            parts.append('</ul>')
        parts.append('<p class="empty" id="noresult">걸리는 게 없다.</p>')

    parts.append('</div><script>%s</script></body></html>' % JS)
    return "\n".join(parts)


def rebuild(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    entries = load_entries(root)
    index = root / "index.html"
    index.write_text(render_index(entries, root), encoding="utf-8")
    return index, len(entries)


def main():
    ap = argparse.ArgumentParser(description="pensiv 색인을 다시 만든다")
    ap.add_argument("--root", help="펜시브 루트 (기본: $PENSIV_ROOT 또는 ~/dev/pensiv)")
    args = ap.parse_args()
    root = resolve_root(args.root)
    index, n = rebuild(root)
    print(f"색인 갱신: {index} ({n}개)")


if __name__ == "__main__":
    main()
