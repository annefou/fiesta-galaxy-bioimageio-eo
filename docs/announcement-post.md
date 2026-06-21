# Announcement post — draft

> Vision-first (per `docs/announcement-template.md` + `DOMAIN.md`). Focus: Galaxy,
> reusable workflows across disciplines, and the need for metadata that crosses
> disciplinary boundaries. No author tagging, no bot signatures, ~5 tags.
>
> Fill the three 🔗 links before posting (already filled below).
>
> **Suggested lead image:** `figures/announcement_figure.png` — "One BioImage.IO model,
> two disciplines": the microscopy nuclei it was trained on (left) beside the Landsat
> lakes it segmented unchanged (right, 152 ponds outlined). It carries the cross-discipline
> message in one glance. Secondary option: `figures/main_result.png` (input → segmentation
> → NDWI). For a data-forward post, `figures/robustness.png` (BMZ vs NDWI across 5 scenes).

---

## LinkedIn / blog version (~300 words)

**What if a deep-learning model built for one science could be picked up and run in another — without rewriting a single line of code?**

We have the pieces. The Carpentries and CodeRefinery taught us to write reproducible code; FAIR4RS gave software a citable identity; Galaxy lets anyone run a real analysis workflow in a browser, no install, no cluster. The next step isn't more compute — it's **workflows and metadata that cross disciplinary boundaries**.

A workflow is only reusable *across* fields if the metadata travels with it. The BioImage Model Zoo describes each model's inputs — axes, size, channels — precisely enough that software from a completely different domain can hand it the right tensor. Nanopublications make the *claim*, the *method*, and the *provenance* machine-readable and findable beyond the field they were minted in. The bottleneck to cross-discipline reuse is rarely the algorithm — it's metadata that stops at the disciplinary border.

So we tested it. We took a nucleus-segmentation model from the BioImage Model Zoo — trained only on fluorescence microscopy of cells — and ran it **unchanged** through a Galaxy bioimaging workflow on **satellite imagery**. On a 2020 Landsat scene of Arctic thermokarst ponds it delineated 152 water bodies (~221 km²), within ~5% of NDWI, the standard remote-sensing water index. A microscopy tool, mapping lakes from space, on usegalaxy.eu.

And every step is a separate, signed, atomic nanopublication:
🔗 PICO → AIDA → FORRT Claim → Replication Study → Outcome → CiTO Citation (+ Research Software)
🔗 Walk-through (Jupyter Book): https://annefou.github.io/fiesta-galaxy-bioimageio-eo/
🔗 The actual Galaxy runs (every tool version + parameter): https://usegalaxy.eu/u/annefou/h/fiesta-bioimage-io-on-eo
🔗 Archived + citable: https://doi.org/10.5281/zenodo.20782777

The Galaxy community is gathering this week at the Galaxy Community Conference. I'll miss it this year — but Beatriz [SURNAME / @handle], who leads OSCARS-FIESTA, will be there: find her to talk about reusable image-analysis workflows across disciplines.

The science worked. The harder question is metadata: what shared vocabulary would let a workflow built in one discipline be discovered, trusted, and reused in another? What's missing in your field?

#OpenScience #FAIR4RS #Galaxy #ReproducibleResearch #Metadata

---

## Bluesky / Mastodon thread (5 posts)

**1/**
What if a deep-learning model built for one science could be run in another — no code rewrite?
We have reproducible code (Carpentries, CodeRefinery), citable software (FAIR4RS), browser-run workflows (Galaxy). The next step: workflows + metadata that cross disciplines. 🧵

**2/**
A workflow is only reusable *across* fields if its metadata travels with it. BioImage Model Zoo says exactly what a model expects (axes, size, channels). Nanopublications make the claim + method + provenance machine-readable beyond their home field. The bottleneck isn't the algorithm — it's metadata that stops at the disciplinary border.

**3/**
So we tested it: a nucleus-segmentation model from the BioImage Model Zoo — trained only on fluorescence microscopy — run **unchanged** through a Galaxy workflow on **satellite imagery**. It delineated 152 Arctic thermokarst ponds (~221 km²), within ~5% of NDWI, the standard remote-sensing water index. A microscopy tool mapping lakes from space, on usegalaxy.eu.

**4/**
Every step is a signed, atomic nanopublication:
PICO → AIDA → FORRT Claim → Replication Study → Outcome → CiTO (+ Research Software).
Walk-through: https://annefou.github.io/fiesta-galaxy-bioimageio-eo/
Galaxy runs: https://usegalaxy.eu/u/annefou/h/fiesta-bioimage-io-on-eo
Archive: https://doi.org/10.5281/zenodo.20782777

**5/**
The Galaxy Community Conference is happening this week. I'll miss it this year — but Beatriz [SURNAME / @handle], who leads OSCARS-FIESTA, will be there. Find her to talk reusable image-analysis workflows across disciplines.

**6/**
The science worked. The open question is metadata: what shared vocabulary lets a workflow built in one discipline be found, trusted, and reused in another? What's missing in your field?
#OpenScience #FAIR4RS #Galaxy #Metadata
