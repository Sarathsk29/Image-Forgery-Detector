from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import JSON, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class CaseStatus(str, Enum):
    open = "open"
    closed = "closed"


class AnalysisType(str, Enum):
    image_forgery = "image_forgery"
    document_forgery = "document_forgery"
    ai_edited = "ai_edited"


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class ForgeryStatus(str, Enum):
    authentic = "authentic"
    tampered = "tampered"
    suspicious = "suspicious"


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    access_key_hash: Mapped[str] = mapped_column(String(255))
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[CaseStatus] = mapped_column(SqlEnum(CaseStatus), default=CaseStatus.open)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    evidence_items: Mapped[list[Evidence]] = relationship(back_populates="case", cascade="all, delete-orphan")
    analysis_jobs: Mapped[list[AnalysisJob]] = relationship(back_populates="case", cascade="all, delete-orphan")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(128))
    size: Mapped[int] = mapped_column(Integer)
    storage_url: Mapped[str] = mapped_column(String(500))
    storage_path: Mapped[str] = mapped_column(String(500))
    file_hash: Mapped[str] = mapped_column(String(64))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    case: Mapped[Case] = relationship(back_populates="evidence_items")
    analysis_jobs: Mapped[list[AnalysisJob]] = relationship(back_populates="evidence", cascade="all, delete-orphan")


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    evidence_id: Mapped[int] = mapped_column(ForeignKey("evidence.id"))
    analysis_type: Mapped[AnalysisType] = mapped_column(SqlEnum(AnalysisType))
    status: Mapped[JobStatus] = mapped_column(SqlEnum(JobStatus), default=JobStatus.queued)
    progress_message: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    case: Mapped[Case] = relationship(back_populates="analysis_jobs")
    evidence: Mapped[Evidence] = relationship(back_populates="analysis_jobs")
    result: Mapped[AnalysisResult | None] = relationship(back_populates="job", uselist=False, cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("analysis_jobs.id"), unique=True)
    forgery_status: Mapped[ForgeryStatus] = mapped_column(SqlEnum(ForgeryStatus))
    confidence_score: Mapped[float] = mapped_column()
    summary: Mapped[str] = mapped_column(Text)
    methods: Mapped[list[str]] = mapped_column(JSON)
    findings: Mapped[dict] = mapped_column(JSON)
    artifact_urls: Mapped[list[str]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    job: Mapped[AnalysisJob] = relationship(back_populates="result")
    report: Mapped[Report | None] = relationship(back_populates="analysis_result", uselist=False, cascade="all, delete-orphan")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    analysis_result_id: Mapped[int] = mapped_column(ForeignKey("analysis_results.id"), unique=True)
    local_path: Mapped[str] = mapped_column(String(500))
    public_url: Mapped[str] = mapped_column(String(500))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    analysis_result: Mapped[AnalysisResult] = relationship(back_populates="report")

