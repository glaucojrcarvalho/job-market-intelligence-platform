# API Examples

## Health

```bash
curl http://localhost:8000/health
```

## Readiness

```bash
curl http://localhost:8000/ready
```

## Metrics

```bash
curl http://localhost:8000/metrics
```

## Upload A Job

```bash
curl -X POST http://localhost:8000/v1/jobs:upload \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Backend Engineer",
    "description": "We need Python, FastAPI, PostgreSQL and AWS experience. Docker is required.",
    "source_name": "manual_upload",
    "work_mode": "remote",
    "location_text": "Remote - Brazil",
    "salary_text": "10000-15000 USD"
  }'
```

## List Jobs

```bash
curl http://localhost:8000/v1/jobs
```

The list remains unbounded when no query parameters are provided for compatibility. Public
interfaces should request a bounded result set and may filter by source or work mode:

```bash
curl "http://localhost:8000/v1/jobs?limit=20&offset=0&source_name=manual_upload&work_mode=remote"
```

`limit` accepts 1 through 100. `offset` must be zero or greater. Supported work-mode values are
`remote`, `hybrid`, `onsite`, and `unknown`.

## Get A Job

```bash
curl http://localhost:8000/v1/jobs/1
```

Job detail responses add the stored description, company, source URL, publication time, observation
time, employment type, structured location, seniority hint, and enrichment when those values are
available. Missing source fields remain `null`; the API does not infer them.

## Top Skills

```bash
curl http://localhost:8000/v1/analytics/skills/top
```

## Top Technologies

```bash
curl http://localhost:8000/v1/analytics/technologies/top
```

## Skill Co-Occurrence

```bash
curl http://localhost:8000/v1/analytics/skills/cooccurrence
```

## Candidate Matches

```bash
curl -X POST http://localhost:8000/v1/candidates/matches \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Python engineer with AWS API experience.",
    "skills": [
      {"name": "python"},
      {"name": "sql"}
    ],
    "location": "Brazil",
    "years_experience": 5
  }'
```

Candidate profiles use bounded structured input:

- summary: 10 to 2,000 characters after trimming
- skills: 1 to 50 entries, each with a 1 to 100 character name
- optional proficiency: 1 to 50 characters
- optional location: 1 to 255 characters
- optional years of experience: 0 to 80

The endpoint does not accept CV files or require names, email addresses, or contact details.

## Expected Response Characteristics

Job enrichment responses include:

- role family
- seniority
- skill list
- technology list
- evidence-bearing skill and technology detail
- heuristic summary

Candidate match responses include:

- match score
- matching skills
- missing skills
- confidence
- explanation reasons
