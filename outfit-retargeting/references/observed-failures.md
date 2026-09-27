# Observed failures - P09 female armour on CombatGirls (Unity 6000.6, 2026-09-28)

Local observations, not universal thresholds.

- One leg's armour seemed missing after the transfer: it was buried in the thicker target leg (vertex counts showed both legs). Push-out fixed it.
- Gloves floated at shoulder height: the weight-mapping helper walked up the parents and stopped at the first spine bone, so arm and leg weights went to the spine. The rest pose looked right; only animation showed it.
- After fixing that, nothing changed: overwriting the existing mesh asset with `EditorUtility.CopySerialized` dropped the arm piece's weights (34 bones built, 1 saved). Deleting and recreating the asset fixed it.
- Glove fingers stuck out straight: fingers had been carried rigidly with the hand. Per-finger segments fixed them; a finger joint the target lacks threw an exception that stopped the first piece (the top vanished) until missing bones fell back to their humanoid parent.
- White blobs on the chest had three causes in turn: large flat cloth triangles let the fuller target bust show between pushed vertices; an earlier stage had left the original full body on beside the masked copy; outward-only rays missed cloth sitting inside the skin. A capture with the body hidden proved the blobs were skin (the "two cloth layers swapped" hypothesis was wrong).
- The character stopped animating and its weapons froze (user report): a pose-holding capture script ran before Play mode had started, disabled the character script and Animator in the edit-mode scene, and the retargeter saved that scene.
- Long skirts and robes (3 of 12 sets) rose stiffly with the thigh in a lunge: skinned to the legs, same as the source without cloth physics.
- Numbers from the run: torso hips-to-neck 0.421 vs 0.358 m, upper-chest-to-neck 0.169 vs 0.085 m, max push-out 13-43 mm, covered body triangles 2,335-6,244 of 8,694 per set, 12 sets built in about 170 s.

Project evidence (quiz): `docs/character-system/outfit-retargeting.md`, `arca-client/Assets/Editor/P09OutfitRetargeter.cs`, `docs/character-system/references/measurements/2026-09-28-p09-on-combatgirls/`.
