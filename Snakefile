# Snakefile — orchestrates the cross-discipline pipeline end-to-end.
#
# Each rule wraps a jupytext notebook (the notebook stays the source of truth).
# notebooks/03 runs the BioImage.IO workflow on usegalaxy.eu when a key is present
# (~/.galaxy_eu_key), else the byte-identical local TorchScript fallback.
#
# Usage:
#   snakemake --cores 1            # run everything
#   snakemake --cores 1 -n         # dry run

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        f"{FIGURES}/main_result.png",
        f"{FIGURES}/robustness.png",
        f"{RESULTS}/segmentation.csv",


# ---------- 01: Data download (Microsoft Planetary Computer; self-contained) ----------
rule data_download:
    output:
        f"{DATA}/raw/sources.json",
    log:
        f"{RESULTS}/logs/01_data_download.log",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 01_data_download.py 2>&1 | tee ../{{log}}"


# ---------- 02: Data clean (-> 256x256 inverted-NIR PNG + NDWI) ----------
rule data_clean:
    input:
        f"{DATA}/raw/sources.json",
    output:
        f"{DATA}/clean/alaska_acp_2020.png",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 02_data_clean.py"


# ---------- 03: Segmentation (Galaxy workflow or local fallback) ----------
rule analysis:
    input:
        f"{DATA}/clean/alaska_acp_2020.png",
    output:
        f"{RESULTS}/segmentation.csv",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 03_analysis.py"


# ---------- 04: Figures ----------
rule figures:
    input:
        f"{RESULTS}/segmentation.csv",
    output:
        f"{FIGURES}/main_result.png",
        f"{FIGURES}/robustness.png",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 04_figures.py"
