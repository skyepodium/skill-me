# Observed fitting failures

CombatGirls Face_04 + generated Short1/2/4 and a braid, 2026-09-27. These are local observations, not universal thresholds.

## Volume and clearance (Short1 pilot)

- Outward-only fitting removed large visible scalp exposure but produced excessive outer volume. Inner side/back layers were closer to the scalp than Original despite a larger silhouette. Measure inner and outer envelopes separately.
- A root cap added for rear coverage showed a straight forehead edge through the bangs. Matching cap-on/off captures isolated the cause.
- A direct scalp-relative radial compression retained pre-existing head intersections and caused large normal changes in thin faces. A monotone radial formula alone did not ensure acceptable render triangles.
- A smooth fitted cage with a global residual margin removed tested head crossings but over-compressed some thin surfaces. A collision-free count did not make this an acceptable hairstyle.
- Scaling and translating whole disconnected parts preserved each part's surface, but a large wrapping part required excessive translation and left a visibly broken root arrangement. Disconnected Tripo parts were not a reliable semantic decomposition.
- Modest affine volume reduction plus a conservative shared angular outward field worked for Short1 (~11k triangles).

## Thickness compression (Short1/2/4)

- Keeping the inner layer and compressing thickness toward Original's outer envelope reduced the wig look (Short1 outer side gap 26.6 → 13 mm, Original 13.1). Crown barely moved at first: 5° bins near the pole held only outer-layer vertices, so thickness read as zero. Neighbourhood r_in/r_out fixed it.
- Taking the neighbourhood minimum pulled the anchor under the scalp toward the nape and pushed the back into the head (491 crossings). Anchoring at scalp + clearance per direction fixed it.
- Stronger compression matched the crown numerically (13.5 mm vs 14.8) but rendered shredded strands and dark patches; rejected on the image.
- A normal guard that reverted turned faces plus three neighbour rings toward the input re-lifted a whole crown clump (19.6 mm above Original); smoothing the local displacement instead brought it to 3.5 mm.
- The affine + angular field step validated on Short1 crumpled the bangs of the dense Short4 (62k triangles); per-vertex thickness mapping made it worse. Skipping that step and smoothing the displacement along the mesh (60 passes) kept strands clean.
- Short2/4 still crossed the head after the Short1 pipeline (root cap 2.5 mm vs 4 mm). Reverting toward a crossing input cannot fix it; pushing crossing faces outward did.

## Bangs and shading

- The usual crown/forehead rays (15–85° from the head centre) missed the fringe hanging over the face. Measured separately, it floated 12–17 mm from the face (Original 8.3). Thinning cannot move a single-layer fringe; translating it inward reduced this to 9–12 mm.
- "Broken texture / blotchy" on untextured Tripo hair was back-face shading: open sheets rendered two-sided with URP Lit. Front-only culling removed it on all three hairs without exposing holes.
- A claim that reduction opened holes was wrong: the open-edge ratio rose (1.1 → 18%) only because interior edges were removed; the open-edge count fell.

## Layered braid (Tripo, 1.9M triangles, 115 parts, no UVs)

- Placement by the cranial band left the inner skull shell up to 7 cm inside the skull; the scalp push-off lifted the back by 7.9 cm and the thickness step pulled it back 6 cm, crossing layers into torn streaks at the back (the user's "broken texture").
- Deleting parts mostly under the scalp (50 %) also caught the main shell and left the sides bald. Fitting the shell to the scalp first, then deleting faces entirely 1.5 cm under the scalp, removed 406 hidden faces and brought the largest lift from 72 mm to 17.6 mm (Short1/2/4: 18–27 mm).
- The remaining high crown (35.5 mm vs 13–19 mm) was the style's own layer thickness. The neighbourhood thickness step folded layered strands into spikes; a scalp-anchored smooth factor per direction lowered it to 16.3 mm cleanly.
- Face-framing locks cut the cheeks by ~13 mm. Tried in order: per-vertex push (hooks, waves), rigid move per connected piece (moved the root cap too — an invalid test, later misreported as "splits locks"), one bend per side and height (wings, horns), per-lock curve along the face normal (adopted; 14 locks, max 7.4 mm).
- Guards switched by height (z 1.56, 1.62, 1.70) or with a fade each left a fold at the boundary. Excluding small pieces from the guards instead removed every flap.
- A 30k triangle budget split linearly by part folded thin side locks; 45k split by `count^0.7` matched a 90k linear split visually.
- Remaining: 13 crossing pairs at one point inside the nape, about 3x the pinholes of the bob (20 vs 6 in five views).

Project evidence, when working in quiz: `docs/character-system/hair-fitting.md`, `docs/character-system/references/measurements/2026-09-27-hair-volume-fit/`, `…/2026-09-27-hair-thickness-fit/`, `scripts/blender/hair_volume_fit.py`, `scripts/blender/hair_thickness_fit.py`, `scripts/blender/fit_braid_hair.py`, `hair_crown_compress.py`, `hair_lock_bend.py`; braid section of `docs/character-system/hair-fitting.md`. The skill does not depend on those paths in other projects.
