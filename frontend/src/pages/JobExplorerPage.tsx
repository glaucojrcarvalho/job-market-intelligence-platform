import { useCallback, useState } from 'react'

import {
  getJob,
  listJobs,
  type JobDetail,
  type JobSummary,
  type WorkMode,
} from '../api/jobs'
import { PanelState } from '../components/PanelState'
import { useApiResource } from '../hooks/useApiResource'

const pageSize = 12
const workModes: { value: WorkMode | ''; label: string }[] = [
  { value: '', label: 'All work modes' },
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'onsite', label: 'On-site' },
  { value: 'unknown', label: 'Not specified' },
]

function formatLabel(value: string) {
  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function displayValue(value: string | null | undefined) {
  return value?.trim() || 'Not provided'
}

function displayEnum(value: string | null | undefined) {
  return !value || value === 'unknown' ? 'Not provided' : formatLabel(value)
}

function formatDate(value: string | null) {
  if (!value) {
    return 'Not provided'
  }

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return 'Not provided'
  }

  return new Intl.DateTimeFormat('en', {
    dateStyle: 'medium',
    timeZone: 'UTC',
  }).format(date)
}

function safeSourceUrl(value: string | null) {
  if (!value) {
    return null
  }

  try {
    const url = new URL(value)
    return url.protocol === 'http:' || url.protocol === 'https:'
      ? url.toString()
      : null
  } catch {
    return null
  }
}

function JobDetailPanel({
  jobId,
  onClose,
}: {
  jobId: number
  onClose: () => void
}) {
  const load = useCallback(
    (signal: AbortSignal) => getJob(jobId, signal),
    [jobId],
  )
  const detail = useApiResource(load)

  return (
    <section
      className="job-detail-shell"
      id={`job-detail-${jobId}`}
      aria-labelledby={`job-detail-title-${jobId}`}
    >
      <div className="job-detail-toolbar">
        <p>Selected job details</p>
        <button type="button" onClick={onClose}>
          Close details
        </button>
      </div>
      <PanelState
        state={detail.state}
        isEmpty={() => false}
        emptyTitle="Job details are unavailable"
        emptyMessage="No detail was returned for this job."
        errorTitle="Job details could not be loaded"
        onRetry={detail.retry}
      >
        {(job) => <JobDetailContent job={job} />}
      </PanelState>
    </section>
  )
}

function JobDetailContent({ job }: { job: JobDetail }) {
  const sourceUrl = safeSourceUrl(job.source_url)
  const seniority =
    job.enrichment?.seniority && job.enrichment.seniority !== 'unknown'
      ? job.enrichment.seniority
      : job.seniority_hint
  const location =
    job.location.raw_text ||
    [job.location.city, job.location.region, job.location.country]
      .filter(Boolean)
      .join(', ')

  return (
    <article className="job-detail">
      <header className="job-detail-header">
        <div>
          <p className="panel-kicker">{formatLabel(job.source_name)}</p>
          <h2 id={`job-detail-title-${job.job_id}`}>{job.title}</h2>
          <p>{displayValue(job.company_name)}</p>
        </div>
        <span className="job-mode">{displayEnum(job.work_mode)}</span>
      </header>

      <dl className="job-facts">
        <div>
          <dt>Location</dt>
          <dd>{displayValue(location)}</dd>
        </div>
        <div>
          <dt>Seniority</dt>
          <dd>{displayEnum(seniority)}</dd>
        </div>
        <div>
          <dt>Employment</dt>
          <dd>{displayEnum(job.employment_type)}</dd>
        </div>
        <div>
          <dt>Published</dt>
          <dd>{formatDate(job.posted_at)}</dd>
        </div>
        <div>
          <dt>Observed</dt>
          <dd>{formatDate(job.observed_at)}</dd>
        </div>
        <div>
          <dt>Source</dt>
          <dd>
            {sourceUrl ? (
              <a href={sourceUrl} rel="noreferrer" target="_blank">
                {formatLabel(job.source_name)}
                <span className="visually-hidden"> (opens in a new tab)</span>
              </a>
            ) : (
              formatLabel(job.source_name)
            )}
          </dd>
        </div>
      </dl>

      {job.enrichment?.summary && (
        <section className="job-detail-section">
          <h3>Role summary</h3>
          <p>{job.enrichment.summary}</p>
        </section>
      )}

      <section className="job-detail-section">
        <h3>Description</h3>
        <p className="job-description">{job.description}</p>
      </section>

      <div className="job-taxonomy-grid">
        <TaxonomyList
          title="Skills"
          items={job.enrichment?.skills ?? []}
          emptyMessage="No skills detected"
        />
        <TaxonomyList
          title="Technologies"
          items={job.enrichment?.technologies ?? []}
          emptyMessage="No technologies detected"
        />
      </div>
    </article>
  )
}

function TaxonomyList({
  title,
  items,
  emptyMessage,
}: {
  title: string
  items: string[]
  emptyMessage: string
}) {
  return (
    <section className="taxonomy-group">
      <h3>{title}</h3>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p>{emptyMessage}</p>
      )}
    </section>
  )
}

function JobCard({
  job,
  selected,
  onSelect,
}: {
  job: JobSummary
  selected: boolean
  onSelect: () => void
}) {
  return (
    <article className={selected ? 'job-card job-card-selected' : 'job-card'}>
      <div className="job-card-topline">
        <span>{formatLabel(job.source_name)}</span>
        <span>{displayEnum(job.work_mode)}</span>
      </div>
      <h2>{job.title}</h2>
      <p className="job-company">{displayValue(job.company_name)}</p>
      <dl className="job-card-facts">
        <div>
          <dt>Location</dt>
          <dd>{displayValue(job.location_text)}</dd>
        </div>
        <div>
          <dt>Employment</dt>
          <dd>{displayEnum(job.employment_type)}</dd>
        </div>
      </dl>
      <button
        className="job-detail-button"
        type="button"
        aria-expanded={selected}
        aria-controls={selected ? `job-detail-${job.job_id}` : undefined}
        onClick={onSelect}
      >
        {selected ? 'Details selected' : 'View details'}
        <span aria-hidden="true">→</span>
      </button>
    </article>
  )
}

export function JobExplorerPage() {
  const [offset, setOffset] = useState(0)
  const [workMode, setWorkMode] = useState<WorkMode | ''>('')
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null)

  const loadJobs = useCallback(
    (signal: AbortSignal) =>
      listJobs(
        {
          limit: pageSize + 1,
          offset,
          workMode: workMode || undefined,
        },
        signal,
      ),
    [offset, workMode],
  )
  const jobs = useApiResource(loadJobs)

  function updateWorkMode(value: string) {
    setWorkMode(value as WorkMode | '')
    setOffset(0)
    setSelectedJobId(null)
  }

  return (
    <div className="job-explorer page-stack">
      <header className="page-header job-explorer-header">
        <div>
          <p className="eyebrow">Job explorer</p>
          <h1>Inspect the roles behind the signals.</h1>
          <p className="page-lead">
            Browse bounded results, filter by supported work mode, and inspect
            the available enrichment and source context.
          </p>
        </div>
        <div className="explorer-filter">
          <label htmlFor="work-mode-filter">Work mode</label>
          <select
            id="work-mode-filter"
            value={workMode}
            onChange={(event) => updateWorkMode(event.target.value)}
          >
            {workModes.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </header>

      <PanelState
        state={jobs.state}
        isEmpty={(data) => data.length === 0}
        emptyTitle={workMode ? 'No jobs match this work mode' : 'No jobs are stored yet'}
        emptyMessage={
          workMode
            ? 'Choose another work mode or return to all available jobs.'
            : 'Jobs will appear here after manually authored or authorized records are added.'
        }
        errorTitle="Jobs could not be loaded"
        onRetry={jobs.retry}
      >
        {(data) => {
          const visibleJobs = data.slice(0, pageSize)
          const hasNextPage = data.length > pageSize
          const pageNumber = Math.floor(offset / pageSize) + 1

          return (
            <>
              <div className="explorer-results-heading">
                <p>
                  Page {pageNumber} · Showing {visibleJobs.length} job
                  {visibleJobs.length === 1 ? '' : 's'}
                </p>
                <p>Missing source fields are shown as not provided.</p>
              </div>

              <div className="job-grid">
                {visibleJobs.map((job) => (
                  <JobCard
                    job={job}
                    selected={selectedJobId === job.job_id}
                    onSelect={() => setSelectedJobId(job.job_id)}
                    key={job.job_id}
                  />
                ))}
              </div>

              {selectedJobId !== null && (
                <JobDetailPanel
                  jobId={selectedJobId}
                  onClose={() => setSelectedJobId(null)}
                  key={selectedJobId}
                />
              )}

              <nav className="pagination" aria-label="Job result pages">
                <button
                  type="button"
                  disabled={offset === 0}
                  onClick={() => {
                    setOffset((current) => Math.max(0, current - pageSize))
                    setSelectedJobId(null)
                  }}
                >
                  Previous
                </button>
                <span>Page {pageNumber}</span>
                <button
                  type="button"
                  disabled={!hasNextPage}
                  onClick={() => {
                    setOffset((current) => current + pageSize)
                    setSelectedJobId(null)
                  }}
                >
                  Next
                </button>
              </nav>
            </>
          )
        }}
      </PanelState>
    </div>
  )
}
