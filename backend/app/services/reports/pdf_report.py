from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.models.entities import AnalysisJob, AnalysisResult, Case, Evidence


def generate_pdf_report(case: Case, evidence: Evidence, job: AnalysisJob, result: AnalysisResult, artifacts: list[dict]) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColor(colors.HexColor("#070c11"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setFillColor(colors.HexColor("#e7eef7"))
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(40, height - 50, "Digital Forgery Analysis Report")

    pdf.setFont("Helvetica", 10)
    lines = [
        f"Case ID: {case.case_id}",
        f"Evidence: {evidence.original_filename}",
        f"Analysis Type: {job.analysis_type.value}",
        f"Forgery Status: {result.forgery_status.value.title()}",
        f"Confidence Score: {result.confidence_score:.2f}",
        f"Generated: {result.created_at.isoformat()}",
        f"Methods: {', '.join(result.methods)}",
        f"Summary: {result.summary}",
    ]

    current_y = height - 85
    for line in lines:
        for wrapped in _wrap_text(line, 95):
            pdf.drawString(40, current_y, wrapped)
            current_y -= 15

    findings = result.findings
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, current_y - 10, "Conclusion")
    pdf.setFont("Helvetica", 10)
    current_y -= 30
    for wrapped in _wrap_text(findings.get("conclusion", result.summary), 95):
        pdf.drawString(40, current_y, wrapped)
        current_y -= 15

    current_y -= 10
    for artifact in artifacts[:2]:
        local_path = artifact.get("local_path")
        if not local_path or not Path(local_path).exists():
            continue
        if current_y < 220:
            pdf.showPage()
            pdf.setFillColor(colors.HexColor("#070c11"))
            pdf.rect(0, 0, width, height, fill=1, stroke=0)
            pdf.setFillColor(colors.HexColor("#e7eef7"))
            current_y = height - 50
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(40, current_y, artifact.get("label", "Artifact"))
        current_y -= 10
        image = ImageReader(local_path)
        pdf.drawImage(image, 40, current_y - 180, width=240, height=180, preserveAspectRatio=True, mask="auto")
        current_y -= 200

    pdf.save()
    return buffer.getvalue()


def _wrap_text(value: str, width: int) -> list[str]:
    words = value.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines

