# Verifying a sky in the Unity editor (Unity CLI)

Observed with Unity CLI 1.0.0-beta.8 and Unity 6000.6. Run `unity --help` and `unity command --project-path <project>` first; options change between versions.

## Connect

- `unity status --json` → `STATUS_NO_INSTANCES` while the editor is open means the project lacks the Pipeline package. `unity pipeline list --json` shows `hasPipelinePackage:false`. `unity pipeline install --project-path <project>` adds `com.unity.pipeline` to `Packages/manifest.json` (tell the user; it is a project change).
- The editor imports packages and scripts only when focused. Bring it forward (`open -a <Unity.app>` or `unity command editor_focus`) and poll `unity status` until connected.

## Compile and shader health

```bash
unity command --project-path <p> recompile --focus true      # then poll recompile_status
unity command --project-path <p> eval --code 'var s=UnityEngine.Shader.Find("<Shader/Name>"); return UnityEditor.ShaderUtil.ShaderHasError(s)+" msgs="+UnityEditor.ShaderUtil.GetShaderMessageCount(s);'
unity command --project-path <p> console --level error --tail 20
```

`recompile` completing does not cover shaders; check `ShaderHasError` explicitly.

## Capture the game view

- `capture_game_view --source screen --save_path X` (Play mode) rewrites the path to `Assets/X`. Save under `Assets/Temp/...`, copy the PNGs out, then `delete_asset --asset Assets/Temp --confirm true`, so captures never stay in the project.
- Reproduce camera angles by setting the rig's own state (e.g. `eval` with reflection on the pitch/yaw fields) rather than moving the camera transform, which the rig overwrites every frame. Restore the initial values afterwards.
- Sweep: the default view, both pitch limits, and opposite yaws. Stitch them into one grid (`ffmpeg ... xstack`) for review.
- Material values can be changed live in Play mode with `set_material_properties`, then captured immediately. The change is saved into the asset.

## Time-dependent effects (wind)

- An unfocused editor stops advancing `Time.time` even in Play mode, and two captures come out identical. Run `editor_focus`, then confirm that `Time.time` advances between two `eval` calls.
- Create a disabled temporary camera aimed at the sky, capture it twice with `capture_game_view --camera <name>` several seconds apart, measure the pixel difference, then destroy the camera.

## URP and CLI notes (Unity 6000.6, CLI 1.0.0-beta.8)

- **URP skybox shaders:** use `HLSLPROGRAM` with `Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl`. Read the sun from `_MainLightPosition`. A shader compiled before the URP package finished importing logs "Couldn't open include file"; reimport it and check `ShaderHasError`.
- **Materials created at runtime:** `Shader.Find` on a URP shader can be stripped from builds. Copy a template material asset instead.
- **Materials embedded in scenes:** a scene built by code stores its materials inside the scene file. After a pipeline switch, rebuild the scene with its builder rather than converting it by hand. Diff the hierarchy before and after.
- **`package_add`:** takes `--identifier name@version --confirm true --wait true`. The call can report a network error while the domain reloads. Confirm with `package_status` and by resolving a type from the package.
- **`eval` / `eval_file`:** the code runs as a method body, so `using` directives are not allowed. Fully qualify the types.
- **Timeouts:** "Main thread operation timed out after 5000ms" can be reported while the work still completes. Re-read the resulting state before retrying.
- **Waiting in Play mode:** loop `open -a <Unity.app>` (or `editor_focus`) and poll with `eval` until the cutscene or opening reports complete. Unfocused editors do not advance time.

## Evidence levels

Script compile, shader compile, a numeric coverage sweep, Game-view captures and hands-on play are different checks. Report which ran. Angle captures made with reflection count as camera-state reproduction, not as manual WASD/drag testing.
