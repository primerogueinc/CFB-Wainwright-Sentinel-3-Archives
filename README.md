# CFB Wainwright fire: Sentinel-3 archive

Raw, unmodified Copernicus Sentinel-3 exports covering the Oct. 17, 2026 fire at CFB Wainwright, Alberta, kept so anyone can check the analysis in the [CFB Wainwright fire archive](https://github.com/primerogueinc/cfb-wainwright-fire-archive).

Sentinel-3 carries two imaging instruments:
- **OLCI**: colour, 21 bands at about 300 m. Sees smoke and burn scars; blocked by cloud.
- **SLSTR**: thermal, 1 km (fire channels F1 and F2, thermal S7-S9) and 500 m (shortwave S1-S6). Detects active fire by its heat, day and night.

Each folder `sentinel-3/<instrument>/<date UTC>/` holds the files exactly as exported from [Copernicus Browser](https://browser.dataspace.copernicus.eu/), a `manifest.json` (SHA-256 of every file, frame, pixel size, band values at the fire's origin, the Range 2 point and the road head, cloud check) and a preview.

## Exports

| Date (UTC) | Instrument | Files | Usable | Folder |
|---|---|---|---|---|
| 2026-10-16 | OLCI | 27 (21 bands + 6 layers) | No: cloud over the base | [`sentinel-3/OLCI/2026-10-16/`](sentinel-3/OLCI/2026-10-16/) |

Earlier OLCI exports for Oct. 4, 16, 17 and 18 (fewer bands) are in the fire archive under [`data/copernicus/manual_exports/sentinel3_olci`](https://github.com/primerogueinc/cfb-wainwright-fire-archive/tree/authentic-stoic-alternative-hypothesis/data/copernicus/manual_exports/sentinel3_olci).

## Adding an export

```
python3 scripts/ingest.py path/to/Browser_images.zip [--note "night pass"]
```

## Licence

Scripts and documentation: MIT (see LICENSE). Data: Copernicus Sentinel data are free and open under the [Copernicus data policy](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice); credit "Contains modified Copernicus Sentinel data [2026]" when reusing.

Maintained by Prime Rogue Inc.
