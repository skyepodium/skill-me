# Observed cases: Train sea station, 2026-09-19

Evidence originated in the train project's `DESIGN.md`, `docs/asset-polish-lessons.ko.md`, per-asset rework reports, Blender scripts, renders and GLB checks. These are bounded observations from a stylized static-prop pipeline. They do not establish a universal cartoon aesthetic or validate animated characters and dynamic toon lighting.

| Case | Observation and useful decision |
| --- | --- |
| Train | Separating body, windows and wheels made level correction, regular windows and independent wheel rotation possible. The user reported improvement. Repair structure as well as appearance when the defect is mechanical. |
| First station-wide polish | Blanket palette conversion confused material roles, and deleting contours to hide dark patches weakened the requested look. The user preferred the raw Meshy models. Reassess the source per asset instead of copying the train's treatment. |
| Lamp | Restarted from the raw model, preserved glass/frame UV texture, corrected roof/pedestal colors, and added silhouette plus four glass boundaries. An old mesh masquerading as the parent remained in one export and had to be removed explicitly. |
| Bench | Kept six generated parts and their proportions. Original mint-frame texture survived; wood-only colors replaced mint texture streaks on boards. Part outlines and a small back-board gap improved separation. Six parts was a fact about this source, not a required bench topology. |
| Platform | Kept a generated deck and four footed piers, retained pier texture, and cleaned only deck/marking colors. Preserved the deck's accepted scene height while extending supports to meet the water. Structural fit justified changing proportions. |
| Shelter | Reused 42 generated parts, including 22 roof boards. Narrowed uneven gaps, removed rejected roof-cover helpers, retained cream frame/slate-foot texture, and cleaned roof-only color contamination. Added selected roof seams after hull-only boundaries remained weak. Board count still differed from the input image; this was source-preserving correction, not exact reconstruction. |

The lamp, bench, platform and shelter passed recorded technical checks and were visually inspected. Do not promote those facts into blanket user aesthetic approval. The user calling an asset “better” is also narrower than adopting every detail of a pipeline.

## Contextual parameters, not defaults

The project used near-black `#171B24` contours for new props, mint roofs, cream frames and slate feet. Typical hull widths varied with asset size: roughly 0.003 on a 1.28-wide bench and 0.0045–0.006 on a 2.30-wide shelter. A 1–2px contour at a 1080p game view was a trial target, not a measured guarantee across all cameras.

Never copy these world-space widths, part counts, axis assumptions, semantic height thresholds or palette choices into another generated mesh without checking its scale and intended style. Color similarity does not identify a part's function.

## What remains unproven

- A reusable toon shader responding to changing light and shadow.
- Character skinning, facial expression and deformation-safe contours.
- Stable line thickness across arbitrary perspective distances and resolutions.
- Perceptual superiority based only on file validity, mesh count or geometry tests.

When asked for one of these, identify it as additional work and validate it in the intended renderer rather than claiming the static-prop recipe already solves it.
