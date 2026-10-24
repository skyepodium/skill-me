---
name: pensiv
description: File a finished HTML page into the local pensiv archive (~/dev/pensiv) with a title, date, tags and a one-line note, then rebuild the browsable index. Use for "펜시브에 저장해", "펜시브에 넣어줘", "pensiv", or any request to keep, archive or file an HTML report, visual or write-up so it can be found again later. Also covers the personal Confluence wiki upload that follows it, when one is configured.
---

# Pensiv

A pensiv entry is not a backup. It is a memory pulled out and set down so a later
reader — almost always the same person, months on — can find it and know what it
was. The HTML is the easy part. The title, the note and the tags are what make the
archive worth having, so they get the attention.

The archive lives at `~/dev/pensiv` unless `$PENSIV_ROOT` or `--root` says otherwise.
One entry is one folder: `<root>/<date>-<slug>/index.html` plus a `meta.json`.
`<root>/index.html` is generated from those meta files and is how the archive is read.

## 1. Settle what is being filed

Find the local `.html` file. If the page was produced earlier in this session, use that
file. If it exists only as a published Artifact or a URL, save the source HTML to disk
first — a link is a `--source-url` on the entry, never a substitute for the file, because
the point of the archive is that it still opens when the link does not. Once filed, the
copy in the archive is the original; the URL is just another place the same thing sits.

A page authored as an artifact is a fragment — no `<!doctype>`, no `<head>`, no charset,
because the publisher adds those. It renders on the web and breaks when opened as a file.
Step 3 repairs that; do not hand-edit the fragment to fix it yourself.

Never file a page you have not read. The note in step 2 cannot be written without it.

**Done when:** one readable local `.html` path is in hand.

## 2. Write the note before filing

- **Title** — the page's own `<title>` is the default and is usually right. Override it
  only when it would not identify the page in a list of fifty.
- **Note** — one line, in the user's own register: what this is and why it was made.
  Write what the filename does not already say. "스택챈 로드맵" is not a note; "보름
  대기 동안 뭘 할지 정한 것 + 앱 두 개 판정" is.
- **Tags** — one to three, lowercase, reusable across entries. Prefer tags that will
  group things later (`esp32`, `회고`, `업무보고`) over ones true of a single entry.
- **Source** — the Artifact URL, wiki page, ticket or repo the page came from, if any.

**Done when:** title, a one-line note and one to three tags exist, and none of them
merely restates the filename.

## 3. File it

Run the script once:

```
python3 scripts/store_entry.py <html-file> \
  --note "한 줄 메모" --tags "tag1,tag2" --source-url "<url-or-omit>"
```

Add `--title` to override, `--date YYYY-MM-DD` to backdate, `--asset PATH` (repeatable)
for images or stylesheets the page needs, and `--new` to force a separate entry instead
of updating an existing one with the same date and slug.

The script copies the page, makes it a standalone document, writes `meta.json`, and
rebuilds the index in one pass. Do not write the entry folder by hand.

Read what it prints. Two lines matter:

- **`조각 HTML이라 문서로 감쌌다`** or **`charset이 없어서 넣었다`** — the stored page was
  repaired so it opens from disk. The untouched file is kept as `original.html`.
  Pass `--raw` only when the bytes must not change and you accept that it may not open.
- **`주의: 외부 리소스를 부른다`** — the page needs the network to look right. Say which
  hosts in the report, and put it in the note when it affects how the page reads.

**Done when:** the script printed `created:` or `updated:` and an index count, and the
count matches what the archive should now hold.

## 4. Personal wiki, only if configured

Read `<root>/pensiv.json`. If it has a `confluence` block, follow
[references/confluence.md](references/confluence.md). If the file or the block is absent,
say in one line that the wiki step was skipped because no personal wiki is configured,
and stop. Do not invent an upload, a page URL or a success message.

**Done when:** the wiki was either uploaded with a real returned URL, or reported as
skipped and unconfigured.

## 5. Report

Give the entry folder path and the index path, both clickable. Say the note and tags you
filed it under, so a wrong guess gets corrected now rather than in six months. Keep it to
a few lines; the archive is the deliverable, not the description of it.

## Archive rules

- **The index is generated.** Never hand-edit `<root>/index.html`. Edit the entry's
  `meta.json` and run `scripts/rebuild_index.py`, which rereads every entry from disk.
- **Moving or deleting is just moving or deleting folders**, then rebuilding the index.
  An entry whose `index.html` is gone is shown greyed out as `파일 없음` rather than
  silently dropped.
- **Every stored page opens on its own.** That is the one promise the archive makes, and
  it is why pages are normalised on the way in rather than copied blind.
- **Self-contained is still better.** A page pulling a CDN font or script loses a little
  more each year. The archive records those hosts and flags the entry `외부 리소스`, but
  it cannot fetch them back. Inline what matters before filing something important.
- **The original stays where it was.** Pensiv keeps a copy, so the working file can be
  edited or deleted freely afterwards.
- Entry folders are plain files. Finder, `grep` and git all work on them; the archive is
  not a database and should never need this skill to be read.

See [references/archive-layout.md](references/archive-layout.md) for the `meta.json`
fields and for moving the archive elsewhere.
