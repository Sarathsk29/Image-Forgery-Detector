from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.case import CaseDetail, CreateCaseRequest, CreateCaseResponse, EvidenceRead, OpenCaseRequest
from app.schemas.analysis import AnalysisJobRead, AnalysisResultRead
from app.services.cases import create_case, get_case_by_public_id, require_case_access, save_evidence


router = APIRouter()


@router.post("/cases", response_model=CreateCaseResponse)
def create_case_route(payload: CreateCaseRequest, db: Session = Depends(get_db)) -> CreateCaseResponse:
    case, access_key = create_case(db, payload.title, payload.notes)
    return CreateCaseResponse(case_id=case.case_id, access_key=access_key, status=case.status.value, created_at=case.created_at)


@router.post("/cases/open", response_model=CaseDetail)
def open_case_route(payload: OpenCaseRequest, db: Session = Depends(get_db)) -> CaseDetail:
    case = require_case_access(db, payload.case_id, payload.access_key)
    # Build response with latest result per evidence
    evidence_items = []
    for ev in case.evidence_items:
        latest_job = None
        # find latest completed job for this evidence that has a result
        jobs = [j for j in case.analysis_jobs if j.evidence_id == ev.id and j.status.name == "completed" and j.result is not None]
        if jobs:
            latest_job = sorted(jobs, key=lambda j: j.created_at, reverse=True)[0]
        ev_data = EvidenceRead.model_validate(ev).model_dump()
        if latest_job and latest_job.result:
            ev_data["latest_result"] = AnalysisResultRead.model_validate(latest_job.result).model_dump()
        else:
            ev_data["latest_result"] = None
        evidence_items.append(ev_data)

    case_dict = {
        "case_id": case.case_id,
        "title": case.title,
        "notes": case.notes,
        "status": case.status.value,
        "created_at": case.created_at,
        "evidence_items": evidence_items,
        "analysis_jobs": [AnalysisJobRead.model_validate(j).model_dump() for j in case.analysis_jobs],
    }
    return CaseDetail.model_validate(case_dict)


@router.get("/cases/{case_id}", response_model=CaseDetail)
def get_case_route(case_id: str, access_key: str, db: Session = Depends(get_db)) -> CaseDetail:
    case = require_case_access(db, case_id, access_key)
    # reuse open_case_route logic
    evidence_items = []
    for ev in case.evidence_items:
        latest_job = None
        jobs = [j for j in case.analysis_jobs if j.evidence_id == ev.id and j.status.name == "completed" and j.result is not None]
        if jobs:
            latest_job = sorted(jobs, key=lambda j: j.created_at, reverse=True)[0]
        ev_data = EvidenceRead.model_validate(ev).model_dump()
        if latest_job and latest_job.result:
            ev_data["latest_result"] = AnalysisResultRead.model_validate(latest_job.result).model_dump()
        else:
            ev_data["latest_result"] = None
        evidence_items.append(ev_data)

    case_dict = {
        "case_id": case.case_id,
        "title": case.title,
        "notes": case.notes,
        "status": case.status.value,
        "created_at": case.created_at,
        "evidence_items": evidence_items,
        "analysis_jobs": [AnalysisJobRead.model_validate(j).model_dump() for j in case.analysis_jobs],
    }
    return CaseDetail.model_validate(case_dict)


@router.post("/cases/{case_id}/evidence", response_model=EvidenceRead)
async def upload_evidence_route(
    case_id: str,
    access_key: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> EvidenceRead:
    case = require_case_access(db, case_id, access_key)
    raw_data = await file.read()
    evidence = save_evidence(db, case, file, raw_data)
    return EvidenceRead.model_validate(evidence)


@router.get("/cases/{case_id}/evidence", response_model=list[EvidenceRead])
def list_evidence_route(case_id: str, access_key: str, db: Session = Depends(get_db)) -> list[EvidenceRead]:
    case = require_case_access(db, case_id, access_key)
    return [EvidenceRead.model_validate(item) for item in case.evidence_items]

