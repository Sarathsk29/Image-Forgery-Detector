from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateCaseRequest(BaseModel):
    title: str | None = None
    notes: str | None = None


class OpenCaseRequest(BaseModel):
    case_id: str
    access_key: str


class EvidenceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    mime_type: str
    size: int
    storage_url: str
    file_hash: str
    uploaded_at: datetime
    latest_result: Optional["AnalysisResultRead"] = None


class CreateCaseResponse(BaseModel):
    case_id: str
    access_key: str
    status: str
    created_at: datetime


class CaseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    case_id: str
    title: str | None
    notes: str | None
    status: str
    created_at: datetime


class CaseDetail(CaseSummary):
    evidence_items: list[EvidenceRead]
    analysis_jobs: list["AnalysisJobRead"]


from app.schemas.analysis import AnalysisJobRead, AnalysisResultRead  # noqa: E402

EvidenceRead.model_rebuild()
CaseDetail.model_rebuild()

