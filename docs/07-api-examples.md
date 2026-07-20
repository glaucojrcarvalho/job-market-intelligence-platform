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

## Get A Job

```bash
curl http://localhost:8000/v1/jobs/1
```

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
