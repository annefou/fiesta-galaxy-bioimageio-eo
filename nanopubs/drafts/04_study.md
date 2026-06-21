# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting. Method verified against `notebooks/01–04` + `scripts/galaxy_workflow.py`.

## Field-by-field draft

### Short URI suffix for study ID (text input, required)

```
bmz-eo-water-study
```

### Label/name of replication study (text input, required)

```
Cross-discipline application of a BioImage.IO nucleus model to EO water segmentation via Galaxy
```

### Study type (dropdown, required)

- [ ] Reproduction Study — direct reproduction: same methodology, same tools.
- [x] Replication Study — replication with different methodology or conditions.
- [ ] Reproduction/Replication Study — both.

*Rationale: the Galaxy tool, model weights, axes/size and post-processing are identical to the original microscopy tutorial; the **conditions** change (satellite imagery of water bodies instead of fluorescence microscopy of nuclei). Same method, new data domain → Replication Study.*

### Search for a FORRT claim (search/select, required)

```
<paste Claim URI from PUBLISHED.md step 03 after publishing>
```

### Describe what part of the claim is reproduced/replicated (textarea, required)

Scope only — no method, no results.

```
Whether the segmentation behaviour of the BioImage.IO nucleus-boundary workflow — delineating discrete bright "blob" objects and yielding their total area and count — holds when the input is optical satellite imagery of open-water bodies rather than fluorescence microscopy of cell nuclei, benchmarked against the NDWI water index. In scope: open-water delineation (total area and body count) on cloud-screened peak-summer Landsat composites of an Arctic thermokarst-pond landscape. Out of scope: instance-level ecological accuracy, sub-pixel or turbid water, temporal/climate trends, and any retraining or fine-tuning of the model.
```

### Describe how the claim is reproduced/replicated (textarea, required)

Method in plain prose — no result numbers.

```
Annual peak-summer (July–August) Landsat Collection-2 Level-2 surface-reflectance composites were built over the Alaska Arctic Coastal Plain from the Microsoft Planetary Computer, fill-masked and median-composited, then resampled to a 256×256 single-channel image with the near-infrared band inverted so that water reads as bright objects on a dark background. Each image was run through the unchanged Galaxy "Process image using a BioImage.IO model" workflow (main_workflow.ga; NucleiSegmentationBoundaryModel; input axes bcyx, size 256,256,1,1) on usegalaxy.eu via BioBlend: model inference, split into foreground and boundary channels, compute foreground minus boundaries, threshold at 0.6, convert to a connected-component label map, and overlay. Total water area was taken as thresholded pixels times per-pixel ground area; body count as the number of labels. NDWI was computed from the green and near-infrared bands as the comparator. A byte-identical local TorchScript path (torch.load of the same model, identical post-processing) reproduces the Galaxy result for credential-free CI.
```

### Describe any deviations from original methodology (textarea, optional)

```
Relative to the original Galaxy microscopy tutorial, only the input domain changed: DAPI fluorescence images of nuclei were replaced by inverted near-infrared Landsat composites of pond landscapes. The model weights, input axes and size, inference tool version, and the full post-processing chain (split → foreground−boundaries → threshold 0.6 → label map → overlay) are unchanged. No retraining, fine-tuning, or architecture change was performed.
```

### Search keywords (Wikidata) (multi-select, optional)

- image segmentation
- deep learning
- thermokarst

### Search discipline (Wikidata) (search, optional)

- remote sensing

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
