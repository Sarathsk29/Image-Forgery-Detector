from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.schemas.analysis import AnalysisJobRead, AnalysisResultRead, ArtifactRead, CreateAnalysisRequest, ReportRead
from app.services.analysis_runner import run_analysis_job
from app.services.cases import create_analysis_job, get_job_by_id, require_case_access


router = APIRouter()


def _execute_background_job(job_id: int) -> None:
    with SessionLocal() as db:
        job = get_job_by_id(db, job_id)
        if job is not None:
            run_analysis_job(db, job)


@router.post("/cases/{case_id}/analyses", response_model=AnalysisJobRead)
def create_analysis_route(
    case_id: str,
    payload: CreateAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> AnalysisJobRead:
    case = require_case_access(db, case_id, payload.access_key)
    job = create_analysis_job(db, case, payload.evidence_id, payload.analysis_type)
    background_tasks.add_task(_execute_background_job, job.id)
    return AnalysisJobRead.model_validate(job)


@router.get("/analyses/{job_id}", response_model=AnalysisJobRead)
def get_analysis_job_route(job_id: int, access_key: str = Query(...), db: Session = Depends(get_db)) -> AnalysisJobRead:
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis job not found.")
    require_case_access(db, job.case.case_id, access_key)
    return AnalysisJobRead.model_validate(job)


@router.get("/analyses/{job_id}/result", response_model=AnalysisResultRead)
def get_analysis_result_route(job_id: int, access_key: str = Query(...), db: Session = Depends(get_db)) -> AnalysisResultRead:
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis job not found.")
    require_case_access(db, job.case.case_id, access_key)
    if not job.result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result is not ready yet.")
    manifest = job.result.findings.get("artifact_manifest", [])
    artifacts = [ArtifactRead(label=item["label"], url=item["url"]) for item in manifest]
    return AnalysisResultRead(
        forgery_status=job.result.forgery_status.value,
        confidence_score=job.result.confidence_score,
        summary=job.result.summary,
        methods=job.result.methods,
        findings=job.result.findings,
        artifacts=artifacts,
    )


@router.get("/analyses/{job_id}/report", response_model=ReportRead)
def get_analysis_report_route(job_id: int, access_key: str = Query(...), db: Session = Depends(get_db)) -> ReportRead:
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis job not found.")
    require_case_access(db, job.case.case_id, access_key)
    if not job.result or not job.result.report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis report is not ready yet.")
    return ReportRead(url=job.result.report.public_url, generated_at=job.result.report.generated_at)

