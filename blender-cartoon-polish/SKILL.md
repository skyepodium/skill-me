---
name: blender-cartoon-polish
description: Refine existing Meshy or other generated 3D assets in Blender for a reference-led cartoon look while preserving source geometry and useful textures; verify outlines, materials, placement, and exported GLB in the target viewer. Use for 카툰 에셋 보정, Meshy 원본 재보정, 검은 외곽선 개선, or Blender-to-GLB visual regressions. Focuses on existing assets, not new model generation or a general-purpose toon shader system.
---

# Blender Cartoon Polish

Improve an existing generated asset without discarding what makes the source work. Use the user's reference and the project's design contract to decide what to preserve, repair, and verify. The default technique here is fixed color regions plus outlines, not a claim of lighting-responsive toon shading.

## Establish the correction

- Locate the requested asset, preserved generation source, current derived version, reference image, scene assembly script, and relevant `DESIGN.md` or equivalent. Inspect actual images/models rather than inferring quality from filenames or reports.
- If the user asks to restart from the Meshy original, import that original. Keep it unchanged and retain a recoverable copy of the rejected version outside the active scene. If the original cannot be located, say so; do not silently treat the rejected derivative as the original.
- Record a short asset-local correction note: **preserve / observed defects / intended changes / fit constraints / evidence needed**. Reuse the project's existing report format. This is an implementation record, not a permission gate.
- Identify part roles before assigning colors. Source texture similarity, object names, height thresholds, and disconnected components are clues, not universal semantic labels.
- Determine the intended rendering contract. Near-black contours are central to the train project that informed this skill, but follow another project's outline color, line-free style, or lighting requirements when specified.

## Work in Blender

Use available Blender integration or the installed Blender CLI/Python API. Inspect local build scripts before writing new ones. Discover paths and supported options in the current environment; do not assume a particular machine, Blender version, or MCP connection.

Prefer narrow corrections:

- **Geometry:** level or align defective features; fix pivots, wheel axes, contact and spacing when relevant. Preserve source topology, rounded edges and proportions where they already work. Fit structural assets to actual contact dimensions rather than blindly forcing uniform scaling.
- **Materials:** preserve useful UV textures. Replace only regions with demonstrated contamination or unreadable color roles. A roof can need clean mint faces while posts keep their texture. Do not quantize the entire asset into the palette of a previously successful asset.
- **Silhouette:** if using inverted hulls, inspect seam welding, winding, closure and scale before expanding. Keep the hull and body in the same transform/animation hierarchy. Calibrate width to the asset's final on-screen size.
- **Internal boundaries:** hulls do not reliably draw window frames or roof-board seams. Add selected contours following the actual surface when the reference needs them. Avoid triangle-edge wireframes, hovering strokes, z-fighting and an unrelated cover mesh that hides the source shape.

For export-specific failures, read [Blender and GLB pitfalls](references/blender-glb-pitfalls.md). For analogous repair decisions, read [Observed cases](references/observed-cases.md). Use those as evidence, not a universal recipe.

## Integrate and compare

- Inspect the old root's object type before replacement: a named asset root may itself be a mesh. Remove the rejected body and its helpers from the export set, preserving required placement and animation. Hiding it in the render is insufficient.
- Keep corrections reproducible in the project's builder where one exists. Export the standalone asset and update the assembled scene when that is part of the requested scope.
- Compare reference, source and corrected model. Match source/corrected camera, background and projected size; use the input image for shape and color roles rather than pretending its perspective is identical.
- Inspect front, oblique and rear views in Blender **and the actual target viewer**. Also inspect final scene scale, connections and clearance. Test an animated asset at meaningful times, not only frame one.
- If the target viewer cannot run, deliver the verified artifacts and explicitly identify the missing runtime check. Do not claim a screenshot or viewer validation that was not performed.

## Completion evidence

Choose checks that prove the change, not a generic large test suite:

- Source is unchanged; the output contains the intended bodies/helpers without rejected duplicates.
- Exported textures, material mode, face culling and outlines survive loading. Closed-part expectations apply to the chosen hull technique, not all 3D assets.
- Dimensions, grounding, pivots and existing motion relevant to the changed asset still work.
- Screenshots show the original defects improved without losing the protected features. Numeric validation alone does not prove aesthetic improvement.

Report **technical checks**, **visual inspection**, and **user adoption** separately. Stop once the scoped correction is verified; do not polish neighboring assets, generate paid replacements, publish, or push merely because this skill was invoked. Do not require a new approval round for authorized local edits. Record any visible remaining defect instead of expanding into indefinite polishing.

For a family of assets, establish the method on a representative asset before applying it broadly. Transfer principles; re-evaluate segmentation, dimensions, colors and line width per asset. New observations belong in the local design/lesson record; promote them to this skill only when the user requests a skill update.
