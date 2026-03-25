from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateAnalysisRequest(BaseModel):
    access_key: str
    evidence_id: int
    analysis_type: str = Field(pattern="^(image_forgery|document_forgery|ai_edited)$")


class AnalysisJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    evidence_id: int
    analysis_type: str
    status: str
    progress_message: str | None
    error_text: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


class ArtifactRead(BaseModel):
    label: str
    url: str


class AnalysisResultRead(BaseModel):
    forgery_status: str
    confidence_score: float
    summary: str
    methods: list[str]
    findings: dict
    artifacts: list[ArtifactRead]


class ReportRead(BaseModel):
    url: str
    generated_at: datetime

