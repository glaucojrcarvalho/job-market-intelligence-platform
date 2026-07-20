"""ORM models for persistent storage."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from job_market.infrastructure.db.base import Base

JSONVariant = JSON().with_variant(JSONB, "postgresql")


class RawJobRecordModel(Base):
    __tablename__ = "raw_job_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    jobs: Mapped[list["JobModel"]] = relationship(back_populates="raw_record")


class JobModel(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    raw_job_record_id: Mapped[int | None] = mapped_column(
        ForeignKey("raw_job_records.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    work_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    employment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    seniority_hint: Mapped[str] = mapped_column(String(50), nullable=False)
    location_country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_raw_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    compensation_currency: Mapped[str | None] = mapped_column(String(20), nullable=True)
    compensation_minimum: Mapped[float | None] = mapped_column(Float, nullable=True)
    compensation_maximum: Mapped[float | None] = mapped_column(Float, nullable=True)
    compensation_raw_text: Mapped[str | None] = mapped_column(String(255), nullable=True)

    raw_record: Mapped[RawJobRecordModel | None] = relationship(back_populates="jobs")
    enrichment: Mapped["JobEnrichmentModel | None"] = relationship(
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan",
    )
    match_results: Mapped[list["CandidateMatchModel"]] = relationship(back_populates="job")


class JobEnrichmentModel(Base):
    __tablename__ = "job_enrichments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    role_family: Mapped[str | None] = mapped_column(String(100), nullable=True)
    seniority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    classification_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    classification_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[list[dict]] = mapped_column(JSONVariant, nullable=False, default=list)
    technologies: Mapped[list[dict]] = mapped_column(JSONVariant, nullable=False, default=list)

    job: Mapped[JobModel] = relationship(back_populates="enrichment")


class CandidateProfileModel(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    years_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    skills: Mapped[list[dict]] = mapped_column(JSONVariant, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    match_results: Mapped[list["CandidateMatchModel"]] = relationship(
        back_populates="candidate_profile"
    )


class CandidateMatchModel(Base):
    __tablename__ = "candidate_matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    candidate_profile_id: Mapped[int | None] = mapped_column(
        ForeignKey("candidate_profiles.id", ondelete="SET NULL"),
        nullable=True,
    )
    job_id: Mapped[int | None] = mapped_column(
        ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    matching_skills: Mapped[list[str]] = mapped_column(JSONVariant, nullable=False, default=list)
    missing_skills: Mapped[list[str]] = mapped_column(JSONVariant, nullable=False, default=list)
    reasons: Mapped[list[dict]] = mapped_column(JSONVariant, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    candidate_profile: Mapped[CandidateProfileModel | None] = relationship(
        back_populates="match_results"
    )
    job: Mapped[JobModel | None] = relationship(back_populates="match_results")
