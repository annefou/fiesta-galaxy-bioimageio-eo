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
# # 03 — Segmentation analysis (Galaxy BioImage.IO workflow)
#
# Runs the **BioImage.IO nuclei-segmentation Galaxy workflow** (`workflow/main_workflow.ga`)
# on each cleaned EO scene and measures the segmented water:
#
# - **water area** (km²) from the thresholded mask
# - **pond count** from the connected-component label map
# - **NDWI baseline area** (km²) for an independent cross-check
#
# **Two execution paths** (see `scripts/galaxy_workflow.py`):
#
# - **Galaxy (showcased):** if `~/.galaxy_eu_key` is present, the workflow runs on
#   **usegalaxy.eu** via BioBlend — *this is the FIESTA result: cross-image analysis
#   with Galaxy*. The invocation id is recorded for provenance.
# - **Local fallback (CI):** otherwise the *same algorithm* runs offline
#   (`torch.load(TorchScript)` → `foreground − boundaries` → threshold 0.6 → label),
#   so the Jupyter Book builds hermetically without a key.

# %%
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import imageio.v3 as iio
import xarray as xr

sys.path.insert(0, str(Path("../scripts").resolve()))
from galaxy_workflow import segment, water_metrics, have_galaxy_key  # noqa: E402

CLEAN, RESULTS = Path("../data/clean"), Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
print("execution path:", "Galaxy (usegalaxy.eu)" if have_galaxy_key()
      else "local TorchScript fallback")


# %% [markdown]
# ## Run the workflow on every scene and collect metrics

# %%
rows = []
for png in sorted(CLEAN.glob("alaska_acp_*.png")):
    year = int(png.stem.split("_")[-1])
    out = segment(png, RESULTS)                      # Galaxy or local
    thr = np.asarray(iio.imread(out["threshold"]))
    lab = np.asarray(iio.imread(out["labelmap"]))

    ndwi_da = xr.open_dataarray(CLEAN / f"alaska_acp_{year}_ndwi.nc")
    px_km2 = float(ndwi_da.attrs["pixel_area_km2"])
    m = water_metrics(thr, lab, px_km2)
    ndwi_area = round(float((ndwi_da.to_numpy() > 0).sum()) * px_km2, 2)

    rows.append({"year": year, "engine": out["engine"],
                 "bmz_area_km2": m["water_area_km2"], "n_ponds": m["n_ponds"],
                 "ndwi_area_km2": ndwi_area,
                 "bmz_vs_ndwi": round(m["water_area_km2"] / ndwi_area, 2)
                 if ndwi_area else None,
                 "invocation_id": out.get("invocation_id", "")})
    print(f"  {year}: {m['n_ponds']} ponds, {m['water_area_km2']} km^2 "
          f"(NDWI {ndwi_area} km^2)")

df = pd.DataFrame(rows).sort_values("year")
df.to_csv(RESULTS / "segmentation.csv", index=False)
df

# %% [markdown]
# ## What this shows
#
# The bioimaging model — trained only on fluorescence-microscopy nuclei — produces
# a valid pond segmentation on **every** independent EO scene (cross-discipline
# transfer, run through the Galaxy tools). On a clean scene the segmented area
# agrees with NDWI to within tens of percent.
#
# The year-to-year `bmz_area_km2` is **not** a climate time series: annual median
# composites differ in cloud/snow/radiometry, so the spread reflects input quality,
# not lake change (the NDWI baseline swings the same way). The multiple scenes are
# included as **robustness** evidence — the workflow runs across diverse EO inputs —
# not as a trend. A defensible trend would need per-scene QA/cloud masking.
