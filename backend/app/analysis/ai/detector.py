from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.analysis.common import clamp_score, encode_cv_image, score_to_status
from app.analysis.image.ela import perform_ela
from app.core.config import get_settings
from app.services.storage.service import get_storage_service


def analyze_ai_edited_image(case_id: str, image_path: str) -> dict:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to read uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ela = perform_ela(case_id, image_path)

    edges = cv2.Canny(gray, 80, 180)
    edge_ratio = float(np.count_nonzero(edges) / edges.size)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    residual = cv2.absdiff(gray, blurred)
    block_size = 16
    block_variances = []
    for y in range(0, residual.shape[0] - block_size + 1, block_size):
        for x in range(0, residual.shape[1] - block_size + 1, block_size):
            block = residual[y : y + block_size, x : x + block_size]
            block_variances.append(float(np.var(block)))
    variance_std = float(np.std(block_variances) / 50.0) if block_variances else 0.0

    vertical_boundaries = np.abs(np.diff(gray[:, 7::8].astype(np.float32), axis=1)).mean() / 40.0 if gray.shape[1] > 16 else 0.0
    horizontal_boundaries = np.abs(np.diff(gray[7::8, :].astype(np.float32), axis=0)).mean() / 40.0 if gray.shape[0] > 16 else 0.0
    compression_score = float((vertical_boundaries + horizontal_boundaries) / 2.0)

    heatmap_base = cv2.normalize(residual, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap = cv2.applyColorMap(heatmap_base, cv2.COLORMAP_TURBO)
    heatmap_asset = get_storage_service().save_artifact(
        case_id,
        f"{Path(image_path).stem}-ai-noise-map.png",
        encode_cv_image(heatmap),
        "image/png",
        label="Noise inconsistency map",
    )

    model_score = _optional_model_score(image_path)
    methods = ["ELA", "Edge discontinuity analysis", "Noise residual analysis", "Compression artifact analysis"]
    weighted = 0.35 * ela["score"] + 0.15 * min(edge_ratio * 5.0, 1.0) + 0.35 * min(variance_std * 3.0, 1.0) + 0.15 * min(compression_score * 3.0, 1.0)
    if model_score is not None:
        weighted = (weighted * 0.7) + (model_score * 0.3)
        methods.append("Optional pretrained classifier")

    score = clamp_score(weighted)
    summary_prefix = "Heuristic + classifier" if model_score is not None else "Heuristic-only"
    conclusion = (
        "Combined artifact signals are consistent with hidden edits or synthetic post-processing."
        if score >= 0.4
        else "The analyzed image does not show strong synthetic-edit signatures under the configured heuristics."
    )
    artifacts = [
        {"label": heatmap_asset.label, "url": heatmap_asset.public_url, "local_path": heatmap_asset.local_path},
        ela["artifact"],
    ]
    return {
        "forgery_status": score_to_status(score),
        "confidence_score": score,
        "summary": f"{summary_prefix} analysis flagged ELA score {ela['score']:.2f}, edge ratio {edge_ratio:.3f}, and noise inconsistency {variance_std:.3f}.",
        "methods": methods,
        "findings": {
            "ela_score": round(ela["score"], 4),
            "edge_ratio": round(edge_ratio, 4),
            "noise_inconsistency": round(variance_std, 4),
            "compression_artifact_score": round(compression_score, 4),
            "optional_model_score": None if model_score is None else round(model_score, 4),
            "conclusion": conclusion,
            "artifact_manifest": [{"label": artifact["label"], "url": artifact["url"]} for artifact in artifacts],
        },
        "artifacts": artifacts,
    }


def _optional_model_score(image_path: str) -> float | None:
    settings = get_settings()
    if not settings.optional_ai_model_path:
        return None
    try:
        import torch
        from PIL import Image
        from torchvision import transforms

        model = torch.jit.load(settings.optional_ai_model_path, map_location="cpu")
        model.eval()
        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )
        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = model(tensor).sigmoid().item()
        return clamp_score(float(output))
    except Exception:
        return None

