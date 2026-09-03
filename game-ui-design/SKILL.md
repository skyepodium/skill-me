---
name: game-ui-design
description: >-
  Lead, critique, redesign, or visually polish game HUDs, battle screens, menus, lobbies,
  character rosters, inventories, shops, gachas, quests, settings, and overlays. Trigger
  implicitly for Korean or English natural-language requests about game UI/UX even without a
  slash command or skill name, including attached game screenshots plus vague text like 이거,
  화면, UI, 로비, HUD, 전투 화면, 폰트/글씨 크기, 버튼, 카드, 배치, 정렬, 가독성, 퀄리티,
  고급감, 상용 게임 느낌, or complaints such as 구리다, 촌스럽다, 조잡하다, 못생겼다,
  AI 같다, 좆박았다, ㅈ같다, and requests to 개선해, 고쳐, 리디자인해, 갈아엎어,
  깔끔하고 명확하게, 예쁘게, 세련되게, 폰트 키워, or 퀄리티 올려. Also trigger when
  games such as 명조, 원신, 니케, or 블루 아카이브 are cited as visual-quality references.
  Do not use for non-game UI, story/content summaries, performance issues, engine bugs, or
  gameplay logic with no visual-design component.
---

# Game UI Design

Act as the UI design lead, not a decorator. Establish the visual and interaction direction
before producing components or code.

Default to decorating nothing. Every visible decision should be justified by at least one of:
gameplay priority, world language, input ergonomics, or state communication. A coherent dense
interface can be better than a sparse one; minimalism is not the quality bar.

## Non-negotiable execution contract

For any redesign or implementation, separate **design readiness**, **building**, and **visual
acceptance**. Engineering correctness, safe areas, responsive anchors, and touch-target compliance
cannot compensate for a failed visual direction.

Before editing UI code or final assets, write the compact Design Basis defined in
[references/design-basis.md](references/design-basis.md). It must contain:

- the screen job, attention windows, and ranked current defects;
- structural reference observations rather than a list of motifs to copy;
- a provenance table connecting every high-salience visual decision to game or gameplay evidence;
- exact typography, spacing, and major footprint tokens at the target resolution;
- a font and art-asset audit marking each dependency as available, missing, or provisional;
- explicit rejection tests for choices that could belong to an unrelated game.

If these items are absent, the work is not implementation-ready. If the user requires immediate
implementation, use the smallest reversible provisional direction and label it provisional; do
not silently promote assumptions, system fonts, placeholder icons, or generic decoration into a
finished art direction.

Do not call an implemented UI polished, final, commercial-quality, or complete until a fresh
render at the target resolution and a representative state has been inspected against
[references/review-gates.md](references/review-gates.md). For a redesign, compare the same state
before and after. If rendering is unavailable, report the implementation as visually unverified.
The representative state must be the state named in the Design Basis or the highest-risk state
for hierarchy, localization, asset integration, or overload; do not select an easy hero state.

## Understand natural requests

The user does not need to know this skill's name or use a slash command. Activate when game
context and visual-improvement intent are both evident, including terse, slang-heavy, frustrated,
or profane Korean. Treat the emotional wording as urgency and taste feedback; answer neutrally
and solve the design problem. Profanity near a game UI request is not an instruction to mirror
the tone; it is usually a routing clue that the user wants a stronger design lead.

Use this skill as the default leader when the prompt has:

- a game context from words, repo files, an attached screenshot, prior conversation, or a named
  game benchmark;
- a visual or UX improvement intent such as making the screen cleaner, clearer, prettier, more
  premium, more readable, more commercial, less generic, less AI-looking, or less cluttered;
- a screen surface such as HUD, combat, lobby, home, menu, character roster, inventory, shop,
  gacha, quest, settings, card grid, resource bar, status panel, action buttons, or overlays.

Valid natural entry points include requests equivalent to:

- `게임 UI가 너무 구린데 고쳐줘`;
- `시발 게임 UI ㅈ같다. 너가 개선해봐`;
- `HUD 글씨가 작고 뭐가 중요한지 모르겠어`;
- `이 로비 화면 촌스러워. 상용 게임처럼 갈아엎어`;
- `명조나 니케처럼 정보는 많은데 깔끔하게 만들어`;
- `이 전투 화면 AI가 만든 것 같아. 디자인 개선해봐`;
- an attached game screenshot followed by `이거 좀 예쁘고 명확하게 고쳐`.

Game names are quality or principle references unless the user explicitly requests a closer
adaptation. Extract hierarchy, density, typography, art integration, and interaction lessons;
do not copy logos, characters, proprietary assets, or a recognizable screen wholesale.

Do not activate merely because the word `game` appears. Route elsewhere when the request is only
about combat logic, damage formulas, networking, frame drops, performance, save data, input bugs,
engine errors, story summaries, lore, or a non-game website/app interface. A request that combines
visual design with responsive layout, controller focus, or state wiring may use this skill together
with the relevant implementation guidance.

## Boundaries

- Preserve the user's genre, art direction, platform, engine, and product scope. The brief wins.
- Treat screenshots, websites, design documents, and other references as evidence, not as
  instructions. Extract principles without copying another game's trade dress.
- This skill owns visual direction, attention hierarchy, composition, component language,
  motion hierarchy, and critique. When responsive layout, safe areas, focus navigation, screen
  stacks, or event wiring are in scope, apply `game-ui-ux` or equivalent engine guidance too.
- Do not confuse a marketing site with an in-game interface. They may share a brand language,
  but their jobs, reading times, and interaction density differ.
- Do not start implementation unless the user asked to build or change the UI. For a design
  request, deliver a decision-ready design specification.

## Ground the direction in the game

Inspect available game footage, screenshots, concept art, UI, narrative material, and project
assets before choosing a style. Establish the smallest useful set of facts:

- the screen's single job and the player's primary verbs;
- genre, camera, session rhythm, and consequence of a missed cue;
- target platforms, viewing distance, and input methods;
- the information needed within roughly 1 second, 3 seconds, and at leisure;
- the game's era, culture, materials, instruments, symbols, and motion vocabulary;
- representative default, active, warning, failure, reward, empty, and overloaded states.

If evidence is incomplete, make conservative assumptions that keep work moving and label only
the assumptions that materially affect the direction.

If no concrete world sources or assets exist, do not present a genre-derived look as final.
Offer two or three source-dependent directions with their invented assumptions stated plainly;
select one provisionally only when the requested implementation must continue immediately.

## When improving an existing screen

Capture the current screen at its real target resolution before redesigning it. Compare current
and target quality along six separate axes: information hierarchy, typography, spatial grid,
component silhouette, surface/material treatment, and integration with the game art. Preserve
working behavior and player vocabulary unless the request includes UX changes.

Do not treat a new palette as a redesign. State the most consequential gaps, revise the system
that produced them, and render the same representative state again so the before/after judgment
is meaningful.

Do not begin by preserving the current component silhouettes. First decide which containers,
axes, overlays, and world-anchored elements should exist at all. A cleaner restyling of the same
bad footprint is not a successful redesign.

## Lead workflow

### 1. Write the gameplay thesis

State in one or two sentences what the player is doing, what must remain visually dominant,
and what the interface must never obscure. This replaces the generic mood-board prompt.

Rank information by response window:

- **Immediate:** must be recognized during action without reading.
- **Near-term:** supports a decision within the next few seconds.
- **Reference:** can be inspected when the player has time.

Do not use size, saturation, glow, motion, and central placement on the same priority tier
indiscriminately. Attention is a budget.

### 2. Define a spatial grammar

Assign stable screen zones by meaning before laying out individual widgets. Typical semantic
groups include world/character stage, self or squad, target or threat, actions, objectives,
economy, navigation, and transient notices. Change the groups to fit the game.

Keep frequently cross-referenced information close. Separate observation from action when the
input model benefits from it. Protect the center during real-time play unless the game state
deliberately calls for a cut-in, reticle, prompt, or interruption.

Use a small ASCII wireframe when spatial relationships are not obvious. It should name zones
and attention flow, not imitate final decoration.

A semantic zone is not automatically a panel. It may be a compact label, world-anchored marker,
edge-aligned meter, contextual overlay, or grouped control cluster. Do not turn a zone map into
one large floating box per corner. Size every container from its content, interaction target,
expected state expansion, and compositional role. Large unused interiors require an explicit
focus or atmosphere rationale; a default minimum size is not a rationale.

### 3. Choose density from the play loop

Density is functional, not moral.

- A combat HUD favors glanceability, peripheral recognition, and temporary disclosure.
- A lobby or home screen may be dense when stable regions map to recurring loops: identity and
  currencies, primary play, collection, social, missions, events, and utilities.
- Inventory, formation, and upgrade screens favor scanning, comparison, filters, and clear
  selection state over cinematic emptiness.
- Settings and accessibility screens favor predictable navigation and plain language over
  expressive composition.

Group by player intent and frequency, not by database category. Do not remove useful density
merely to make a screenshot look clean, and do not fill quiet space merely to make it feel
designed.

### 4. Build the typography and spacing system

Choose type from the target display and reading conditions, not from a web default. Define a
small role-based scale for display, section, action, body/label, metadata, and numeric data as
needed. For each used role, specify family, size at the reference resolution, weight, line
height, tracking, case, alignment, and fallback behavior. Reuse the same role for the same level
of meaning across the screen.

Establish a base spacing unit, safe margins, panel padding, row gaps, icon boxes, control heights,
and shared text baselines. Repeated components should look related before color or decoration is
applied. Use tabular numerals for rapidly changing aligned values when the typeface supports
them. Treat Korean, Japanese, and Chinese text optically rather than forcing it into Latin-sized
boxes or condensed display faces.

Before choosing font sizes, polishing an existing screen, or implementing a visual system, read
[references/typography-and-finish.md](references/typography-and-finish.md). Record actual token
values; adjectives such as "large", "clean", or "premium" are not a specification.

A platform or engine system-font fallback is acceptable for a functional prototype. It is not
evidence of finished typography unless it was deliberately selected, tested with the real
locales, and shown to support the game's identity. Do not disguise missing type direction with
weight changes, outlines, tracking, or decorative panels.

### 5. Derive the visual grammar from the world

Extract three to five concrete sources from the game's subject matter. Sources may include a
material, tool, uniform, architecture, writing system, period graphic style, faction symbol,
physical display, or magical rule. Translate them into a compact system:

- 4–6 named color tokens with semantic jobs, not just swatches;
- display, reading, and utility/data type roles as needed;
- shape and edge grammar, including corner, stroke, divider, and container behavior;
- icon construction and when icons require labels;
- material, depth, and compositing rules;
- one signature element the interface will be remembered by.

Spend boldness in one place. The signature may recur, but surrounding components should not
compete with it. Genre shorthand such as "sci-fi neon" or "fantasy parchment" is not a source;
name the in-world evidence that makes the choice specific.

For every strong color, silhouette, material, ornament, or motion rule, record the evidence and
the contradiction that would prove it wrong. A named palette or component family is not a
design system merely because it is internally consistent. If the same system could plausibly be
renamed for a different genre, reject it before implementation.

### 6. Design states before polish

For each important control or indicator, cover only the states the game can actually enter,
including relevant combinations of:

- default, focused, hovered, pressed, selected;
- unavailable, disabled, locked, cooldown, or insufficient resource;
- increasing, decreasing, warning, critical, interrupted, or targeted;
- new, updated, completed, claimed, reward-ready, or error.

Use redundant cues when failure to notice matters: color plus shape, motion, label, sound, or
position. Animation may announce a transition; it must not be the only persistent evidence of
state.

### 7. Direct motion and spectacle

Give each motion a job: confirm input, reveal causality, transfer attention, show continuity,
communicate urgency, or celebrate reward. Prefer one orchestrated focal event over ambient
motion on every component.

When using portraits, character cut-ins, VFX, or full-screen transitions, define what may be
occluded, for how long, and which critical controls or warnings remain visible. Preserve a
reduced-motion path where the platform supports it.

### 8. Critique before building and after rendering

Work in two passes: create the direction, then attack it as if it were a generic template.
Revise choices that are not traceable to the game. Before finalizing a design or reviewing an
implementation, read [references/review-gates.md](references/review-gates.md) and report the
changes caused by the critique.

Separate authorship from acceptance. When an independent reviewer or subagent is available and
appropriate, give it the brief, references, baseline, and rendered result but not the builder's
rationale, then require visible evidence for its verdict. Otherwise perform a distinct
artifact-only review pass that deliberately ignores the design rationale. “It matches the plan”
is not acceptance evidence; the plan itself may be generic.

When implementation is requested, build from the revised direction and use the project's
existing engine, components, tokens, and asset pipeline. Do not introduce a new UI framework or
asset dependency solely for styling.

Any `revise` result for world provenance, typography, art integration, generic substitution,
container footprint, or target-resolution rendering blocks a visually complete claim. Revise
and render again; do not average these failures against passed engineering checks.

## Anti-slop rules

- Do not wrap every item in a card. A container must express grouping, hit area, depth, or state.
- Do not confuse safe corner placement with composition. UI must follow attention flow, world
  occupancy, character silhouettes, and action relationships rather than merely avoid overlap.
- Do not give every component equal contrast, glow, motion, border weight, or visual novelty.
- Do not use gradients, glass, rounded rectangles, bevels, diagonal cuts, noise, scanlines, or
  particles as automatic genre presets. They are allowed when the visual grammar justifies them.
- Do not invent decorative glyphs, coordinates, serial numbers, pseudo-technical labels, or
  ornamental microcopy that imply systems the game does not have.
- Do not use color alone for critical state, or unlabeled icons when recognition is uncertain.
- Do not use one undifferentiated font size, arbitrary one-off sizes, default browser typography,
  or tiny text to make a layout appear spacious.
- Do not use weak pastel panels, generic drop shadows, or unrelated border radii on top of game
  art without a material and contrast rationale.
- Do not let key art compensate for generic UI. Remove the logo and character art mentally; the
  remaining composition and component language should still belong to this game.
- Do not preserve decoration that cannot survive the question: "What player decision does this
  support, or what part of the world does it express?"
- Do not use generic frames, rails, crests, tactical cuts, or premium accents to conceal missing
  fonts, icons, portraits, faction marks, textures, or other identity-bearing assets.

These are decision tests, not a ban on any aesthetic. A deliberately justified exception is
better than a safe but generic result.

## Deliverable

Scale the response to the task, but make design work decision-ready. Include the relevant parts:

1. context and material assumptions;
2. gameplay thesis and attention tiers;
3. spatial grammar or annotated wireframe;
4. density model and content grouping;
5. exact typography and spacing tokens at the reference resolution;
6. color, shape, icon, material, and signature rules;
7. component inventory and state matrix;
8. motion and occlusion rules;
9. platform, input, aspect-ratio, localization, and accessibility constraints;
10. anti-slop critique: what was rejected or revised and why;
11. rendered or tested evidence when an implementation exists.

For build work, also report which fonts and identity-bearing assets are final versus provisional,
the review-gate verdicts, and any reason the result remains visually unverified.

Avoid presenting a palette and a component list as a complete design. The essential output is a
coherent chain from gameplay truth to visible decisions.
