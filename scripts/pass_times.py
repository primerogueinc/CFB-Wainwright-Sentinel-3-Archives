"""Predict Sentinel-3A/3B passes over CFB Wainwright (52.77N, 110.90W) from two-line elements (TLEs).
Usage: python3 scripts/pass_times.py > pass_times.csv
TLEs from keeptrack.space (Space-Track for S3A, epoch 2026-10-22 20:28 UTC; CelesTrak for S3B, epoch 2026-09-17 04:48 UTC).
Time of closest approach of the ground track, 10 s steps; the S3B elements are a month old, so its times may be off by up to about a minute.
SLSTR's nadir swath is about 1,400 km wide, so passes with cross-track distance under about 700 km see the base."""
from skyfield.api import EarthSatellite, load, wgs84
import numpy as np
ts = load.timescale()
TLES = {"S3A": ("1 41335U 16011A   26295.85287742  .00000078  00000+0  50133-4 0  9992", "2 41335  98.6232   1.3869 0001312  96.5206 263.6124 14.26736878556260"),
        "S3B": ("1 43437U 18039A   26260.20006803  .00000057  00000+0  41568-4 0  9996", "2 43437  98.6275 326.4001 0001308  76.2044 283.9282 14.26737806437249")}
la0, lo0 = np.radians(52.77), np.radians(-110.90)
print("satellite,pass_utc,pass_mdt,direction,day_or_night,cross_track_km,within_nadir_swath")
rows = []
for name, (l1, l2) in TLES.items():
    sat = EarthSatellite(l1, l2, name, ts)
    t = ts.utc(2026, 10, 10, 0, np.arange(0, 16 * 24 * 360) / 6.0)
    sp = wgs84.subpoint_of(sat.at(t)); lat, lon = sp.latitude.radians, sp.longitude.radians
    d = 6371 * np.arccos(np.clip(np.sin(lat) * np.sin(la0) + np.cos(lat) * np.cos(la0) * np.cos(lon - lo0), -1, 1))
    for i in range(1, len(d) - 1):
        if d[i] < d[i - 1] and d[i] <= d[i + 1] and d[i] < 900:
            u = t[i].utc_datetime(); m = t[i].utc_datetime().timestamp() - 6 * 3600
            import datetime as dt
            md = dt.datetime.utcfromtimestamp(m)
            asc = lat[i + 1] > lat[i]
            rows.append((u, f"{name},{u:%Y-%m-%d %H:%M},{md:%Y-%m-%d %H:%M},{'ascending' if asc else 'descending'},{'night' if asc else 'day'},{d[i]:.0f},{'yes' if d[i] < 700 else 'edge'}"))
for _, r in sorted(rows): print(r)
