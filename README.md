# CFB Wainwright fire: Sentinel-3 archive

Raw, unmodified Copernicus Sentinel-3 exports covering the Oct. 17, 2026 fire at CFB Wainwright, Alberta, kept so anyone can check the analysis in the [CFB Wainwright fire archive](https://github.com/primerogueinc/cfb-wainwright-fire-archive).

Sentinel-3 carries two imaging instruments:
- **OLCI**: colour, 21 bands at about 300 m. Sees smoke and burn scars; blocked by cloud.
- **SLSTR**: thermal, 1 km (fire channels F1 and F2, thermal S7-S9) and 500 m (shortwave S1-S6). Detects active fire by its heat, day and night.

Each folder `sentinel-3/<instrument>/<date UTC>/` holds the files exactly as exported from [Copernicus Browser](https://browser.dataspace.copernicus.eu/), a `manifest.json` (SHA-256 of every file, frame, pixel size, band values at the fire's origin, the Range 2 point and the road head, cloud check) and a preview.

## Exports

**Pass times.** Copernicus Browser exports carry only the UTC date; the time of the pass is not in the files. `pass_times.csv` lists every Sentinel-3A and 3B pass over the base from Oct. 10 to 25, predicted from published orbital elements by `scripts/pass_times.py` (S3B times may be off by up to about a minute). Day passes are late morning to early afternoon MDT; night passes 10-11 p.m. MDT, dated the next day in UTC. On Oct. 17 the day passes were at 11:33 a.m. (S3B, base near the swath edge) and **12:11 p.m. MDT (S3A, almost directly overhead)**. A day export is a mosaic of that UTC day's day passes; which pass a given pixel comes from is not recorded.

| Date (UTC) | Instrument | Files | Usable | Folder |
|---|---|---|---|---|
| 2026-10-22 | SLSTR L1B (day) | 23 | Yes: Day pass. Clear (0% cold cloud). No hot pixels: no active fire. | [`sentinel-3/SLSTR/2026-10-22/`](sentinel-3/SLSTR/2026-10-22/) |
| 2026-10-21 | SLSTR L1B (day) | 23 | Yes: Day pass. Clear (0% cold cloud). No hot pixels: no active fire. | [`sentinel-3/SLSTR/2026-10-21/`](sentinel-3/SLSTR/2026-10-21/) |
| 2026-10-20 | SLSTR L1B (day) | 23 | Yes: clear. No active fire | [`sentinel-3/SLSTR/2026-10-20/`](sentinel-3/SLSTR/2026-10-20/) |
| 2026-10-19 | SLSTR L1B (day) | 23 | Yes: mostly clear. No active fire | [`sentinel-3/SLSTR/2026-10-19/`](sentinel-3/SLSTR/2026-10-19/) |
| 2026-10-18 | SLSTR L1B (day) | 23 | Yes: clear. No active fire. Burn scar visible (near-infrared halved, surface ~1.6 K warmer) | [`sentinel-3/SLSTR/2026-10-18/`](sentinel-3/SLSTR/2026-10-18/) |
| 2026-10-17 | SLSTR L1B (day) | 23 | Yes, with limits: heat at the fire seen through thin cloud. Strongest anomalies in the frame at the origin (S7 +17 K) and about 1.5 km east-southeast (F1 +18 K); 1 km pixels | [`sentinel-3/SLSTR/2026-10-17/`](sentinel-3/SLSTR/2026-10-17/) |
| 2026-10-16 | SLSTR L1B (day) | 23 (S1-S9, F1, F2 + layers) | No: cloud over the whole frame (11 µm brightness temperature below 270 K everywhere, cloud tops near -16 °C); no fire signal possible | [`sentinel-3/SLSTR/2026-10-16/`](sentinel-3/SLSTR/2026-10-16/) |
| 2026-10-16 | OLCI | 27 (21 bands + 6 layers) | No: cloud over the base | [`sentinel-3/OLCI/2026-10-16/`](sentinel-3/OLCI/2026-10-16/) |

### SLSTR L2 (land surface temperature, NDVI)

| Date (UTC) | Product | Files | Usable | Folder |
|---|---|---|---|---|
| 2026-10-17 | LST + NDVI | 4 | No: cloud over the base (fire-area median -9 °C). LST is an 11-12 µm product and shows no fire signal through cloud; the noon heat at the fire is in the L1B mid-infrared channels | [`sentinel-3/SLSTR_L2/2026-10-17/`](sentinel-3/SLSTR_L2/2026-10-17/) |
| 2026-10-16 | LST + NDVI | 4 | No: Cloud over the base (fire-area median 268.5 K, -5 °C); values are cloud tops, not usable. NDVI 0.11-0.12, half of Oct. 15 | [`sentinel-3/SLSTR_L2/2026-10-16/`](sentinel-3/SLSTR_L2/2026-10-16/) |
| 2026-10-15 | LST + NDVI | 4 | Yes: clear. Pre-fire baseline (fire area about 11 °C, NDVI 0.22-0.29) | [`sentinel-3/SLSTR_L2/2026-10-15/`](sentinel-3/SLSTR_L2/2026-10-15/) |
| 2026-10-14 | LST + NDVI | 4 | No: cloud over the base (values are cloud tops, about -20 °C) | [`sentinel-3/SLSTR_L2/2026-10-14/`](sentinel-3/SLSTR_L2/2026-10-14/) |

Earlier OLCI exports for Oct. 4, 16, 17 and 18 (fewer bands) are in the fire archive under [`data/copernicus/manual_exports/sentinel3_olci`](https://github.com/primerogueinc/cfb-wainwright-fire-archive/tree/authentic-stoic-alternative-hypothesis/data/copernicus/manual_exports/sentinel3_olci).

## Adding an export

```
python3 scripts/ingest.py path/to/Browser_images.zip [--note "night pass"]
```

## Licence

Scripts and documentation: MIT (see LICENSE). Data: Copernicus Sentinel data are free and open under the [Copernicus data policy](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice); credit "Contains modified Copernicus Sentinel data [2026]" when reusing.

Maintained by Prime Rogue Inc.
