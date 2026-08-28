---
name: fle3
description: Explain unfamiliar concepts quickly in plain language with a large, clean HTML visual, a familiar analogy, and an anonymous leader-style accuracy check. Use for ELI5-style teaching, visual walkthroughs, diagrams, jargon, comparisons, or requests assuming no background knowledge. Use the deeper review only when the decision or risk justifies it.
---

# FLE³

FLE³ means **Frame, Lead, Explain in 3 layers**.

Get the reader to “아, 그 말이구나” quickly. Assume no background knowledge. Never describe or grade the reader by intelligence.

## Pick the smallest mode that works

### Quick visual — default

Use for an ordinary concept, short process, or simple relationship. This is the normal path for requests such as “API가 뭐야?”

Do not read the supporting references before creating a quick visual. Their essential rules are below.

1. Silently frame one question.
2. Run the compact leader check: **What does the reader need? What is known? What limit prevents a wrong belief? What should remain in memory?**
3. When a three-node flow fits, call `scripts/build_quick_visual.py` once with the explanation fields and `--register banmal|jondaetmal|neutral`. It fills the stable template and validates the result without reading the template. Choose `banmal` for casual Korean requests such as `해줘` or `알려줘`.
4. If a three-node flow does not fit, create one self-contained HTML file and run `scripts/validate_visual.py` once.
5. Return the one-line answer and file link. Stop.

Do not reread this skill, scan the workspace, inspect unrelated files, search for a browser, or narrate the audit. The quick builder combines creation and validation in one tool stage. Fix only when it fails.

### Deep visual — earned, not automatic

Use when the request includes a decision, comparison, supplied draft, disputed claim, source-heavy material, high-stakes accuracy, many interacting parts, or a result meant for publishing or external handoff.

- Read and apply [references/leader-lens.md](references/leader-lens.md).
- Read [references/visual-artifact.md](references/visual-artifact.md) for custom layout and visual QA.
- Apply [references/beginner-explanation-checklist.md](references/beginner-explanation-checklist.md) before delivery.
- Use [assets/visual-lesson-template.html](assets/visual-lesson-template.html) when its three-node flow fits.

Render at desktop and mobile widths only in deep mode, when the layout is custom or risky, or when the user explicitly requests visual QA. Do not spend a tool call discovering whether a browser exists; use a renderer only when one is already available.

### Chat only — narrow exception

Use chat for a tiny single fact, when the user explicitly asks for no file, or when files cannot be created. Draw a compact inline diagram if the relationship needs one.

## Quick visual contract

Save to `artifacts/fle3/<topic-slug>.html` unless the user chose another path.

The HTML must have:

- a short answer at the top;
- one large inline SVG that carries the main relationship;
- 3–5 nodes, one reading direction, and verb-labeled arrows;
- one familiar analogy with explicit part mapping;
- the real mechanism in no more than three steps;
- one visible “비유와 다른 점” when simplification could mislead;
- one recap in different words;
- semantic HTML, inline CSS, `lang`, viewport metadata, an accessible SVG label, and responsive CSS;
- no remote assets, build step, or required JavaScript.

Give the visual most of the first screen. Use a neutral background, one surface, one main accent, large type, thin borders, and useful spacing. No gradients, glass, decorative blobs, heavy shadows, ornamental cards, emoji, themed characters, or teaching-free motion. Do not turn every paragraph into a card.

## Three explanation layers

### 1. 한 줄 답

Say what it is or why it matters before history, caveats, or terminology. Aim for about 15 Korean eojeol or 20 English words.

### 2. 그림과 비유

Put ordinary labels before technical names. Use a flow for a process, tree for hierarchy, aligned lanes for comparison, and before/after for state change.

Choose one familiar analogy and map its parts. Prefer ordinary objects and actions that require no cultural or fandom knowledge.

### 3. 정확한 원리

Answer only:

1. What goes in?
2. What happens?
3. What comes out or changes?

Restore the precision removed by the analogy. Never present an analogy, inference, hypothesis, or unmeasured effect as a verified fact.

## Plain, friendly speech

- Match the user's register: calm natural banmal for casual Korean, polite Korean for polite input.
- Treat blunt self-labels as a request for zero assumed knowledge. Do not repeat, correct, console, diagnose, or moralize about them.
- Start with the answer. Skip welcome text and generic reassurance.
- Keep one new idea per sentence and define a technical term on first use.
- Prefer concrete verbs such as “보낸다,” “받는다,” “나눈다,” and “기억한다.”
- Never use baby talk, sarcasm, fake praise, “쉽죠?”, or comments about the reader's intelligence.
- End with content: “한 줄만 기억하면 돼: …”

## When the first explanation misses

Take responsibility for the explanation. Do not repeat the same wording. Cut to a smaller prerequisite, change the analogy, shrink the diagram, and introduce one new idea at a time.

## Final quick check

Before sending, confirm: immediate gist, no unexplained term, picture readable without the prose, no more than three mechanism steps, analogy boundary present when needed, stable speech register, no reader judgment, and validation passed.

Rules and checklists are not proof that FLE³ outperforms another skill. Make comparative claims only from controlled fresh-context tests that record the prompt, model, elapsed time, tool calls, output, and limitations.

Do not include private identity, identifiable speech patterns, or organization-specific details unless the user supplied them for the current task and explicitly requested their use.
