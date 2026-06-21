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
# # 04 — Figures
#
# - `figures/main_result.png` — the headline cross-discipline figure: EO input →
#   BioImage.IO segmentation (pond outlines) → NDWI baseline, for one clean scene.
# - `figures/robustness.png` — segmented water area (BMZ vs NDWI) across all scenes,
#   showing the workflow runs on every independent EO input.

# %%
from pathlib import Path

import numpy as np
import pandas as pd
import imageio.v3 as iio
import xarray as xr
import matplotlib.pyplot as plt
from skimage.segmentation import find_boundaries

CLEAN, RESULTS, FIGS = Path("../data/clean"), Path("../results"), Path("../figures")
FIGS.mkdir(parents=True, exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
HERO = 2020  # clean scene for the headline panel

# %% [markdown]
# ## Headline figure — input | segmentation | NDWI

# %%
img = np.asarray(iio.imread(CLEAN / f"alaska_acp_{HERO}.png"))
lab = np.asarray(iio.imread(RESULTS / f"alaska_acp_{HERO}__labelmap.tiff"))
ndwi = xr.open_dataarray(CLEAN / f"alaska_acp_{HERO}_ndwi.nc").to_numpy()

overlay = np.stack([img] * 3, axis=-1).astype("uint8")
overlay[find_boundaries(lab, mode="outer")] = [255, 0, 0]  # red pond outlines

fig, ax = plt.subplots(1, 3, figsize=(13, 4.6))
ax[0].imshow(img, cmap="gray"); ax[0].set_title(f"EO input (inverted NIR, {HERO})")
ax[1].imshow(overlay); ax[1].set_title(f"BioImage.IO segmentation\n{int(lab.max())} ponds (via Galaxy)")
ax[2].imshow(ndwi > 0, cmap="Blues"); ax[2].set_title("NDWI baseline (water)")
for a in ax:
    a.set_xticks([]); a.set_yticks([])
fig.suptitle("Galaxy bioimaging tools applied cross-discipline to Earth Observation",
             fontsize=13, y=1.02)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(FIGS / "main_result.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## Robustness — water area across independent scenes

# %%
df = pd.read_csv(RESULTS / "segmentation.csv").sort_values("year")
x = np.arange(len(df)); w = 0.38
fig, ax = plt.subplots(figsize=(8, 4.3))
ax.bar(x - w / 2, df["bmz_area_km2"], w, label="BioImage.IO (Galaxy)", color="#c1272d")
ax.bar(x + w / 2, df["ndwi_area_km2"], w, label="NDWI baseline", color="#0066cc")
ax.set_xticks(x); ax.set_xticklabels(df["year"])
ax.set_xlabel("Scene (year)"); ax.set_ylabel("Segmented water area (km$^2$)")
ax.set_title("Workflow runs on every independent EO scene\n"
             "(spread reflects composite quality, not a climate trend)")
ax.legend()
fig.tight_layout()
fig.savefig(FIGS / "robustness.png", dpi=150, bbox_inches="tight")
plt.show()

print("wrote figures/main_result.png and figures/robustness.png")
