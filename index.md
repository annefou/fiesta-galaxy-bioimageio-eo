# fiesta-galaxy-bioimageio-eo

> **Galaxy bioimaging tools, applied cross-discipline to Earth Observation.**
>
> Part of OSCARS-FIESTA. Reuses the GTN tutorial [`gxy.io/GTN:T00534`](https://gxy.io/GTN:T00534) and the BioImage Model Zoo model [10.5281/zenodo.6647674](https://doi.org/10.5281/zenodo.6647674).

A BioImage Model Zoo *nucleus-segmentation* model — trained only on fluorescence microscopy — is run **unchanged** through a Galaxy workflow on **usegalaxy.eu** to segment water bodies (thermokarst ponds) in Landsat imagery. On a 2020 Alaska scene it found **152 ponds** (~221 km²), within ~5 % of the NDWI water index (~211 km²); across five scenes it stays within 0.74–1.19× of NDWI. This repository produces:

- A reproducible pipeline (Snakefile + notebooks), runnable on Galaxy or via a byte-identical local fallback.
- A Science Live nanopublication chain documenting the claim, method, and outcome with provenance.
- A Zenodo-archived release (source + container image) with a citable DOI.

## Quick start

```bash
git clone https://github.com/annefou/fiesta-galaxy-bioimageio-eo.git
cd fiesta-galaxy-bioimageio-eo
pixi install
pixi run snakemake --cores 1
```

Or with Docker:

```bash
docker run --rm ghcr.io/annefou/fiesta-galaxy-bioimageio-eo:latest
```

## Structure

- `paper/` — the source paper PDF (drop yours in there).
- `notebooks/` — jupytext `.py` notebooks that drive the pipeline.
- `data/` — downloaded by `notebooks/01_data_download.py`, never committed.
- `nanopubs/` — drafts of the FORRT chain field-by-field, plus the published-URI registry.
- `docs/` — operating manuals (FORRT form fields, chain decision tree, claim-type vocabulary).
- `figures/` — curated figures used in the Jupyter Book.

## Nanopublication chain

The published chain is listed in [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md). Each step links to its viewer URL on the Science Live platform.

## Citation

If you use this work, please cite this software ([`CITATION.cff`](CITATION.cff), DOI minted on first release), plus the reused model ([10.5281/zenodo.6647674](https://doi.org/10.5281/zenodo.6647674)) and method ([`gxy.io/GTN:T00534`](https://gxy.io/GTN:T00534)).
