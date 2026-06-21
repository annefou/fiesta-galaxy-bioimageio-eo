# 01 — PICO Research Question (question-rooted, comparative)

> Chain shape: **question-rooted, comparative** (no upstream paper; the claim is posed here, with NDWI as the comparator). See `docs/chain-decision-tree.md`. The `01_quote.md` and `01_pcc.md` alternates have been removed.

**Form heading:** *"PICO Research Question — Define a research question using the PICO framework (Population, Intervention, Comparator, Outcome)"*

## Field-by-field draft

### Short ID (text input, required)

```
bmz-nuclei-model-eo-water
```

### Research Question Title (text input, required)

10–200 characters.

```
Can a bioimaging nucleus-segmentation model segment open water in satellite imagery via Galaxy?
```

### Complete Research Question (textarea, required)

```
In Landsat satellite imagery of an Arctic thermokarst-pond landscape (Population), does a BioImage Model Zoo nucleus-segmentation deep-learning model applied without retraining through a Galaxy BioImage.IO workflow (Intervention), compared with the standard NDWI water index (Comparator), delineate open-water bodies with a comparable total water area and number of distinct bodies (Outcome)?
```

### Question Type (radio button, required)

- [ ] Causation
- [ ] Descriptive
- [x] Effectiveness
- [ ] Experience
- [ ] Prediction

### Population (P) (textarea, required)

```
Optical multispectral satellite imagery of landscapes containing many small open-water bodies — here Landsat surface-reflectance scenes of the Arctic Coastal Plain of northern Alaska, a terrain dense with thermokarst ponds.
```

### Intervention (I) (textarea, required)

```
A deep-learning nucleus/boundary-segmentation model from the BioImage Model Zoo, originally trained on fluorescence-microscopy images of cell nuclei, applied without retraining to the satellite imagery through a Galaxy BioImage.IO inference workflow — i.e. a cross-discipline transfer of a bioimaging segmentation model to remote sensing.
```

### Comparison (C) (textarea, required)

```
The Normalized Difference Water Index (NDWI), the standard remote-sensing index for delineating surface water from green and near-infrared reflectance.
```

### Outcome (O) (textarea, required)

```
Delineation of open-water bodies — the total water area and the count of distinct water bodies — and the degree to which these agree with the NDWI baseline.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
