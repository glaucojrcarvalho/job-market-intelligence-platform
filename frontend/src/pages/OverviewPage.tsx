import { Link } from 'react-router'

import { apiBaseUrl } from '../api/client'

const repositoryUrl =
  'https://github.com/glaucojrcarvalho/job-market-intelligence-platform'

const capabilities = [
  {
    number: '01',
    title: 'Market signals',
    description:
      'Understand which skills and technologies appear in jobs stored in this instance.',
    to: '/market',
    label: 'Explore market',
  },
  {
    number: '02',
    title: 'Job evidence',
    description:
      'Inspect normalized job information and its available source context.',
    to: '/jobs',
    label: 'Browse jobs',
  },
  {
    number: '03',
    title: 'Explainable matching',
    description:
      'Compare a structured skill profile with jobs using deterministic factors.',
    to: '/match',
    label: 'Try matching',
  },
]

export function OverviewPage() {
  return (
    <div className="overview">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Open-source product · Active development</p>
          <h1>See the software engineering market more clearly.</h1>
          <p className="hero-lead">
            Structured job data, readable market signals, and explainable
            candidate matching—built to make evidence easier to explore.
          </p>
          <div className="button-row">
            <Link className="button button-primary" to="/market">
              Explore the platform
            </Link>
            <a className="button button-secondary" href={`${apiBaseUrl}/docs`}>
              Open API docs
            </a>
          </div>
        </div>

        <aside className="status-card" aria-labelledby="current-status">
          <div className="status-card-topline">
            <span className="live-dot" aria-hidden="true" />
            <span>Current status</span>
          </div>
          <h2 id="current-status">Local product foundation</h2>
          <p>
            The API, manual ingestion, deterministic enrichment, analytics,
            and matching run locally.
          </p>
          <dl>
            <div>
              <dt>Data source</dt>
              <dd>Manual or synthetic records</dd>
            </div>
            <div>
              <dt>External ingestion</dt>
              <dd>Not operational</dd>
            </div>
            <div>
              <dt>Live deployment</dt>
              <dd>Not available</dd>
            </div>
          </dl>
        </aside>
      </section>

      <section className="capabilities" aria-labelledby="capabilities-heading">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Product paths</p>
            <h2 id="capabilities-heading">
              From job descriptions to useful context
            </h2>
          </div>
          <p>
            Each experience is grounded in the same normalized backend
            contracts.
          </p>
        </div>

        <div className="capability-grid">
          {capabilities.map((capability) => (
            <article className="capability-card" key={capability.number}>
              <span className="card-number" aria-hidden="true">
                {capability.number}
              </span>
              <h3>{capability.title}</h3>
              <p>{capability.description}</p>
              <Link className="text-link" to={capability.to}>
                {capability.label}
                <span aria-hidden="true"> →</span>
              </Link>
            </article>
          ))}
        </div>
      </section>

      <section className="developer-strip" aria-labelledby="developer-heading">
        <div>
          <p className="eyebrow">Developer access</p>
          <h2 id="developer-heading">Prefer the underlying contracts?</h2>
          <p>
            Inspect system health, generated OpenAPI documentation, source
            code, and the architecture decisions directly.
          </p>
        </div>
        <div className="developer-links">
          <a href={`${apiBaseUrl}/docs`}>Swagger / OpenAPI</a>
          <a href={`${apiBaseUrl}/health`}>Health endpoint</a>
          <a href={repositoryUrl}>Repository</a>
          <a href={`${repositoryUrl}/blob/main/docs/03-architecture.md`}>
            Architecture
          </a>
        </div>
      </section>
    </div>
  )
}
