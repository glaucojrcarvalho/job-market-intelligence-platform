# Product Vision

## Overview

Software Engineering Market Intelligence Platform transforms raw software-engineering job
postings into normalized, queryable market intelligence for engineers, recruiters, hiring
managers, and career advisors.

The repository began with a GeekHunter-based exploratory notebook. Version 2 preserves that
foundation while evolving toward a multi-source product. The current backend accepts manual
records, normalizes and enriches them, and exposes API workflows. Continuous external ingestion
and a public product are target capabilities, not current ones.

## Project Evolution

### Version 1 — Single-source market analysis

Version 1 used GeekHunter job data for exploratory analysis of technology demand and job
characteristics. The notebook remains valuable historical evidence and an analytical foundation;
it is not part of the application runtime.

### Version 2 — Multi-source market intelligence platform

Version 2 is an incremental evolution toward supported, authorized source connectors, a
source-independent job model, market analytics, job discovery, candidate matching, and future
AI-assisted insights. The first public-product milestone is a deployed, usable experience backed
by a validated real data source.

## Vision Statement

Build a trustworthy product that helps people understand software-engineering labor-market demand,
discover relevant roles, identify skill gaps, and compare candidates with jobs using transparent,
explainable intelligence.

## Target Users

- Software Engineers
- Backend Engineers
- Data Engineers
- Data Scientists
- Machine Learning Engineers
- Recruiters
- Career Coaches

## User Problems

- Job descriptions are noisy, inconsistent, and hard to compare at scale.
- Skills are described with many synonyms and informal phrasing.
- Candidates struggle to understand which technologies matter most in the current market.
- Recruiters and coaches lack structured evidence for role, seniority, and skill expectations.
- Existing job boards optimize for browsing, not market intelligence.

## Value Proposition

The platform turns unstructured job postings into structured, queryable intelligence:

- What skills, frameworks, databases, and cloud providers are most requested.
- Which skills frequently co-occur.
- How requirements differ across junior, mid, senior, and staff roles.
- Which jobs best match a candidate profile.
- Which skills a candidate is missing and why that matters.

## Product Principles

- Treat job postings as data products, not just scraped pages.
- Prefer deterministic enrichment before adding LLM dependencies.
- Keep outputs explainable and evidence-based.
- Preserve a clear boundary between exploration and production.
- Optimize for maintainability and reviewable incremental delivery.

## Scope Direction

### Near Term

- Build a backend platform around ingestion, normalization, enrichment, analytics, and matching.
- Select one supported real source first, while keeping source-specific mapping behind adapters.
- Expose all major capabilities through a FastAPI application.

### Longer Term

- Add scheduled imports from authorized APIs, feeds, or company-hosted ATS endpoints.
- Support candidate profile analysis and job matching.
- Add semantic search and selective LLM-assisted summaries.
- Expand to trend intelligence over time and region.

## Non-Goals For The Early Product

- Building a large frontend before the backend contract is stable.
- Using LLMs for core extraction tasks that are better handled deterministically.
- Supporting every job board immediately.
- Optimizing for scraping scale before validating the normalized domain model.

## Engineering Principles

The platform is developed with the following engineering principles:

- documented product requirements
- clean architecture
- typed Python modules
- API-first capabilities
- persistent storage
- automated tests
- CI/CD
- containerization
- cloud-ready infrastructure
