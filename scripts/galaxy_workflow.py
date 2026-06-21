"""Run the BioImage.IO nuclei-segmentation workflow on an image — two ways.

`run_on_galaxy()` invokes the *actual* Galaxy workflow (`workflow/main_workflow.ga`)
on usegalaxy.eu via BioBlend — the showcased FIESTA path (cross-image analysis
*with Galaxy*). `run_local()` reproduces the exact same algorithm offline
(`torch.load(TorchScript); model(x)` → `foreground - boundaries` → threshold 0.6
→ label map), so CI and the Jupyter Book build hermetically without a key.

`segment()` picks Galaxy when a key is present, else the local fallback.

Model: NucleiSegmentationBoundaryModel (BioImage Model Zoo), Zenodo
10.5281/zenodo.6647674 — TorchScript weights, uploaded to Galaxy as datatype `zip`.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_GA = ROOT / "workflow" / "main_workflow.ga"
MODEL_PATH = ROOT / "data" / "raw" / "nucleisegboundary_torchscript.pt"
MODEL_URL = "https://zenodo.org/record/6647674/files/weights-torchscript.pt?download=1"

GALAXY_URL = "https://usegalaxy.eu"
KEY_FILE = Path.home() / ".galaxy_eu_key"
CACHE = ROOT / "results" / ".galaxy_cache.json"
HISTORY_NAME = "FIESTA BioImage.IO on EO"
MODEL_LABEL, IMAGE_LABEL = "BioImage.IO Model", "Image for Prediction"
THRESHOLD = 0.6  # GTN tutorial value for (foreground - boundaries)

# Map Galaxy step tool-ids -> output tags we keep.
WANT = {"ip_threshold": "threshold", "ip_binary_to_labelimage": "labelmap",
        "ip_overlay_images": "overlay"}


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def have_galaxy_key() -> bool:
    return KEY_FILE.exists() and bool(KEY_FILE.read_text().strip())


def download_model(dest: Path = MODEL_PATH) -> Path:
    """Fetch the TorchScript model weights from Zenodo (once)."""
    if dest.exists():
        return dest
    import urllib.request
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading model -> {dest.name}")
    urllib.request.urlretrieve(MODEL_URL, dest)
    return dest


def water_metrics(threshold_mask: np.ndarray, label_map: np.ndarray,
                  pixel_area_km2: float) -> dict:
    """Water area (km^2) from the binary mask + pond count from the label map."""
    n_water = int((threshold_mask > 0).sum())
    n_ponds = int(len(np.unique(label_map)) - 1)  # drop background label 0
    return {"water_px": n_water,
            "water_area_km2": round(n_water * pixel_area_km2, 2),
            "n_ponds": n_ponds}


# --------------------------------------------------------------------------- #
# Path A — the actual Galaxy workflow on usegalaxy.eu (BioBlend)
# --------------------------------------------------------------------------- #
def _cache() -> dict:
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def _save_cache(c: dict) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(c, indent=2))


def _wait_ok(gi, ds_id, what):
    while True:
        st = gi.datasets.show_dataset(ds_id)["state"]
        if st == "ok":
            return
        if st in ("error", "failed_metadata", "discarded"):
            raise RuntimeError(f"{what} failed: {st}")
        time.sleep(5)


def run_on_galaxy(image_path: Path, out_dir: Path) -> dict:
    """Invoke main_workflow.ga on usegalaxy.eu; download threshold/labelmap/overlay.

    Returns {tag: path}. Reuses one uploaded model + imported workflow across calls.
    """
    from bioblend.galaxy import GalaxyInstance

    image_path, out_dir = Path(image_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    gi = GalaxyInstance(GALAXY_URL, key=KEY_FILE.read_text().strip())
    c = _cache()

    if not c.get("history_id"):
        c["history_id"] = gi.histories.create_history(HISTORY_NAME)["id"]
        _save_cache(c)
    if not c.get("workflow_id"):
        c["workflow_id"] = gi.workflows.import_workflow_from_local_path(
            str(WORKFLOW_GA))["id"]
        _save_cache(c)
    if not c.get("model_ds_id"):
        model = download_model()
        out = gi.tools.upload_file(str(model), c["history_id"], file_type="zip")
        c["model_ds_id"] = out["outputs"][0]["id"]
        _wait_ok(gi, c["model_ds_id"], "model")
        _save_cache(c)

    up = gi.tools.upload_file(str(image_path), c["history_id"], file_type="png")
    img_ds = up["outputs"][0]["id"]
    _wait_ok(gi, img_ds, "image")

    inv = gi.workflows.invoke_workflow(
        c["workflow_id"],
        inputs={MODEL_LABEL: {"id": c["model_ds_id"], "src": "hda"},
                IMAGE_LABEL: {"id": img_ds, "src": "hda"}},
        inputs_by="name", history_id=c["history_id"])
    gi.invocations.wait_for_invocation(inv["id"], maxwait=3600, interval=15)

    stem, paths = image_path.stem, {}
    for s in gi.invocations.show_invocation(inv["id"]).get("steps", []):
        if not s.get("job_id"):
            continue
        job = gi.jobs.show_job(s["job_id"])
        tag = next((v for k, v in WANT.items() if k in job.get("tool_id", "")), None)
        if not tag:
            continue
        for _, o in job.get("outputs", {}).items():
            _wait_ok(gi, o["id"], tag)
            ext = gi.datasets.show_dataset(o["id"]).get("extension", "dat")
            dest = out_dir / f"{stem}__{tag}.{ext}"
            gi.datasets.download_dataset(o["id"], file_path=str(dest),
                                         use_default_filename=False)
            paths[tag] = dest
    paths["engine"] = "galaxy:usegalaxy.eu"
    paths["invocation_id"] = inv["id"]
    return paths


# --------------------------------------------------------------------------- #
# Path B — local same-algorithm fallback (hermetic; CI)
# --------------------------------------------------------------------------- #
def run_local(image_path: Path, out_dir: Path) -> dict:
    """Reproduce the Galaxy pipeline offline with the same TorchScript model.

    Mirrors the tool's main.py (torch.load + model(x)) and the workflow's
    post-processing: foreground - boundaries, threshold 0.6, connected-component
    label map. Same algorithm, no Galaxy account.
    """
    import torch
    from scipy import ndimage
    import imageio.v3 as iio

    image_path, out_dir = Path(image_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    model = torch.load(download_model(), map_location="cpu", weights_only=False)
    model.eval()

    img = np.asarray(iio.imread(image_path)).astype("float32")
    if img.ndim == 3:
        img = img[..., 0]
    x = torch.from_numpy(img)[None, None]  # bcyx: (1, 1, H, W)
    with torch.no_grad():
        pred = model(x).numpy()[0]         # (2, H, W): [0]=foreground, [1]=boundary
    combined = pred[0] - pred[1]           # workflow step 6: foreground - boundaries
    threshold = (combined > THRESHOLD).astype("uint8") * 255
    # 8-connectivity to match Galaxy's binary2labelimage (skimage default).
    label_map, _ = ndimage.label(threshold > 0, structure=np.ones((3, 3)))

    stem = image_path.stem
    iio.imwrite(out_dir / f"{stem}__threshold.tiff", threshold)
    iio.imwrite(out_dir / f"{stem}__labelmap.tiff", label_map.astype("uint16"))
    return {"threshold": out_dir / f"{stem}__threshold.tiff",
            "labelmap": out_dir / f"{stem}__labelmap.tiff",
            "engine": "local:torchscript"}


def segment(image_path: Path, out_dir: Path, prefer_galaxy: bool = True) -> dict:
    """Galaxy when a key is available, else the local same-algorithm fallback.

    Set FIESTA_ENGINE=local to force the hermetic local path (used by CI and to
    regenerate figures offline); FIESTA_ENGINE=galaxy to require Galaxy.
    """
    import os
    engine = os.environ.get("FIESTA_ENGINE", "").lower()
    if engine == "local":
        return run_local(image_path, out_dir)
    if engine == "galaxy" or (prefer_galaxy and have_galaxy_key()):
        return run_on_galaxy(image_path, out_dir)
    return run_local(image_path, out_dir)
