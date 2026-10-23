"""Quick assessment of one SLSTR L1B folder: day or night, cloud, and hot-pixel candidates near the fire.
Usage: python3 scripts/assess_slstr.py sentinel-3/SLSTR/<date>/   (writes assessment into manifest.json)"""
import sys, glob, json, os
import numpy as np, rasterio
from scipy import ndimage
D = sys.argv[1].rstrip("/") + "/"
g = lambda b: rasterio.open(glob.glob(D + f"*_{b}_(Raw).tiff")[0])
r = g("S8"); s8 = r.read(1).astype(float); s7 = g("S7").read(1).astype(float); f1 = g("F1").read(1).astype(float); s1 = g("S1").read(1).astype(float)
valid = s8 > 0
night = bool(np.nanmedian(s1[valid]) < 0.02)
cold = s8 < 270
out = {"pass": "night" if night else "day", "S8_median_K": round(float(np.median(s8[valid])), 1),
       "cold_cloud_frac": round(float(cold[valid].mean()), 2)}
# hot-pixel test: MIR (max of S7, F1) brightness temperature well above the local 15x15 median, and MIR-TIR well above local
mir = np.maximum(s7, f1); d = mir - s8
med = ndimage.median_filter(mir, 15); dmed = ndimage.median_filter(d, 15)
thr = (6, 6) if night else (12, 10)
cand = valid & (mir - med > thr[0]) & (d - dmed > thr[1]) & ~cold
box = np.zeros_like(valid)
i0, j0 = r.index(-110.98, 52.81); i1, j1 = r.index(-110.82, 52.73); box[max(i0, 0):i1 + 1, max(j0, 0):j1 + 1] = True
pts = []
for i, j in zip(*np.where(cand & box)):
    x, y = r.xy(i, j); pts.append({"lon": round(x, 4), "lat": round(y, 4), "MIR_K": round(mir[i, j], 1), "excess_K": round(mir[i, j] - med[i, j], 1)})
out["hot_pixels_in_fire_area"] = pts
fz = {}
for k, (lo, la) in {"origin": (-110.9214, 52.7764), "B_road_head": (-110.89965, 52.77045)}.items():
    i, j = r.index(lo, la); fz[k] = {"S7_K": round(s7[i, j], 1), "F1_K": round(f1[i, j], 1), "S8_K": round(s8[i, j], 1), "local_MIR_median_K": round(med[i, j], 1)}
out["at_points"] = fz
out["usable"] = bool(out["cold_cloud_frac"] < 0.5)
mp = D + "manifest.json"; m = json.load(open(mp)); m["qa"]["assessment"] = out; m["qa"]["usable"] = out["usable"] or bool(pts)
json.dump(m, open(mp, "w"), indent=1); print(json.dumps(out, indent=1))
