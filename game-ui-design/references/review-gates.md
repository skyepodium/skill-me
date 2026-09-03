# Game UI Review Gates

Read this reference when critiquing a direction, reviewing an implementation, or deciding
whether a game UI is ready to hand off. Apply only the gates relevant to the requested screen
and platform.

Use `pass`, `revise`, or `blocked` for each gate and cite visible evidence. `Blocked` means the
necessary game or platform fact is unavailable; it does not mean the design is merely imperfect.

## 1. Gameplay truth

- Can the screen's job and primary player verb be stated without aesthetic language?
- Are immediate, near-term, and reference information visibly different?
- Does prominence track consequence and response time rather than stakeholder importance?
- Can the player identify the next valid action in the intended time window?

Revise if the hierarchy was derived from a component inventory rather than player decisions.

## 2. Spatial grammar and density

- Does each region have a stable semantic role?
- Are frequently compared values close enough to scan together?
- Does the world, character, or board retain the space required for play?
- Is dense content grouped into recognizable routes instead of a uniform wall?
- Is sparse space serving focus, anticipation, or atmosphere rather than hiding missing content?
- Do transient alerts have a destination and expiry instead of accumulating permanently?

For touch interfaces, inspect reach, hand occlusion, accidental activation risk, and whether
actions and observations are sensibly separated. For controller interfaces, inspect initial
focus, focus order, focus visibility, and recovery after a modal closes.

## 3. Typography, alignment, and finish

- The reference resolution, display class, and reading conditions are stated.
- Used text roles have actual family, size, weight, line-height, and alignment values.
- Critical and interactive labels remain readable at 100% scale on the target display.
- CJK strings are tested directly rather than inferred from Latin placeholder widths.
- Repeated labels, numbers, icons, cards, and controls share baselines and dimensions.
- Panel padding and inter-group gaps come from a small spacing family, not isolated guesses.
- Text over artwork has deliberate local contrast without indiscriminate outlines and shadows.
- Surface edges, border weights, shadows, and radii belong to the same component grammar.
- Pixel-art scenes avoid accidental fractional placement and soft web-component styling.

Revise if the screen is described as clean or polished without measurable type and spacing
tokens or a render at the target resolution.

## 4. Distinctiveness

Run these tests without treating any single one as a universal veto:

- **Source traceability:** each strong motif maps to a concrete in-world source.
- **Substitution:** replacing the title and proper nouns with another game should create visible
  contradictions, not a plausible reskin.
- **Key-art removal:** without logos and character art, layout, type, shapes, and motion still
  communicate the intended game.
- **Genre-default audit:** neon, parchment, glass, bevels, rounded cards, tactical grids, and
  ornamental numbers appear only when justified.
- **Signature budget:** one memorable device leads; secondary elements support it.

Revise generic choices instead of adding more decoration on top of them.

## 5. State readability

Inspect representative controls and status indicators in default, selected or focused,
unavailable, warning, and completion states.

- State remains identifiable without relying on color alone.
- Cooldown, locked, disabled, and unaffordable are not visually conflated.
- New, reward-ready, error, and urgent notifications have different meanings and do not all use
  the same red badge.
- Labels and numbers retain contrast over the most hostile plausible background.
- Motion introduces a change but a stable visual cue remains afterward.
- Icons have labels, tooltips, onboarding, or strong repeated context when recognition is not
  self-evident.

## 6. Composition and spectacle

- Only one visual event leads at a time.
- Cut-ins, VFX, reward bursts, and transitions have an explicit occlusion budget.
- Critical health, threat, timing, or confirmation information survives spectacle.
- Repeated ambient animation does not compete with actionable change.
- Character poses and silhouettes are given room intentionally; they are not just background
  art behind arbitrary panels.

## 7. Robustness

When artifacts can be rendered or run, inspect the smallest useful matrix rather than one hero
screenshot:

- target aspect ratios and safe areas;
- smallest and largest supported viewport or viewing distance;
- default, peak-action, critical, modal, empty, and overloaded content states as applicable;
- longest plausible localized labels and large text settings;
- mouse/touch plus keyboard/gamepad focus where supported;
- reduced-motion and color-independent critical states.

Use screenshots to judge visual hierarchy. A blur or squint check should leave the intended
focal order visible. Check a grayscale view when critical meaning may depend on hue. Record what
was actually observed; do not claim devices or resolutions that were not tested.

For redesigns, compare before and after at the same resolution and representative state. Reject
changes that improve decoration while leaving type hierarchy, alignment axes, or art integration
unchanged.

## 8. Final anti-slop challenge

Ask:

1. What would be lost if each decorative effect were removed?
2. Which decision could not have been made before learning about this specific game?
3. Is any component styled primarily to fill space or look "premium"?
4. Does every repeated motif still carry the same meaning?
5. Did the critique remove or simplify anything, or merely add more polish?

If the answer reveals that key choices are interchangeable with another game, return to the
world-derived visual grammar. Finish by listing the concrete revisions the review produced.
