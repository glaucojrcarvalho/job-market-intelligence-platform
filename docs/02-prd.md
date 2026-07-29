# Product Requirements Document

## Document Status

- Status: Active
- Date: July 19, 2026
- Product: Software Engineering Market Intelligence Platform

## 1. Problem Statement

Technical professionals and talent stakeholders rely on unstructured job postings to understand market demand, but job descriptions are noisy, inconsistent, and difficult to analyze systematically.

The current ecosystem is optimized for vacancy discovery, not labor-market intelligence. Users can browse listings, but they cannot easily answer higher-value questions such as:

- which technologies are most requested right now
- which skills commonly appear together
- how expectations differ by seniority
- which cloud providers dominate a segment
- which jobs best match a candidate profile
- which skills a candidate should develop next

## 2. Product Goal

Create a usable market-intelligence product that ingests software-engineering job postings from
supported sources and transforms them into normalized data for discovery, analytics, and
candidate matching.

The current repository is a backend foundation. Manual upload, deterministic enrichment,
analytics, and matching are implemented. An operational external source, scheduled ingestion,
deduplication, public interface, and production deployment remain release work.

## 3. Target Users

### Primary Users

- Software Engineers
- Backend Engineers
- Data Engineers
- Data Scientists
- Machine Learning Engineers

### Secondary Users

- Recruiters
- Career Coaches

## 4. User Needs

### Engineers Need

- visibility into current demand by skill, framework, cloud, and seniority
- evidence-based assessment of market fit
- prioritized recommendations for skill development
- job matching with explainable reasons

### Recruiters And Coaches Need

- structured understanding of role requirements
- better comparison across postings
- market trends by region and seniority
- evidence-backed candidate guidance

## 5. Value Proposition

The platform converts raw job descriptions into structured data products that support:

- market intelligence
- trend analysis
- candidate-job matching
- explainable recommendations

Unlike a notebook or generic scraper, the product will provide repeatable ingestion, normalized data, API access, and production-quality engineering.

## 6. Product Scope

### Implemented Foundation

- manual job upload through the API
- raw job storage
- normalized job model
- deterministic enrichment for skills, technologies, cloud providers, frameworks, and seniority
- analytics endpoints for skill and technology frequency and skill co-occurrence
- structured candidate profile intake per request
- candidate-job match scoring
- evidence and missing-skill output
- health endpoints
- OpenAPI documentation

### Planned Product MVP

- one authorized and operational external source connector
- scheduled, observable, and idempotent ingestion
- deterministic deduplication and update detection
- filtering and pagination for job discovery
- a minimal public job explorer and market dashboard
- production deployment and a verified demo URL

### Out Of Scope For The Product MVP

- broad multi-source scraping coverage
- polished end-user frontend
- real-time streaming ingestion
- fully autonomous LLM-driven extraction
- recruiter CRM workflows
- advanced recommendation personalization

## 7. MVP Feature Set

### A. Job Ingestion

- ingest job postings from one validated source adapter
- accept manual job payload upload through API
- validate incoming payloads
- persist raw and normalized records separately

### B. Normalization

- clean text fields
- normalize seniority labels
- normalize work arrangement labels
- normalize skill names using a controlled vocabulary
- normalize salary ranges when present
- normalize locations to a standard structure

### C. AI And NLP Enrichment

- rule-based or dictionary-based skill extraction
- cloud provider detection
- framework and database detection
- role family classification
- seniority classification
- optional summary generation behind an interface, disabled by default

### D. Analytics

- top skills
- top technologies
- demand by location
- demand by seniority
- remote versus on-site distribution
- skill co-occurrence summaries

### E. Candidate Analysis

- ingest CV or structured candidate profile
- compute match score against jobs
- return matching skills
- return missing skills
- return evidence snippets
- return confidence score

### F. Platform

- FastAPI service
- PostgreSQL persistence
- structured logging
- health and readiness endpoints
- test suite
- Dockerized local environment

## 8. Functional Requirements

### Ingestion Requirements

- The system must accept job payloads through a typed API contract.
- The system must support source-specific adapters.
- The system must preserve raw source content for traceability.
- The system must deduplicate jobs using deterministic keys or heuristics.

### Enrichment Requirements

- The system must extract skills and technologies from job descriptions.
- The system must classify role family and seniority.
- The system must expose normalized enrichment results through the API.
- The system should provide explanation metadata where possible.

### Analytics Requirements

- The system must provide aggregate analytics endpoints.
- The system should support filtering by source, location, role family, seniority, and work mode.
- The system should expose counts and frequencies in machine-readable format.

### Candidate Matching Requirements

- The system must accept a candidate profile or CV-derived input.
- The system must score jobs against the candidate profile.
- The system must explain strong and weak match factors.
- The system should provide confidence with each match result.

### Platform Requirements

- The system must expose OpenAPI documentation.
- The system must provide health and readiness endpoints.
- The system must support environment-based configuration.
- The system must return consistent error responses.

## 9. Non-Functional Requirements

- Maintainable codebase with clean separation of concerns
- Type-safe Python implementation
- Testable service boundaries
- Production-ready logging and error handling
- Reasonable performance for batch ingestion and read-heavy analytics
- Extensibility for future AI providers and data sources
- Security-conscious configuration and secrets handling

## 10. Success Metrics

### Product Metrics

- number of jobs ingested successfully
- percentage of jobs normalized successfully
- percentage of jobs enriched successfully
- candidate match response usefulness from qualitative review
- number of analytics queries supported by API

### Engineering Metrics

- automated test pass rate
- type-check pass rate
- deployment success rate
- ingestion failure rate
- API error rate
- time to onboard a new source adapter

## 11. Risks And Trade-Offs

### Key Risks

- scraping sources may change HTML structure
- skill normalization can be noisy without a curated taxonomy
- candidate matching can appear authoritative before it is truly calibrated
- LLM features can add cost, latency, and explainability concerns

### Trade-Off Decisions

- prefer deterministic extraction first for transparency and reliability
- prefer one source well-implemented over many brittle adapters
- prefer API-first backend maturity before frontend investment
- preserve notebook reproducibility, but do not let it dictate production architecture

## 12. MVP Release Criteria

The product MVP will be ready when:

- at least one ingestion source is operational
- jobs are stored in PostgreSQL
- normalized and enriched job records are queryable through FastAPI
- analytics endpoints are available and documented
- candidate-job match scoring is available
- automated tests cover critical services and API flows
- the application runs locally through Docker Compose
- a minimal public interface and verified deployment are available

## 13. Future Roadmap

### Near-Term After MVP

- add scheduled imports
- add more source adapters
- improve skill taxonomy and normalization quality
- add trend analysis over time
- add semantic search for jobs and skills

### Later-Stage Enhancements

- LLM-assisted summaries and reasoning
- recruiter-facing benchmarking workflows
- candidate learning-path recommendations
- region and salary benchmarking
- monitoring dashboards and alerts

## 14. Open Product Questions

- Which additional sources provide sufficient data quality and stable integration terms?
- Which enrichment metrics should determine whether deterministic extraction needs augmentation?
- What confidence calibration is required before match scores can support higher-stakes workflows?
- At what ingestion volume should synchronous processing move to queue-backed workers?
