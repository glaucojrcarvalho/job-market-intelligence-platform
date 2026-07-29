import { requestJson } from './client'

export type WorkMode = 'remote' | 'hybrid' | 'onsite' | 'unknown'

export type JobSummary = {
  job_id: number
  title: string
  source_name: string
  work_mode: string
  location_text: string | null
  salary_text: string | null
  company_name: string | null
  source_url: string | null
  posted_at: string | null
  employment_type: string
}

export type JobLocation = {
  country: string | null
  region: string | null
  city: string | null
  raw_text: string | null
}

export type JobEnrichment = {
  job_id: number | null
  role_family: string | null
  seniority: string | null
  confidence: number | null
  skills: string[]
  technologies: string[]
  summary: string | null
}

export type JobDetail = JobSummary & {
  description: string
  location: JobLocation
  seniority_hint: string
  observed_at: string | null
  enrichment: JobEnrichment | null
}

export type JobListQuery = {
  limit?: number
  offset?: number
  workMode?: WorkMode
}

export function listJobs(query: JobListQuery, signal?: AbortSignal) {
  const search = new URLSearchParams()
  if (query.limit !== undefined) {
    search.set('limit', String(query.limit))
  }
  if (query.offset !== undefined) {
    search.set('offset', String(query.offset))
  }
  if (query.workMode !== undefined) {
    search.set('work_mode', query.workMode)
  }

  const queryString = search.size > 0 ? `?${search}` : ''
  return requestJson<JobSummary[]>(`/v1/jobs${queryString}`, { signal })
}

export function getJob(jobId: number, signal?: AbortSignal) {
  return requestJson<JobDetail>(`/v1/jobs/${jobId}`, { signal })
}
