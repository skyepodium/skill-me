# Blender / GLB pitfalls observed in asset refinement

These checks come from a Blender 5.1.2 → GLB → model-viewer workflow. Recheck version-specific behavior in the current installation. The specific scripts used by the train project are examples, not portable algorithms.

## Black patches or disappearing contours

Inspect whether the defect belongs to the source mesh, hull geometry, or material culling.

- UV seams can duplicate vertices at the same position. Weld with a scale-aware tolerance that does not join intentional gaps or adjacent pieces, while retaining per-corner UV data.
- Orient connected surfaces consistently. Signed volume is useful for closed components; do not blindly use it to orient open sheets.
- Expand along appropriate normals, then reverse hull faces. A large offset or bad normals can produce spikes or black internal fragments.
- Inverted hulls require back-face culling. Double-sided black hull materials can cover the body. Blender renderer settings and GLB `doubleSided` are separate checks.
- In the train project, Blender preview used a backfacing/transparent shader arrangement while GLB used single-sided materials. That was an environment-specific solution, not an export guarantee for arbitrary node graphs.
- Fix the source of a contour failure rather than deleting all outlines when outlines are required by the design.

## Texture or color changes after export

- Decide whether the asset should be unlit or should respond to lighting. Unlit preserves authored colors but will not demonstrate a dynamic toon light ramp.
- Inspect the exported material and embedded images. A node graph that looks correct in Blender may not export as intended.
- In the train exporter, emission materials were converted to `KHR_materials_unlit`. The conversion needed to carry **both color and texture** to the base-color material; retaining only an emissive factor lost the texture.
- Verify RGB conversion and color management if a manually assigned color changes appearance. Avoid repeated sRGB/linear conversion without checking what each interface expects.
- Prefer supported exporter behavior. If the project already patches GLB JSON, preserve binary chunks, alignment, texture references and unrelated material properties. Do not introduce binary rewriting just because the train project used it.

## Export contains an old body

A root name such as `station-lamp` does not prove the object is an empty. Inspect type, mesh ownership, children, local transforms and collection membership. Replacing children alone can retain the rejected parent mesh. Inspect the actual exported hierarchy and selected export objects; viewport/render hiding may not exclude objects.

Keep the immutable assembly source separate from the rebuilt result. Avoid accidentally making the latest derived scene the next build's input and accumulating outlines or helpers on every run.

## Roof seams and frame boundaries

An inverted hull primarily describes silhouette. Coplanar adjacent parts can hide one another's contours. First correct spacing and actual geometry, then trace only needed internal boundaries.

Surface-following strokes may use source face contours or ray intersections. Check misses and joints, endpoint contact, both roof slopes, surface offset and export conversion. A nearest-point fallback can conceal a real gap or introduce a floating line; inspect it instead of treating the fallback as proof of correctness.

## Fit and animation

Measure contact in scene coordinates, not only local bounding boxes. A standalone bottom-centered pivot can be correct while the asset floats after placement. Preserve accepted assembly transforms explicitly.

For mechanical motion, test the affected invariants: level body, wheel centers, axle directions, route clearance and return to start. A plausible still image is not evidence of rolling contact.

## Minimal evidence record

```text
Asset / preserved source / reference:
Features protected / observed defects / changes:
Source integrity and relevant output checks:
Matched source/corrected views:
Blender views / target viewer views / scene-scale check:
Existing movement checks, if affected:
Remaining defect / technical result / visual result / user adoption status:
```
