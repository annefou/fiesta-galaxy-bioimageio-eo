# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting. Numbers verified against `results/galaxy_provenance.json` + `results/segmentation.csv`.

## Field-by-field draft

### Short URI suffix for outcome ID (text input, required)

```
bmz-eo-water-outcome
```

### Plain-text label for the outcome (text input, required)

```
BioImage.IO model delineates EO open water within ~30% of NDWI across five scenes
```

### Search for a FORRT replication study (search/select, required)

```
<paste Study URI from PUBLISHED.md step 04 after publishing>
```

### Repository URL (text input, required)

```
https://github.com/annefou/fiesta-galaxy-bioimageio-eo
```

### Completion date (date picker, required)

```
2026-06-21
```

### Validation status (dropdown, required)

- [x] Validated
- [ ] PartiallySupported
- [ ] Contradicted

*The cross-discipline transfer works: the model delineates open water and its area agrees with NDWI to within the stated ~30 percent. (If a stricter, quantitative-equivalence reading of the claim is preferred, `PartiallySupported` would be the conservative choice — agreement varies 0.74–1.19× across scenes.)*

### Confidence level (dropdown, required)

```
Moderate
```

*Five scenes, one region; agreement is consistent in direction but varies in magnitude — adequate evidence, partial quantitative agreement.*

### Describe the overall conclusion about the original claim (textarea, required)

```
A nucleus-segmentation model from the BioImage Model Zoo, trained only on fluorescence microscopy and applied without retraining through the unchanged Galaxy BioImage.IO workflow, successfully delineates open-water bodies in Landsat imagery of an Arctic thermokarst-pond landscape. Across five peak-summer scenes (2000–2020) the model's total water area stays within about 30 percent of the standard NDWI index (2020: 221 vs 211 km², within ~5 percent), demonstrating that the bioimaging "many bright blobs" segmentation behaviour transfers to remote-sensing water mapping. Galaxy and a local TorchScript reimplementation give byte-identical masks.
```

### Describe the evidence that supports your conclusion (textarea, required)

```
Alaska Arctic Coastal Plain, peak-summer Landsat C2 L2 composites, run on usegalaxy.eu. BMZ water area vs NDWI water area (km², ratio): 2000 = 198 vs 266 (0.74×); 2005 = 223 vs 187 (1.19×); 2010 = 201 vs 240 (0.84×); 2015 = 170 vs 187 (0.91×); 2020 = 221 vs 211 (1.05×). Distinct water-body ("pond") counts: 135–200. Galaxy-vs-local parity on the 2020 scene: mask IoU = 1.000 with identical area and pond count. Public Galaxy history (tool versions, parameters, datasets) and per-scene invocation IDs are recorded in results/galaxy_provenance.json; figures in figures/main_result.png and figures/robustness.png.
```

### Describe what limits the conclusions of the study (textarea, optional)

```
Scene-to-scene agreement varies (0.74–1.19× of NDWI), driven by annual-composite quality — residual cloud, snow/ice timing and radiometric differences — not by real change in the landscape; this is explicitly NOT a temporal or climate trend. NDWI is itself an index proxy, not ground truth, so the comparison establishes consistency between two automated methods rather than absolute accuracy. The study covers a single thermokarst region, one model, optical peak-summer imagery only, with no retraining and no instance-level validation. The result demonstrates cross-discipline transferability of the Galaxy bioimaging workflow, not a calibrated operational water-mapping product.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
