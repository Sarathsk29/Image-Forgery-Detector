from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np


def clamp_score(value: float) -> float:
    return max(0.0, min(0.99, float(value)))


def score_to_status(score: float) -> str:
    if score >= 0.67:
        return "tampered"
    if score >= 0.4:
        return "suspicious"
    return "authentic"


def encode_cv_image(image: np.ndarray, extension: str = ".png") -> bytes:
    success, buffer = cv2.imencode(extension, image)
    if not success:
        raise ValueError("Failed to encode image artifact.")
    return BytesIO(buffer.tobytes()).getvalue()

