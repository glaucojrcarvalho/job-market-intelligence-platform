import { requestJson } from './client'
import { listJobs } from './jobs'

export type { JobSummary } from './jobs'

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
  return listJobs({}, signal)
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
