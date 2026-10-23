"""Ingest a raw Copernicus Browser Sentinel-3 export (OLCI or SLSTR) into sentinel-3/<instrument>/<date>/.
Usage: python3 scripts/ingest.py EXPORT.zip [--note "day pass, ~17:40 UTC"]
Copies files unchanged; writes manifest.json (SHA-256 per file, frame, pixel size, fire-pixel values, cloud check) and a preview."""
import sys, os, re, json, hashlib, zipfile, tempfile, glob, shutil
import numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POINTS = {"origin": (-110.9214, 52.7764), "A_range2": (-110.90632, 52.77279), "B_road_head": (-110.89965, 52.77045)}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def main(zin, note):
    import rasterio
    from PIL import Image
    tmp = tempfile.mkdtemp(); zipfile.ZipFile(zin).extractall(tmp)
    files = sorted(f for f in glob.glob(tmp + "/**/*", recursive=True) if os.path.isfile(f))
    groups = {}
    for f in files:
        m = re.match(r"(\d{4}-\d{2}-\d{2})-\d{2}_\d{2}_\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_Sentinel-3_(OLCI|SLSTR)_(.+)\.(tiff?|jpe?g|png)$", os.path.basename(f), re.I)
        if not m: print("skip", os.path.basename(f)); continue
        groups.setdefault((m.group(1), m.group(2).upper()), []).append(f)
    for (date, inst), fs in groups.items():
        sub = date if not note else date + "_" + re.sub(r"[^a-z0-9]+", "-", note.lower()).strip("-")[:20]
        dest = os.path.join(REPO, "sentinel-3", inst, sub); os.makedirs(dest, exist_ok=True)
        tifs = [f for f in fs if f.lower().endswith((".tif", ".tiff"))]
        qa = {}
        if tifs:
            r = rasterio.open(tifs[0])
            qa = {"crs": str(r.crs), "pixel_deg": list(r.res), "pixel_m_approx": [round(r.res[0] * 111320 * np.cos(np.radians(52.77))), round(r.res[1] * 110950)],
                  "bounds": [round(v, 4) for v in r.bounds], "values_at_points": {}}
            for f in tifs:
                if "(Raw)" not in f: continue
                rr = rasterio.open(f); a = rr.read(1); band = re.search(r"_([A-Z0-9]+)_\(Raw\)", f).group(1)
                for k, (lo, la) in POINTS.items():
                    i, j = rr.index(lo, la)
                    if 0 <= i < a.shape[0] and 0 <= j < a.shape[1]: qa["values_at_points"].setdefault(k, {})[band] = round(float(a[i, j]), 4)
            if inst == "OLCI":
                b = next((f for f in tifs if "_B04_(Raw)" in f), None)
                if b:
                    a = rasterio.open(b).read(1); v = a[a > 0]
                    qa["blue_B04_median"] = round(float(np.median(v)), 3); qa["cloud_flag"] = bool(qa["blue_B04_median"] > 0.15)
        vis = next((f for f in fs if re.search(r"True_color|False_color|Fire|RGB", f) and f.lower().endswith((".tif", ".tiff"))), None)
        prev = []
        if vis:
            x = np.moveaxis(rasterio.open(vis).read([1, 2, 3]).astype("float32"), 0, -1)
            p = np.percentile(x, 99.5) or 1; im = Image.fromarray((np.clip(x / p, 0, 1) * 255).astype("uint8"))
            im.thumbnail((1200, 1200)); im.save(os.path.join(dest, "preview.jpg"), quality=85); prev.append("preview.jpg")
        for f in fs: shutil.copy2(f, os.path.join(dest, os.path.basename(f)))
        man = {"source": "Copernicus Browser export (Sentinel Hub), received from Prime Rogue", "date_utc": date, "instrument": inst, "note": note or "",
               "layers": sorted(re.sub(r".*Sentinel-3_(OLCI|SLSTR)_", "", os.path.splitext(os.path.basename(f))[0]) for f in fs),
               "n_files": len(fs), "qa": qa, "previews": prev, "original_upload": os.path.basename(zin), "original_upload_sha256": sha(zin),
               "files": {os.path.basename(f): {"bytes": os.path.getsize(f), "sha256": sha(f)} for f in fs},
               "licence": "Contains modified Copernicus Sentinel data [2026]"}
        json.dump(man, open(os.path.join(dest, "manifest.json"), "w"), indent=1)
        print(date, inst, len(fs), qa.get("pixel_m_approx"), "cloud" if qa.get("cloud_flag") else "")
    shutil.rmtree(tmp)
if __name__ == "__main__":
    note = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None
    main(sys.argv[1], note)
