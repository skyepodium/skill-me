#!/usr/bin/env python3
"""Compare FLE3 with a small HTML-ELI5 control prompt over fresh Codex runs."""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import tempfile
import time
from pathlib import Path

from validate_visual import validate


QUESTION = "API가 뭔지 배경지식 없는 사람도 이해하게 그림으로 쉽게 설명해줘."
CONTROL = """Create one standalone HTML visual lesson for the question below.
Use one large diagram and very little text. Explain in plain Korean with one familiar analogy.
Keep the design clean and functional. Save the result to {output}.
Question: {question}
"""
FLE3 = """Read and follow the FLE3 skill at {skill}.
Treat this as a fresh request with no prior context. Save the visual lesson to {output}.
Question: {question}
"""


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def summarize(rows: list[dict[str, object]]) -> dict[str, float]:
    elapsed = [float(row["elapsed_seconds"]) for row in rows]
    return {
        "mean_seconds": round(statistics.mean(elapsed), 2),
        "median_seconds": round(statistics.median(elapsed), 2),
        "min_seconds": round(min(elapsed), 2),
        "max_seconds": round(max(elapsed), 2),
        "p80_seconds": round(percentile(elapsed, 0.8), 2),
    }


def run_once(
    *, variant: str, prompt: str, run_dir: Path, model: str, effort: str, timeout: int
) -> dict[str, object]:
    output = run_dir / "lesson.html"
    log = run_dir / "events.jsonl"
    final = run_dir / "final.txt"
    command = [
        "codex",
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox",
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--cd",
        str(run_dir),
        "--output-last-message",
        str(final),
        prompt,
    ]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    elapsed = time.monotonic() - started
    log.write_text(completed.stdout, encoding="utf-8")
    (run_dir / "stderr.txt").write_text(completed.stderr, encoding="utf-8")
    events = []
    for line in completed.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    tool_calls = sum(
        event.get("type") == "item.completed"
        and event.get("item", {}).get("type") == "command_execution"
        for event in events
    )
    turn_events = [event for event in events if event.get("type") == "turn.completed"]
    usage = turn_events[-1].get("usage", {}) if turn_events else {}
    structural_errors = validate(output) if output.is_file() else ["artifact missing"]
    return {
        "variant": variant,
        "elapsed_seconds": round(elapsed, 2),
        "exit_code": completed.returncode,
        "artifact_exists": output.is_file(),
        "artifact_bytes": output.stat().st_size if output.is_file() else 0,
        "structural_valid": not structural_errors,
        "structural_errors": structural_errors,
        "tool_calls": tool_calls,
        "usage": usage,
        "run_dir": str(run_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--variant", choices=("control", "fle3", "both"), default="both")
    parser.add_argument("--label", default="baseline")
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--effort", default="low")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    root = Path(tempfile.mkdtemp(prefix=f"fle3-benchmark-{args.label}-"))
    variants = ("control", "fle3") if args.variant == "both" else (args.variant,)
    rows: list[dict[str, object]] = []

    for variant in variants:
        for index in range(1, args.runs + 1):
            run_dir = root / variant / str(index)
            run_dir.mkdir(parents=True)
            output = run_dir / "lesson.html"
            if variant == "control":
                prompt = CONTROL.format(output=output, question=QUESTION)
            else:
                prompt = FLE3.format(skill=skill_dir / "SKILL.md", output=output, question=QUESTION)
            row = run_once(
                variant=variant,
                prompt=prompt,
                run_dir=run_dir,
                model=args.model,
                effort=args.effort,
                timeout=args.timeout,
            )
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)

    report = {
        "label": args.label,
        "question": QUESTION,
        "model": args.model,
        "reasoning_effort": args.effort,
        "runs_per_variant": args.runs,
        "control_definition": "Short HTML-ELI5 control prompt; not the unavailable original plugin.",
        "results": rows,
        "summary": {
            variant: summarize([row for row in rows if row["variant"] == variant])
            for variant in variants
        },
        "artifact_root": str(root),
    }
    destination = args.output or (root / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"report={destination}")
    return 0 if all(
        row["exit_code"] == 0
        and row["artifact_exists"]
        and (row["variant"] != "fle3" or row["structural_valid"])
        for row in rows
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
