---
name: outfit-retargeting
description: Refit skinned clothing, armour, weapons, helmets/hats and hair made for one rigged humanoid character onto a different humanoid body (other proportions, pose, skeleton names) in Unity - pose matching, per-segment proportion transfer, weight remapping, push-out, hiding covered skin, weapon sockets - and verify it with a pilot set, matched captures and motion poses.
---

# Outfit Retargeting

Developed from fitting the P09 female armour (12 sets, sword, shield) onto the CombatGirls body in Unity. The method is reusable; thresholds and bone names are asset-specific. Read [observed failures](references/observed-failures.md) before choosing a fix.

## Analyse with leader-thinking-trainer

When the user asks for analysis or a report, load `leader-thinking-trainer` first: conclusion, facts, what was and was not checked, eliminated hypotheses, next check. Mark claims as fact, inference or unverified.

## 1. Decide feasibility from the skeletons and bodies, not the clothes

Measure both characters at rest: humanoid bone positions (hips, neck, head, shoulders, hands, feet), rest pose (T vs A), bone names and counts, whether the body is one mesh or split per region, which submeshes of each outfit piece are skin, and which bones the piece is weighted to. Same-sex humanoids are usually feasible; the differences that matter are pose, segment lengths (e.g. torso +18 %, arms +13 %) and how each spine is split. A male outfit on a female-only body is not a fitting task.

## 2. Pilot one set with written acceptance criteria

State the criteria before the first run and report against them: no visible poke-through in four views; no creases at shoulders, elbows and hips in idle, run and attack; design matches the source side by side. Turn stages on one at a time and compare each from the same cameras. Only then run every set with the same code.

## 3. Transfer

1. **Pose:** apply the target's rest pose to the source through the humanoid rig (`HumanPoseHandler.GetHumanPose` on the target, `SetHumanPose` on the source) and bake the pieces (`BakeMesh`) in that pose.
2. **Proportions:** carry every vertex by the bone segments it is weighted to - scale the offset along the segment by the length ratio, keep the offset across it, rotate the segment axis onto the target's. Treat the spine as one hips-to-neck segment when the two spines are split differently; give fingers their own segments; replace a bone missing on either side by its humanoid parent.
3. **Weights:** keep the source's skin weights and map each bone to the target bone of its nearest humanoid ancestor. Do not re-transfer weights from a different body surface.
4. **Skin submeshes:** drop the source pieces' own skin; the target body shows instead.
5. **Push-out:** move vertices within a few millimetres of the target body outward, smoothing the move along the piece.
6. **Hide covered skin (decisive):** per outfit, copy the target body without the triangles the outfit covers - a triangle is covered when rays from its corners and centre along **both** normal directions meet the outfit within a few centimetres - and keep the original body off. Push-out alone leaves curved skin between large cloth triangles and fails in motion.
7. **Weapons:** read the source socket (constraint source, offsets; pick the hand source when a constraint also has a carry source), keep the weapon's world rotation and offset from the hand in the matched pose, and parent it to the target hand. Bake skinned weapons (bows) to static meshes.
8. **End bones** (head, hands, finger tips, toes) have no direction: carry them without rotation. Using each rig's local up axis turned helmets around the head.
9. **Headwear:** keep the source size, align by a clear landmark, and fit it over every target hair: a uniform scale about the head centre from the hair's outer radius (a high percentile), applied through one pivot bone under the head that the helmets are skinned to, not one object per helmet and hair.
10. **Hair:** carry it with the head and push it out of the head and face; hair bones follow the head by a constraint the editor does not evaluate, so move the hair from the rest head to the matched head. For sway, keep the bone chains: copy the hair skeleton (with its head colliders, without the constraint) under the target head by the same transform and weight the hair to the copies.
11. **Separate pieces:** list every source renderer of a set (cloaks and capes are often separate renderers under the chest) and compare with the pieces transferred. Pieces that hang free and swing do not hide skin.
12. **Cloth physics:** copy the vendor's cloth components and parameters as they are; move only what is tied to position - painted selections (stored in the cloth's local space; move each point like its nearest vertex, since mesh-cloth points sit on a reduced proxy) and colliders (same segment transfer, lengths scaled with the segment). Turn off pre-built data (it references the source's transforms). Recreate the init data in the editor from the target's rest pose, clearing its version and hashes first: some tools only store new data when the hash differs, and a copied bone skeleton hashes the same as the source.

In editor scripts use `TryGetComponent`: a missing component comes back as a fake null that passes `is`. Save derived meshes by deleting and recreating the asset: `EditorUtility.CopySerialized` into an existing mesh dropped skin weights. Keep derived meshes of purchased assets out of git and regenerable by a menu command.

## 4. Verify

- A sheet per set: idle front/side/back plus an attack pose; the source side by side for design.
- Count distinct weighted bones after saving; one bone means lost weights.
- Close-ups of chest, shoulders, hands; motion poses at several normalized times.
- The switch UI shows exactly one outfit and restores the original.
- After any tool that saves the scene, check the character script and Animator are still enabled.
- Report long skirts/capes that follow the legs as a physics task, separately from fitting.
- Cloth: every cloth's status (valid, running, init data used) while switching pieces mid-animation; the same frames with physics off and on, measuring tips and hems relative to their parent bone; the console.

Judge placement against the source side by side before "fixing" it. Isolate a visual defect by turning one thing off (hide the body, hide one piece) before theorizing. Scripts that disable components to hold a pose must refuse to run outside Play mode. Build the temporary source and target instances in a preview scene, so they can never be saved into the working scene. Before trusting positions in the working scene, check the character is in its rest pose; scenes can be saved in an animated pose. Read the configuration of the prefab the vendor actually uses (a variant can differ from the base).

Keep project constants and scripts in the project; promote only verified rules here (source `dev/skill-me/outfit-retargeting`, linked into `~/.claude/skills` and `~/.codex/skills`).
