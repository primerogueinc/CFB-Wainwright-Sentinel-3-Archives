# Sentinel-3 SLSTR fire radiative power (SL_2_FRP), Oct. 18, 2026 passes

Added Nov. 27, 2026. Source: Microsoft Planetary Computer, `sentinel-3-slstr-frp-l2-netcdf` (non-time-critical products). Planetary Computer carries only the 1 km MWIR fire file (`FRP_in.nc`), not the 500 m SWIR files. Each folder also has the product manifest and the 1 km cloud and land flags (`flags_in.nc`). Checksums in `SHA256SUMS`. Contains modified Copernicus Sentinel data (2026).

The six passes for Oct. 16-17 (including the two night passes after the fire) are in the fire archive: `cfb-wainwright-fire-archive-2/data/rubicon-ridge/raw/sentinel3_frp/`.

| Pass (MDT) | Pass (UTC) | Satellite | Nearest pixel to burn centre | Cloud at the burn (1 km flags) | Fire detections within 60 km |
|---|---|---|---|---|---|
| Oct. 18, 11:42 a.m. | Oct. 18 17:42 | S3A | 0.24 km | Clear (1% of the 11 × 11 km window flagged) | **None** |
| Oct. 18, 10:33 p.m. | Oct. 19 04:33 | S3B | 0.58 km | Cloudy ("medium_high", whole window) | None (cloud: inconclusive) |
| Oct. 18, 11:08 p.m. | Oct. 19 05:08 | S3A | 0.47 km | Cloudy ("medium_high", whole window) | None (cloud: inconclusive); 57 fire pixels elsewhere in the granule |

**Reading:** the clear 11:42 a.m. pass on Oct. 18 found no fire above SLSTR's 1 km detection threshold anywhere within 60 km. Any burning that day, including at the south-east edge where VIIRS (375 m) recorded detections, was too small or too cool for SLSTR to detect. The two night passes were cloud-covered over the burn and cannot answer the question either way.
