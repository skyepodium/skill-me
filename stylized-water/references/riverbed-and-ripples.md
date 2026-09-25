# Riverbed and ripple normal map

## Riverbed seen through the water (terrain shader snippet)

The water is translucent, so whatever the terrain draws under the surface shows through. Paint sand with pebble patches below the water line. This goes inside the terrain's fragment shader, after the land colours are chosen:

```hlsl
// _WaterSurfaceY: world height of the water plane. _RiverbedColor / _RiverbedPebbleColor: sand and pebbles.
half underwater = smoothstep(_WaterSurfaceY - 0.02, _WaterSurfaceY - 0.12, input.world.y);
half pebbles = smoothstep(0.45, 0.65, MeadowFbm(xz * 3.0 + 21.0));
half3 riverbed = lerp(_RiverbedColor.rgb, _RiverbedPebbleColor.rgb, pebbles);
ground = lerp(ground, riverbed, underwater);
```

Carve the channel in the terrain heightmap so the bed sits well below the water plane (e.g. −0.35 m against a surface at +0.045 m). Share the river half-width between the terrain generator and the water material from one constant.

## Tileable ripple normal (editor C#)

Heights come from value noise on a lattice that wraps every `frequency` cells, so the map tiles. Normals come from central differences, and the result is imported as a Normal Map with Repeat wrapping. Reuse the `TileableFbm` / wrapped value-noise helpers from the `worley-cloud-noise` baker or any wrapped noise.

```csharp
private static string WriteRippleNormal(string path, int size = 256, int frequency = 8, float slopeScale = 6f)
{
    var heights = new float[size, size];
    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++)
            heights[x, y] = TileableFbm(x / (float)size, y / (float)size, frequency, 3);
    var texture = new Texture2D(size, size, TextureFormat.RGBA32, false, true);
    for (int y = 0; y < size; y++)
    {
        for (int x = 0; x < size; x++)
        {
            float dx = (heights[(x + 1) % size, y] - heights[(x - 1 + size) % size, y]) * slopeScale;
            float dy = (heights[x, (y + 1) % size] - heights[x, (y - 1 + size) % size]) * slopeScale;
            Vector3 normal = new Vector3(-dx, -dy, 1f).normalized;
            texture.SetPixel(x, y, new Color(normal.x * 0.5f + 0.5f, normal.y * 0.5f + 0.5f, normal.z * 0.5f + 0.5f, 1f));
        }
    }
    texture.Apply();
    File.WriteAllBytes(path, texture.EncodeToPNG());
    Object.DestroyImmediate(texture);
    AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
    var importer = (TextureImporter)AssetImporter.GetAtPath(path);
    importer.textureType = TextureImporterType.NormalMap;
    importer.wrapMode = TextureWrapMode.Repeat;
    importer.SaveAndReimport();
    return path;
}
```
