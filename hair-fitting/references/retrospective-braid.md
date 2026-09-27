# Retrospective: braid fit (2026-09-27)

A layered Tripo braid (1.9M triangles, 115 parts, no UVs) fitted to CombatGirls Face_04, reusing the Short1/2/4 pipeline.
Figures come from the session transcript; the counts below are approximate (command lines matched by pattern).

## Outcome and cost

- 67 minutes from request to the accepted result; about 111 shell commands, about 27 Unity capture cycles.
- The first 25 minutes ran without a report to the user. The user then asked what was wrong, and on review found two defects
  that had not been measured: a raised crown back and "broken texture" (crossing layers).
- The decisive measurement (which part the scalp push-off hit first in each direction) came 43 minutes in. After it, the
  remaining defects were fixed in about 24 minutes.

## Why it took many trials (cause, then evidence)

1. **Parameters were tuned before the driver was measured.** Triangle budgets, fade bands, guard heights and clearance values
   were varied while the real cause was structural: a hidden fold of the inner shell drove a 7 cm lift, and every on/off
   boundary folded strands. Evidence: 5 guard/fade variants and 4 bend variants each moved the defect instead of removing it.
2. **A validated pipeline was run whole on a different kind of hair.** The skill already said a method must be re-checked,
   not reused, when the mesh changes. Running placement → thickness → clearance at once made each defect hard to attribute.
3. **An existing rule was skipped.** The skill required region-specific heights against the reference hair. It was not
   measured, so the crown (35.5 mm vs 13–19 mm) reached the user as a defect.
4. **Invalid experiments produced wrong conclusions.** A rigid move per part also moved the root cap, a capture showed the
   wrong hair, and two renders looked "unchanged" without a pixel check. Each led to a rejected method or wasted run.
5. **A step was judged by its intermediate output.** The shell fit looked like a wig before the step that removes the
   volume; it was rejected, then needed later.
6. **Symptoms were patched downstream.** Face clearance pushes were added at the end of the chain while the placement still
   carried a 7 cm error upstream.
7. **The feedback loop was slow.** Unity reimport + Play + capture took most of a minute and was used for decisions that the
   Blender stage strip could make in seconds.

## Next time: higher quality in less time

1. **State acceptance criteria before the first run.** For example: no visible crossings in five views; face gap ≥ 4 mm; height
   per region within about ±5 mm of the reference hair; no flaps, horns or streaks; triangle budget. Report against them.
2. **Run one diagnostic pass first** (a few minutes): parts and triangles; share of each part under the scalp; largest lift
   per direction with the first-hit part; height per region; crossings by region. Fix whatever it flags upstream first.
3. **Build the chain one stage at a time.** Accept placement only when the largest lift is under about 3 cm, then add one
   stage and compare its stage strip. Never change two things between compared runs.
4. **Validate each experiment**: the intended change happened (pixel difference, selected asset, moved-vertex count), and
   nothing else moved (for example the root cap).
5. **Blender stage strip for decisions, Unity for acceptance.** One Unity pass at the end, with five views and close-ups.
6. **Report early.** Share the diagnostic and the plan before long tuning. The user sees defects that metrics miss.

## Quality levers that worked (reuse)

- Delete faces entirely more than 1.5 cm under the scalp before any scalp push.
- Split corrections by piece: guards on shells and the root cap, a per-lock curve for hanging locks.
- A crown compression anchored on the scalp, with one smooth factor per direction.
- Split triangles per part in proportion to `count^0.7`.

## Still open after the braid

- About 3x the pinholes of the bob (20 vs 6 in five views).
- Sides only 2.5 mm above the scalp (Original 19.9 mm).
- 13 crossing pairs at one hidden point inside the nape.
- Motion, cloth, face-shape combinations, iPhone.
