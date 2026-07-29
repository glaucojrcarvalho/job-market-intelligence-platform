import {
  type FormEvent,
  useEffect,
  useRef,
  useState,
} from 'react'

import {
  matchCandidate,
  type CandidateProfile,
  type MatchResult,
} from '../api/candidates'
import { EmptyState, ErrorState, LoadingState } from '../components/AsyncState'

type SkillRow = { id: number; name: string; proficiency: string }
type FormErrors = { summary?: string; skills?: string; years?: string }
type ResultState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: MatchResult[] }
  | { status: 'error'; message: string }

const initialSkill: SkillRow = { id: 1, name: '', proficiency: '' }

function percentage(value: number) {
  return `${Math.round(Math.max(0, Math.min(1, value)) * 100)}%`
}

function validate(
  summary: string,
  skills: SkillRow[],
  years: string,
): FormErrors {
  const errors: FormErrors = {}
  const trimmedSummary = summary.trim()
  const namedSkills = skills.filter((skill) => skill.name.trim())

  if (trimmedSummary.length < 10) {
    errors.summary = 'Enter at least 10 characters.'
  } else if (trimmedSummary.length > 2000) {
    errors.summary = 'Keep the summary within 2,000 characters.'
  }

  if (namedSkills.length === 0) {
    errors.skills = 'Add at least one skill.'
  } else if (
    new Set(namedSkills.map((skill) => skill.name.trim().toLocaleLowerCase()))
      .size !== namedSkills.length
  ) {
    errors.skills = 'Remove duplicate skills.'
  } else if (
    namedSkills.some(
      (skill) =>
        skill.name.trim().length > 100 ||
        skill.proficiency.trim().length > 50,
    )
  ) {
    errors.skills = 'Keep skill names within 100 characters and levels within 50.'
  }

  const numericYears = Number(years)
  if (
    years.trim() &&
    (!Number.isFinite(numericYears) || numericYears < 0 || numericYears > 80)
  ) {
    errors.years = 'Enter a value from 0 to 80.'
  }

  return errors
}

function SkillList({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="match-skills">
      <h3>{title}</h3>
      {items.length > 0 ? (
        <ul>
          {items.map((item) => <li key={item}>{item}</li>)}
        </ul>
      ) : (
        <p>None reported</p>
      )}
    </section>
  )
}

function MatchCard({ match, rank }: { match: MatchResult; rank: number }) {
  return (
    <article className="match-card">
      <header>
        <div>
          <p className="panel-kicker">Rank {rank} · {match.source_name}</p>
          <h2>{match.job_title}</h2>
        </div>
        <div className="match-score" aria-label={`Match score ${percentage(match.match_score)}`}>
          <strong>{percentage(match.match_score)}</strong>
          <span>match</span>
        </div>
      </header>
      <p className="match-confidence">
        Confidence: <strong>{percentage(match.confidence)}</strong>
      </p>
      <div className="match-skill-grid">
        <SkillList title="Matched skills" items={match.matching_skills} />
        <SkillList title="Missing skills" items={match.missing_skills} />
      </div>
      {match.reasons.length > 0 && (
        <section className="match-reasons">
          <h3>Why this result</h3>
          <ul>
            {match.reasons.map((reason, index) => (
              <li key={`${reason.type}-${index}`}>{reason.message}</li>
            ))}
          </ul>
        </section>
      )}
    </article>
  )
}

export function CandidateMatchingPage() {
  const [summary, setSummary] = useState('')
  const [location, setLocation] = useState('')
  const [years, setYears] = useState('')
  const [skills, setSkills] = useState<SkillRow[]>([initialSkill])
  const [nextSkillId, setNextSkillId] = useState(2)
  const [errors, setErrors] = useState<FormErrors>({})
  const [result, setResult] = useState<ResultState>({ status: 'idle' })
  const controllerRef = useRef<AbortController | null>(null)
  const resultsRef = useRef<HTMLElement>(null)

  useEffect(() => () => controllerRef.current?.abort(), [])
  useEffect(() => {
    if (result.status === 'success') resultsRef.current?.focus()
  }, [result.status])

  function updateSkill(id: number, field: 'name' | 'proficiency', value: string) {
    setSkills((current) =>
      current.map((skill) =>
        skill.id === id
          ? {
              id: skill.id,
              name: field === 'name' ? value : skill.name,
              proficiency:
                field === 'proficiency' ? value : skill.proficiency,
            }
          : skill,
      ),
    )
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const nextErrors = validate(summary, skills, years)
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    const profile: CandidateProfile = {
      summary: summary.trim(),
      skills: skills
        .filter((skill) => skill.name.trim())
        .map((skill) => ({
          name: skill.name.trim(),
          proficiency: skill.proficiency.trim() || undefined,
        })),
      ...(location.trim() ? { location: location.trim() } : {}),
      ...(years.trim() ? { years_experience: Number(years) } : {}),
    }

    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    setResult({ status: 'loading' })
    try {
      const data = await matchCandidate(profile, controller.signal)
      if (!controller.signal.aborted) setResult({ status: 'success', data })
    } catch {
      if (!controller.signal.aborted) {
        setResult({
          status: 'error',
          message: 'Check that the API is available, then try again.',
        })
      }
    }
  }

  return (
    <div className="matching-page page-stack">
      <header className="page-header matching-header">
        <div>
          <p className="eyebrow">Candidate matching</p>
          <h1>Compare a skill profile with stored roles.</h1>
          <p className="page-lead">
            Get explainable, deterministic rankings based on the jobs available
            in this instance—not a hiring decision or assessment.
          </p>
        </div>
        <aside className="privacy-note">
          <strong>Keep it anonymous</strong>
          <p>Do not enter names, email addresses, contact details, or other personal information.</p>
        </aside>
      </header>

      <div className="matching-layout">
        <form className="candidate-form" onSubmit={submit} noValidate>
          <div className="form-heading">
            <h2>Candidate profile</h2>
            <p>Fields marked required are used by the current matching model.</p>
          </div>
          <div className="field">
            <label htmlFor="candidate-summary">Professional summary <span>Required</span></label>
            <textarea
              id="candidate-summary"
              value={summary}
              maxLength={2000}
              aria-invalid={Boolean(errors.summary)}
              aria-describedby={errors.summary ? 'summary-error' : 'summary-help'}
              onChange={(event) => setSummary(event.target.value)}
              rows={5}
            />
            <p id="summary-help" className="field-help">Describe relevant experience without identifying details.</p>
            {errors.summary && <p id="summary-error" className="field-error">{errors.summary}</p>}
          </div>

          <fieldset className="skill-fieldset" aria-describedby={errors.skills ? 'skills-error' : undefined}>
            <legend>Skills <span>Required</span></legend>
            {skills.map((skill, index) => (
              <div className="skill-row" key={skill.id}>
                <div className="field">
                  <label htmlFor={`skill-${skill.id}`}>Skill {index + 1}</label>
                  <input
                    id={`skill-${skill.id}`}
                    value={skill.name}
                    maxLength={100}
                    onChange={(event) => updateSkill(skill.id, 'name', event.target.value)}
                  />
                </div>
                <div className="field">
                  <label htmlFor={`proficiency-${skill.id}`}>Level <span>Optional</span></label>
                  <input
                    id={`proficiency-${skill.id}`}
                    value={skill.proficiency}
                    maxLength={50}
                    placeholder="e.g. advanced"
                    onChange={(event) => updateSkill(skill.id, 'proficiency', event.target.value)}
                  />
                </div>
                {skills.length > 1 && (
                  <button type="button" className="remove-skill" onClick={() => setSkills((current) => current.filter((item) => item.id !== skill.id))}>
                    Remove <span className="visually-hidden">skill {index + 1}</span>
                  </button>
                )}
              </div>
            ))}
            {errors.skills && <p id="skills-error" className="field-error">{errors.skills}</p>}
            <button
              type="button"
              className="add-skill"
              disabled={skills.length >= 50}
              onClick={() => {
                setSkills((current) => [...current, { id: nextSkillId, name: '', proficiency: '' }])
                setNextSkillId((current) => current + 1)
              }}
            >
              + Add another skill
            </button>
          </fieldset>

          <div className="optional-fields">
            <div className="field">
              <label htmlFor="candidate-location">Location <span>Optional</span></label>
              <input id="candidate-location" value={location} maxLength={255} onChange={(event) => setLocation(event.target.value)} />
            </div>
            <div className="field">
              <label htmlFor="candidate-years">Years of experience <span>Optional</span></label>
              <input id="candidate-years" type="number" min="0" max="80" step="0.5" value={years} aria-invalid={Boolean(errors.years)} aria-describedby={errors.years ? 'years-error' : undefined} onChange={(event) => setYears(event.target.value)} />
              {errors.years && <p id="years-error" className="field-error">{errors.years}</p>}
            </div>
          </div>
          <button className="button button-primary match-submit" type="submit" disabled={result.status === 'loading'}>
            {result.status === 'loading' ? 'Calculating matches…' : 'Find matching jobs'}
          </button>
        </form>

        <section className="matching-results" aria-live="polite" aria-labelledby="matching-results-title" ref={resultsRef} tabIndex={-1}>
          <h2 id="matching-results-title">Ranked results</h2>
          {result.status === 'idle' && <EmptyState title="Ready when you are" message="Complete the profile to compare it with currently stored jobs." />}
          {result.status === 'loading' && <LoadingState message="Comparing this profile with stored jobs." />}
          {result.status === 'error' && <ErrorState title="Matches could not be calculated" message={result.message} />}
          {result.status === 'success' && result.data.length === 0 && <EmptyState title="No matching jobs found" message="The API returned no ranked roles for this profile and current dataset." />}
          {result.status === 'success' && result.data.length > 0 && (
            <div className="match-list">
              <p className="result-count">{result.data.length} ranked {result.data.length === 1 ? 'job' : 'jobs'}</p>
              {result.data.map((match, index) => <MatchCard match={match} rank={index + 1} key={match.match_id ?? `${match.job_id}-${index}`} />)}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
