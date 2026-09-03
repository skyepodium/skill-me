# Game UI Design Basis

Use this compact preflight before changing UI code or producing final assets. Its purpose is to
make arbitrary taste choices visible before they harden into implementation. Keep it short enough
to drive the work; do not turn it into a mood-board essay.

## 1. Screen truth

- **Screen and target state:** name the exact screen, representative state, reference resolution,
  aspect ratio, platform, input, and locale.
- **Player job:** state the primary verb and decision.
- **Attention windows:** list what must read in about 1 second, 3 seconds, and at leisure.
- **Do-not-obscure:** identify world, character, board, threat, or timing content the UI must protect.
- **Current defects:** rank the three to five largest visible failures by player and art impact.

## 2. Reference decomposition

For each reference, record relationships rather than adjectives or isolated motifs:

| Dimension | Observation | Transferable principle | What must not be copied |
| --- | --- | --- | --- |
| Hierarchy | What wins at thumbnail size? | Contrast allocation | Brand marks or exact composition |
| Typography | Role ratios, width, weight, baseline behavior | Type hierarchy | Proprietary lettering |
| Spatial system | Axes, zones, gutters, art stage | Attention flow | Screen-for-screen layout |
| Footprint | Content-to-container relationship | Density and disclosure | Arbitrary panel dimensions |
| Art integration | Crops, local contrast, background suppression | UI/world compositing | Characters or trade dress |
| State and motion | Where saturation and motion are spent | State hierarchy | Signature effects |

A reference is not understood if the notes reduce to colors, corner cuts, glass, glow, cards,
or “premium.” Explain how the parts cooperate.

## 3. World-to-UI provenance

Record every high-salience decision before implementation:

| UI decision | Game or gameplay evidence | Intended consequence | Rejection test |
| --- | --- | --- | --- |
| Example: selected edge treatment | A real faction insignia uses a split vertical stroke | Selection reads as faction-owned | Reject if it resembles generic sci-fi brackets without the insignia |

Evidence may come from architecture, equipment, costume construction, maps, writing tools,
faction symbols, magic rules, sound, or player verbs. “Fantasy,” “tactical,” “premium,” and
“anime” are categories, not evidence.

Every strong color, shape, material, ornament, and signature motion needs a row. Utility geometry
may be neutral, but it must still obey the shared type, spacing, alignment, and state system.

## 4. Measurable system

At the stated reference resolution, record:

- font family and fallback for every used role;
- size, weight, line height, tracking, case, and alignment for every used role;
- base spacing unit, safe margins, panel padding, gutters, icon boxes, and control heights;
- major container bounds or maximum footprints;
- crop, anchor, and local-contrast rules for character and world art.

For each major container, state why it exists and what determines its footprint: content,
interaction target, expected state expansion, or deliberate negative space. As a diagnostic,
inspect any panel whose visible area is roughly more than twice what its current content and
padding require. Keep it only with a concrete interaction or composition reason.

## 5. Font and asset readiness

List identity-bearing dependencies and mark each `available`, `missing`, or `provisional`:

- display and reading fonts, including required CJK glyph coverage;
- portraits, class/faction marks, status and action icons;
- frames, textures, cursors, particles, audio cues, and motion assets as applicable.

Missing assets do not authorize generic substitutes disguised as final design. Either generate,
commission, derive, or scope the needed asset through an authorized workflow, or keep the result
explicitly provisional. System fonts and text glyphs used as icons are provisional unless the
Design Basis gives a game-specific reason for them.

## 6. Readiness verdict

Mark the direction:

- `ready` when its hierarchy, provenance, tokens, footprints, and required assets are defined;
- `provisional` when implementation can safely test a named assumption;
- `blocked` when a missing choice or asset would force an arbitrary high-salience decision.

Only `ready` proceeds toward visually final implementation. `Provisional` may proceed for a
reversible prototype, but it cannot receive a polished or commercial-quality completion claim.
