from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from app.services.reports.pdf_report import generate_pdf_report


def test_generate_pdf_report_returns_pdf_bytes(tmp_path: Path) -> None:
    image_path = tmp_path / "artifact.png"
    Image.new("RGB", (160, 100), color=(20, 80, 120)).save(image_path)

    case = SimpleNamespace(case_id="CASE-20260325-ABC123")
    evidence = SimpleNamespace(original_filename="sample.png")
    job = SimpleNamespace(analysis_type=SimpleNamespace(value="image_forgery"))
    result = SimpleNamespace(
        forgery_status=SimpleNamespace(value="suspicious"),
        confidence_score=0.72,
        methods=["SIFT", "ELA"],
        summary="Suspicious duplicated features were found.",
        findings={"conclusion": "Further manual review is recommended."},
        created_at=datetime.now(UTC),
    )
    artifacts = [{"label": "Overlay", "local_path": str(image_path), "url": "/storage/artifacts/sample.png"}]

    report_bytes = generate_pdf_report(case, evidence, job, result, artifacts)

    assert report_bytes.startswith(b"%PDF")
    assert len(report_bytes) > 500

