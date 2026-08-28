---
name: ios-app-store-copy
description: Create and validate multilingual, copy-ready App Store Connect listing text for an iOS launch, app update, or locale expansion. Use for app names, subtitles, promotional text, descriptions, keywords, review notes, shared submission values, and localized What's New copy. Do not use for building, signing, uploading, or submitting an app.
---

# iOS App Store Copy

Produce one Markdown artifact that a person can copy into App Store Connect without mixing in research notes or an investigation diary.

## Choose the mode

- `launch`: Create the full listing for the first app version. Do not add `What's New`; App Store Connect does not expose it for the first version.
- `update`: Create localized `What's New` copy for an existing app version. Change other listing fields only when the user asks.
- `add-locales`: Add full listing fields for new App Store locales while preserving existing locale copy.

Read [references/output-contract.md](references/output-contract.md) before creating an artifact. It defines the exact sections, field limits, locale grouping rules, and candidate criteria.

## Establish product truth

Use repository evidence and user-provided facts to identify the app, version, build, bundle identifier, positioning, reachable features, URLs, supported locales, data practices, account requirements, advertising or analytics SDKs, encryption use, content rights, age-rating answers, and reviewer instructions.

Classify every material claim as verified or unresolved. Never infer privacy, advertising, login, encryption, age rating, content rights, or regulatory answers merely because no contrary evidence was noticed. A draft may say `확인 필요`; a candidate may not.

Use the app's actual user-visible behavior. Do not mention internal architecture, test counts, implementation details, planned features, or capabilities absent from the submitted build.

## Write the copy

1. Choose a source locale and write a concise source-language listing from verified product facts.
2. Localize by meaning and natural store language, not sentence-by-sentence literal translation.
3. Group multiple App Store locales only when they intentionally share identical copy. Keep the locale codes visible in the heading.
4. Preserve existing copy in `update` and `add-locales` modes unless the user explicitly requests a rewrite.
5. Save to `artifacts/ios-app-store-copy/<candidate-id>.md` unless the user chose another path.

Keep analysis outside the artifact. The final document contains only scope, copyable shared values, the validation table, localized fields, and a short unresolved-items section when needed.

## Validate

Run the bundled validator from the skill directory:

```bash
python3 scripts/validate_copy.py <artifact.md> --write-report
```

The validator checks required sections by mode, locale duplication, URLs, field lengths, UTF-8 keyword bytes, repeated visible keywords, unresolved candidate values, and version consistency. `--write-report` replaces or inserts the deterministic length table.

If validation fails, fix the artifact and run it once more. Do not weaken a product-truth error to make the validator pass. If a fact cannot be verified, keep the document in `draft` and report the unresolved item.

## Deliver

Return the artifact link, mode, locales covered, validation result, and unresolved facts. Stop there. Do not upload or submit anything to App Store Connect without a separate explicit request and authorization.
