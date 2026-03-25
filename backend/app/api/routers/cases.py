from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.case import CaseDetail, CreateCaseRequest, CreateCaseResponse, EvidenceRead, OpenCaseRequest
from app.services.cases import create_case, get_case_by_public_id, require_case_access, save_evidence


router = APIRouter()


@router.post("/cases", response_model=CreateCaseResponse)
def create_case_route(payload: CreateCaseRequest, db: Session = Depends(get_db)) -> CreateCaseResponse:
    case, access_key = create_case(db, payload.title, payload.notes)
    return CreateCaseResponse(case_id=case.case_id, access_key=access_key, status=case.status.value, created_at=case.created_at)


@router.post("/cases/open", response_model=CaseDetail)
def open_case_route(payload: OpenCaseRequest, db: Session = Depends(get_db)) -> CaseDetail:
    case = require_case_access(db, payload.case_id, payload.access_key)
    return CaseDetail.model_validate(case)


@router.get("/cases/{case_id}", response_model=CaseDetail)
def get_case_route(case_id: str, access_key: str, db: Session = Depends(get_db)) -> CaseDetail:
    case = require_case_access(db, case_id, access_key)
    return CaseDetail.model_validate(case)


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

