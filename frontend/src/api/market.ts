import { requestJson } from './client'

export type JobSummary = {
  job_id: number
  title: string
  source_name: string
  work_mode: string
  location_text: string | null
  salary_text: string | null
}

export type MetricBucket = {
  label: string
  value: number
}

export type SkillCooccurrence = {
  left_skill: string
  right_skill: string
  frequency: number
}

export function getJobs(signal?: AbortSignal) {
  return requestJson<JobSummary[]>('/v1/jobs', { signal })
}

export function getTopSkills(signal?: AbortSignal) {
  return requestJson<MetricBucket[]>('/v1/analytics/skills/top', { signal })
}

export function getTopTechnologies(signal?: AbortSignal) {
  return requestJson<MetricBucket[]>(
    '/v1/analytics/technologies/top',
    { signal },
  )
}

export function getSkillCooccurrence(signal?: AbortSignal) {
  return requestJson<SkillCooccurrence[]>(
    '/v1/analytics/skills/cooccurrence',
    { signal },
  )
}
