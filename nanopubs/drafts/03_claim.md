# 03 — FORRT Claim

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Field-by-field draft

### Short URI suffix as claim ID (text input, required)

```
bmz-eo-water-transfer
```

### Label of the claim (text input, required)

```
BioImage.IO nucleus model segments Earth-observation open water via Galaxy
```

### Search for an AIDA sentence (search/select, required)

URI of the AIDA published in step 02.

```
<paste AIDA URI from PUBLISHED.md step 02 after publishing>
```

### Type of FORRT claim (dropdown, required)

See `docs/claim-type-vocabulary.md`.

- [ ] computational performance
- [ ] scalability
- [ ] data quality
- [ ] data governance
- [ ] descriptive pattern
- [x] model performance
- [ ] statistical significance

*Rationale: the claim is about how well a deep-learning model delineates water (its segmentation performance benchmarked against NDWI) — `model performance`.*

### Source URI (text input, optional)

Full URL form.

```
https://github.com/annefou/fiesta-galaxy-bioimageio-eo
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.
