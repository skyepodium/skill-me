---
name: hair-fitting
description: Fit generated or outsourced 3D hair (bobs, layered or braided styles) to an existing character head in Blender and Unity; diagnose scalp penetration, wig-like volume, a raised crown, face-framing locks cutting the face, flaps/horns/streaks after fitting, floating bangs, crumpled strands and blotchy shading; and preserve the hairstyle while validating the fitted result.
---

# Hair Fitting

Developed from a CombatGirls Face_04 + Tripo Short1/2/4 and braid pilot. The workflow is reusable; its geometry parameters are not a general fitting recipe. Read [observed failures](references/observed-failures.md) when selecting a correction method.

## Analyse with leader-thinking-trainer first

Every diagnosis and every report of a result MUST use the `leader-thinking-trainer` skill: load it before analysing. State the conclusion first, then the facts that prove it, what was checked and what was not, the hypotheses eliminated and how, the remaining unknowns, and what the next check will decide. Mark each claim as fact, inference or unverified. When a later measurement contradicts an earlier claim, say so explicitly and correct the record.

Isolate the cause before changing geometry. Render the source, each derived stage and the current output with the same camera, lighting and material, so a defect is pinned to the stage that introduced it. Symptoms often have a different cause than the user's words suggest (see "Shading" below).

## Measure before correcting

Most wasted iterations came from tuning a correction before knowing what drove it. Before changing geometry, record:

- **Largest lift per direction after placement, and the first hair part hit from the head centre.** A scalp push-off that lifts "every layer by the first hair met from the centre" is only as good as that first hit. A hidden interior fold 4 cm from the centre lifted a whole crown back by 7 cm; the fix was deleting faces that lie entirely deep under the scalp, not rescaling.
- **Share of each part under the scalp.** If the largest part (the inner skull shell) is under the scalp, the placement scale is wrong. If only small parts are deep inside, they are hidden filler.
- **Hair height above the scalp per region** (crown, crown back, back, sides, front top), next to the reference hair.
- **Where crossings are**, grouped by region: face-framing locks and skull shell need different corrections.

## Establish the fit

Locate the unmodified source, active derived hair, builder and target head. Preserve source hashes and a recoverable previous output before overwriting anything. Record what the user wants preserved: parting, bangs, length, tips, asymmetry and silhouette.

Check what the source actually contains before judging "texture" problems: UV layers, images, material count. Generated hair downloaded without textures has no UVs; a vendor preview image is not the file.

Read the actual target geometry including scalp shared with the body, face, ears and relevant neck/shoulder areas. Identify units, axes, attachment transform and neutral pose. A face-only mesh is often not the complete head. A style reference is not a mandatory width for every hairstyle.

Compare hair alone and hair on the head at the same pose and camera. Distinguish missing geometry, head penetration, backface culling, material transparency and intentionally open partings. Added root caps must be measured separately from original locks.

## Choose a bounded correction

- Align by anatomical landmarks; whole-asset bounds can be dominated by long strands, a ponytail or a braid. Scale by the cranial band (a few centimetres below the crown), then fit the inner skull shell to the scalp plus a small gap. Judge the resulting volume only after the thickness/crown step; the shell fit alone looks like a wig and was rejected prematurely once.
- Consider scalp clearance, outer silhouette and strand preservation together. Outward-only collision correction can inflate the hair into a wig; uniform shrink can penetrate the scalp.
- **Wig-like volume:** keep the inner layer and compress thickness per direction toward the reference hair's outer envelope, `r' = r_in + (r - r_in) * k`. Measure `r_in`/`r_out` over a neighbourhood of roughly a centimetre on the head, not one small angular bin: near the crown a bin holds only outer-layer vertices and blocks compression. Anchor `r_in` at least a clearance above the local scalp, or the neighbourhood minimum follows a lower part of the skull and collapses layers onto the floor. Keep a minimum layer thickness where the reference is a single thin shell.
- **Bangs over the face are one layer:** thinning does not move them. Measure the face-to-fringe gap separately (region below the usual crown/forehead rays) and translate the fringe inward toward the reference, limited by a face clearance.
- **Dense meshes crumple under per-vertex motion.** Smooth the displacement along the mesh (not the positions) so a strand's front, back and neighbours move together, then re-apply the scalp floor. A method validated on a ~10k-triangle hair must be re-checked, not reused, on a 60k one.
- Guards must not undo the correction. Reverting turned faces toward the input with wide neighbour rings lifted a whole clump back up; smooth the local displacement instead. If the input itself crosses the head, reverting cannot fix it: push crossing faces outward in small steps.
- Identify root/bang/side/back/tip regions where the method needs them. Disconnected components are clues, not proof of strand semantics.
- **Split corrections by piece, not by height.** Every on/off boundary in space (a height or front/back cut-off, or a fade band) folded the strands crossing it into flaps or horns. Give the large shells and the root cap the push/guard corrections; move each hanging lock as a whole.
- **Face-framing locks that cut the face:** bend each lock as one smooth curve along its height, sized by that lock's own clearance deficit, along the local face normal (sideways at the cheeks, forward over the eye corners). Moving every vertex at a height by the neediest lock's amount flared the others into wings; per-vertex pushes made hooks and waves.
- **Raised crown on layered hair:** compress toward the scalp with one smooth factor per direction, `r' = s + (r - s)k`, anchored on the scalp surface. A neighbourhood inner-hair anchor jumped between layers and folded them into spikes. Run crossing guards before this step; running them after it raised small flaps at the parting.
- **Reduction budget:** split triangles per part in proportion to `count^0.7` (not linearly); thin long locks otherwise fold into zig-zags.
- Preserve layered spacing. Projecting every layer to the same scalp surface can collapse thickness and create flicker.
- For long curls, looping strands or strongly concave regions, radial order does not identify semantic layers. Restrict radial fitting to a validated scalp-adjacent region.
- Root backing must follow intended coverage. Inspect it on/off through the bangs and parting.
- When constraints conflict, use a local manual correction or reject that derivative. Do not hide the defect by deleting the head or expanding the hair without limit.

Render every stage from the same cameras in one strip before judging. The first stage where a defect appears is its cause; the user's word for it ("broken texture") often names a different mechanism (crossing layers, flipped flaps, pinholes).

Develop on one representative hair before transferring a method to others, and re-verify each transfer. Keep per-asset parameters and source-derived outputs reproducible. Bake final placement once; do not normalize again on Unity import.

## Shading

Blotchy light/dark patches on untextured hair are usually back faces, not a broken texture or a bad reduction. Generated strands are often open sheets; a two-sided lit material shades the back faces with the front normal. Prove it by rendering the same frame with both sides, front only and back only. If front-only removes the blotches without exposing holes, cull back faces (or use a shader that flips normals on back faces). Check every hair that shares the material, and the upward camera angles where back faces could matter.

Count open edges, not their ratio, before blaming decimation for holes: collapse reduction keeps boundary edges while removing interior ones, so the ratio rises without new holes.

## Verify before adoption

Before comparing two captures, prove they differ (pixel difference or the selected state): a capture of the wrong hair and a render without the new blend weights each produced a wrong conclusion. Use matching front, oblique, side, back and top views in both the modeling tool and the actual target viewer, plus the user's own reported angle. Include close-up inspection of changed regions. Control character pose as well as camera; a paused screen capture may be stale, so verify the capture source produces a fresh render.

Measure bounds and region-specific gap distributions, including minima, against the reference hair: crown, front, sides, back and the fringe over the face. Median radial distance is not a collision test. Test triangles against the head surface; vertices can lie outside while a face passes through. Report root-cap and lock results separately. Check deformation area ratios and large normal changes as review flags, not as automatic proof of inverted geometry. Numbers can look right while the render is wrong (over-compression can pass every metric and still look shredded); the image decides.

State limitations of the checker: open surfaces invalidate naive inside/outside tests; sampled points miss unsampled intersections; segment tests may exclude coplanar or endpoint contact. A zero count proves only the tested geometry and conditions.

Static fitting, attachment, facial-shape compatibility, animation, cloth and device performance are separate states. Do not claim an unrigged rigid preview meets moving-hair quality. After rigging, inspect continuous running, attacks, turns, stopping, facial changes and shoulder contact, plus hair-switch/teleport initialization.

## Capture reusable learning

Record each attempted method, parameter/source version, measurements, matched captures, rejection reason and adoption status in the project. Promote verified decision rules to this skill (source: `dev/skill-me/hair-fitting`, linked into `~/.codex/skills` and `~/.claude/skills`); retain asset-specific constants and experimental scripts in the project. Never turn one successful head/style into universal compatibility.
