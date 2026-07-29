import {
  getJobs,
  getSkillCooccurrence,
  getTopSkills,
  getTopTechnologies,
  type JobSummary,
} from '../api/market'
import { MetricBars } from '../components/MetricBars'
import { PanelState } from '../components/PanelState'
import { useApiResource } from '../hooks/useApiResource'

const displayedMetricLimit = 8
const workModeOrder = ['remote', 'hybrid', 'onsite', 'unknown']

function formatLabel(value: string) {
  return value
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

function countWorkModes(jobs: JobSummary[]) {
  const counts = new Map<string, number>()

  for (const job of jobs) {
    const workMode = workModeOrder.includes(job.work_mode)
      ? job.work_mode
      : 'unknown'
    counts.set(workMode, (counts.get(workMode) ?? 0) + 1)
  }

  return [...counts.entries()].toSorted(([left], [right]) => {
    const leftIndex = workModeOrder.indexOf(left)
    const rightIndex = workModeOrder.indexOf(right)
    const normalizedLeft = leftIndex === -1 ? workModeOrder.length : leftIndex
    const normalizedRight = rightIndex === -1 ? workModeOrder.length : rightIndex
    return normalizedLeft - normalizedRight || left.localeCompare(right)
  })
}

export function MarketDashboardPage() {
  const jobs = useApiResource(getJobs)
  const skills = useApiResource(getTopSkills)
  const technologies = useApiResource(getTopTechnologies)
  const cooccurrence = useApiResource(getSkillCooccurrence)

  return (
    <div className="dashboard page-stack">
      <header className="page-header dashboard-header">
        <div>
          <p className="eyebrow">Market dashboard</p>
          <h1>Signals from the jobs stored here.</h1>
          <p className="page-lead">
            Explore current skill, technology, co-occurrence, and work-mode
            counts returned by the platform API.
          </p>
        </div>
        <aside className="coverage-note" aria-label="Dataset coverage">
          <span aria-hidden="true">i</span>
          <p>
            Counts describe this instance only. The API does not yet provide
            coverage, freshness, or live-ingestion guarantees.
          </p>
        </aside>
      </header>

      <section className="dashboard-summary" aria-labelledby="summary-heading">
        <div className="panel-heading">
          <div>
            <p className="panel-kicker">Snapshot</p>
            <h2 id="summary-heading">Stored market records</h2>
          </div>
          <p>Job count and API-provided work modes.</p>
        </div>

        <PanelState
          state={jobs.state}
          isEmpty={(data) => data.length === 0}
          emptyTitle="No jobs are stored yet"
          emptyMessage="Market totals and work-mode counts will appear after manually authored or authorized records are added."
          errorTitle="Job summary is unavailable"
          onRetry={jobs.retry}
        >
          {(data) => (
            <div className="summary-grid">
              <article className="total-card">
                <p>Jobs in this instance</p>
                <strong>{data.length}</strong>
                <span>Not live market coverage</span>
              </article>

              <div className="work-mode-grid" aria-label="Work-mode distribution">
                {countWorkModes(data).map(([label, value]) => (
                  <article className="summary-card" key={label}>
                    <p>{formatLabel(label)}</p>
                    <strong>{value}</strong>
                    <span>
                      {Math.round((value / data.length) * 100)}% of stored jobs
                    </span>
                  </article>
                ))}
              </div>
            </div>
          )}
        </PanelState>
      </section>

      <div className="dashboard-grid">
        <section className="dashboard-panel" aria-labelledby="skills-heading">
          <div className="panel-heading">
            <div>
              <p className="panel-kicker">Demand signals</p>
              <h2 id="skills-heading">Top skills</h2>
            </div>
            <p>Mentions across enriched jobs.</p>
          </div>
          <PanelState
            state={skills.state}
            isEmpty={(data) => data.length === 0}
            emptyTitle="No skill metrics yet"
            emptyMessage="Skill counts appear when stored jobs have enrichment results."
            errorTitle="Skill metrics are unavailable"
            onRetry={skills.retry}
          >
            {(data) => (
              <MetricBars
                items={data.slice(0, displayedMetricLimit)}
                ariaLabel="Top skills by number of enriched jobs"
              />
            )}
          </PanelState>
        </section>

        <section
          className="dashboard-panel"
          aria-labelledby="technologies-heading"
        >
          <div className="panel-heading">
            <div>
              <p className="panel-kicker">Tooling signals</p>
              <h2 id="technologies-heading">Top technologies</h2>
            </div>
            <p>Detected tools and platforms.</p>
          </div>
          <PanelState
            state={technologies.state}
            isEmpty={(data) => data.length === 0}
            emptyTitle="No technology metrics yet"
            emptyMessage="Technology counts appear when stored jobs have enrichment results."
            errorTitle="Technology metrics are unavailable"
            onRetry={technologies.retry}
          >
            {(data) => (
              <MetricBars
                items={data.slice(0, displayedMetricLimit)}
                ariaLabel="Top technologies by number of enriched jobs"
              />
            )}
          </PanelState>
        </section>
      </div>

      <section
        className="dashboard-panel cooccurrence-panel"
        aria-labelledby="cooccurrence-heading"
      >
        <div className="panel-heading">
          <div>
            <p className="panel-kicker">Relationships</p>
            <h2 id="cooccurrence-heading">Skills that appear together</h2>
          </div>
          <p>
            Distinct skill pairs found in the same enriched job. Frequency is
            shown as text and is not represented by colour alone.
          </p>
        </div>
        <PanelState
          state={cooccurrence.state}
          isEmpty={(data) => data.length === 0}
          emptyTitle="No skill relationships yet"
          emptyMessage="At least one enriched job with two detected skills is required."
          errorTitle="Skill relationships are unavailable"
          onRetry={cooccurrence.retry}
        >
          {(data) => (
            <div className="table-scroll">
              <table className="cooccurrence-table">
                <caption className="visually-hidden">
                  Most frequent skill pairs
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Skill pair</th>
                    <th scope="col">Jobs together</th>
                  </tr>
                </thead>
                <tbody>
                  {data.slice(0, displayedMetricLimit).map((item) => (
                    <tr key={`${item.left_skill}:${item.right_skill}`}>
                      <td>
                        <span>{item.left_skill}</span>
                        <span aria-hidden="true">+</span>
                        <span>{item.right_skill}</span>
                      </td>
                      <td>{item.frequency}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </PanelState>
      </section>
    </div>
  )
}
