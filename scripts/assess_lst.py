"""Assess one SLSTR L2 LST folder: values at the reference points and whether the base is under cloud.
Usage: python3 scripts/assess_lst.py sentinel-3/SLSTR_L2/<date>/   (updates manifest.json and prints a one-line finding)"""
import sys, glob, json
import numpy as np, rasterio
D = sys.argv[1].rstrip("/") + "/"
r = rasterio.open(glob.glob(D + "*LST_(Raw).tiff")[0]); a = r.read(1).astype(float)
nd = glob.glob(D + "*NDVI_(Raw).tiff"); n = rasterio.open(nd[0]).read(1).astype(float) if nd else None
P = {"origin": (-110.9214, 52.7764), "A_range2": (-110.90632, 52.77279), "B_road_head": (-110.89965, 52.77045)}
vals = {}
for k, (lo, la) in P.items():
    i, j = r.index(lo, la); vals[k] = {"LST_K": round(a[i, j], 1)}
    if n is not None: vals[k]["NDVI"] = round(float(n[i, j]), 3)
i0, j0 = r.index(-110.98, 52.81); i1, j1 = r.index(-110.82, 52.73); box = a[max(i0, 0):i1 + 1, max(j0, 0):j1 + 1]
v = box[(box > 200) & (box < 350)]
med = float(np.median(v)) if len(v) else float("nan")
nb = n[max(i0, 0):i1 + 1, max(j0, 0):j1 + 1] if n is not None else None
cloud = (med < 268) or (nb is not None and np.nanmedian(nb) < 0.08 and med < 275)
f = ("Cloud over the base (fire-area median %.1f K, %.0f °C); values are cloud tops, not usable." % (med, med - 273.15)) if cloud else \
    ("Clear over the base: fire-area median LST %.1f K (%.1f °C)." % (med, med - 273.15))
m = json.load(open(D + "manifest.json")); m["qa"]["assessment"] = {"finding": f, "fire_area_median_K": round(med, 1), "values_at_points": vals}
m["qa"]["usable"] = not cloud; json.dump(m, open(D + "manifest.json", "w"), indent=1)
print(("OK " if not cloud else "CLOUD ") + f); print(json.dumps(vals))
