#!/usr/bin/env python3
"""File an HTML deliverable into the pensiv archive and refresh the index.

    python3 store_entry.py <html-file> [--title T] [--slug S] [--date YYYY-MM-DD]
                           [--tags a,b] [--source-url URL] [--note TEXT]
                           [--asset PATH ...] [--new] [--raw] [--root DIR]

Each entry becomes one folder, `<root>/<date>-<slug>/`, holding the page as
index.html plus a meta.json the index is rebuilt from.

The page is normalised on the way in so that it opens on its own from disk: a
fragment (an artifact-authored page with no <html> or <head>) is wrapped in a
document skeleton, and a document with no charset gets one. The untouched file
is kept beside it as original.html whenever normalising changed anything.
Re-filing the same date and slug updates that entry in place unless --new.
Standard library only.
"""

import argparse
import html as html_mod
import json
import re
import shutil
import sys
from datetime import date as date_cls
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rebuild_index import rebuild, resolve_root  # noqa: E402

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
SLUG_KEEP = re.compile(r"[^0-9A-Za-z가-힣._-]+")
HTML_TAG_RE = re.compile(r"<html\b[^>]*>", re.IGNORECASE)
HEAD_TAG_RE = re.compile(r"<head\b[^>]*>", re.IGNORECASE)
CHARSET_RE = re.compile(r"<meta[^>]+charset", re.IGNORECASE)
REMOTE_RE = re.compile(
    r"<(?:link|script|img|iframe|source|video|audio|embed)\b[^>]*?"
    r"\b(?:src|href)\s*=\s*[\"'](https?://[^\"'/]+)",
    re.IGNORECASE,
)

# Mirrors the base styles an artifact page is published with, so a page
# authored as a fragment looks the same in the archive as it did on the web.
SKELETON_HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root {
  color-scheme: light;
  padding-top: env(safe-area-inset-top, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
body { margin: 0; font: 14px -apple-system, "Apple SD Gothic Neo", system-ui, sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
</style>
</head>
<body>
"""
SKELETON_TAIL = "\n</body>\n</html>\n"

CHARSET_META = '\n<meta charset="utf-8">'


def slugify(text, fallback="entry"):
    s = SLUG_KEEP.sub("-", (text or "").strip())
    s = re.sub(r"-{2,}", "-", s).strip("-._")
    # Latin stays lowercase for predictable paths; Hangul is left as typed.
    s = "".join(c.lower() if c.isascii() else c for c in s)
    return s[:60] or fallback


def extract_title(html_text):
    m = TITLE_RE.search(html_text[:8192])
    if not m:
        return None
    title = html_mod.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
    return title or None


def normalize(text):
    """Make the page a standalone document. Returns (html, what_changed)."""
    m_html = HTML_TAG_RE.search(text)
    if not m_html:
        return SKELETON_HEAD + text + SKELETON_TAIL, "wrapped"
    if CHARSET_RE.search(text[:4096]):
        return text, None
    m_head = HEAD_TAG_RE.search(text)
    at = m_head.end() if m_head else m_html.end()
    return text[:at] + CHARSET_META + text[at:], "charset"


def remote_hosts(text):
    return sorted({m.group(1).lower() for m in REMOTE_RE.finditer(text)})


def pick_folder(root, stem, allow_update):
    target = root / stem
    if not target.exists():
        return target, "created"
    if allow_update:
        return target, "updated"
    n = 2
    while (root / f"{stem}-{n}").exists():
        n += 1
    return root / f"{stem}-{n}", "created"


def main():
    ap = argparse.ArgumentParser(description="HTML 하나를 펜시브에 담는다")
    ap.add_argument("source", help="담을 HTML 파일")
    ap.add_argument("--root", help="펜시브 루트 (기본: $PENSIV_ROOT 또는 ~/dev/pensiv)")
    ap.add_argument("--title", help="제목 (기본: HTML의 <title>, 없으면 파일명)")
    ap.add_argument("--slug", help="폴더 이름에 쓸 슬러그 (기본: 파일명)")
    ap.add_argument("--date", help="YYYY-MM-DD (기본: 오늘)")
    ap.add_argument("--tags", default="", help="쉼표로 구분한 태그")
    ap.add_argument("--source-url", dest="source_url", default="",
                    help="같은 내용이 올라가 있는 곳. 아티팩트 URL, 위키, 티켓")
    ap.add_argument("--note", default="", help="한 줄 메모. 나중의 내가 읽을 것")
    ap.add_argument("--asset", action="append", default=[],
                    help="같이 복사할 파일 (이미지, css 등). 여러 번 쓸 수 있다")
    ap.add_argument("--new", action="store_true",
                    help="같은 이름이 있어도 덮어쓰지 않고 새 항목으로 만든다")
    ap.add_argument("--raw", action="store_true",
                    help="문서로 감싸지 않고 원본 바이트 그대로 담는다")
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"없는 파일: {src}")
    if src.suffix.lower() not in (".html", ".htm"):
        sys.exit(f"HTML 파일이 아니다: {src.name}")

    text = src.read_text(encoding="utf-8", errors="replace")
    title = args.title or extract_title(text) or src.stem

    if args.date:
        try:
            day = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            sys.exit(f"날짜 형식이 YYYY-MM-DD가 아니다: {args.date}")
    else:
        day = date_cls.today()

    slug = slugify(args.slug or src.stem, fallback="entry")
    root = resolve_root(args.root)
    root.mkdir(parents=True, exist_ok=True)

    target, action = pick_folder(root, f"{day.isoformat()}-{slug}", allow_update=not args.new)
    target.mkdir(parents=True, exist_ok=True)

    if args.raw:
        page, changed = text, None
    else:
        page, changed = normalize(text)

    (target / "index.html").write_text(page, encoding="utf-8")

    original = target / "original.html"
    if changed:
        shutil.copy2(src, original)
    elif original.exists():
        original.unlink()

    copied = []
    for a in args.asset:
        ap_path = Path(a).expanduser().resolve()
        if not ap_path.exists():
            print(f"에셋 없음, 건너뜀: {ap_path}")
            continue
        dest = target / ap_path.name
        if ap_path.is_dir():
            shutil.copytree(ap_path, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(ap_path, dest)
        copied.append(ap_path.name)

    hosts = remote_hosts(page)

    meta_path = target / "meta.json"
    created = day.isoformat()
    if meta_path.exists():
        try:
            created = json.loads(meta_path.read_text(encoding="utf-8")).get("created", created)
        except (OSError, json.JSONDecodeError):
            pass

    meta = {
        "title": title,
        "date": day.isoformat(),
        "created": created,
        "updated": datetime.now().isoformat(timespec="seconds"),
        "file": "index.html",
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "source": args.source_url,
        "note": args.note,
        "origin": str(src),
        "assets": copied,
        "normalized": changed,
        "remote_hosts": hosts,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index, n = rebuild(root)
    print(f"{action}: {target}")
    if changed == "wrapped":
        print("조각 HTML이라 문서로 감쌌다 (doctype, charset, body). 원본은 original.html")
    elif changed == "charset":
        print("charset이 없어서 넣었다. 원본은 original.html")
    if copied:
        print(f"에셋 {len(copied)}개 복사: {', '.join(copied)}")
    if hosts:
        print(f"주의: 외부 리소스를 부른다 ({', '.join(hosts)}). 오프라인에서는 그 부분이 빠진다")
    print(f"색인: {index} ({n}개)")


if __name__ == "__main__":
    main()
