from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.analysis.common import clamp_score, encode_cv_image, score_to_status
from app.analysis.image.ela import perform_ela
from app.services.storage.service import get_storage_service


def _detector():
    if hasattr(cv2, "SIFT_create"):
        return cv2.SIFT_create(), "SIFT", cv2.NORM_L2
    return cv2.ORB_create(nfeatures=1500), "ORB fallback", cv2.NORM_HAMMING


def analyze_copy_move(case_id: str, image_path: str) -> dict:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to read uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector, detector_label, matcher_norm = _detector()
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    if descriptors is None or len(keypoints) < 12:
        ela = perform_ela(case_id, image_path)
        score = ela["score"] * 0.45
        return {
            "forgery_status": score_to_status(score),
            "confidence_score": clamp_score(score),
            "summary": "Limited local feature similarity was detected. ELA output is available for manual review.",
            "methods": [detector_label, "ELA"],
            "findings": {
                "keypoints": len(keypoints),
                "filtered_matches": 0,
                "inlier_matches": 0,
                "regions": [],
                "conclusion": "Not enough repeated local features were found to strongly indicate copy-move tampering.",
                "artifact_manifest": [{"label": ela["artifact"]["label"], "url": ela["artifact"]["url"]}],
            },
            "artifacts": [ela["artifact"]],
        }

    matcher = cv2.BFMatcher(matcher_norm, crossCheck=False)
    raw_matches = matcher.knnMatch(descriptors, descriptors, k=3)
    filtered: list[cv2.DMatch] = []
    seen_pairs: set[tuple[int, int]] = set()

    for group in raw_matches:
        candidates = [match for match in group if match.queryIdx != match.trainIdx]
        if len(candidates) < 2:
            continue
        best, next_best = candidates[0], candidates[1]
        pt_a = np.array(keypoints[best.queryIdx].pt)
        pt_b = np.array(keypoints[best.trainIdx].pt)
        distance = np.linalg.norm(pt_a - pt_b)
        pair_key = tuple(sorted((best.queryIdx, best.trainIdx)))
        if best.distance < 0.72 * next_best.distance and distance > 24 and pair_key not in seen_pairs:
            seen_pairs.add(pair_key)
            filtered.append(best)

    selected = filtered[:50]
    inliers: list[cv2.DMatch] = []
    if len(filtered) >= 4:
        src = np.float32([keypoints[m.queryIdx].pt for m in filtered]).reshape(-1, 1, 2)
        dst = np.float32([keypoints[m.trainIdx].pt for m in filtered]).reshape(-1, 1, 2)
        _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 6.0)
        if mask is not None:
            inliers = [match for match, keep in zip(filtered, mask.ravel().tolist()) if keep]
            selected = inliers[:50] or selected

    overlay = image.copy()
    mask_img = np.zeros(gray.shape, dtype=np.uint8)
    regions = []
    for match in selected:
        start = tuple(int(value) for value in keypoints[match.queryIdx].pt)
        end = tuple(int(value) for value in keypoints[match.trainIdx].pt)
        cv2.circle(overlay, start, 10, (40, 90, 255), 2)
        cv2.circle(overlay, end, 10, (255, 90, 40), 2)
        cv2.line(overlay, start, end, (85, 220, 255), 1)
        cv2.circle(mask_img, start, 18, 180, -1)
        cv2.circle(mask_img, end, 18, 255, -1)
        regions.append(
            {
                "from": {"x": start[0], "y": start[1]},
                "to": {"x": end[0], "y": end[1]},
                "distance": round(float(np.linalg.norm(np.array(start) - np.array(end))), 2),
            }
        )

    heatmap = cv2.GaussianBlur(mask_img, (0, 0), 15)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    blend = cv2.addWeighted(image, 0.45, heatmap, 0.55, 0)

    storage = get_storage_service()
    overlay_asset = storage.save_artifact(case_id, f"{Path(image_path).stem}-copymove-overlay.png", encode_cv_image(overlay), "image/png", label="Matched region overlay")
    heatmap_asset = storage.save_artifact(case_id, f"{Path(image_path).stem}-copymove-heatmap.png", encode_cv_image(blend), "image/png", label="Suspicious region heatmap")
    ela = perform_ela(case_id, image_path)

    match_ratio = len(selected) / max(len(keypoints), 1)
    inlier_ratio = len(inliers) / max(len(filtered), 1) if filtered else 0.0
    score = clamp_score(0.42 * min(len(selected) / 25.0, 1.0) + 0.28 * ela["score"] + 0.3 * inlier_ratio)
    conclusion = (
        "Repeated local features and spatially consistent matches suggest possible cloned or duplicated content."
        if score >= 0.4
        else "Only weak self-similarity was detected; manual inspection is still recommended."
    )

    artifacts = [
        {"label": overlay_asset.label, "url": overlay_asset.public_url, "local_path": overlay_asset.local_path},
        {"label": heatmap_asset.label, "url": heatmap_asset.public_url, "local_path": heatmap_asset.local_path},
        ela["artifact"],
    ]
    return {
        "forgery_status": score_to_status(score),
        "confidence_score": score,
        "summary": f"{detector_label} found {len(selected)} suspicious feature correspondences with ELA support score {ela['score']:.2f}.",
        "methods": [detector_label, "RANSAC filtering", "ELA heatmap"],
        "findings": {
            "keypoints": len(keypoints),
            "filtered_matches": len(filtered),
            "inlier_matches": len(inliers),
            "match_ratio": round(match_ratio, 4),
            "regions": regions[:20],
            "conclusion": conclusion,
            "artifact_manifest": [{"label": artifact["label"], "url": artifact["url"]} for artifact in artifacts],
        },
        "artifacts": artifacts,
    }

