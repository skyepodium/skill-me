#!/usr/bin/env python3
"""Validate the structural contract of a generated FLE3 HTML lesson."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class LessonParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.tags.append((tag, dict(attrs)))

    def has_tag(self, name: str) -> bool:
        return any(tag == name for tag, _ in self.tags)

    def attrs_for(self, name: str) -> list[dict[str, str | None]]:
        return [attrs for tag, attrs in self.tags if tag == name]


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.is_file():
        return [f"File not found: {path}"]
    if path.suffix.lower() != ".html":
        errors.append("Output must use the .html extension")

    content = path.read_text(encoding="utf-8")
    parser = LessonParser()
    parser.feed(content)

    if not re.search(r"<!doctype\s+html>", content, re.IGNORECASE):
        errors.append("Missing HTML doctype")
    if re.search(r"FLE3_[A-Z0-9_]+|\b[A-Z][A-Z0-9_]*_DETAIL\b", content):
        errors.append("Unreplaced FLE3 template marker found")
    if not parser.has_tag("title"):
        errors.append("Missing <title>")
    if not parser.has_tag("h1"):
        errors.append("Missing <h1>")
    if not parser.has_tag("svg"):
        errors.append("Missing main SVG visual")

    html_tags = parser.attrs_for("html")
    if not html_tags or not html_tags[0].get("lang"):
        errors.append("Missing document language on <html>")

    viewport_found = any(
        attrs.get("name", "").lower() == "viewport" and attrs.get("content")
        for attrs in parser.attrs_for("meta")
    )
    if not viewport_found:
        errors.append("Missing viewport metadata")

    accessible_svg = any(
        attrs.get("role") == "img"
        and (attrs.get("aria-label") or attrs.get("aria-labelledby"))
        for attrs in parser.attrs_for("svg")
    )
    if not accessible_svg:
        errors.append("SVG needs role=img and an accessible label")

    remote_assets: list[str] = []
    for tag in ("img", "script", "link"):
        for attrs in parser.attrs_for(tag):
            location = attrs.get("src") or attrs.get("href") or ""
            if re.match(r"https?://", location):
                remote_assets.append(location)
    if remote_assets:
        errors.append("Remote runtime asset found: " + ", ".join(remote_assets))

    if "@media" not in content:
        errors.append("Missing responsive CSS media query")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    args = parser.parse_args()

    errors = validate(args.html_file)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print(f"[OK] FLE3 visual structure is valid: {args.html_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
