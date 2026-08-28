# Output contract

Use this reference when creating or reviewing an App Store Connect copy artifact.

## Artifact shape

Write one Markdown file in this order:

````markdown
# {App} iOS App Store Connect 입력 문구 — {candidate-id}

## 범위

- 후보 식별자: `{candidate-id}`
- 상태: `draft` or `candidate`
- 모드: `launch`, `update`, or `add-locales`
- 대상 버전: `{version}`
- 대상 빌드: `{build}`
- 번들 식별자: `{bundle-id}`
- 기본 로케일: `{locale}`
- 대상 로케일: `{locale list}`
- 제품 포지셔닝: {one verified sentence}

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

## 입력값 길이 검증

The validator owns this table. Generate it with `--write-report`.

## 영어 `en-US`, `en-GB`

### 앱 이름
```text
Example
```

### 부제
```text
A concise value statement
```

### 프로모션 텍스트
```text
Optional promotional copy.
```

### 설명
```text
Plain-text product description.
```

### 키워드
```text
focused,comma,separated,keywords
```

## 확인 필요

- Only unresolved facts that block candidate status.
````

The field heading may be plain text or a level-three Markdown heading. Always put the copyable value in a fenced `text` block immediately after its field heading.

Omit `## 확인 필요` from a candidate. Include it only in a draft that has unresolved facts.

## Mode requirements

### `launch`

- Include scope, shared inputs, and full localized listing fields.
- Require app name, subtitle, description, and keywords for every locale group.
- Promotional text is optional.
- Do not include `새로운 기능`; Apple does not make What's New available for the first version.

### `update`

- Include scope and `새로운 기능` for every target locale group.
- What's New describes only user-observable changes in the submitted version.
- Do not regenerate the full listing unless the user asked to change it.

### `add-locales`

- Include scope, shared inputs, and full listing fields for only the new locales.
- Preserve previously submitted locale copy by reference rather than duplicating it.
- Include `새로운 기능` when the target is a later app version and that field is needed for the added locale.

## Shared values

For `launch` and `add-locales`, provide these verified values:

- support URL;
- privacy policy URL;
- version;
- copyright;
- primary category.

Add marketing URL, secondary category, routing coverage file, privacy answers, export-compliance answers, age-rating answers, content-rights explanation, reviewer contact, sign-in instructions, and review notes when relevant. Use `확인 필요` in a draft instead of inventing an answer.

## Current Apple limits

The validator defaults follow Apple's current App Store Connect reference:

- app name: 2–30 characters;
- subtitle: at most 30 characters;
- promotional text: at most 170 characters;
- description: at most 4,000 characters;
- keywords: at most 100 UTF-8 bytes;
- What's New: at most 4,000 characters and unavailable for the first version.

Verify changed limits against Apple's official references before updating the validator:

- https://developer.apple.com/help/app-store-connect/reference/app-information/app-information/
- https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information
- https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations

## Localization rules

- App Store metadata locales and Xcode binary localizations are different sets. Do not derive one mechanically from the other.
- Keep locale codes in every localized section heading.
- Share one block across regional locales only when the exact copy is intentional for all of them.
- Preserve brand spelling, product facts, feature count, privacy claims, and limitations across languages.
- Adapt grammar, punctuation, headings, and examples to the locale.
- Do not add competitor names, unsupported superlatives, ranking claims, prices, or unverified features.

## Candidate gate

Use `candidate` only when:

- all copy is backed by verified product facts;
- required fields exist for every target locale;
- deterministic validation passes;
- privacy, login, advertising, analytics, encryption, age rating, content rights, and reviewer access are resolved when applicable;
- a human can identify exactly what to paste and where.

Otherwise keep the status as `draft` and list the smallest unresolved facts under `## 확인 필요`.
