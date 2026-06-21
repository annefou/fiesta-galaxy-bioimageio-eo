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
# # 02 — Data clean
#
# Turns each raw Landsat composite into the **exact input the BioImage.IO model
# expects**: a 256×256, single-channel 8-bit PNG. Water is dark in NIR, so we
# **invert** it — each pond becomes a bright "nucleus" on a dark background,
# matching the fluorescence-microscopy images the model was trained on.
#
# We also compute the **NDWI** water index (the standard remote-sensing baseline)
# and save it as NetCDF, for an independent cross-check in notebook 03.

# %%
from pathlib import Path

import numpy as np
import xarray as xr
from PIL import Image

RAW, CLEAN = Path("../data/raw"), Path("../data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)
SIZE = 256                 # model input size (axes bcyx, 256,256,1,1)
NIR_CLIP = 0.3             # land is bright in NIR; clip then normalise


# %%
def to_256(arr: np.ndarray) -> np.ndarray:
    a = arr.astype("float32")
    if np.isnan(a).any():
        a = np.where(np.isnan(a), np.nanmedian(a), a)
    return np.asarray(Image.fromarray(a).resize((SIZE, SIZE), Image.BILINEAR),
                      dtype="float32")


def clean_one(nc_path: Path):
    comp = xr.open_dataset(nc_path)
    year = int(comp.attrs["year"])
    green = to_256(comp["green"].to_numpy())
    nir = to_256(comp["nir08"].to_numpy())

    # Galaxy model input: inverted NIR -> ponds bright.
    n = np.clip(nir, 0, NIR_CLIP) / NIR_CLIP
    img8 = (255 * (1.0 - n)).astype("uint8")
    Image.fromarray(img8, mode="L").save(CLEAN / f"alaska_acp_{year}.png")

    # NDWI baseline (McFeeters): water > 0. Pixel area rescaled to the 256 grid.
    ndwi = (green - nir) / (green + nir + 1e-6)
    px_km2 = float(comp.attrs["pixel_area_km2"]) * (comp["nir08"].size / (SIZE * SIZE))
    xr.DataArray(ndwi, dims=("y", "x"), name="ndwi",
                 attrs={"year": year, "pixel_area_km2": px_km2}
                 ).to_netcdf(CLEAN / f"alaska_acp_{year}_ndwi.nc")
    print(f"  {year}: alaska_acp_{year}.png + NDWI")


# %%
for nc in sorted(RAW.glob("alaska_acp_*.nc")):
    clean_one(nc)
print("clean inputs ready in data/clean/")
