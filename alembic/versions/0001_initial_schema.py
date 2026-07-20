"""Create initial persistence schema.

Revision ID: 0001_initial_schema
Revises: None
Create Date: 2026-07-19 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_job_records",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(length=100), nullable=False),
        sa.Column("source_job_id", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("raw_job_record_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_name", sa.String(length=100), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("work_mode", sa.String(length=50), nullable=False),
        sa.Column("employment_type", sa.String(length=50), nullable=False),
        sa.Column("seniority_hint", sa.String(length=50), nullable=False),
        sa.Column("location_country", sa.String(length=100), nullable=True),
        sa.Column("location_region", sa.String(length=100), nullable=True),
        sa.Column("location_city", sa.String(length=100), nullable=True),
        sa.Column("location_raw_text", sa.String(length=255), nullable=True),
        sa.Column("compensation_currency", sa.String(length=20), nullable=True),
        sa.Column("compensation_minimum", sa.Float(), nullable=True),
        sa.Column("compensation_maximum", sa.Float(), nullable=True),
        sa.Column("compensation_raw_text", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["raw_job_record_id"], ["raw_job_records.id"], ondelete="SET NULL"),
    )
    op.create_table(
        "job_enrichments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("job_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("role_family", sa.String(length=100), nullable=True),
        sa.Column("seniority", sa.String(length=50), nullable=True),
        sa.Column("classification_confidence", sa.Float(), nullable=True),
        sa.Column("classification_evidence", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("technologies", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "candidate_profiles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("years_experience", sa.Float(), nullable=True),
        sa.Column("skills", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "candidate_matches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("candidate_profile_id", sa.Integer(), nullable=True),
        sa.Column("job_id", sa.Integer(), nullable=True),
        sa.Column("job_title", sa.String(length=255), nullable=False),
        sa.Column("source_name", sa.String(length=100), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("matching_skills", sa.JSON(), nullable=False),
        sa.Column("missing_skills", sa.JSON(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["candidate_profile_id"], ["candidate_profiles.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("candidate_matches")
    op.drop_table("candidate_profiles")
    op.drop_table("job_enrichments")
    op.drop_table("jobs")
    op.drop_table("raw_job_records")
