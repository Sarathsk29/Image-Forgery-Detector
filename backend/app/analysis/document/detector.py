from __future__ import annotations

from io import BytesIO
from pathlib import Path
from statistics import median

import fitz
import numpy as np
import pytesseract
from PIL import Image, ImageDraw

from app.analysis.common import clamp_score, score_to_status
from app.analysis.image.ela import perform_ela_on_pil
from app.core.config import get_settings
from app.services.storage.service import get_storage_service


def analyze_document_forgery(case_id: str, file_path: str, filename: str) -> dict:
    suffix = Path(filename).suffix.lower()
    metadata_flags: list[str] = []
    page_findings: list[dict] = []
    artifacts: list[dict] = []
    scores: list[float] = []

    if suffix == ".pdf":
        document = fitz.open(file_path)
        metadata = document.metadata or {}
        if metadata.get("creationDate") and metadata.get("modDate") and metadata.get("creationDate") != metadata.get("modDate"):
            metadata_flags.append("Modification timestamp differs from creation timestamp.")
        if metadata.get("producer") and metadata.get("creator") and metadata["producer"] != metadata["creator"]:
            metadata_flags.append("Producer and creator metadata differ, which may indicate re-export or editing.")

        for page_index in range(min(document.page_count, 5)):
            page = document.load_page(page_index)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            image = Image.open(BytesIO(pixmap.tobytes("png"))).convert("RGB")
            text_info = page.get_text("dict")
            fonts = [span.get("size", 0) for block in text_info.get("blocks", []) for line in block.get("lines", []) for span in line.get("spans", []) if span.get("size")]
            font_outlier_ratio = _font_outlier_ratio(fonts)
            ocr = _ocr_analysis(image, case_id, f"{Path(filename).stem}-page-{page_index + 1}")
            ela = perform_ela_on_pil(case_id, image, f"{Path(filename).stem}-page-{page_index + 1}", label=f"Page {page_index + 1} ELA")
            page_score = clamp_score(0.45 * ela["score"] + 0.25 * font_outlier_ratio + 0.3 * ocr["low_confidence_ratio"])
            scores.append(page_score)
            artifacts.append(ela["artifact"])
            if ocr["artifact"]:
                artifacts.append(ocr["artifact"])
            page_findings.append(
                {
                    "page": page_index + 1,
                    "ela_score": round(ela["score"], 4),
                    "font_outlier_ratio": round(font_outlier_ratio, 4),
                    "low_confidence_ratio": round(ocr["low_confidence_ratio"], 4),
                    "suspicious_boxes": ocr["boxes"][:20],
                    "page_score": round(page_score, 4),
                }
            )
    else:
        image = Image.open(file_path).convert("RGB")
        ocr = _ocr_analysis(image, case_id, Path(filename).stem)
        ela = perform_ela_on_pil(case_id, image, Path(filename).stem, label="Document ELA")
        page_score = clamp_score(0.6 * ela["score"] + 0.4 * ocr["low_confidence_ratio"])
        scores.append(page_score)
        artifacts.append(ela["artifact"])
        if ocr["artifact"]:
            artifacts.append(ocr["artifact"])
        page_findings.append(
            {
                "page": 1,
                "ela_score": round(ela["score"], 4),
                "low_confidence_ratio": round(ocr["low_confidence_ratio"], 4),
                "suspicious_boxes": ocr["boxes"][:20],
                "page_score": round(page_score, 4),
            }
        )
        metadata = {}

    overall_score = clamp_score((sum(scores) / max(len(scores), 1)) + (0.08 if metadata_flags else 0.0))
    conclusion = (
        "Document analysis found suspicious layout, OCR confidence, or metadata inconsistencies that warrant manual verification."
        if overall_score >= 0.4
        else "No strong tampering indicator dominated the document analysis, though localized anomalies may still merit review."
    )
    return {
        "forgery_status": score_to_status(overall_score),
        "confidence_score": overall_score,
        "summary": f"Document analysis reviewed {len(page_findings)} page(s) with metadata, OCR, and ELA-based heuristics.",
        "methods": ["Metadata analysis", "OCR structure analysis", "Page-level ELA"],
        "findings": {
            "metadata_flags": metadata_flags,
            "page_findings": page_findings,
            "conclusion": conclusion,
            "artifact_manifest": [{"label": artifact["label"], "url": artifact["url"]} for artifact in artifacts],
            "metadata_snapshot": metadata if suffix == ".pdf" else {},
        },
        "artifacts": artifacts,
    }


def _font_outlier_ratio(font_sizes: list[float]) -> float:
    if len(font_sizes) < 4:
        return 0.0
    med = median(font_sizes)
    outliers = [size for size in font_sizes if abs(size - med) > max(1.5, med * 0.25)]
    return clamp_score(len(outliers) / len(font_sizes))


def _ocr_analysis(image: Image.Image, case_id: str, base_name: str) -> dict:
    settings = get_settings()
    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
    try:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    except Exception:
        return {"low_confidence_ratio": 0.0, "boxes": [], "artifact": None}

    draw = ImageDraw.Draw(image.copy())
    boxes = []
    total = 0
    low = 0
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for i, text in enumerate(data.get("text", [])):
        conf_raw = data.get("conf", ["-1"])[i]
        try:
            conf = float(conf_raw)
        except (TypeError, ValueError):
            conf = -1.0
        if conf < 0:
            continue
        total += 1
        if conf < 45:
            low += 1
            x, y, w, h = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            draw.rectangle((x, y, x + w, y + h), outline="#ff7a7a", width=2)
            boxes.append({"x": x, "y": y, "width": w, "height": h, "confidence": round(conf, 2), "text": text})

    artifact = None
    if boxes:
        buffer = BytesIO()
        overlay.save(buffer, "PNG")
        stored = get_storage_service().save_artifact(case_id, f"{base_name}-ocr-hotspots.png", buffer.getvalue(), "image/png", label="OCR anomaly overlay")
        artifact = {"label": stored.label, "url": stored.public_url, "local_path": stored.local_path}
    ratio = clamp_score(low / max(total, 1))
    return {"low_confidence_ratio": ratio, "boxes": boxes, "artifact": artifact}

