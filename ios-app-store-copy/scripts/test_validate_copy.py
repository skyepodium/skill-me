#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_copy.py")


def scope(mode: str, status: str = "candidate") -> str:
    return f"""# Example iOS App Store Connect 입력 문구 — ios-global-20260828-A1

## 범위

- 후보 식별자: `ios-global-20260828-A1`
- 상태: `{status}`
- 모드: `{mode}`
- 대상 버전: `1.0`
- 대상 빌드: `1`
- 번들 식별자: `com.example.app`
- 기본 로케일: `en-US`
- 대상 로케일: `en-US`, `ko-KR`
- 제품 포지셔닝: A focused example app.
"""


COMMON = """
## 공통 입력값

### 지원 URL
```text
https://example.com/support
```

### 개인정보 처리방침 URL
```text
https://example.com/privacy
```

### 버전
```text
1.0
```

### 저작권
```text
2026 Example
```

### 기본 카테고리
```text
유틸리티
```
"""


FULL_LOCALES = """
## 영어 `en-US`

### 앱 이름
```text
Example Focus
```

### 부제
```text
Do one thing clearly
```

### 설명
```text
Example Focus helps you do one verified thing clearly.
```

### 키워드
```text
simple,focused,clear
```

## 한국어 `ko-KR`

### 앱 이름
```text
Example 집중
```

### 부제
```text
한 가지에 선명하게 집중
```

### 설명
```text
검증된 한 가지 기능에 집중하도록 돕습니다.
```

### 키워드
```text
간단함,몰입,명료함
```
"""


class ValidatorTests(unittest.TestCase):
    def run_validator(
        self, content: str, *args: str
    ) -> tuple[subprocess.CompletedProcess[str], str]:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "copy.md"
            artifact.write_text(content, encoding="utf-8")
            result = subprocess.run(
                ["python3", str(SCRIPT), str(artifact), *args],
                check=False,
                capture_output=True,
                text=True,
            )
            return result, artifact.read_text(encoding="utf-8")

    def test_launch_writes_report_and_passes(self) -> None:
        result, artifact = self.run_validator(
            scope("launch") + COMMON + FULL_LOCALES, "--write-report"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## 입력값 길이 검증", artifact)
        self.assertIn("| 영어 | `en-US` |", artifact)

    def test_launch_rejects_whats_new(self) -> None:
        content = (
            scope("launch")
            + COMMON
            + FULL_LOCALES.replace(
                "### 키워드",
                "### 새로운 기능\n```text\nFirst release.\n```\n\n### 키워드",
                1,
            )
        )
        result, _ = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("launch mode must not include", result.stderr)

    def test_update_requires_whats_new(self) -> None:
        result, _ = self.run_validator(scope("update") + FULL_LOCALES)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing 새로운 기능", result.stderr)

    def test_update_with_whats_new_passes(self) -> None:
        update_locales = """
## 영어 `en-US`, `en-GB`

### 새로운 기능
```text
- Timers now preserve local presets more reliably.
```

## 한국어 `ko-KR`

### 새로운 기능
```text
- 기기에 저장한 타이머 프리셋을 더 안정적으로 유지합니다.
```
"""
        result, _ = self.run_validator(scope("update") + update_locales)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_add_locales_full_listing_passes(self) -> None:
        result, artifact = self.run_validator(
            scope("add-locales") + COMMON + FULL_LOCALES, "--write-report"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| 한국어 | `ko-KR` |", artifact)

    def test_candidate_rejects_placeholder_and_long_name(self) -> None:
        broken = (
            FULL_LOCALES.replace("Example Focus", "X" * 31, 1)
            + "\n## 확인 필요\n\n- 확인 필요\n"
        )
        result, _ = self.run_validator(scope("launch") + COMMON + broken)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("app name is 31 characters", result.stderr)
        self.assertIn("unresolved placeholder", result.stderr)

    def test_candidate_rejects_unresolved_section_without_placeholder(self) -> None:
        content = (
            scope("launch")
            + COMMON
            + FULL_LOCALES
            + "\n## 확인 필요\n\n- Export compliance answer is unresolved.\n"
        )
        result, _ = self.run_validator(content)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not include an unresolved-items section", result.stderr)


if __name__ == "__main__":
    unittest.main()
