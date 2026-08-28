#!/usr/bin/env python3
"""Validate and report on ios-app-store-copy Markdown artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

FIELD_NAMES = (
    "앱 이름",
    "부제",
    "프로모션 텍스트",
    "설명",
    "새로운 기능",
    "이 버전에서 업그레이드된 사항",
    "키워드",
    "지원 URL",
    "마케팅 URL",
    "개인정보 처리방침 URL",
    "버전",
    "저작권",
    "기본 카테고리",
    "보조 카테고리",
    "라우팅 앱 커버리지 파일",
    "앱 개인정보 보호",
    "수출 규정 준수",
    "연령 등급",
    "콘텐츠 권한 설명",
    "메모",
    "앱 심사 메모",
)

FULL_LISTING_FIELDS = ("앱 이름", "부제", "설명", "키워드")
PLACEHOLDER_RE = re.compile(r"(?:확인\s*필요|\bTODO\b|\bTBD\b|\?\?\?)", re.IGNORECASE)
SCOPE_VALUE_RE = re.compile(r"^-\s*([^:]+):\s*`?([^`\n]+?)`?\s*$", re.MULTILINE)
LOCALE_CODE_RE = re.compile(r"^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?$")


@dataclass
class LocaleBlock:
    heading: str
    locales: list[str]
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def heading_name(line: str) -> str | None:
    stripped = re.sub(r"^#{1,6}\s+", "", line.strip())
    return stripped if stripped in FIELD_NAMES else None


def fenced_value(lines: list[str], start: int) -> tuple[str | None, int]:
    index = start
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines) or not lines[index].strip().startswith("```"):
        return None, start
    index += 1
    content: list[str] = []
    while index < len(lines) and not lines[index].strip().startswith("```"):
        content.append(lines[index].rstrip("\n"))
        index += 1
    if index >= len(lines):
        return None, start
    return "\n".join(content).strip(), index + 1


def extract_fields(lines: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0
    while index < len(lines):
        name = heading_name(lines[index])
        if name:
            value, next_index = fenced_value(lines, index + 1)
            if value is not None:
                canonical = (
                    "새로운 기능" if name == "이 버전에서 업그레이드된 사항" else name
                )
                fields[canonical] = value
                index = next_index
                continue
        index += 1
    return fields


def parse_locale_blocks(text: str) -> list[LocaleBlock]:
    lines = text.splitlines(keepends=True)
    starts: list[int] = []
    for index, line in enumerate(lines):
        if line.startswith("## ") and not line.startswith("### "):
            codes = re.findall(r"`([^`]+)`", line)
            if codes and all(LOCALE_CODE_RE.match(code) for code in codes):
                starts.append(index)

    blocks: list[LocaleBlock] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        heading = lines[start].strip()[3:]
        locales = re.findall(r"`([^`]+)`", heading)
        blocks.append(
            LocaleBlock(heading, locales, extract_fields(lines[start + 1 : end]))
        )
    return blocks


def scope_values(text: str) -> dict[str, str]:
    return {key.strip(): value.strip() for key, value in SCOPE_VALUE_RE.findall(text)}


def section_text(text: str, title: str) -> str:
    match = re.search(rf"^## {re.escape(title)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    following = re.search(r"^## (?!#)", text[match.end() :], re.MULTILINE)
    end = match.end() + following.start() if following else len(text)
    return text[match.end() : end]


def valid_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def keyword_items(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def validate(text: str) -> tuple[Result, list[LocaleBlock]]:
    result = Result()
    scope_section = section_text(text, "범위")
    scope = scope_values(scope_section)
    mode = scope.get("모드")
    status = scope.get("상태", "draft")
    blocks = parse_locale_blocks(text)

    if not scope_section:
        result.error("missing '## 범위' section")
    if mode not in {"launch", "update", "add-locales"}:
        result.error("scope must declare mode as launch, update, or add-locales")
    if status not in {"draft", "candidate"}:
        result.error("scope status must be draft or candidate")
    if not blocks:
        result.error("no localized sections with App Store locale codes were found")

    seen: set[str] = set()
    for block in blocks:
        for locale in block.locales:
            if locale in seen:
                result.error(f"locale appears more than once: {locale}")
            seen.add(locale)

        required = ("새로운 기능",) if mode == "update" else FULL_LISTING_FIELDS
        for required_field in required:
            if not block.fields.get(required_field, "").strip():
                result.error(f"{block.heading}: missing {required_field}")

        if mode == "launch" and "새로운 기능" in block.fields:
            result.error(f"{block.heading}: launch mode must not include 새로운 기능")

        name = block.fields.get("앱 이름", "")
        subtitle = block.fields.get("부제", "")
        promotional = block.fields.get("프로모션 텍스트", "")
        description = block.fields.get("설명", "")
        whats_new = block.fields.get("새로운 기능", "")
        keywords = block.fields.get("키워드", "")

        if name and not 2 <= len(name) <= 30:
            result.error(
                f"{block.heading}: app name is {len(name)} characters; expected 2-30"
            )
        if subtitle and len(subtitle) > 30:
            result.error(
                f"{block.heading}: subtitle is {len(subtitle)} characters; maximum is 30"
            )
        if promotional and len(promotional) > 170:
            result.error(
                f"{block.heading}: promotional text is {len(promotional)} characters; maximum is 170"
            )
        if description and len(description) > 4000:
            result.error(
                f"{block.heading}: description is {len(description)} characters; maximum is 4000"
            )
        if whats_new and len(whats_new) > 4000:
            result.error(
                f"{block.heading}: What's New is {len(whats_new)} characters; maximum is 4000"
            )
        keyword_bytes = len(keywords.encode("utf-8"))
        if keywords and keyword_bytes > 100:
            result.error(
                f"{block.heading}: keywords use {keyword_bytes} UTF-8 bytes; maximum is 100"
            )

        visible = f"{name} {subtitle}".casefold()
        duplicates = [
            keyword
            for keyword in keyword_items(keywords)
            if keyword.casefold() in visible
        ]
        if duplicates:
            result.warn(
                f"{block.heading}: keywords repeat visible terms: {', '.join(duplicates)}"
            )

    common = extract_fields(section_text(text, "공통 입력값").splitlines(keepends=True))
    if mode in {"launch", "add-locales"}:
        for required_common in (
            "지원 URL",
            "개인정보 처리방침 URL",
            "버전",
            "저작권",
            "기본 카테고리",
        ):
            if not common.get(required_common, "").strip():
                result.error(f"shared values are missing {required_common}")

    for url_field in ("지원 URL", "마케팅 URL", "개인정보 처리방침 URL"):
        if common.get(url_field) and not valid_url(common[url_field]):
            result.error(f"{url_field} is not a complete http(s) URL")

    scope_version = scope.get("대상 버전")
    if scope_version and common.get("버전") and scope_version != common["버전"]:
        result.error(
            f"scope version {scope_version} does not match shared version {common['버전']}"
        )

    unresolved_section = section_text(text, "확인 필요")
    if status == "candidate" and unresolved_section:
        result.error("candidate must not include an unresolved-items section")
    if status == "candidate" and PLACEHOLDER_RE.search(text):
        result.error("candidate contains an unresolved placeholder")
    elif status == "draft" and PLACEHOLDER_RE.search(text):
        result.warn("draft contains unresolved values")

    return result, blocks


def report_table(blocks: list[LocaleBlock]) -> str:
    rows = [
        "| 언어 그룹 | App Store 로케일 | 앱 이름 | 부제 | 프로모션 텍스트 | 설명 | 새로운 기능 | 키워드 바이트 |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for block in blocks:
        fields = block.fields
        group = re.sub(r"\s*`[^`]+`(?:,\s*`[^`]+`)*\s*$", "", block.heading).strip()
        rows.append(
            "| {group} | {locales} | {name} | {subtitle} | {promo} | {description} | {whats_new} | {keywords} |".format(
                group=group,
                locales=", ".join(f"`{locale}`" for locale in block.locales),
                name=len(fields.get("앱 이름", "")) or "—",
                subtitle=len(fields.get("부제", "")) or "—",
                promo=len(fields.get("프로모션 텍스트", "")) or "—",
                description=len(fields.get("설명", "")) or "—",
                whats_new=len(fields.get("새로운 기능", "")) or "—",
                keywords=len(fields.get("키워드", "").encode("utf-8")) or "—",
            )
        )
    return "\n".join(rows)


def write_report(path: Path, text: str, table: str) -> str:
    section = f"## 입력값 길이 검증\n\n{table}\n\n"
    pattern = re.compile(
        r"^## 입력값 길이 검증\s*$.*?(?=^## (?!#))", re.MULTILINE | re.DOTALL
    )
    if pattern.search(text):
        updated = pattern.sub(section, text, count=1)
    else:
        locale_heading = re.search(
            r"^## .+`[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?`", text, re.MULTILINE
        )
        if not locale_heading:
            raise ValueError("cannot insert report before a localized section")
        updated = (
            text[: locale_heading.start()] + section + text[locale_heading.start() :]
        )
    path.write_text(updated, encoding="utf-8")
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="insert or replace the Markdown length table",
    )
    args = parser.parse_args()

    try:
        text = args.artifact.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    result, blocks = validate(text)
    if args.write_report and blocks:
        try:
            text = write_report(args.artifact, text, report_table(blocks))
            result, blocks = validate(text)
        except (OSError, ValueError) as error:
            result.error(str(error))

    for warning in result.warnings:
        print(f"[WARN] {warning}")
    for error in result.errors:
        print(f"[ERROR] {error}", file=sys.stderr)

    if result.errors:
        print(
            f"[FAIL] {len(result.errors)} error(s), {len(result.warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1

    print(
        f"[OK] {len(blocks)} locale group(s), {sum(len(block.locales) for block in blocks)} locale(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
