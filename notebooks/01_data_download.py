# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 — Data download
#
# Fetches Landsat annual composites for a thermokarst-pond region from the
# **Microsoft Planetary Computer** STAC API (free, anonymous) and saves each as a
# self-describing NetCDF (green + NIR surface reflectance) in `data/raw/`.
#
# These ponds are the Earth-observation analogue of cell nuclei: many small,
# discrete bright/dark blobs. We will feed them to a BioImage Model Zoo
# *nucleus-segmentation* model — the FIESTA cross-discipline experiment.
#
# **Self-contained:** the repo ships no data; this notebook is the only path that
# brings it in. **No credentials needed** for Planetary Computer.

# %%
import json
import time
from pathlib import Path

import numpy as np
import planetary_computer
import pystac_client
from odc.stac import load as stac_load


def retry(fn, tries=5, delay=10):
    """Planetary Computer occasionally times out under load — retry with backoff."""
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 — transient API/network errors
            if i == tries - 1:
                raise
            print(f"    retry {i + 1}/{tries} after error: {str(e)[:80]}")
            time.sleep(delay * (i + 1))

RAW = Path("../data/raw")
RAW.mkdir(parents=True, exist_ok=True)

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
SR_SCALE, SR_OFFSET, SR_FILL = 0.0000275, -0.2, 0  # Landsat C2 L2 scaling + nodata

# Arctic Coastal Plain, N Alaska (near Teshekpuk Lake) — very high pond density.
BBOX = [-152.7, 70.15, -151.7, 70.50]
CRS, RES_M = "EPSG:3413", 120          # polar-stereographic -> round ponds, metric px
YEARS = [2000, 2005, 2010, 2015, 2020]  # 5 independent scenes (robustness evidence)

# %% [markdown]
# ## Source registry

# %%
SOURCES = [{
    "name": "Landsat Collection-2 Level-2 surface reflectance",
    "doi": None,
    "url": STAC_URL,
    "collection": "landsat-c2-l2",
    "provider": "Microsoft Planetary Computer",
    "license": "public-domain (USGS)",
    "bbox": BBOX, "crs": CRS, "resolution_m": RES_M, "years": YEARS,
}]


# %% [markdown]
# ## Download one annual composite

# %%
def fetch_year(year: int, cloud_lt: int = 60) -> Path:
    out = RAW / f"alaska_acp_{year}.nc"
    if out.exists():
        print(f"  {year}: cached")
        return out
    cat = pystac_client.Client.open(STAC_URL,
                                    modifier=planetary_computer.sign_inplace)
    items = retry(lambda: list(cat.search(
        collections=["landsat-c2-l2"], bbox=BBOX,
        datetime=f"{year}-07-01/{year}-08-31",   # peak Arctic open water (min snow/ice)
        query={"eo:cloud_cover": {"lt": cloud_lt},
               "platform": {"in": ["landsat-5", "landsat-7", "landsat-8", "landsat-9"]}},
    ).items()))
    if not items:
        print(f"  {year}: SKIP (no scenes < {cloud_lt}% cloud)")
        return None
    def _build():
        ds = stac_load(items, bands=["green", "nir08"], bbox=BBOX,
                       crs=CRS, resolution=RES_M, groupby="solar_day", chunks={})
        ds = ds.where(ds != SR_FILL)             # mask fill before compositing
        return (ds.median(dim="time") * SR_SCALE + SR_OFFSET).compute()

    comp = retry(_build)
    comp = comp.assign_attrs(year=year, n_scenes=len(items), bbox=str(BBOX),
                             crs=CRS, resolution_m=RES_M,
                             pixel_area_km2=(RES_M / 1000.0) ** 2)
    comp.to_netcdf(out)
    print(f"  {year}: {len(items)} scenes -> {out.name}")
    return out


# %%
written = [p for y in YEARS if (p := fetch_year(y))]
(RAW / "sources.json").write_text(json.dumps({"sources": SOURCES}, indent=2))
print(f"\n{len(written)} composites in data/raw/; sources logged")
