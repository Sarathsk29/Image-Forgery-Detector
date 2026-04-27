from __future__ import annotations

from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageEnhance

from app.analysis.common import clamp_score
from app.services.storage.service import get_storage_service


def perform_ela(case_id: str, image_path: str, label: str = "ELA visualization") -> dict:
    image = Image.open(image_path).convert("RGB")
    return perform_ela_on_pil(case_id, image, Path(image_path).stem, label)


def perform_ela_on_pil(case_id: str, image: Image.Image, base_name: str, label: str = "ELA visualization") -> dict:
    jpeg_buffer = BytesIO()
    image.save(jpeg_buffer, "JPEG", quality=90)
    jpeg_buffer.seek(0)
    recompressed = Image.open(jpeg_buffer).convert("RGB")
    diff = ImageChops.difference(image, recompressed)
    diff_arr = np.asarray(diff).astype(np.float32)
    ela_gap = np.percentile(diff_arr, 99.5) - np.median(diff_arr)
    score = clamp_score(float(ela_gap) / 10.0)

    extrema = diff.getextrema()
    max_diff = max(channel[1] for channel in extrema) or 1
    scale = 255 / max_diff
    ela_image = ImageEnhance.Brightness(diff).enhance(scale * 1.8)

    png_buffer = BytesIO()
    ela_image.save(png_buffer, "PNG")
    stored = get_storage_service().save_artifact(
        case_id,
        f"{base_name}-ela.png",
        png_buffer.getvalue(),
        "image/png",
        label=label,
    )
    return {
        "score": score,
        "artifact": {
            "label": label,
            "url": stored.public_url,
            "local_path": stored.local_path,
        },
    }

