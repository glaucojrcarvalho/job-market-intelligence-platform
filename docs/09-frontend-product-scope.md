# Frontend Product Scope

## Document status

- Status: Proposed
- Date: July 29, 2026
- Delivery phase: First public product interface
- Scope: Product definition and API audit only

## Purpose

The first frontend turns the existing FastAPI workflows into a small, understandable product
without redesigning the backend. It must help a visitor understand the platform, inspect the data
stored in the running instance, explore supported analytics, browse jobs, and try deterministic
candidate matching.

This phase does not make the platform a live labor-market feed. The current production path
accepts manually uploaded jobs, and no authorized external connector or scheduled ingestion is
operational. Every product page must keep that limitation visible.

## Product principles

- Present implemented capabilities separately from planned capabilities.
- Render values returned by the API; do not hardcode usage-like metrics.
- Describe the dataset as records stored in this instance, not as complete market coverage.
- Display missing values as unavailable; do not invent company, location, salary, or provenance.
- Keep matching request-scoped and avoid CV uploads, accounts, and unnecessary personal data.
- Make loading, empty, failure, and partial-data states first-class interface states.
- Preserve direct access to OpenAPI documentation and system health information.
- Use synthetic, manually authored data for development, tests, and screenshots.

## Intended users and primary journeys

### Visitor

1. Opens the overview.
2. Understands what the platform implements today.
3. Sees that displayed data may be manual or synthetic and is not live market coverage.
4. Opens the dashboard, job explorer, or developer documentation.

### Market explorer

1. Opens the dashboard.
2. Sees the number of jobs stored in this instance.
3. Compares top skills and technologies and inspects skill co-occurrence.
4. Understands the dataset limitation and can move to the underlying jobs.

### Candidate

1. Enters a short professional summary and a list of skills.
2. Optionally enters location and years of experience.
3. Submits the profile without uploading a CV or creating an account.
4. Reviews ranked jobs, match score, matched skills, missing skills, confidence, and deterministic
   reasons.

### Developer

1. Opens Swagger/OpenAPI documentation, health, repository, or architecture documentation.
2. Can distinguish the browser product from developer-facing API access.

## Initial information architecture

The frontend is a single-page application with four primary routes.

| Route | Page | Purpose |
| --- | --- | --- |
| `/` | Product overview | Explain the product, current status, implemented workflows, data limitation, and developer links. |
| `/market` | Market dashboard | Visualize supported aggregates from jobs stored in the current instance. |
| `/jobs` | Job explorer | List jobs and reveal the supported details and enrichment for a selected job. |
| `/match` | Candidate matching | Collect a minimal structured profile and display ranked, explainable results. |

The persistent application shell contains the product name, primary navigation, a dataset
limitation notice, and a link to API documentation. On small screens, navigation may wrap or use a
keyboard-accessible disclosure control.

## Current API audit

The audit reflects `main` as of July 29, 2026.

### System and developer access

| Endpoint | Current response | Frontend use | Gap or constraint |
| --- | --- | --- | --- |
| `GET /health` | Service status | Developer link and optional availability check | Sufficient for the first interface. |
| `GET /ready` | Repository and environment checks | Developer diagnostics only | Do not expose internal detail as a product metric. |
| `GET /version` | App name, version, environment | Product status metadata | Does not describe dataset source, freshness, or ingestion mode. |
| `GET /metrics` | Process-local request counters | Developer diagnostics only | Not market analytics and must not be presented as product usage. |
| `GET /docs` | Generated Swagger UI | Developer access | Link directly; do not make it the primary experience. |
| `GET /openapi.json` | OpenAPI document | Development and contract reference | Sufficient. |

### Jobs

| Endpoint | Current response | Frontend use | Gap or constraint |
| --- | --- | --- | --- |
| `POST /v1/jobs:upload` | Stored job plus enrichment | Existing manual ingestion workflow | Not part of the public frontend in this phase. |
| `GET /v1/jobs` | ID, title, source name, work mode, location text, salary text | Initial list, total stored jobs, source labels, and client-side work-mode count | No pagination, filtering, company, source URL, timestamps, seniority, skills, technologies, or total metadata. |
| `GET /v1/jobs/{job_id}` | List fields plus enrichment | Selected-job enrichment, including role family, seniority, skills, technologies, and summary | Still omits description, company, source URL, publication time, observation time, employment type, and structured location. |

The domain and database already store several omitted fields, including company name, source URL,
publication time, employment type, and normalized location components. Observation time exists on
the linked raw record. Exposing them requires an explicit, tested response-contract change.

### Analytics

| Endpoint | Current response | Frontend use | Gap or constraint |
| --- | --- | --- | --- |
| `GET /v1/analytics/skills/top` | Skill label and count | Ranked bar or list visualization | No limit, filters, total, or freshness metadata. |
| `GET /v1/analytics/technologies/top` | Technology label and count | Ranked bar or list visualization | No limit, filters, total, or freshness metadata. |
| `GET /v1/analytics/skills/cooccurrence` | Skill pair and frequency | Compact table or accessible relationship list | No limit or filters; large datasets may require backend bounding later. |

The current dashboard can also derive the total job count and work-mode distribution from
`GET /v1/jobs`. That is acceptable for the small local dataset but is not a scalable aggregation
contract.

Seniority distribution is not supportable without fetching every job detail individually.
Location and salary analytics are not implemented. These visualizations must remain absent until
dedicated aggregates exist.

### Candidate matching

| Endpoint | Current response | Frontend use | Gap or constraint |
| --- | --- | --- | --- |
| `POST /v1/candidates/matches` | Ranked match results with job ID/title, source, score, matched skills, missing skills, confidence, and reasons | Complete initial matching journey | Request validation is minimal; empty summary or skills are currently accepted by the schema. Matches are persisted by the SQL repository even though candidate profiles are request-scoped. |

The supported request fields are summary, skills with optional proficiency, optional location,
and optional years of experience. The UI will require a non-empty summary and at least one
non-empty skill before submission. It will explain that scores are deterministic indicators, not
calibrated hiring recommendations.

## Metrics approved for the first dashboard

| Metric | Source | Presentation |
| --- | --- | --- |
| Total stored jobs | Length of `GET /v1/jobs` | Summary count labeled “jobs in this instance.” |
| Top skills | `GET /v1/analytics/skills/top` | Accessible ranked bars with numeric values. |
| Top technologies | `GET /v1/analytics/technologies/top` | Accessible ranked bars with numeric values. |
| Skill co-occurrence | `GET /v1/analytics/skills/cooccurrence` | Table or ranked pair list with frequencies. |
| Work-mode distribution | Derived from `GET /v1/jobs` | Counts for API-provided values, including `unknown`. |

The following are explicitly deferred: seniority distribution, location distribution, salary
analytics, historical trends, freshness trends, source coverage, and any metric implying active
users or live ingestion.

## Page-level scope

### Product overview

Include:

- product name and concise value proposition;
- “under active development” status;
- implemented capability summary;
- prominent notice that data is stored in the running instance and may be manual or synthetic;
- statement that no live external ingestion or verified public deployment exists;
- links to market, jobs, matching, API docs, health, repository, and architecture.

Do not include fabricated customer counts, coverage claims, testimonials, or production URLs.

### Market dashboard

Fetch jobs and all three analytics endpoints independently. A failure in one panel must not erase
successful panels. Include:

- a page-level loading state for initial navigation;
- per-panel loading and failure states;
- a meaningful zero-job state with no fake chart values;
- numeric values in text as well as visual marks;
- the dataset limitation notice adjacent to the metrics.

### Job explorer

The target experience includes a bounded or paginated list, supported filters, source provenance,
and a selected-job detail. The initial implementation must wait for the response-contract gap
identified below rather than invent missing fields.

For absent optional values, use neutral text such as “Not provided.” Never convert absence into
“remote,” a company name, a location, or a salary.

### Candidate matching

Use a structured form, not CV upload. Required frontend inputs are a short summary and one or more
skills. Location, years of experience, and skill proficiency remain optional.

Results show the API-provided rank order, score, matched skills, missing skills, confidence, and
reason messages. Empty results explain that no stored jobs are available to compare. Validation
errors are associated with their fields and announced to assistive technology.

The page must state that:

- profiles are submitted for matching without a user account;
- users should not enter names, emails, contact details, or other sensitive information;
- scores are deterministic and not suitable for automated hiring decisions.

## Required interface states

Every API-backed page or panel must define:

- **loading:** progress text or skeleton with an accessible status message;
- **empty:** explanation tied to the actual missing dataset or result;
- **failure:** plain-language message, retry action, and retained successful content;
- **success:** readable content with values represented in text;
- **partial data:** unavailable optional fields remain visibly unavailable.

Controls use semantic elements, programmatic labels, keyboard operation, visible focus styles,
sufficient contrast, and touch targets suitable for mobile layouts. No chart may communicate its
meaning through color alone.

## Data provenance and public-safety policy

Until an authorized connector is operational, the global notice should read substantially:

> Data shown comes from records stored in this instance and may be manually uploaded or synthetic.
> It does not represent live or complete job-market coverage.

Each job displays `source_name`. A source link, publication time, observation time, and last
updated time may be shown only after the API exposes those values. `manual_upload` must be rendered
as “Manual upload,” not as an external feed.

Development fixtures and screenshots must contain only synthetic, manually authored records.
They must not contain personal candidate information, credentials, personal paths, private hosts,
browser account details, or copied job-board records without redistribution permission.

## Backend gaps and delivery boundaries

Backend changes should be narrowly scoped, preserve existing fields, and receive API tests.

| Priority | Gap | Smallest credible change | Delivery boundary |
| --- | --- | --- | --- |
| Required before browser API calls | No CORS configuration | Add an environment-configured allow-list for the local frontend origin; default to no cross-origin access outside configured environments. | Compose integration PR because it is required by the deployed local topology. |
| Required for credible job explorer | Job responses omit available detail and provenance | Extend detail response additively with company, description, source URL, publication time, employment type, and structured location; expose observation time only through the linked raw record. | Dedicated backend PR before or alongside the job explorer, not hidden in UI code. |
| Required as datasets grow | Job list has no pagination, result limit, filters, or metadata | Add bounded `limit`/`offset` parameters and a compatible paginated response strategy; document any contract transition. | Dedicated backend PR because it changes the public list contract. |
| Required for explicit dataset labeling | No dataset status or freshness contract | Add a small public status response describing ingestion mode, known source types, record count, and latest observation when those semantics are reliable. | Dedicated backend/product-status PR; use the conservative static notice until then. |
| Deferred dashboard capability | No seniority, location, salary, source, or time aggregates | Add only aggregates justified by populated normalized fields and coverage metadata. | One independently reviewable analytics API PR per coherent contract. |
| Validation hardening | Candidate schema accepts empty summary/skills and unconstrained experience | Add backward-conscious validation with API tests and clear `422` responses. | Candidate matching UI PR if treated as inseparable form support, otherwise a preceding backend PR. |

No backend changes are part of this documentation PR.

## Frontend delivery sequence

1. Establish the React application shell, routes, API configuration, and reusable states.
2. Build the dashboard from currently supported responses.
3. Address the required job response and pagination gaps in independently reviewable backend work.
4. Build the job explorer against the documented contract.
5. Build and validate the candidate matching form.
6. Add CORS and integrate the frontend into Docker Compose.
7. Add frontend tests, build checks, and repository-sensitive-file scanning to CI.
8. Add safe screenshots and update the public README.

Each step starts from the latest merged `main` and is delivered through its own pull request.

## Acceptance criteria for the frontend phase

- The four product routes run locally and remain usable on narrow screens.
- Dashboard values come from backend responses and label dataset limitations.
- Jobs are explorable without direct API knowledge and absent values are not invented.
- Candidate matching works without CV upload or unnecessary personal data.
- Empty, loading, partial, and failure states are tested.
- Docker Compose starts frontend, API, and PostgreSQL with environment-configured URLs and ports.
- CI validates frontend and existing backend quality without weakening current checks.
- Public screenshots use safe synthetic data.
- Documentation separates implemented behavior, limitations, and future work.
