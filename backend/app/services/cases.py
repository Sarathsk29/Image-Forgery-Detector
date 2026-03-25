from __future__ import annotations

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.core.security import generate_access_key, generate_case_id, hash_access_key, sha256_bytes, verify_access_key
from app.models.entities import AnalysisJob, AnalysisType, Case, CaseStatus, Evidence, JobStatus
from app.services.storage.service import get_storage_service, guess_content_type


SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
SUPPORTED_DOCUMENT_SUFFIXES = {".pdf"}


def _case_query(case_id: str):
    return (
        select(Case)
        .where(Case.case_id == case_id)
        .options(selectinload(Case.evidence_items), selectinload(Case.analysis_jobs))
    )


def get_case_by_public_id(db: Session, case_id: str) -> Case | None:
    return db.execute(_case_query(case_id)).scalar_one_or_none()


def require_case_access(db: Session, case_id: str, access_key: str) -> Case:
    case = get_case_by_public_id(db, case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")
    if not verify_access_key(access_key, case.access_key_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access key.")
    return case


def create_case(db: Session, title: str | None, notes: str | None) -> tuple[Case, str]:
    access_key = generate_access_key()
    case = Case(case_id=generate_case_id(), access_key_hash=hash_access_key(access_key), title=title, notes=notes, status=CaseStatus.open)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case, access_key


def _validate_upload(file: UploadFile, size: int) -> None:
    settings = get_settings()
    suffix = ""
    if file.filename and "." in file.filename:
        suffix = "." + file.filename.rsplit(".", 1)[1].lower()
    if size > settings.max_upload_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 5 MB limit.")
    if suffix not in SUPPORTED_IMAGE_SUFFIXES | SUPPORTED_DOCUMENT_SUFFIXES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type.")


def save_evidence(db: Session, case: Case, file: UploadFile, raw_data: bytes) -> Evidence:
    _validate_upload(file, len(raw_data))
    storage = get_storage_service()
    stored = storage.save_upload(case.case_id, file.filename or "evidence.bin", raw_data, guess_content_type(file.filename or "evidence.bin"))
    evidence = Evidence(
        case_id=case.id,
        original_filename=file.filename or "evidence.bin",
        mime_type=file.content_type or guess_content_type(file.filename or "evidence.bin"),
        size=len(raw_data),
        storage_url=stored.public_url,
        storage_path=stored.storage_path,
        file_hash=sha256_bytes(raw_data),
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


def create_analysis_job(db: Session, case: Case, evidence_id: int, analysis_type: str) -> AnalysisJob:
    evidence = next((item for item in case.evidence_items if item.id == evidence_id), None)
    if not evidence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence item not found in case.")
    job = AnalysisJob(
        case_id=case.id,
        evidence_id=evidence.id,
        analysis_type=AnalysisType(analysis_type),
        status=JobStatus.queued,
        progress_message="Analysis queued.",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_by_id(db: Session, job_id: int) -> AnalysisJob | None:
    return db.execute(select(AnalysisJob).where(AnalysisJob.id == job_id).options(selectinload(AnalysisJob.result))).scalar_one_or_none()

