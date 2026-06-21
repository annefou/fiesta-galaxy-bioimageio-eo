# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

### AIDA sentence (textarea, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Ends with a full stop.

```
A BioImage Model Zoo nucleus-segmentation model, applied without retraining through a Galaxy workflow, delineates open-water bodies in Landsat imagery with a total water area agreeing with the NDWI water index to within about 30 percent.
```

### Select related topics/tags (dropdown, optional)

Intended labels (pick from the platform vocabulary if present):

```
image segmentation; remote sensing; deep learning
```

### Relates to this nanopublication (text input, required)

URI of the PICO published in step 01.

```
<paste PICO URI from PUBLISHED.md step 01 after publishing>
```

### Supported by datasets (repeatable group, optional)

- Landsat Collection-2 Level-2 surface reflectance (Microsoft Planetary Computer): https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2

### Supported by other publications (repeatable group, optional)

*(skip — optional. Left empty deliberately: see the known platform bug below — populating BOTH datasets and publications has caused publishing to fail. The reused model + tutorial are cited at the CiTO step 06 instead.)*

> **Known platform bug (2026-04-26):** if both *Supported by datasets* AND *Supported by other publications* are populated and publishing fails, fall back to publishing this AIDA via Nanodash (URI namespace becomes `https://w3id.org/np/...`, still valid and citable).

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.
