from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.analysis.ai.detector import analyze_ai_edited_image
from app.analysis.document.detector import analyze_document_forgery
from app.analysis.image.copy_move import analyze_copy_move
from app.models.entities import AnalysisJob, AnalysisResult, ForgeryStatus, JobStatus, Report
from app.services.reports.pdf_report import generate_pdf_report
from app.services.storage.service import get_storage_service


def run_analysis_job(db: Session, job: AnalysisJob) -> None:
    job.status = JobStatus.processing
    job.progress_message = "Processing forensic analysis."
    job.started_at = datetime.now(UTC)
    db.commit()
    db.refresh(job)

    case = job.case
    evidence = job.evidence
    try:
        if job.analysis_type.value == "image_forgery":
            payload = analyze_copy_move(case.case_id, evidence.storage_path)
        elif job.analysis_type.value == "document_forgery":
            payload = analyze_document_forgery(case.case_id, evidence.storage_path, evidence.original_filename)
        else:
            payload = analyze_ai_edited_image(case.case_id, evidence.storage_path)

        result = AnalysisResult(
            job_id=job.id,
            forgery_status=ForgeryStatus(payload["forgery_status"]),
            confidence_score=payload["confidence_score"],
            summary=payload["summary"],
            methods=payload["methods"],
            findings=payload["findings"],
            artifact_urls=[artifact["url"] for artifact in payload["artifacts"]],
        )
        db.add(result)
        db.commit()
        db.refresh(result)

        report_bytes = generate_pdf_report(case, evidence, job, result, payload["artifacts"])
        stored_report = get_storage_service().save_report(case.case_id, f"{job.id}-report.pdf", report_bytes)
        report = Report(analysis_result_id=result.id, local_path=stored_report.local_path, public_url=stored_report.public_url)
        db.add(report)

        job.status = JobStatus.completed
        job.progress_message = "Analysis completed."
        job.completed_at = datetime.now(UTC)
        db.commit()
    except Exception as exc:
        job.status = JobStatus.failed
        job.error_text = str(exc)
        job.progress_message = "Analysis failed."
        job.completed_at = datetime.now(UTC)
        db.commit()

