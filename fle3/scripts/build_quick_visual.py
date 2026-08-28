#!/usr/bin/env python3
"""Build and validate a stable three-node FLE3 visual without loading the template into model context."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from validate_visual import validate


FIELDS = (
    "title",
    "answer",
    "diagram_title",
    "diagram_description",
    "action_one",
    "action_two",
    "node_one",
    "node_one_detail",
    "node_two",
    "node_two_detail",
    "node_three",
    "result",
    "analogy",
    "boundary",
    "step_one_title",
    "step_one",
    "step_two_title",
    "step_two",
    "step_three_title",
    "step_three",
    "recap",
)


def marker(field: str) -> str:
    if field == "answer":
        return "FLE3_ONE_LINE_ANSWER"
    return "FLE3_" + field.upper()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--register", required=True, choices=("banmal", "jondaetmal", "neutral")
    )
    for field in FIELDS:
        parser.add_argument("--" + field.replace("_", "-"), required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.register == "banmal":
        polite_patterns = ("요.", "요?", "예요", "이에요", "습니다", "세요")
        violations = [
            field
            for field in FIELDS
            if any(pattern in getattr(args, field) for pattern in polite_patterns)
        ]
        if violations:
            raise SystemExit(
                "Banmal output contains polite endings in: " + ", ".join(violations)
            )
    skill_dir = Path(__file__).resolve().parents[1]
    template = (skill_dir / "assets" / "visual-lesson-template.html").read_text(
        encoding="utf-8"
    )

    rendered = template
    for field in sorted(FIELDS, key=lambda item: len(marker(item)), reverse=True):
        rendered = rendered.replace(marker(field), html.escape(getattr(args, field)))

    leftovers = sorted(set(re.findall(r"FLE3_[A-Z0-9_]+", rendered)))
    if leftovers:
        raise SystemExit("Unreplaced template markers: " + ", ".join(leftovers))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    errors = validate(args.output)
    if errors:
        args.output.unlink(missing_ok=True)
        raise SystemExit("; ".join(errors))

    print(f"[OK] Built and validated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
